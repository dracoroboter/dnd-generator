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
from datetime import datetime

ERRORS = []
WARNINGS = []
LOG = []  # tutte le righe per il report

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
    else:
        (error if required else warn)(f"{label} mancante: {os.path.relpath(path)}")
        return False

def check_dir_exists(path, label, required=True):
    if os.path.isdir(path):
        ok(label)
        return True
    else:
        (error if required else warn)(f"Directory {label} mancante: {os.path.relpath(path)}")
        return False

def check_sections(filepath, sections, label):
    if not os.path.isfile(filepath):
        return
    content = open(filepath, encoding="utf-8").read()
    for section in sections:
        pattern = rf"^##\s+{re.escape(section)}"
        if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            ok(f"{label}: sezione '{section}'")
        else:
            error(f"{label}: sezione '## {section}' mancante")

def check_naming_conventions(adventure_dir):
    # File .md devono essere PascalCase
    for root, dirs, files in os.walk(adventure_dir):
        rel_root = os.path.relpath(root, adventure_dir)
        for f in files:
            if not f.endswith(".md"):
                continue
            # Escludi file speciali con naming fisso
            if f in ("README.md", "AdventureBook.md", "PlanBook.md"):
                continue
            # PascalCase: inizia con maiuscola, niente trattini o underscore (eccetto NPC_)
            if not re.match(r'^[A-Z][A-Za-z0-9_]*\.md$', f):
                error(f"Naming non PascalCase: {os.path.join(rel_root, f)}")

        # Directory devono essere minuscole (eccetto moduli NN_ e root)
        for d in dirs:
            rel_d = os.path.join(rel_root, d)
            # Moduli: NN_NomeModulo — ok
            if re.match(r'^\d{2}_', d):
                continue
            # Directory di sistema
            if d.startswith('.'):
                continue
            if d != d.lower():
                error(f"Directory non minuscola: {rel_d}/")

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

def check_forbidden(adventure_dir):
    for forbidden in ["versioni", "Versioni", "Versions"]:
        path = os.path.join(adventure_dir, forbidden)
        if os.path.isdir(path):
            error(f"Directory '{forbidden}/' presente — le release vanno in releases/<NomeAvventura>/")

KNOWN_MAIN_SECTIONS = {
    "Lore", "Introduzione", "NPC principali", "Struttura dell'avventura",
    "Plot generale", "Consigli al master", "Running Gag", "Foreshadowing",
    "Agganci futuri", "Concept", "Ambientazione",
}

KNOWN_MODULE_SECTIONS = {
    "Descrizione", "Obiettivo", "Luoghi interni", "Luoghi e incontri", "Nemici",
    "Indizi chiave", "Ricompense", "Note al master", "Finale", "Milestone",
}

KNOWN_NPC_SECTIONS = {
    "Informazioni generali", "Descrizione", "Motivazioni", "Note al master",
    "Stat Block", "Agganci futuri", "Capacità notevoli", "Ruolo nell'avventura",
    "Da definire", "Running Gag",
}

def check_unknown_sections(filepath, known, label):
    if not os.path.isfile(filepath):
        return
    content = open(filepath, encoding="utf-8").read()
    found = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    for s in found:
        s_clean = s.strip()
        if s_clean not in known:
            warn(f"{label}: sezione non prevista '## {s_clean}'")

def check_modules(adventure_dir):
    modules = sorted([
        d for d in os.listdir(adventure_dir)
        if os.path.isdir(os.path.join(adventure_dir, d)) and re.match(r'^\d{2}_', d)
    ])
    if not modules:
        warn("Nessun modulo (NN_NomeModulo/) trovato")
        return
    for mod in modules:
        mod_dir = os.path.join(adventure_dir, mod)
        mod_name = mod[3:]
        mod_file = os.path.join(mod_dir, f"{mod_name}.md")
        if check_file_exists(mod_file, f"Modulo {mod}/{mod_name}.md"):
            check_sections(mod_file, ["Descrizione", "Obiettivo", "Ricompense", "Note al master"], f"Modulo {mod}")

def check_npcs(adventure_dir):
    personaggi_dir = os.path.join(adventure_dir, "personaggi")
    if not os.path.isdir(personaggi_dir):
        return
    npcs = [f for f in os.listdir(personaggi_dir) if f.startswith("NPC_") and f.endswith(".md")]
    if not npcs:
        warn("Nessuna scheda NPC trovata in personaggi/")
        return
    for npc in sorted(npcs):
        npc_path = os.path.join(personaggi_dir, npc)
        check_sections(npc_path, ["Informazioni generali", "Descrizione", "Motivazioni", "Note al master"], f"NPC {npc}")
        check_unknown_sections(npc_path, KNOWN_NPC_SECTIONS, f"NPC {npc}")

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

    section("File obbligatori")
    check_file_exists(os.path.join(adventure_dir, "README.md"), "README.md")
    check_file_exists(os.path.join(adventure_dir, "AdventureBook.md"), "AdventureBook.md")
    check_file_exists(os.path.join(adventure_dir, "PlanBook.md"), "PlanBook.md")
    main_md = os.path.join(adventure_dir, f"{adventure_name}.md")
    check_file_exists(main_md, f"{adventure_name}.md")
    check_file_exists(os.path.join(adventure_dir, "mappe", "MappaGenerale.md"), "mappe/MappaGenerale.md")
    check_file_exists(os.path.join(adventure_dir, "Cover.png"), "Cover.png", required=False)

    section("Directory")
    check_dir_exists(os.path.join(adventure_dir, "mappe"), "mappe/")
    check_dir_exists(os.path.join(adventure_dir, "personaggi"), "personaggi/", required=False)
    check_forbidden(adventure_dir)
    check_saga_metadata(adventure_dir)

    section("Sezioni documento principale")
    # Obbligatorie
    check_sections(main_md,
        ["Lore", "Introduzione", "NPC principali", "Struttura dell'avventura"],
        adventure_name)
    check_unknown_sections(main_md, KNOWN_MAIN_SECTIONS, adventure_name)
    # Consigliate (warning)
    if os.path.isfile(main_md):
        content = open(main_md, encoding="utf-8").read()
        for s in ["Plot generale", "Consigli al master"]:
            if not re.search(rf"^##\s+{re.escape(s)}", content, re.MULTILINE | re.IGNORECASE):
                warn(f"{adventure_name}: sezione consigliata '## {s}' assente")

    section("Moduli")
    check_modules(adventure_dir)

    section("Schede NPC")
    check_npcs(adventure_dir)

    section("Naming convention")
    check_naming_conventions(adventure_dir)

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

    # Genera report
    LOG.append(f"\n---\n")
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
