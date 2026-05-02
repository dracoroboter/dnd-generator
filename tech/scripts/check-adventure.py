#!/usr/bin/env python3
"""
check-adventure.py — Verifica la normalizzazione di un'avventura
Uso: python3 tech/scripts/check-adventure.py <NomeAvventura>
Esempio: python3 tech/scripts/check-adventure.py LAnelloDelConte

Output: stampa a schermo + genera tech/reports/ReportNormalization_<NomeAvventura>_<timestamp>.md
"""

import sys
import os
import re
import json
from datetime import datetime
from pathlib import Path

ERRORS = []
WARNINGS = []
LOG = []


def is_multilingual(adventure_dir):
    """Check if adventure uses multilingual structure."""
    return os.path.isfile(os.path.join(adventure_dir, "manifest.json"))


def get_lang_dir(adventure_dir, lang="it"):
    """Get language-specific content directory."""
    if is_multilingual(adventure_dir):
        return os.path.join(adventure_dir, lang)
    return adventure_dir


def get_default_lang(adventure_dir):
    """Get default language from manifest."""
    manifest = os.path.join(adventure_dir, "manifest.json")
    if os.path.isfile(manifest):
        with open(manifest) as f:
            return json.loads(f.read()).get("default_lang", "it")
    return "it"


def error(msg):
    line = f"  ✗ {msg}"
    ERRORS.append(line)
    LOG.append(line)

def warn(msg):
    line = f"  ⚠ {msg}"
    WARNINGS.append(line)
    LOG.append(line)

def ok(msg):
    line = f"  ✓ {msg}"
    print(line)
    LOG.append(line)

def section(title):
    line = f"\n[ {title} ]"
    print(line)
    LOG.append(line)

def check_file_exists(path, label, required=True):
    if os.path.isfile(path):
        ok(label)
        return True
    (error if required else warn)(f"{label} mancante: {os.path.relpath(path)}")
    return False

def check_dir_exists(path, label, required=True):
    if os.path.isdir(path):
        ok(label)
        return True
    (error if required else warn)(f"Directory {label} mancante: {os.path.relpath(path)}")
    return False

def check_sections(filepath, sections, label):
    if not os.path.isfile(filepath):
        return
    content = open(filepath, encoding="utf-8").read()
    for s in sections:
        if re.search(rf"^##\s+{re.escape(s)}", content, re.MULTILINE | re.IGNORECASE):
            ok(f"{label}: sezione '{s}'")
        else:
            error(f"{label}: sezione '## {s}' mancante")


KNOWN_MAIN_SECTIONS = {
    "Lore", "Introduzione", "NPC principali", "Struttura dell'avventura",
    "Plot generale", "Consigli al master", "Running Gag", "Foreshadowing",
    "Agganci futuri", "Concept", "Ambientazione",
}

# Sezioni con prefisso accettato (match parziale)
KNOWN_MAIN_PREFIXES = {"Appendice"}


KNOWN_MODULE_SECTIONS = {
    "Descrizione", "Obiettivo", "Luoghi interni", "Luoghi e incontri", "Nemici",
    "Indizi chiave", "Ricompense", "Note al master", "Finale", "Milestone",
}

KNOWN_NPC_SECTIONS = {
    # Obbligatorie
    "Informazioni generali", "Descrizione", "Motivazioni", "Note al master",
    # Meccaniche (npc-format.md)
    "Stat Block", "Attacchi", "Azioni bonus", "Reazioni",
    # Opzionali (npc-format.md)
    "Capacità notevoli", "Ruolo nell'avventura", "Agganci futuri", "Da definire",
    # Narrative
    "Backstory", "Punti aperti", "Running Gag",
}

def check_unknown_sections(filepath, known, label, prefixes=None):
    if not os.path.isfile(filepath):
        return
    content = open(filepath, encoding="utf-8").read()
    for s in re.findall(r'^##\s+(.+)$', content, re.MULTILINE):
        name = s.strip()
        if name in known:
            continue
        if prefixes and any(name.startswith(p) for p in prefixes):
            continue
        warn(f"{label}: sezione non prevista '## {name}'")

def check_naming_conventions(adventure_dir):
    # In multilingual mode, check inside lang dir
    check_base = get_lang_dir(adventure_dir)
    for root, dirs, files in os.walk(check_base):
        rel_root = os.path.relpath(root, check_base)
        # Skip other/ directories entirely
        if "other" in Path(rel_root).parts:
            dirs.clear()
            continue
        for f in files:
            if not f.endswith(".md"):
                continue
            if f in ("README.md", "AdventureBook.md", "PlanBook.md"):
                continue
            if not re.match(r'^[A-Z][A-Za-z0-9_]*\.md$', f):
                error(f"Naming non PascalCase: {os.path.join(rel_root, f)}")
        for d in dirs:
            if re.match(r'^\d{2}_', d) or d.startswith('.') or d == "other":
                continue
            if d != d.lower():
                error(f"Directory non minuscola: {os.path.join(rel_root, d)}/")


def check_deprecated(adventure_dir):
    """Check for deprecated files and directories."""
    # Deprecated directories (italian names)
    for old_name, new_name in [("mappe", "maps"), ("personaggi", "characters")]:
        old_path = os.path.join(adventure_dir, old_name)
        if os.path.isdir(old_path):
            error(f"Directory deprecata '{old_name}/' — rinominare in '{new_name}/'")

    # Deprecated MappaGenerale.md
    mg = os.path.join(adventure_dir, "maps", "MappaGenerale.md")
    if os.path.isfile(mg):
        warn("maps/MappaGenerale.md deprecato — splittare in un .md per ogni mappa (stesso nome del PNG)")

    # Deprecated MappaDM.md in modules
    for d in sorted(os.listdir(adventure_dir)):
        if not re.match(r'^\d{2}_', d):
            continue
        dm = os.path.join(adventure_dir, d, "maps", "MappaDM.md")
        if os.path.isfile(dm):
            warn(f"{d}/maps/MappaDM.md deprecato — rinominare con nome specifico PascalCase")

    # Forbidden directories
    for forbidden in ["versioni", "Versioni", "Versions"]:
        if os.path.isdir(os.path.join(adventure_dir, forbidden)):
            error(f"Directory '{forbidden}/' presente — le release vanno in releases/<NomeAvventura>/")


def check_maps(adventure_dir):
    """Check map conventions in maps/ and module maps/."""
    lang_dir = get_lang_dir(adventure_dir)
    multilingual = is_multilingual(adventure_dir)

    # Root maps: images in adventure_dir/maps/, descriptions in lang_dir/maps/
    maps_dir = os.path.join(adventure_dir, "maps")
    desc_dir = os.path.join(lang_dir, "maps") if multilingual else maps_dir
    if os.path.isdir(maps_dir) or os.path.isdir(desc_dir):
        _check_maps_dir(maps_dir if os.path.isdir(maps_dir) else desc_dir, "maps",
                        desc_dir=desc_dir if multilingual else None)

    # Module maps
    mod_base = lang_dir if multilingual else adventure_dir
    for d in sorted(os.listdir(mod_base)):
        if not re.match(r'^\d{2}_', d):
            continue
        mod_maps_img = os.path.join(adventure_dir, d, "maps") if multilingual else os.path.join(mod_base, d, "maps")
        mod_maps_desc = os.path.join(mod_base, d, "maps")
        if os.path.isdir(mod_maps_img) or os.path.isdir(mod_maps_desc):
            _check_maps_dir(mod_maps_img if os.path.isdir(mod_maps_img) else mod_maps_desc,
                            f"{d}/maps",
                            desc_dir=mod_maps_desc if multilingual else None)


def _check_maps_dir(maps_dir, label, desc_dir=None):
    """Check a single maps directory. If desc_dir is set, descriptions are there."""
    if desc_dir is None:
        desc_dir = maps_dir

    pngs = set()
    mds = set()
    svgs = set()

    if os.path.isdir(maps_dir):
        files = [f for f in os.listdir(maps_dir) if os.path.isfile(os.path.join(maps_dir, f))]
        pngs = {os.path.splitext(f)[0] for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))}
        svgs = {os.path.splitext(f)[0] for f in files if f.lower().endswith(".svg")}

    if os.path.isdir(desc_dir):
        desc_files = [f for f in os.listdir(desc_dir) if os.path.isfile(os.path.join(desc_dir, f))]
        mds = {os.path.splitext(f)[0] for f in desc_files if f.endswith(".md")}

    # PNG without corresponding .md
    for name in sorted(pngs - mds):
        warn(f"{label}/{name}.png senza descrizione {name}.md corrispondente")

    # SVG alongside PNG (should be in other/)
    for name in sorted(svgs & pngs):
        warn(f"{label}/{name}.svg duplica {name}.png — spostare SVG in other/")

    # SVG without PNG (acceptable but flag)
    for name in sorted(svgs - pngs):
        ok(f"{label}/{name}.svg (solo SVG, nessun PNG)")


def check_statblocks(adventure_dir):
    """Check stat block naming conventions."""
    lang_dir = get_lang_dir(adventure_dir)
    sb_dir = os.path.join(lang_dir, "characters", "statblock")
    if not os.path.isdir(sb_dir):
        return

    for f in sorted(os.listdir(sb_dir)):
        if not f.endswith(".png"):
            continue
        if f.startswith("NPC_") or f.startswith("MON_"):
            ok(f"Stat block: {f}")
        else:
            warn(f"characters/statblock/{f} — naming non riconosciuto (atteso NPC_* o MON_*). "
                 "Se è un PG, spostare in other/pg/")


def check_orphan_files(adventure_dir):
    """Flag files that don't match any known pattern."""
    known_root_files = {"README.md", "AdventureBook.md", "PlanBook.md", "DiscussioneNarrativa.md", "manifest.json"}
    adventure_name = os.path.basename(adventure_dir)
    multilingual = is_multilingual(adventure_dir)

    for f in sorted(os.listdir(adventure_dir)):
        path = os.path.join(adventure_dir, f)
        if os.path.isdir(path):
            continue
        if f in known_root_files:
            continue
        # In multilingual mode, main .md is under lang dir, not root
        if not multilingual and f == f"{adventure_name}.md":
            continue
        if f.endswith((".png", ".jpg", ".jpeg", ".svg")):
            warn(f"File immagine in root: {f} — dovrebbe stare in img/, maps/ o characters/img/?")
        elif f.startswith("DM_Prep") or f.startswith("StatBlock_"):
            continue  # meta-documents, ok in root


def check_modules(adventure_dir):
    lang_dir = get_lang_dir(adventure_dir)
    modules = sorted([
        d for d in os.listdir(lang_dir)
        if os.path.isdir(os.path.join(lang_dir, d)) and re.match(r'^\d{2}_', d)
    ])
    if not modules:
        warn("Nessun modulo (NN_NomeModulo/) trovato")
        return
    for mod in modules:
        mod_dir = os.path.join(lang_dir, mod)
        mod_name = mod[3:]
        mod_file = os.path.join(mod_dir, f"{mod_name}.md")
        if check_file_exists(mod_file, f"Modulo {mod}/{mod_name}.md"):
            check_sections(mod_file, ["Descrizione", "Obiettivo", "Ricompense", "Note al master"], f"Modulo {mod}")


def check_npcs(adventure_dir):
    lang_dir = get_lang_dir(adventure_dir)
    md_dir = os.path.join(lang_dir, "characters", "markdown")
    if not os.path.isdir(md_dir):
        # Fallback: check characters/ root for legacy layout
        md_dir = os.path.join(lang_dir, "characters")
        if not os.path.isdir(md_dir):
            return
    npcs = [f for f in os.listdir(md_dir) if f.startswith("NPC_") and f.endswith(".md")]
    if not npcs:
        warn("Nessuna scheda NPC trovata in characters/markdown/")
        return
    for npc in sorted(npcs):
        npc_path = os.path.join(md_dir, npc)
        check_sections(npc_path, ["Informazioni generali", "Descrizione", "Motivazioni", "Note al master"], f"NPC {npc}")
        check_unknown_sections(npc_path, KNOWN_NPC_SECTIONS, f"NPC {npc}")


def check_saga_metadata(adventure_dir):
    readme = os.path.join(adventure_dir, "README.md")
    if not os.path.isfile(readme):
        return
    content = open(readme, encoding="utf-8").read()
    if "**Saga**:" not in content:
        return
    for field in ["**Posizione**:", "**Segue**:", "**Precede**:"]:
        if field not in content:
            error(f"README.md: campo saga '{field}' mancante")


def main():
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <NomeAvventura>")
        sys.exit(1)

    adventure_name = sys.argv[1]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../.."))
    adventure_dir = os.path.join(project_root, "adventures", adventure_name)

    if not os.path.isdir(adventure_dir):
        print(f"Errore: directory '{adventure_dir}' non trovata.")
        sys.exit(1)

    print(f"\n=== Check normalizzazione: {adventure_name} ===\n")
    LOG.append(f"# Report Normalizzazione: {adventure_name}")
    LOG.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    lang_dir = get_lang_dir(adventure_dir)

    section("File obbligatori")
    check_file_exists(os.path.join(adventure_dir, "README.md"), "README.md")
    check_file_exists(os.path.join(adventure_dir, "AdventureBook.md"), "AdventureBook.md")
    check_file_exists(os.path.join(adventure_dir, "PlanBook.md"), "PlanBook.md")
    main_md = os.path.join(lang_dir, f"{adventure_name}.md")
    check_file_exists(main_md, f"{adventure_name}.md")

    section("Directory")
    # In multilingual mode, maps/ may not exist in root (e.g. FuoriDaHellfire has no map images)
    if is_multilingual(adventure_dir):
        check_dir_exists(os.path.join(lang_dir, "characters"), "characters/ (in lang dir)", required=False)
    else:
        check_dir_exists(os.path.join(adventure_dir, "maps"), "maps/")
        check_dir_exists(os.path.join(adventure_dir, "characters"), "characters/", required=False)

    section("File e directory deprecati")
    check_deprecated(adventure_dir)

    section("Sezioni documento principale")
    check_sections(main_md,
        ["Lore", "Introduzione", "NPC principali", "Struttura dell'avventura"],
        adventure_name)
    check_unknown_sections(main_md, KNOWN_MAIN_SECTIONS, adventure_name, KNOWN_MAIN_PREFIXES)
    if os.path.isfile(main_md):
        content = open(main_md, encoding="utf-8").read()
        for s in ["Plot generale", "Consigli al master"]:
            if not re.search(rf"^##\s+{re.escape(s)}", content, re.MULTILINE | re.IGNORECASE):
                warn(f"{adventure_name}: sezione consigliata '## {s}' assente")

    section("Moduli")
    check_modules(adventure_dir)

    section("Mappe")
    check_maps(adventure_dir)

    section("Schede NPC")
    check_npcs(adventure_dir)

    section("Stat block")
    check_statblocks(adventure_dir)

    section("Naming convention")
    check_naming_conventions(adventure_dir)
    check_saga_metadata(adventure_dir)

    section("File orfani")
    check_orphan_files(adventure_dir)

    # Summary
    print()
    if ERRORS:
        print(f"ERRORI ({len(ERRORS)}):")
        for e in ERRORS: print(e)
    if WARNINGS:
        print(f"WARNING ({len(WARNINGS)}):")
        for w in WARNINGS: print(w)
    if not ERRORS and not WARNINGS:
        summary = "✓ Tutto ok — avventura normalizzata correttamente."
    elif not ERRORS:
        summary = f"✓ Nessun errore critico ({len(WARNINGS)} warning)."
    else:
        summary = f"✗ {len(ERRORS)} errori, {len(WARNINGS)} warning."
    print(f"\n{summary}")

    # Report
    LOG.append("\n---\n")
    if ERRORS:
        LOG.append(f"## Errori ({len(ERRORS)})")
        LOG.extend(ERRORS)
    if WARNINGS:
        LOG.append(f"\n## Warning ({len(WARNINGS)})")
        LOG.extend(WARNINGS)
    LOG.append(f"\n## Risultato\n{summary}")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    reports_dir = os.path.join(project_root, "tech", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, f"ReportNormalization_{adventure_name}_{timestamp}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG))
    print(f"\nReport: tech/reports/{os.path.basename(report_path)}")

    if ERRORS:
        sys.exit(1)


if __name__ == "__main__":
    main()
