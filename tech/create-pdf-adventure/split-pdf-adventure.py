#!/usr/bin/env python3
"""
split-pdf-adventure.py — Genera PDF divisi per un'avventura D&D.

Uso:
  python3 tech/create-pdf-adventure/split-pdf-adventure.py <NomeAvventura>

Genera 3 PDF in releases/<NomeAvventura>/:
  1. <Nome>_Lore.pdf         — cover + frontmatter + documento principale
  2. <Nome>_Sessioni.pdf     — tutti i moduli (senza mappe inline)
  3. <Nome>_Appendice.pdf    — mappe con descrizione + stat block multi-colonna
"""

import sys, os, subprocess, glob, base64, re
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CSS_FILE = SCRIPT_DIR / "adventure.css"
CREATE_PDF = SCRIPT_DIR / "create-pdf-adventure.py"


def run_create_pdf(adventure, only, suffix, lowres=False):
    """Run create-pdf-adventure.py with --only flag."""
    cmd = ["python3", str(CREATE_PDF), adventure, "--only", only]
    if lowres:
        cmd.append("--lowres")
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
    if r.returncode != 0:
        print(f"  ERRORE: {r.stderr.strip()}")
        return None
    # Find the generated PDF
    for line in r.stdout.split("\n"):
        if "PDF generato" in line:
            print(f"  {line.strip()}")
    return True


def find_modules(adventure_dir):
    """Find module directory numbers."""
    nums = []
    for d in sorted(adventure_dir.iterdir()):
        m = re.match(r"(\d+)_", d.name)
        if d.is_dir() and m:
            nums.append(m.group(1))
    return nums


def build_appendice_html(adventure_name, adventure_dir):
    """Build custom HTML for appendice: maps with descriptions + stat block grid."""
    css_text = CSS_FILE.read_text()
    parts = [f"<html><head><meta charset='utf-8'><style>{css_text}</style></head><body>"]

    # --- Maps with descriptions ---
    parts.append('<div class="appendix-header"><h1>Appendice — Mappe</h1></div>')

    map_count = 0
    # Collect maps from all module dirs + root maps/
    map_dirs = [adventure_dir / "maps"]
    for d in sorted(adventure_dir.iterdir()):
        if d.is_dir() and re.match(r"\d+_", d.name):
            map_dirs.append(d / "maps")

    for maps_dir in map_dirs:
        if not maps_dir.exists():
            continue
        # Group by stem
        items = {}
        for f in sorted(maps_dir.iterdir()):
            if f.is_dir() or f.name.startswith("."):
                continue
            if "-lowres" in f.stem:
                continue
            stem = f.stem
            if f.suffix == ".md":
                items.setdefault(stem, {"md": None, "img": None})["md"] = f
            elif f.suffix.lower() in (".png", ".jpg", ".jpeg"):
                items.setdefault(stem, {"md": None, "img": None})["img"] = f

        for stem, files in items.items():
            img = files["img"]
            md = files["md"]
            if not img:
                # MD-only map description (no image)
                if md:
                    r = subprocess.run(
                        ["pandoc", str(md), "-f", "markdown", "-t", "html"],
                        capture_output=True, text=True
                    )
                    if r.returncode == 0:
                        parts.append(f'<div class="map-described">{r.stdout}</div>')
                        map_count += 1
                continue

            img_uri = img.as_uri()
            name = stem

            if md:
                # Map with description
                r = subprocess.run(
                    ["pandoc", str(md), "-f", "markdown", "-t", "html"],
                    capture_output=True, text=True
                )
                desc_html = r.stdout if r.returncode == 0 else ""
                parts.append(
                    f'<div class="map-described">'
                    f'<img src="{img_uri}" alt="{name}">'
                    f'<div class="map-description">{desc_html}</div>'
                    f'</div>'
                )
            else:
                # Map without description
                parts.append(
                    f'<div class="map-page">'
                    f'<img src="{img_uri}" alt="{name}">'
                    f'<div class="map-caption">{name}</div>'
                    f'</div>'
                )
            map_count += 1

    print(f"  Appendice mappe: {map_count} mappe")

    # --- Stat blocks multi-column ---
    sb_dir = adventure_dir / "characters" / "statblock"
    statblocks = sorted(
        f for f in sb_dir.iterdir()
        if f.suffix == ".png" and (f.name.startswith("NPC_") or f.name.startswith("MON_"))
    ) if sb_dir.exists() else []

    if statblocks:
        parts.append('<div class="appendix-header"><h1>Appendice — Stat Block</h1></div>')
        parts.append('<div class="statblock-grid">')
        for sb in statblocks:
            name = sb.stem.replace("NPC_", "").replace("MON_", "")
            sb_uri = sb.as_uri()
            parts.append(
                f'<div class="statblock-cell">'
                f'<img src="{sb_uri}" alt="{name}">'
                f'<div class="statblock-name">{name}</div>'
                f'</div>'
            )
        parts.append('</div>')
        print(f"  Appendice stat block: {len(statblocks)} creature (multi-colonna)")

    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <NomeAvventura>")
        sys.exit(1)

    adventure = sys.argv[1]
    adventure_dir = PROJECT_ROOT / "adventures" / adventure
    if not adventure_dir.exists():
        print(f"Errore: {adventure_dir} non trovata.")
        sys.exit(1)

    date_stamp = datetime.now().strftime("%Y%m%d")
    out_dir = PROJECT_ROOT / "releases" / adventure
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== {adventure} — PDF split {date_stamp} ===\n")

    # 1. Lore: cover + frontmatter + doc
    print("[1/3] Lore (cover + frontmatter + documento principale)...")
    run_create_pdf(adventure, "cover,frontmatter,doc", "Lore")
    # Rename
    lore_src = list(out_dir.glob(f"{adventure}_{date_stamp}_only-*.pdf"))
    lore_dst = out_dir / f"{adventure}_{date_stamp}_Lore.pdf"
    if lore_src:
        lore_src[0].rename(lore_dst)
        size = lore_dst.stat().st_size / (1024 * 1024)
        print(f"  → {lore_dst.name} ({size:.1f} MB)\n")

    # 2. Sessioni: all modules without maps
    print("[2/3] Sessioni (tutti i moduli)...")
    mod_nums = find_modules(adventure_dir)
    only_mods = ",".join(mod_nums)
    run_create_pdf(adventure, only_mods, "Sessioni")
    sess_src = list(out_dir.glob(f"{adventure}_{date_stamp}_only-*.pdf"))
    sess_dst = out_dir / f"{adventure}_{date_stamp}_Sessioni.pdf"
    if sess_src:
        sess_src[0].rename(sess_dst)
        size = sess_dst.stat().st_size / (1024 * 1024)
        print(f"  → {sess_dst.name} ({size:.1f} MB)\n")

    # 3. Appendice: maps with descriptions + stat block multi-column (custom HTML)
    print("[3/3] Appendice (mappe descritte + stat block multi-colonna)...")
    html_content = build_appendice_html(adventure, adventure_dir)
    tmp_html = out_dir / f"{adventure}_{date_stamp}_Appendice.html"
    tmp_html.write_text(html_content)

    app_dst = out_dir / f"{adventure}_{date_stamp}_Appendice.pdf"
    r = subprocess.run(
        ["weasyprint", str(tmp_html), str(app_dst)],
        capture_output=True, text=True
    )
    tmp_html.unlink()
    if r.returncode != 0:
        print(f"  ERRORE weasyprint: {r.stderr}")
    else:
        size = app_dst.stat().st_size / (1024 * 1024)
        print(f"  → {app_dst.name} ({size:.1f} MB)\n")

    print(f"=== PDF split generati in {out_dir.relative_to(PROJECT_ROOT)}/ ===")
    for f in sorted(out_dir.glob(f"{adventure}_{date_stamp}_*.pdf")):
        if "only-" not in f.name and "lowres" not in f.name:
            size = f.stat().st_size / (1024 * 1024)
            print(f"  {f.name} ({size:.1f} MB)")


if __name__ == "__main__":
    main()
