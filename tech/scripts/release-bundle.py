#!/usr/bin/env python3
"""
release-bundle.py — Genera lo ZIP di pubblicazione di un'avventura.

Uso:
  python3 tech/scripts/release-bundle.py <NomeAvventura>
  python3 tech/scripts/release-bundle.py <NomeAvventura> --tag v1.0

Flusso completo:
  1. Rigenera stat block + compendium XML (generate-statblocks.py)
  2. Genera PDF fullres + lowres (create-pdf-adventure.py)
  3. Assembla lo ZIP con formato directory standard
  4. Copia lo ZIP in public/

Richiede: generate-statblocks.py, create-pdf-adventure.py già funzionanti.
"""

import sys
import os
import subprocess
import shutil
import zipfile
import glob
import json
from datetime import datetime


def is_multilingual(adv_dir):
    return os.path.isfile(os.path.join(adv_dir, "manifest.json"))

def get_lang_dir(adv_dir, lang="it"):
    if is_multilingual(adv_dir):
        return os.path.join(adv_dir, lang)
    return adv_dir

def get_default_lang(adv_dir):
    manifest = os.path.join(adv_dir, "manifest.json")
    if os.path.isfile(manifest):
        with open(manifest) as f:
            return json.loads(f.read()).get("default_lang", "it")
    return "it"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    if not args:
        print(f"Uso: {sys.argv[0]} <NomeAvventura> [--tag vX.Y]")
        sys.exit(1)

    adventure = args[0]
    tag = None
    for i, f in enumerate(flags):
        if f == "--tag" and i + 1 < len(flags):
            tag = flags[i + 1]
    # Also check sys.argv directly for --tag
    for i, a in enumerate(sys.argv):
        if a == "--tag" and i + 1 < len(sys.argv):
            tag = sys.argv[i + 1]

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    adv_dir = os.path.join(project_root, "adventures", adventure)
    releases_dir = os.path.join(project_root, "releases", adventure)
    public_dir = os.path.join(project_root, "public")

    if not os.path.isdir(adv_dir):
        print(f"Errore: {adv_dir} non trovata.")
        sys.exit(1)

    date_str = datetime.now().strftime("%Y%m%d")
    tag_str = f"_{tag}" if tag else ""
    bundle_name = f"{adventure}{tag_str}_{date_str}"

    print(f"=== Release bundle: {bundle_name} ===\n")

    # Step 1: generate stat blocks + compendium
    print("[1/4] Stat block + compendium...")
    r = subprocess.run(
        ["python3", os.path.join(project_root, "tech/fightclub/generate-statblocks.py"), adventure],
        capture_output=True, text=True, cwd=project_root
    )
    if r.returncode != 0:
        print(f"  Errore: {r.stderr.strip()}")
        sys.exit(1)
    # Count generated
    lines = [l for l in r.stdout.strip().split("\n") if l.startswith("✓")]
    for l in lines:
        print(f"  {l}")

    # Step 2: generate PDFs
    print("[2/4] PDF fullres...")
    r = subprocess.run(
        ["python3", os.path.join(project_root, "tech/create-pdf-adventure/create-pdf-adventure.py"), adventure],
        capture_output=True, text=True, cwd=project_root
    )
    if r.returncode != 0:
        print(f"  Errore: {r.stderr.strip()}")
        sys.exit(1)
    for l in r.stdout.strip().split("\n"):
        if "PDF generato" in l:
            print(f"  {l.strip()}")

    print("  PDF lowres...")
    r = subprocess.run(
        ["python3", os.path.join(project_root, "tech/create-pdf-adventure/create-pdf-adventure.py"), adventure, "--lowres"],
        capture_output=True, text=True, cwd=project_root
    )
    if r.returncode != 0:
        print(f"  Errore: {r.stderr.strip()}")
        sys.exit(1)
    for l in r.stdout.strip().split("\n"):
        if "PDF generato" in l:
            print(f"  {l.strip()}")

    # Step 3: assemble ZIP
    print("[3/4] Assemblaggio ZIP...")

    # Find latest PDFs
    fullres = sorted(glob.glob(os.path.join(releases_dir, f"{adventure}_*.pdf")))
    fullres = [f for f in fullres if "lowres" not in f]
    lowres = sorted(glob.glob(os.path.join(releases_dir, f"{adventure}_*_lowres.pdf")))
    pdf_full = fullres[-1] if fullres else None
    pdf_low = lowres[-1] if lowres else None

    # Compendium
    lang_dir = get_lang_dir(adv_dir)
    compendium = os.path.join(lang_dir, "characters", "fightclub", f"{adventure}_Compendium.xml")

    # Cover
    cover = None
    for ext in (".png", ".jpg"):
        c = os.path.join(adv_dir, "img", f"{adventure}_COVER{ext}")
        if os.path.isfile(c):
            cover = c
            break

    # Maps: collect from all module maps/ dirs + top-level maps/ (images only, in root)
    maps = []
    # In multilingual mode, module map images are in root NN_Name/maps/
    # In legacy mode, they're in the same place
    for maps_dir in glob.glob(os.path.join(adv_dir, "*/maps")) + [os.path.join(adv_dir, "maps")]:
        if os.path.isdir(maps_dir):
            for ext in ("*.png", "*.jpg", "*.jpeg"):
                maps.extend(glob.glob(os.path.join(maps_dir, ext)))
    # Also check lang_dir for module maps (multilingual: images may be in root modules)
    if is_multilingual(adv_dir):
        for maps_dir in glob.glob(os.path.join(lang_dir, "*/maps")):
            if os.path.isdir(maps_dir):
                for ext in ("*.png", "*.jpg", "*.jpeg"):
                    maps.extend(glob.glob(os.path.join(maps_dir, ext)))
    # Exclude other/ subdirs and deduplicate
    maps = list(set(m for m in maps if "/other/" not in m))

    # Stat block PNGs
    sb_dir = os.path.join(lang_dir, "characters", "statblock")
    statblocks = sorted(glob.glob(os.path.join(sb_dir, "*.png"))) if os.path.isdir(sb_dir) else []

    # Build ZIP
    os.makedirs(releases_dir, exist_ok=True)
    zip_path = os.path.join(releases_dir, f"{bundle_name}.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # PDFs — only lowres in the bundle (fullres is for print, separate)
        if pdf_low:
            zf.write(pdf_low, os.path.basename(pdf_low))
            print(f"  + {os.path.basename(pdf_low)}")

        # Compendium
        if os.path.isfile(compendium):
            zf.write(compendium, os.path.basename(compendium))
            print(f"  + {os.path.basename(compendium)}")

        # Cover
        if cover:
            zf.write(cover, os.path.basename(cover))
            print(f"  + {os.path.basename(cover)}")

        # Maps
        for m in maps:
            arcname = f"maps/{os.path.basename(m)}"
            zf.write(m, arcname)
        if maps:
            print(f"  + maps/ ({len(maps)} file)")

        # Stat blocks
        for s in statblocks:
            arcname = f"statblocks/{os.path.basename(s)}"
            zf.write(s, arcname)
        if statblocks:
            print(f"  + statblocks/ ({len(statblocks)} file)")

        # README.txt
        readme = (
            f"{adventure}\n"
            f"{'=' * len(adventure)}\n\n"
            f"Versione: {tag or 'non taggata'}\n"
            f"Data: {datetime.now().strftime('%Y-%m-%d')}\n"
            f"Autore: dracoroboter\n"
            f"Licenza: CC BY-SA 4.0\n\n"
            f"Questo pacchetto è pensato per campagne online (Roll20, VTT).\n"
            f"Per la stampa fisica, usare il PDF printable fullres generato separatamente.\n\n"
            f"Contenuto:\n"
            f"- PDF avventura lowres (senza mappe/stat block inline)\n"
            f"- Compendium XML FightClub ({len(statblocks)} creature)\n"
            f"- {len(maps)} mappe PNG\n"
            f"- {len(statblocks)} stat block PNG\n"
        )
        if cover:
            readme += f"- Copertina\n"
        zf.writestr("README.txt", readme)
        print(f"  + README.txt")

    zip_size = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"\n  ZIP: {zip_path} ({zip_size:.1f} MB)")

    # Step 4: copy to public/
    print("[4/4] Pubblicazione in public/...")
    os.makedirs(public_dir, exist_ok=True)

    # Remove old versions
    for old in glob.glob(os.path.join(public_dir, f"{adventure}_*")):
        os.remove(old)

    dest = os.path.join(public_dir, os.path.basename(zip_path))
    shutil.copy2(zip_path, dest)
    print(f"  → {dest}")

    print(f"\n=== Pubblicazione completata: {os.path.basename(zip_path)} ({zip_size:.1f} MB) ===")


if __name__ == "__main__":
    main()
