#!/usr/bin/env python3
"""
generate-statblocks.py — Genera XML FightClub + stat block PDF/PNG da schede NPC markdown.

Uso:
  python3 tech/fightclub/generate-statblocks.py <NomeAvventura>              # tutti gli NPC/MON (con immagini)
  python3 tech/fightclub/generate-statblocks.py <NomeAvventura> NPC_Korex    # singolo NPC
  python3 tech/fightclub/generate-statblocks.py <NomeAvventura> --no-image   # senza immagini
  python3 tech/fightclub/generate-statblocks.py <NomeAvventura> --lang en    # lingua inglese

Pipeline: .md → .xml (fightclub/) → .pdf + .png (statblock/)
"""

import sys
import os
import subprocess
import glob
import json


def resolve_dirs(project_root, adventure, lang):
    """Resolve directories based on structure (multilingual or legacy)."""
    adv_dir = os.path.join(project_root, "adventures", adventure)
    manifest_path = os.path.join(adv_dir, "manifest.json")

    if os.path.isfile(manifest_path):
        # Multilingual structure: <lang>/characters/{markdown,fightclub,statblock}
        lang_dir = os.path.join(adv_dir, lang)
        md_dir = os.path.join(lang_dir, "characters", "markdown")
        fc_dir = os.path.join(lang_dir, "characters", "fightclub")
        sb_dir = os.path.join(lang_dir, "characters", "statblock")
        # Images are always shared in root
        img_dir = os.path.join(adv_dir, "characters", "img")
    else:
        # Legacy structure
        md_dir = os.path.join(adv_dir, "characters", "markdown")
        fc_dir = os.path.join(adv_dir, "characters", "fightclub")
        sb_dir = os.path.join(adv_dir, "characters", "statblock")
        img_dir = os.path.join(adv_dir, "characters", "img")

    return md_dir, fc_dir, sb_dir, img_dir


def main():
    no_image = "--no-image" in sys.argv
    lang = "it"
    args_clean = []
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--no-image":
            i += 1
            continue
        if sys.argv[i] == "--lang" and i + 1 < len(sys.argv):
            lang = sys.argv[i + 1]
            i += 2
            continue
        args_clean.append(sys.argv[i])
        i += 1

    if len(args_clean) < 1:
        print(f"Uso: {sys.argv[0]} <NomeAvventura> [NomeScheda] [--no-image] [--lang xx]")
        sys.exit(1)

    adventure = args_clean[0]
    single = args_clean[1] if len(args_clean) > 1 else None

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../.."))

    md_dir, fc_dir, sb_dir, img_dir = resolve_dirs(project_root, adventure, lang)

    if not os.path.isdir(md_dir):
        print(f"Errore: {md_dir} non trovata.")
        sys.exit(1)

    os.makedirs(fc_dir, exist_ok=True)
    os.makedirs(sb_dir, exist_ok=True)

    md_to_fc = os.path.join(script_dir, "md-to-fightclub.py")
    md_to_sb = os.path.join(script_dir, "md-to-statblock-pdf.js")

    # Trova schede NPC_*.md e MON_*.md
    if single:
        name = single if single.endswith(".md") else single + ".md"
        md_files = [os.path.join(md_dir, name)]
        if not os.path.isfile(md_files[0]):
            print(f"Errore: {md_files[0]} non trovato.")
            sys.exit(1)
    else:
        md_files = sorted(
            glob.glob(os.path.join(md_dir, "NPC_*.md")) +
            glob.glob(os.path.join(md_dir, "MON_*.md"))
        )

    if not md_files:
        print("Nessuna scheda NPC_*.md o MON_*.md trovata.")
        sys.exit(1)

    errors = 0
    for md_path in md_files:
        base = os.path.splitext(os.path.basename(md_path))[0]
        xml_path = os.path.join(fc_dir, base + ".xml")
        pdf_path = os.path.join(sb_dir, base + ".pdf")
        png_path = os.path.join(sb_dir, base + ".png")

        # MD → XML
        cmd_xml = ["python3", md_to_fc, md_path, "-o", xml_path, "--lang", lang]
        r = subprocess.run(cmd_xml, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ✗ {base}: md→xml fallito: {r.stderr.strip() or r.stdout.strip()}")
            errors += 1
            continue
        print(f"  ✓ {base}.xml")

        # Cerca immagine in characters/img/ (NPC_Nome → Nome.png/.jpg)
        img_path = None
        if not no_image and os.path.isdir(img_dir):
            img_name = base.replace("NPC_", "").replace("MON_", "")
            for ext in (".png", ".jpg", ".jpeg"):
                candidate = os.path.join(img_dir, img_name + ext)
                if os.path.isfile(candidate):
                    img_path = candidate
                    break

        # XML → PDF
        cmd_pdf = ["node", md_to_sb, xml_path, "-o", pdf_path]
        if img_path:
            cmd_pdf += ["--image", img_path]
        r = subprocess.run(cmd_pdf, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ✗ {base}: xml→pdf fallito: {r.stderr.strip() or r.stdout.strip()}")
            errors += 1
            continue
        print(f"  ✓ {base}.pdf")

        # XML → PNG
        cmd_png = ["node", md_to_sb, xml_path, "-o", png_path]
        if img_path:
            cmd_png += ["--image", img_path]
        r = subprocess.run(cmd_png, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ✗ {base}: xml→png fallito: {r.stderr.strip() or r.stdout.strip()}")
            errors += 1
            continue
        print(f"  ✓ {base}.png")

    print()
    if errors:
        print(f"Completato con {errors} errori.")
        sys.exit(1)
    else:
        print(f"✓ {len(md_files)} schede generate in fightclub/ e statblock/")

    # Generate merged compendium XML
    xml_files = sorted(
        glob.glob(os.path.join(fc_dir, "NPC_*.xml")) +
        glob.glob(os.path.join(fc_dir, "MON_*.xml"))
    )
    if xml_files:
        compendium_path = os.path.join(fc_dir, f"{adventure}_Compendium.xml")
        with open(compendium_path, "w", encoding="utf-8") as out:
            out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            out.write('<compendium version="5" auto_indent="NO">\n')
            for xf in xml_files:
                with open(xf, "r", encoding="utf-8") as f:
                    inside = False
                    for line in f:
                        if "<monster>" in line:
                            inside = True
                        if inside:
                            out.write(line)
                        if "</monster>" in line:
                            inside = False
            out.write("</compendium>\n")
        count = len(xml_files)
        print(f"✓ {compendium_path} ({count} creature)")


if __name__ == "__main__":
    main()
