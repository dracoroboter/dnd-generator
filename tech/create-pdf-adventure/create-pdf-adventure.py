#!/usr/bin/env python3
"""
create-pdf-adventure.py — Genera un PDF unico con un'avventura D&D completa.

Uso:
    python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura>

Output:
    releases/<NomeAvventura>/<NomeAvventura>_yyyymmdd.pdf
"""

import subprocess, sys, os, glob, re
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CSS_FILE = SCRIPT_DIR / "adventure.css"

EXCLUDED_FILES = {
    "README.md", "AdventureBook.md", "PlanBook.md",
    "DiscussioneNarrativa.md", "MappaGenerale.md",
}


def md_to_html(md_path):
    """Convert a markdown file to HTML fragment via pandoc."""
    r = subprocess.run(
        ["pandoc", str(md_path), "-f", "markdown", "-t", "html"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"  WARN: pandoc failed for {md_path}: {r.stderr.strip()}")
        return ""
    return r.stdout


def find_cover(adventure_dir):
    """Find cover image in img/ directory."""
    img_dir = adventure_dir / "img"
    if not img_dir.exists():
        return None
    covers = list(img_dir.glob("*_COVER.png")) + list(img_dir.glob("*_COVER.jpg"))
    return covers[0] if covers else None


def find_modules(adventure_dir):
    """Find module directories sorted by number prefix."""
    modules = []
    for d in sorted(adventure_dir.iterdir()):
        if d.is_dir() and re.match(r"\d+_", d.name):
            modules.append(d)
    return modules


def find_module_md(module_dir):
    """Find the main .md file in a module directory (not in subdirs)."""
    candidates = [
        f for f in module_dir.glob("*.md")
        if f.name not in EXCLUDED_FILES
    ]
    return candidates[0] if candidates else None


def find_module_map(module_dir):
    """Find MappaDM.md in module's mappe/ subdirectory."""
    mappa = module_dir / "mappe" / "MappaDM.md"
    return mappa if mappa.exists() else None


def find_statblocks(adventure_dir):
    """Find stat block PNGs, ordered: Korex, Fin, Jason (by appearance)."""
    sb_dir = adventure_dir / "personaggi" / "statblock"
    if not sb_dir.exists():
        return []
    pngs = sorted(sb_dir.glob("NPC_*.png"))
    # Sort by appearance order if we recognize the names
    order = {"NPC_Korex.png": 0, "NPC_FinDitasvelte.png": 1, "NPC_JasonAccordion.png": 2}
    pngs.sort(key=lambda p: order.get(p.name, 99))
    return pngs


def extract_title(adventure_md):
    """Extract H1 title from the main adventure markdown."""
    with open(adventure_md) as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return adventure_md.parent.name


def extract_readme_meta(adventure_dir):
    """Extract level, duration, structure from README.md."""
    readme = adventure_dir / "README.md"
    meta = {}
    if readme.exists():
        with open(readme) as f:
            for line in f:
                for key in ("Livello consigliato", "Durata", "Struttura", "Tono"):
                    if f"**{key}**:" in line:
                        meta[key] = line.split(":", 1)[1].strip()
    return meta


def build_html(adventure_name, adventure_dir):
    """Assemble the full HTML document."""
    parts = []

    # --- CSS ---
    css_text = CSS_FILE.read_text()
    parts.append(f"<html><head><meta charset='utf-8'><style>{css_text}</style></head><body>")

    # --- Cover ---
    cover = find_cover(adventure_dir)
    if cover:
        cover_uri = cover.as_uri()
        parts.append(f'<div class="cover-page"><img src="{cover_uri}"></div>')
        print(f"  Cover: {cover.name}")

    # --- Frontmatter ---
    adventure_md = adventure_dir / f"{adventure_name}.md"
    title = extract_title(adventure_md) if adventure_md.exists() else adventure_name
    meta = extract_readme_meta(adventure_dir)
    date_str = datetime.now().strftime("%Y-%m-%d")

    parts.append('<div class="frontmatter">')
    parts.append(f"<h1>{title}</h1>")
    if meta.get("Tono"):
        parts.append(f'<div class="subtitle">{meta["Tono"]}</div>')
    parts.append("<hr>")
    parts.append('<div class="meta">')
    parts.append("D&amp;D 5e (2014)<br>")
    if meta.get("Livello consigliato"):
        parts.append(f'Livello {meta["Livello consigliato"]}<br>')
    if meta.get("Durata"):
        parts.append(f'{meta["Durata"]}<br>')
    if meta.get("Struttura"):
        parts.append(f'Struttura {meta["Struttura"]}<br>')
    parts.append(f"<br>{date_str}")
    parts.append("</div></div>")
    print(f"  Frontmatter: {title}")

    # --- Main document ---
    if adventure_md.exists():
        html = md_to_html(adventure_md)
        parts.append(f'<div class="section-break">{html}</div>')
        print(f"  Documento: {adventure_md.name}")

    # --- Modules ---
    for mod_dir in find_modules(adventure_dir):
        mod_md = find_module_md(mod_dir)
        if mod_md:
            html = md_to_html(mod_md)
            parts.append(f'<div class="section-break">{html}</div>')
            print(f"  Modulo: {mod_md.name}")

        map_md = find_module_map(mod_dir)
        if map_md:
            html = md_to_html(map_md)
            parts.append(f'<div class="section-break">{html}</div>')
            print(f"  Mappa DM: {mod_dir.name}/mappe/MappaDM.md")

    # --- Stat block appendix ---
    statblocks = find_statblocks(adventure_dir)
    if statblocks:
        parts.append('<div class="appendix-header"><h1>Appendice — Stat Block</h1></div>')
        for sb in statblocks:
            name = sb.stem.replace("NPC_", "").replace("MON_", "")
            sb_uri = sb.as_uri()
            parts.append(f'<div class="statblock-page"><img src="{sb_uri}" alt="{name}"></div>')
            print(f"  Stat block: {sb.name}")

    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 create-pdf-adventure.py <NomeAvventura>")
        sys.exit(1)

    adventure_name = sys.argv[1]
    adventure_dir = PROJECT_ROOT / "adventures" / adventure_name

    if not adventure_dir.exists():
        print(f"Errore: {adventure_dir} non trovata.")
        sys.exit(1)

    # Output
    date_stamp = datetime.now().strftime("%Y%m%d")
    out_dir = PROJECT_ROOT / "releases" / adventure_name
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"{adventure_name}_{date_stamp}.pdf"

    print(f"=== {adventure_name} — PDF {date_stamp} ===\n")

    # Build HTML
    html_content = build_html(adventure_name, adventure_dir)

    # Write temp HTML (for debugging)
    tmp_html = out_dir / f"{adventure_name}_{date_stamp}.html"
    tmp_html.write_text(html_content)

    # Convert to PDF via weasyprint
    print(f"\n  Generazione PDF...")
    r = subprocess.run(
        ["weasyprint", str(tmp_html), str(pdf_path)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"  ERRORE weasyprint: {r.stderr}")
        sys.exit(1)

    # Cleanup temp HTML
    tmp_html.unlink()

    size_mb = pdf_path.stat().st_size / (1024 * 1024)
    print(f"\n=== PDF generato: {pdf_path.relative_to(PROJECT_ROOT)} ({size_mb:.1f} MB) ===")


if __name__ == "__main__":
    main()
