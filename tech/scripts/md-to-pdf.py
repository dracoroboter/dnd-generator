#!/usr/bin/env python3
"""Convert any Markdown file to PDF using the adventure CSS style.

Usage:
    python3 md-to-pdf.py <file.md> [--output <file.pdf>]

If --output is not specified, the PDF is saved next to the source with .pdf extension.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "create-pdf-adventure"
CSS_FILE = SCRIPT_DIR / "adventure.css"
DM_PREP_CSS = SCRIPT_DIR / "dm-prep.css"


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF (adventure style)")
    parser.add_argument("input", help="Markdown file to convert")
    parser.add_argument("--output", "-o", help="Output PDF path (default: same name, .pdf)")
    parser.add_argument("--dm-prep", action="store_true",
                        help="Add DM Prep CSS (no page-break inside stat blocks/tables)")
    args = parser.parse_args()

    md_path = Path(args.input).resolve()
    if not md_path.exists():
        print(f"ERRORE: {md_path} non esiste")
        sys.exit(1)

    if not CSS_FILE.exists():
        print(f"ERRORE: CSS non trovato: {CSS_FILE}")
        sys.exit(1)

    # Auto-detect DM_Prep files
    is_dm_prep = args.dm_prep or "DM_Prep" in md_path.name

    pdf_path = Path(args.output) if args.output else md_path.with_suffix(".pdf")

    # Extract title from first H1 or filename
    title = md_path.stem
    for line in md_path.read_text().splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # Convert MD → HTML via pandoc
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as tmp:
        tmp_html = Path(tmp.name)

    r = subprocess.run(
        ["pandoc", str(md_path), "-t", "html5", "--standalone",
         "--metadata", f"title={title}", "-o", str(tmp_html)],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print(f"ERRORE pandoc: {r.stderr}")
        sys.exit(1)

    # Inject adventure CSS (+ dm-prep CSS if applicable)
    css_text = CSS_FILE.read_text()
    if is_dm_prep and DM_PREP_CSS.exists():
        css_text += "\n" + DM_PREP_CSS.read_text()
    html = tmp_html.read_text()
    html = html.replace("</head>", f"<style>{css_text}</style></head>")
    tmp_html.write_text(html)

    # HTML → PDF via weasyprint
    r = subprocess.run(
        ["weasyprint", str(tmp_html), str(pdf_path)],
        capture_output=True, text=True
    )
    tmp_html.unlink()

    if r.returncode != 0:
        print(f"ERRORE weasyprint: {r.stderr}")
        sys.exit(1)

    size_kb = pdf_path.stat().st_size / 1024
    print(f"✓ {pdf_path} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
