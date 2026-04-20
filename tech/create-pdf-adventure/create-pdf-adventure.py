#!/usr/bin/env python3
"""
create-pdf-adventure.py — Genera un PDF unico con un'avventura D&D completa.

Uso:
    python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> [--fit-cover]

Flags:
    --fit-cover  Adatta cover non-portrait: sfondo scuro, immagine centrata, titolo sovrapposto

Output:
    releases/<NomeAvventura>/<NomeAvventura>_yyyymmdd.pdf
"""

import argparse, subprocess, sys, os, re, base64, io
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CSS_FILE = SCRIPT_DIR / "adventure.css"

EXCLUDED_FILES = {
    "README.md", "AdventureBook.md", "PlanBook.md",
    "DiscussioneNarrativa.md", "MappaGenerale.md",
}

# A4 dimensions for cover generation
A4_W, A4_H = 2480, 3508  # 300 DPI


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
    """Find cover image: img/*_COVER.png (standard convention)."""
    img_dir = adventure_dir / "img"
    if not img_dir.exists():
        return None
    covers = list(img_dir.glob("*_COVER.png")) + list(img_dir.glob("*_COVER.jpg"))
    return covers[0] if covers else None


def is_portrait(img_path):
    """Check if image is portrait (height > width)."""
    from PIL import Image
    with Image.open(img_path) as img:
        return img.height > img.width


def fit_cover(img_path, title, author=None):
    """Create cover: background image scaled to A4, logo top center, title center,
    author + D&D subtitle bottom. Yellow uppercase text with black outline."""
    from PIL import Image, ImageDraw, ImageFont

    # Load and scale background to A4
    bg = Image.open(img_path).convert("RGBA")
    # Scale to cover A4, crop if needed
    scale = max(A4_W / bg.width, A4_H / bg.height)
    new_w, new_h = int(bg.width * scale), int(bg.height * scale)
    bg = bg.resize((new_w, new_h), Image.LANCZOS)
    # Center crop
    left = (new_w - A4_W) // 2
    top = (new_h - A4_H) // 2
    bg = bg.crop((left, top, left + A4_W, top + A4_H)).convert("RGBA")

    # Load logo
    logo_path = SCRIPT_DIR / "img" / "DracoRoboter_logo.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        # Scale logo to ~30% of page width
        logo_w = int(A4_W * 0.30)
        logo_scale = logo_w / logo.width
        logo_h = int(logo.height * logo_scale)
        logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
        # Paste top center
        logo_x = (A4_W - logo_w) // 2
        logo_y = int(A4_H * 0.05)
        bg.paste(logo, (logo_x, logo_y), logo)

    # Setup drawing
    draw = ImageDraw.Draw(bg)
    yellow = (255, 220, 50)
    black = (0, 0, 0)
    blue = (30, 60, 160)

    # Font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(font_path, 140)
    sub_font = ImageFont.truetype(font_path, 60)
    author_font = ImageFont.truetype(font_path, 56)

    def draw_outlined_text(x, y, text, font, fill=yellow, outline=black, width=4):
        """Draw text with outline."""
        for dx in range(-width, width + 1):
            for dy in range(-width, width + 1):
                if dx * dx + dy * dy <= width * width:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline)
        draw.text((x, y), text, font=font, fill=fill)

    def centered_outlined_text(y, text, font, fill=yellow):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (A4_W - tw) // 2
        draw_outlined_text(x, y, text, font, fill=fill)
        return bbox[3] - bbox[1]

    # Title — center of page
    title_upper = title.upper()
    title_bbox = draw.textbbox((0, 0), title_upper, font=title_font)
    title_h = title_bbox[3] - title_bbox[1]
    title_y = int(A4_H * 0.42)
    centered_outlined_text(title_y, title_upper, title_font)

    # Blue stripe under title
    stripe_y = title_y + title_h + int(A4_H * 0.02)
    stripe_margin = int(A4_W * 0.15)
    stripe_h = 12
    draw.rectangle([(stripe_margin, stripe_y), (A4_W - stripe_margin, stripe_y + stripe_h)], fill=blue)

    # Author — bottom area
    author_y = int(A4_H * 0.82)
    if author:
        centered_outlined_text(author_y, author, author_font)

    # D&D subtitle
    dnd_y = author_y + int(A4_H * 0.05)
    centered_outlined_text(dnd_y, "Avventura per D&D 5e", sub_font)

    # Convert to RGB for PDF
    final = Image.new("RGB", (A4_W, A4_H), (0, 0, 0))
    final.paste(bg, mask=bg.split()[3] if bg.mode == "RGBA" else None)

    buf = io.BytesIO()
    final.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


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


def find_maps_in_dir(maps_dir):
    """Find map files (.md and .png) in a maps/ directory, excluding other/.
    Returns list of (md_path_or_None, img_path_or_None) tuples, grouped by base name."""
    if not maps_dir.exists():
        return []
    items = {}
    for f in sorted(maps_dir.iterdir()):
        if f.is_dir() or f.name == "MappaGenerale.md":
            continue
        stem = f.stem
        if f.suffix == ".md":
            items.setdefault(stem, [None, None])[0] = f
        elif f.suffix.lower() in (".png", ".jpg", ".jpeg"):
            items.setdefault(stem, [None, None])[1] = f
    return [(md, img) for md, img in items.values()]


def find_adventure_maps(adventure_dir):
    """Find maps in the adventure root maps/ directory."""
    return find_maps_in_dir(adventure_dir / "maps")


def find_module_maps(module_dir):
    """Find all map files in module's maps/ subdirectory."""
    return find_maps_in_dir(module_dir / "maps")


def find_statblocks(adventure_dir):
    """Find NPC_*.png and MON_*.png stat blocks, alphabetically sorted."""
    sb_dir = adventure_dir / "characters" / "statblock"
    if not sb_dir.exists():
        return []
    return sorted(
        f for f in sb_dir.iterdir()
        if f.suffix == ".png" and (f.name.startswith("NPC_") or f.name.startswith("MON_"))
    )


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
                for key in ("Livello consigliato", "Durata", "Struttura", "Tono", "Autore"):
                    if f"**{key}**:" in line:
                        meta[key] = line.split(":", 1)[1].strip()
    return meta


def build_html(adventure_name, adventure_dir, do_fit_cover=False):
    """Assemble the full HTML document."""
    parts = []

    # --- CSS ---
    css_text = CSS_FILE.read_text()
    parts.append(f"<html><head><meta charset='utf-8'><style>{css_text}</style></head><body>")

    # --- Title (needed for cover and frontmatter) ---
    adventure_md = adventure_dir / f"{adventure_name}.md"
    title = extract_title(adventure_md) if adventure_md.exists() else adventure_name
    meta = extract_readme_meta(adventure_dir)

    # --- Cover ---
    cover = find_cover(adventure_dir)
    if cover:
        if do_fit_cover:
            b64 = fit_cover(cover, title, author=meta.get("Autore"))
            parts.append(f'<div class="cover-page"><img src="data:image/png;base64,{b64}"></div>')
            print(f"  Cover: {cover.name} (con scritte)")
        else:
            cover_uri = cover.as_uri()
            parts.append(f'<div class="cover-page"><img src="{cover_uri}"></div>')
            print(f"  Cover: {cover.name} (immagine pura)")

    # --- Frontmatter ---
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
    if meta.get("Autore"):
        parts.append(f'<br><br><em>{meta["Autore"]}</em>')
    parts.append("</div></div>")
    print(f"  Frontmatter: {title}")

    # --- Main document ---
    if adventure_md.exists():
        html = md_to_html(adventure_md)
        parts.append(f'<div class="section-break">{html}</div>')
        print(f"  Documento: {adventure_md.name}")

    # --- Adventure maps (maps/ root) ---
    for map_md, map_img in find_adventure_maps(adventure_dir):
        if map_md:
            html = md_to_html(map_md)
            parts.append(f'<div class="section-break">{html}</div>')
            print(f"  Mappa (desc): {map_md.name}")
        if map_img:
            name = map_img.stem
            img_uri = map_img.as_uri()
            parts.append(f'<div class="map-page"><img src="{img_uri}" alt="{name}">'
                         f'<div class="map-caption">{name}</div></div>')
            print(f"  Mappa (img): {map_img.name}")

    # --- Modules ---
    for mod_dir in find_modules(adventure_dir):
        mod_md = find_module_md(mod_dir)
        if mod_md:
            html = md_to_html(mod_md)
            parts.append(f'<div class="section-break">{html}</div>')
            print(f"  Modulo: {mod_md.name}")

        # Module maps
        for map_md, map_img in find_module_maps(mod_dir):
            if map_md:
                html = md_to_html(map_md)
                parts.append(f'<div class="section-break">{html}</div>')
                print(f"  Mappa modulo (desc): {mod_dir.name}/maps/{map_md.name}")
            if map_img:
                name = map_img.stem
                img_uri = map_img.as_uri()
                parts.append(f'<div class="map-page"><img src="{img_uri}" alt="{name}">'
                             f'<div class="map-caption">{name}</div></div>')
                print(f"  Mappa modulo (img): {mod_dir.name}/maps/{map_img.name}")

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
    parser = argparse.ArgumentParser(description="Genera PDF unico per un'avventura D&D")
    parser.add_argument("adventure", help="Nome dell'avventura (directory in adventures/)")
    parser.add_argument("--fit-cover", action="store_true",
                        help="Adatta cover non-portrait: sfondo scuro, immagine centrata, titolo")
    args = parser.parse_args()

    adventure_name = args.adventure
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
    html_content = build_html(adventure_name, adventure_dir, do_fit_cover=args.fit_cover)

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
