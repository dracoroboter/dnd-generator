#!/usr/bin/env python3
"""
release-bundle.py - Pubblica un'avventura in public/.

Uso:
  python3 tech/scripts/release-bundle.py <NomeAvventura>
  python3 tech/scripts/release-bundle.py <NomeAvventura> --full

Output in public/:
  - PDF lowres (testo + stat block inline, no immagini)
  - ZIP immagini (mappe, personaggi, scene, cover, oggetti)
  - ZIP stat block (PNG schede meccaniche)
  - Compendium XML (non zippato)

Con --full: genera anche il PDF completo con tutto inline.
"""

import sys
import os
import subprocess
import shutil
import zipfile
import glob
import json
from datetime import datetime


def get_langs(adv_dir):
    manifest = os.path.join(adv_dir, "manifest.json")
    if os.path.isfile(manifest):
        with open(manifest) as f:
            return json.loads(f.read()).get("languages", ["it"])
    return ["it"]


def run(cmd, cwd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        print(f"  ERRORE: {r.stderr.strip()}")
        sys.exit(1)
    return r.stdout


def collect_images(adv_dir):
    """Collect all images from the adventure (maps, characters, scenes, cover, objects).
    Prefers -lowres versions when available."""
    images = []
    img_exts = (".png", ".jpg", ".jpeg")

    def add_from_dir(category, directory):
        if not os.path.isdir(directory):
            return
        seen_bases = set()
        # First pass: collect all files
        all_files = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in img_exts]
        # Prefer lowres: if NomeMappa-lowres.jpg exists, skip NomeMappa.png
        lowres_bases = set()
        for f in all_files:
            if "-lowres" in f:
                base = f.split("-lowres")[0]
                lowres_bases.add(base)
        for f in sorted(all_files):
            base = os.path.splitext(f)[0]
            if "-lowres" in f:
                images.append((category, os.path.join(directory, f)))
            elif base not in lowres_bases:
                images.append((category, os.path.join(directory, f)))

    add_from_dir("maps", os.path.join(adv_dir, "maps"))
    add_from_dir("characters", os.path.join(adv_dir, "characters", "img"))
    add_from_dir("img", os.path.join(adv_dir, "img"))
    add_from_dir("objects", os.path.join(adv_dir, "objects"))

    # */img/scenes/ (module scenes)
    for d in os.listdir(adv_dir):
        scenes_dir = os.path.join(adv_dir, d, "img", "scenes")
        add_from_dir("scenes", scenes_dir)

    return images


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    full = "--full" in sys.argv

    if not args:
        print(f"Uso: {sys.argv[0]} <NomeAvventura> [--full]")
        sys.exit(1)

    adventure = args[0]
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    adv_dir = os.path.join(project_root, "adventures", adventure)
    releases_dir = os.path.join(project_root, "releases", adventure)
    public_dir = os.path.join(project_root, "public")

    if not os.path.isdir(adv_dir):
        print(f"Errore: {adv_dir} non trovata.")
        sys.exit(1)

    langs = get_langs(adv_dir)
    date_str = datetime.now().strftime("%Y%m%d")

    print(f"=== Pubblicazione: {adventure} ({', '.join(langs)}) ===\n")

    # Step 1: stat block + compendium
    print("[1/3] Stat block + compendium...")
    for lang in langs:
        lang_flag = ["--lang", lang] if lang != "it" else []
        out = run(
            ["python3", "tech/fightclub/generate-statblocks.py", adventure] + lang_flag,
            project_root
        )
        for l in out.strip().split("\n"):
            if l.startswith("✓") or "Compendium" in l:
                print(f"  {l}")

    # Step 2: PDF
    print("[2/3] PDF...")
    for lang in langs:
        lang_flag = ["--lang", lang] if lang != "it" else []
        out = run(
            ["python3", "tech/create-pdf-adventure/create-pdf-adventure.py",
             adventure, "--lowres", "--only", "cover,frontmatter,doc,statblocks"] + lang_flag,
            project_root
        )
        for l in out.strip().split("\n"):
            if "PDF generato" in l:
                print(f"  {l.strip()}")

        if full:
            out = run(
                ["python3", "tech/create-pdf-adventure/create-pdf-adventure.py",
                 adventure, "--lowres"] + lang_flag,
                project_root
            )
            for l in out.strip().split("\n"):
                if "PDF generato" in l:
                    print(f"  (full) {l.strip()}")

    # Step 3: pubblica in public/
    print("[3/3] Pubblicazione in public/...")
    os.makedirs(public_dir, exist_ok=True)

    # Rimuovi vecchie versioni
    for old in glob.glob(os.path.join(public_dir, f"{adventure}_*")):
        os.remove(old)

    published = []

    # PDF per ogni lingua
    for lang in langs:
        suffix = f"_{lang}" if lang != "it" else ""
        pattern = os.path.join(releases_dir, f"{adventure}_{date_str}*lowres{suffix}*only*.pdf")
        candidates = sorted(glob.glob(pattern))
        if not candidates:
            pattern = os.path.join(releases_dir, f"{adventure}_{date_str}*lowres{suffix}*.pdf")
            candidates = sorted(glob.glob(pattern))
        if candidates:
            src = candidates[-1]
            dest_name = f"{adventure}_{date_str}_lowres{suffix}.pdf"
            dest = os.path.join(public_dir, dest_name)
            shutil.copy2(src, dest)
            size = os.path.getsize(dest) / (1024 * 1024)
            published.append((dest_name, f"{size:.1f} MB"))

    # ZIP immagini (tutte)
    images = collect_images(adv_dir)
    if images:
        zip_name = f"{adventure}_Images.zip"
        zip_path = os.path.join(public_dir, zip_name)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for category, path in sorted(images, key=lambda x: x[1]):
                arcname = f"{category}/{os.path.basename(path)}"
                zf.write(path, arcname)
        size = os.path.getsize(zip_path) / (1024 * 1024)
        published.append((zip_name, f"{size:.1f} MB ({len(images)} file)"))

    # ZIP stat block + compendium per ogni lingua
    for lang in langs:
        suffix = f"_{lang}" if lang != "it" else ""
        lang_dir = os.path.join(adv_dir, lang) if os.path.isdir(os.path.join(adv_dir, lang)) else adv_dir
        sb_dir = os.path.join(lang_dir, "characters", "statblock")

        if os.path.isdir(sb_dir):
            sb_files = sorted(glob.glob(os.path.join(sb_dir, "*.png")))
            if sb_files:
                zip_name = f"{adventure}_Statblocks{suffix}.zip"
                zip_path = os.path.join(public_dir, zip_name)
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for s in sb_files:
                        zf.write(s, os.path.basename(s))
                size = os.path.getsize(zip_path) / (1024 * 1024)
                published.append((zip_name, f"{size:.1f} MB ({len(sb_files)} file)"))

        # Compendium XML
        fc_dir = os.path.join(lang_dir, "characters", "fightclub")
        comp = os.path.join(fc_dir, f"{adventure}_Compendium.xml")
        if os.path.isfile(comp):
            comp_name = f"{adventure}_Compendium{suffix}.xml"
            dest = os.path.join(public_dir, comp_name)
            shutil.copy2(comp, dest)
            size = os.path.getsize(dest) / 1024
            published.append((comp_name, f"{size:.0f} KB"))

    # Riepilogo
    print(f"\n{'='*60}")
    print(f"Pubblicato in public/:")
    print(f"{'='*60}")
    for name, size in published:
        print(f"  {name:45s} {size}")
    print(f"{'='*60}")
    print(f"\nRicorda di committare i cambiamenti in public/.")


if __name__ == "__main__":
    main()
