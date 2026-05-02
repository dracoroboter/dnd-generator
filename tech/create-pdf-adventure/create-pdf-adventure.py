#!/usr/bin/env python3
"""
create-pdf-adventure.py — Genera un PDF unico con un'avventura D&D completa.

Uso:
    python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> [--raw-cover] [--lowres]
    python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> --only statblocks
    python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> --only 01,statblocks

Flags:
    --raw-cover  Usa l'immagine di copertina così com'è, senza logo, titolo e autore
    --lowres     Usa versioni -lowres.png delle immagini (generate da optimize-images.py)
    --only       Genera PDF parziale con solo le sezioni indicate (comma-separated).
                 Valori: cover, frontmatter, doc, maps, statblocks, NN (numero modulo)

Output:
    releases/<NomeAvventura>/<NomeAvventura>_yyyymmdd.pdf
    releases/<NomeAvventura>/<NomeAvventura>_yyyymmdd_only-<sezioni>.pdf   (parziale)
"""

import argparse, subprocess, sys, os, re, base64, io, json
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CSS_FILE = SCRIPT_DIR / "adventure.css"

EXCLUDED_FILES = {
    "README.md", "AdventureBook.md", "PlanBook.md",
    "DiscussioneNarrativa.md", "MappaGenerale.md",
}

# Prefissi di file esclusi (match parziale)
EXCLUDED_PREFIXES = ("DM_Prep", "StatBlock_")

LOWRES_SUFFIX = "-lowres"

# Multilingual labels — loaded from tech/i18n/<lang>.json
I18N_DIR = SCRIPT_DIR.parent / "i18n"

def load_i18n(lang):
    """Load i18n labels for a language."""
    path = I18N_DIR / f"{lang}.json"
    if path.exists():
        return json.loads(path.read_text())
    # Fallback to Italian
    return json.loads((I18N_DIR / "it.json").read_text())


def is_multilingual(adventure_dir):
    """Check if adventure uses multilingual structure."""
    return (adventure_dir / "manifest.json").exists()


def get_lang_dir(adventure_dir, lang):
    """Get language-specific content directory."""
    if is_multilingual(adventure_dir):
        return adventure_dir / lang
    return adventure_dir


def get_default_lang(adventure_dir):
    """Get default language from manifest, or 'it'."""
    manifest = adventure_dir / "manifest.json"
    if manifest.exists():
        return json.loads(manifest.read_text()).get("default_lang", "it")
    return "it"

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


def resolve_image(img_path, use_lowres):
    """If use_lowres, return -lowres version (.jpg first, then .png) if it exists, else original."""
    if not use_lowres:
        return img_path
    stem = img_path.parent / (img_path.stem + LOWRES_SUFFIX)
    for ext in (".jpg", ".png"):
        candidate = stem.with_suffix(ext)
        if candidate.exists():
            return candidate
    return img_path


def find_cover(adventure_dir):
    """Find cover image: img/*_COVER.png (standard convention)."""
    img_dir = adventure_dir / "img"
    if not img_dir.exists():
        return None
    covers = list(img_dir.glob("*_COVER.png")) + list(img_dir.glob("*_COVER.jpg"))
    covers = [c for c in covers if LOWRES_SUFFIX not in c.stem]
    return covers[0] if covers else None


def is_portrait(img_path):
    """Check if image is portrait (height > width)."""
    from PIL import Image
    with Image.open(img_path) as img:
        return img.height > img.width


def fit_cover(img_path, title, author=None, year=None, scale=1.0, subtitle=None):
    """Create cover: background image scaled to A4, logo top center, title upper-center,
    D&D subtitle under title, author at bottom. White uppercase text with black outline."""
    if subtitle is None:
        subtitle = "Un'avventura Dungeons & Dragons 5e"
    from PIL import Image, ImageDraw, ImageFont

    out_w, out_h = int(A4_W * scale), int(A4_H * scale)

    # Load and scale background
    bg = Image.open(img_path).convert("RGBA")
    s = max(out_w / bg.width, out_h / bg.height)
    new_w, new_h = int(bg.width * s), int(bg.height * s)
    bg = bg.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - out_w) // 2
    top = (new_h - out_h) // 2
    bg = bg.crop((left, top, left + out_w, top + out_h)).convert("RGBA")

    # Dark gradient overlay on top area (for logo visibility)
    gradient_h = int(out_h * 0.18)
    gradient = Image.new("RGBA", (out_w, gradient_h), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(gradient)
    for y_pos in range(gradient_h):
        alpha = int(180 * (1 - y_pos / gradient_h))
        grad_draw.line([(0, y_pos), (out_w, y_pos)], fill=(0, 0, 0, alpha))
    bg = Image.alpha_composite(bg, Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0)))
    bg.paste(gradient, (0, 0), gradient)

    # Load logo and remove grey background
    logo_path = SCRIPT_DIR / "img" / "DracoRoboter_logo.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        data = logo.getdata()
        new_data = []
        for r, g, b, a in data:
            if max(r, g, b) - min(r, g, b) < 30 and max(r, g, b) < 120:
                new_data.append((r, g, b, 0))
            else:
                new_data.append((r, g, b, a))
        logo.putdata(new_data)
        logo_w = int(out_w * 0.20)
        logo_scale = logo_w / logo.width
        logo_h = int(logo.height * logo_scale)
        logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
        logo_x = (out_w - logo_w) // 2
        logo_y = int(out_h * 0.02)
        bg.paste(logo, (logo_x, logo_y), logo)

    # Setup drawing
    draw = ImageDraw.Draw(bg)
    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (30, 60, 160)

    # Font (scaled)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(font_path, int(160 * scale))
    sub_font = ImageFont.truetype(font_path, int(50 * scale))
    outline_w = max(1, int(6 * scale))

    def draw_outlined_text(x, y, text, font, fill=white, outline=black, width=outline_w):
        for dx in range(-width, width + 1):
            for dy in range(-width, width + 1):
                if dx * dx + dy * dy <= width * width:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline)
        draw.text((x, y), text, font=font, fill=fill)

    def centered_outlined_text(y, text, font, fill=white):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (out_w - tw) // 2
        draw_outlined_text(x, y, text, font, fill=fill)
        return bbox[3] - bbox[1]

    # Title — upper area (20% from top)
    title_upper = title.upper()
    title_y = int(out_h * 0.20)
    title_h = centered_outlined_text(title_y, title_upper, title_font)

    # Blue stripe under title
    stripe_y = title_y + title_h + int(out_h * 0.015)
    stripe_margin = int(out_w * 0.15)
    stripe_h = max(1, int(10 * scale))
    draw.rectangle([(stripe_margin, stripe_y), (out_w - stripe_margin, stripe_y + stripe_h)], fill=blue)

    # D&D subtitle — right under stripe
    sub_y = stripe_y + stripe_h + int(out_h * 0.015)
    centered_outlined_text(sub_y, subtitle, sub_font)

    # Author + copyright — bottom
    if author:
        author_y = int(out_h * 0.93)
        centered_outlined_text(author_y, author, sub_font)
        copy_font = ImageFont.truetype(font_path, int(30 * scale))
        copy_y = author_y + int(out_h * 0.035)
        yr = year or datetime.now().strftime("%Y")
        centered_outlined_text(copy_y, f"© {yr} CC BY-SA 4.0", copy_font)

    # Convert to RGB
    final = Image.new("RGB", (out_w, out_h), (0, 0, 0))
    final.paste(bg, mask=bg.split()[3])

    buf = io.BytesIO()
    final.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode(), "jpeg"


def find_modules(adventure_dir, lang_dir=None):
    """Find module directories sorted by number prefix.
    In multilingual mode, modules are under lang_dir."""
    base = lang_dir if lang_dir else adventure_dir
    modules = []
    for d in sorted(base.iterdir()):
        if d.is_dir() and re.match(r"\d+_", d.name):
            modules.append(d)
    return modules


def find_module_md(module_dir):
    """Find the main .md file in a module directory (not in subdirs)."""
    candidates = [
        f for f in module_dir.glob("*.md")
        if f.name not in EXCLUDED_FILES and not f.name.startswith(EXCLUDED_PREFIXES)
    ]
    return candidates[0] if candidates else None


def find_maps_in_dir(maps_dir, desc_dir=None):
    """Find map files (.md and .png) in maps directories.
    In multilingual mode, images are in maps_dir and descriptions in desc_dir.
    Returns list of (md_path_or_None, img_path_or_None) tuples, grouped by base name."""
    if desc_dir is None:
        desc_dir = maps_dir
    items = {}

    # Collect images from maps_dir
    if maps_dir and maps_dir.exists():
        for f in sorted(maps_dir.iterdir()):
            if f.is_dir() or f.name == "MappaGenerale.md":
                continue
            if LOWRES_SUFFIX in f.stem:
                continue
            stem = f.stem
            if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
                items.setdefault(stem, [None, None])[1] = f

    # Collect descriptions from desc_dir
    if desc_dir and desc_dir.exists():
        for f in sorted(desc_dir.iterdir()):
            if f.is_dir() or f.name == "MappaGenerale.md":
                continue
            stem = f.stem
            if f.suffix == ".md":
                items.setdefault(stem, [None, None])[0] = f

    return [(md, img) for md, img in items.values()]


def find_adventure_maps(adventure_dir, lang_dir=None):
    """Find maps in the adventure root maps/ directory.
    Images in adventure_dir/maps/, descriptions in lang_dir/maps/ (if multilingual)."""
    img_maps = adventure_dir / "maps"
    desc_maps = (lang_dir / "maps") if lang_dir else img_maps
    return find_maps_in_dir(img_maps, desc_maps)


def find_module_maps(module_dir, adventure_dir=None, lang_dir=None, mod_name=None):
    """Find all map files in module's maps/ subdirectory.
    In multilingual mode: images in adventure_dir/NN_Name/maps/, descriptions in lang module maps/."""
    if adventure_dir and lang_dir and mod_name:
        img_maps = adventure_dir / mod_name / "maps"
        desc_maps = module_dir / "maps"
    else:
        img_maps = module_dir / "maps"
        desc_maps = img_maps
    return find_maps_in_dir(img_maps, desc_maps)


def find_statblocks(adventure_dir, lang_dir=None):
    """Find NPC_*.png and MON_*.png stat blocks, alphabetically sorted."""
    base = lang_dir if lang_dir else adventure_dir
    sb_dir = base / "characters" / "statblock"
    if not sb_dir.exists():
        return []
    return sorted(
        f for f in sb_dir.iterdir()
        if f.suffix == ".png" and (f.name.startswith("NPC_") or f.name.startswith("MON_"))
    )


def extract_title(adventure_md):
    """Extract H1 title from the main adventure markdown."""
    if not adventure_md.exists():
        return adventure_md.stem
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
                for key in ("Livello consigliato", "Durata", "Struttura", "Tono", "Autore", "Prima stesura"):
                    if f"**{key}**:" in line:
                        meta[key] = line.split(":", 1)[1].strip()
    return meta


def build_html(adventure_name, adventure_dir, raw_cover=False, use_lowres=False, only_sections=None, lang=None):
    """Assemble the full HTML document. If only_sections is set, include only those sections."""
    if lang is None:
        lang = get_default_lang(adventure_dir)
    lang_dir = get_lang_dir(adventure_dir, lang)
    multilingual = is_multilingual(adventure_dir)
    i18n = load_i18n(lang)
    parts = []

    def include(section):
        """Check if a section should be included (None = all)."""
        return only_sections is None or section in only_sections

    # --- CSS ---
    css_text = CSS_FILE.read_text()
    parts.append(f"<html><head><meta charset='utf-8'><style>{css_text}</style></head><body>")

    # --- Title (needed for cover and frontmatter) ---
    adventure_md = lang_dir / f"{adventure_name}.md"
    title = extract_title(adventure_md) if adventure_md.exists() else adventure_name
    meta = extract_readme_meta(adventure_dir)

    # Override title/subtitle from manifest if available
    manifest_path = adventure_dir / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        if "title" in manifest and lang in manifest["title"]:
            title = manifest["title"][lang]
        cover_subtitle = manifest.get("subtitle", {}).get(lang, i18n["pdf_subtitle"])
        # Override frontmatter values from manifest for non-default languages
        fm_overrides = manifest.get("frontmatter", {}).get(lang, {})
        for k, v in fm_overrides.items():
            if k in meta:
                meta[k] = v
    else:
        cover_subtitle = i18n["pdf_subtitle"]

    # --- Cover ---
    cover = find_cover(adventure_dir)
    if cover and include("cover"):
        cover = resolve_image(cover, use_lowres)
        if raw_cover:
            cover_uri = cover.as_uri()
            parts.append(f'<div class="cover-page"><img src="{cover_uri}"></div>')
            print(f"  Cover: {cover.name} (immagine pura)")
        else:
            cover_scale = 0.5 if use_lowres else 1.0
            b64, fmt = fit_cover(cover, title, author=meta.get("Autore"),
                                 year=meta.get("Prima stesura"), scale=cover_scale,
                                 subtitle=cover_subtitle)
            parts.append(f'<div class="cover-page"><img src="data:image/{fmt};base64,{b64}"></div>')
            print(f"  Cover: {cover.name} (con logo/titolo/autore)")

    # --- Frontmatter ---
    if include("frontmatter"):
        date_str = datetime.now().strftime("%Y-%m-%d")

        parts.append('<div class="frontmatter">')
        parts.append(f"<h1>{title}</h1>")
        if meta.get("Tono"):
            parts.append(f'<div class="subtitle">{meta["Tono"]}</div>')
        parts.append("<hr>")
        parts.append('<div class="meta">')
        parts.append("D&amp;D 5e (2014)<br>")
        if meta.get("Livello consigliato"):
            parts.append(f'{i18n["pdf_level"]} {meta["Livello consigliato"]}<br>')
        if meta.get("Durata"):
            parts.append(f'{i18n["pdf_duration"]}: {meta["Durata"]}<br>')
        if meta.get("Struttura"):
            parts.append(f'{i18n["pdf_structure"]}: {meta["Struttura"]}<br>')
        parts.append(f"<br>{date_str}")
        if meta.get("Autore"):
            parts.append(f'<br><br><em>{meta["Autore"]}</em>')
            yr = meta.get("Prima stesura", datetime.now().strftime("%Y"))
            parts.append(f'<br><small>© {yr} CC BY-SA 4.0</small>')
        parts.append("</div></div>")
        print(f"  Frontmatter: {title}")

    # --- Main document ---
    if adventure_md.exists() and include("doc"):
        html = md_to_html(adventure_md)
        parts.append(f'<div class="section-break">{html}</div>')
        print(f"  Documento: {adventure_md.name}")

    # --- Adventure maps (maps/ root) ---
    if include("maps"):
        for map_md, map_img in find_adventure_maps(adventure_dir, lang_dir if multilingual else None):
            if map_md:
                html = md_to_html(map_md)
                parts.append(f'<div class="section-break">{html}</div>')
                print(f"  Mappa (desc): {map_md.name}")
            if map_img:
                map_img = resolve_image(map_img, use_lowres)
                name = map_img.stem.replace(LOWRES_SUFFIX, "")
                img_uri = map_img.as_uri()
                parts.append(f'<div class="map-page"><img src="{img_uri}" alt="{name}">'
                             f'<div class="map-caption">{name}</div></div>')
                print(f"  Mappa (img): {map_img.name}")

    # --- Modules ---
    for mod_dir in find_modules(adventure_dir, lang_dir if multilingual else None):
        mod_num = re.match(r"(\d+)_", mod_dir.name)
        mod_key = mod_num.group(1) if mod_num else None
        if not include(mod_key):
            continue

        mod_md = find_module_md(mod_dir)
        if mod_md:
            html = md_to_html(mod_md)
            parts.append(f'<div class="section-break">{html}</div>')
            print(f"  Modulo: {mod_md.name}")

        # Module maps
        for map_md, map_img in find_module_maps(
                mod_dir, adventure_dir if multilingual else None,
                lang_dir if multilingual else None, mod_dir.name):
            if map_md:
                html = md_to_html(map_md)
                parts.append(f'<div class="section-break">{html}</div>')
                print(f"  Mappa modulo (desc): {mod_dir.name}/maps/{map_md.name}")
            if map_img:
                map_img = resolve_image(map_img, use_lowres)
                name = map_img.stem.replace(LOWRES_SUFFIX, "")
                img_uri = map_img.as_uri()
                parts.append(f'<div class="map-page"><img src="{img_uri}" alt="{name}">'
                             f'<div class="map-caption">{name}</div></div>')
                print(f"  Mappa modulo (img): {mod_dir.name}/maps/{map_img.name}")

    # --- Stat block appendix ---
    statblocks = find_statblocks(adventure_dir, lang_dir if multilingual else None)
    if statblocks and include("statblocks"):
        parts.append(f'<div class="appendix-header"><h1>{i18n["pdf_appendix_statblock"]}</h1></div>')
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
    parser.add_argument("--raw-cover", action="store_true",
                        help="Usa immagine copertina senza elaborazione (no logo, titolo, autore)")
    parser.add_argument("--lowres", action="store_true",
                        help="Usa versioni -lowres.png delle immagini (da optimize-images.py)")
    parser.add_argument("--only", type=str, default=None,
                        help="Sezioni da includere (comma-separated): cover, frontmatter, doc, maps, statblocks, NN")
    parser.add_argument("--lang", type=str, default=None,
                        help="Lingua (default: da manifest.json o 'it')")
    args = parser.parse_args()

    adventure_name = args.adventure
    adventure_dir = PROJECT_ROOT / "adventures" / adventure_name

    if not adventure_dir.exists():
        print(f"Errore: {adventure_dir} non trovata.")
        sys.exit(1)

    # Resolve language
    lang = args.lang or get_default_lang(adventure_dir)

    # Parse --only sections
    only_sections = None
    if args.only:
        only_sections = set(s.strip() for s in args.only.split(","))
        valid = {"cover", "frontmatter", "doc", "maps", "statblocks"}
        for s in only_sections:
            if s not in valid and not re.match(r"^\d+$", s):
                print(f"Errore: sezione '{s}' non valida. Valori: cover, frontmatter, doc, maps, statblocks, NN")
                sys.exit(1)

    # Output
    date_stamp = datetime.now().strftime("%Y%m%d")
    out_dir = PROJECT_ROOT / "releases" / adventure_name
    out_dir.mkdir(parents=True, exist_ok=True)
    only_suffix = ""
    if only_sections:
        only_suffix = "_only-" + "_".join(sorted(only_sections))
    lowres_suffix = "_lowres" if args.lowres else ""
    lang_suffix = f"_{lang}" if lang != get_default_lang(adventure_dir) else ""
    pdf_path = out_dir / f"{adventure_name}_{date_stamp}{only_suffix}{lowres_suffix}{lang_suffix}.pdf"

    print(f"=== {adventure_name} — PDF {date_stamp} (lang={lang}) ===\n")

    # Build HTML
    html_content = build_html(adventure_name, adventure_dir, raw_cover=args.raw_cover,
                              use_lowres=args.lowres, only_sections=only_sections, lang=lang)

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
