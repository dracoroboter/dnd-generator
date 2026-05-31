#!/usr/bin/env python3
"""
check-encounter-difficulty.py — Verifica le difficoltà dichiarate nei moduli

Legge il party dal documento principale, le tabelle nemici dai moduli,
calcola la difficoltà e confronta con quella dichiarata.
Genera un report in tech/reports/.

Uso:
    python3 tech/scripts/check-encounter-difficulty.py <NomeAvventura>
"""

import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime
from fractions import Fraction

# XP thresholds per player level (DMG p.82)
XP_THRESHOLDS = {
    1: [25, 50, 75, 100], 2: [50, 100, 150, 200], 3: [75, 150, 225, 400],
    4: [125, 250, 375, 500], 5: [250, 500, 750, 1100], 6: [300, 600, 900, 1400],
    7: [350, 750, 1100, 1700], 8: [450, 900, 1400, 2100], 9: [550, 1100, 1600, 2400],
    10: [600, 1200, 1900, 2800], 11: [800, 1600, 2400, 3600], 12: [1000, 2000, 3000, 4500],
    13: [1100, 2200, 3400, 5100], 14: [1250, 2500, 3800, 5700], 15: [1400, 2800, 4300, 6400],
    16: [1600, 3200, 4800, 7200], 17: [2000, 3900, 5900, 8800], 18: [2100, 4200, 6300, 9500],
    19: [2400, 4900, 7300, 10900], 20: [2800, 5700, 8500, 12700],
}

# XP by CR (DMG p.274)
XP_BY_CR = {
    0: 10, 0.125: 25, 0.25: 50, 0.5: 100, 1: 200, 2: 450, 3: 700, 4: 1100,
    5: 1800, 6: 2300, 7: 2900, 8: 3900, 9: 5000, 10: 5900, 11: 7200, 12: 8400,
    13: 10000, 14: 11500, 15: 13000, 16: 15000, 17: 18000, 18: 20000, 19: 22000,
    20: 25000, 21: 33000, 22: 41000, 23: 50000, 24: 62000, 25: 75000, 26: 90000,
    27: 105000, 28: 120000, 29: 135000, 30: 155000,
}

# Encounter multipliers by number of monsters (DMG p.82)
def get_multiplier(n_monsters):
    if n_monsters == 1: return 1
    if n_monsters == 2: return 1.5
    if n_monsters <= 6: return 2
    if n_monsters <= 10: return 2.5
    if n_monsters <= 14: return 3
    return 4


# CR → equivalent player level (Xanathar's Guide, solo player matchup table)
CR_TO_LEVEL = {
    0: 1, 0.125: 1, 0.25: 1, 0.5: 1,
    1: 2, 2: 4, 3: 5, 4: 6, 5: 8, 6: 9, 7: 10, 8: 11,
    9: 12, 10: 13, 11: 14, 12: 15, 13: 16, 14: 17,
    15: 18, 16: 18, 17: 19, 18: 19, 19: 20, 20: 20,
}


def cr_to_level(cr):
    """Convert CR to approximate equivalent player level."""
    if cr in CR_TO_LEVEL:
        return CR_TO_LEVEL[cr]
    # For fractional CRs not in table, round to nearest
    closest = min(CR_TO_LEVEL.keys(), key=lambda k: abs(k - cr))
    return CR_TO_LEVEL[closest]


def parse_cr(cr_str):
    """Parse CR string like '1/4', '0.25', '3'."""
    cr_str = cr_str.strip()
    if '/' in cr_str:
        return float(Fraction(cr_str))
    return float(cr_str)


def calc_difficulty(players, monsters):
    """Calculate encounter difficulty.
    players: list of (count, level)
    monsters: list of (count, cr)
    Returns: (difficulty_label, adjusted_xp, thresholds)
    """
    # Party thresholds
    thresholds = [0, 0, 0, 0]  # Easy, Medium, Hard, Deadly
    for count, level in players:
        if level in XP_THRESHOLDS:
            for i in range(4):
                thresholds[i] += count * XP_THRESHOLDS[level][i]

    # Monster XP
    total_monsters = sum(c for c, _ in monsters)
    base_xp = sum(count * XP_BY_CR.get(cr, 0) for count, cr in monsters)
    multiplier = get_multiplier(total_monsters)
    adjusted_xp = int(base_xp * multiplier)

    # Determine difficulty
    if adjusted_xp >= thresholds[3]:
        label = "DEADLY"
    elif adjusted_xp >= thresholds[2]:
        label = "HARD"
    elif adjusted_xp >= thresholds[1]:
        label = "MEDIUM"
    elif adjusted_xp >= thresholds[0]:
        label = "EASY"
    else:
        label = "TRIVIAL"

    return label, adjusted_xp, thresholds


def parse_party_from_doc(doc_path):
    """Parse party composition from a document.
    Looks for patterns like '3 PG lv5', 'Udo (CR 3)', 'Fin (lv3)', '(veterano CR3)', '(rogue lv3)'.
    Returns list of (count, level).
    """
    text = Path(doc_path).read_text()
    players = []

    # Pattern: N PG lvX or N PG lv X or N PG di livello X
    for m in re.finditer(r'(\d+)\s*PG\s*(?:di\s*livello\s*|lv\s*|livello\s*)(\d+)', text, re.IGNORECASE):
        players.append((int(m.group(1)), int(m.group(2))))

    # Pattern: NPC companion with CR
    # e.g. "(CR 3)", "(CR3)", "(veterano CR3)", "(veterano CR 3)"
    for m in re.finditer(r'\([\w\s]*CR\s*(\d+)\)', text, re.IGNORECASE):
        cr = int(m.group(1))
        players.append((1, cr))

    # Pattern: NPC companion with level
    # e.g. "(lv3)", "(rogue lv3)", "(lv 3)"
    for m in re.finditer(r'\([\w\s]*lv\s*(\d+)\)', text, re.IGNORECASE):
        players.append((1, int(m.group(1))))

    return players


def parse_encounters_from_module(module_path):
    """Parse encounter tables from a module.
    Looks for the ## Nemici section with difficulty tables.
    Returns list of dicts with 'monsters', 'declared_difficulty', 'location'.
    Also tries to extract per-module party level from header like '(3 PG lv5 + Udo + Fin)'.
    """
    text = Path(module_path).read_text()
    encounters = []
    module_party = None

    # Try to find per-module party from:
    # 1. "**Party:** 3 PG lv5 + Udo CR3 + Fin lv3" (in module, preferred)
    # 2. "Difficoltà (3 PG lv5 + Udo CR3 + Fin lv3)" (legacy, in table header)
    party_line = re.search(r'\*\*Party:?\*\*:?\s*(.+)', text)
    if not party_line:
        party_line = re.search(r'Difficolt[àa]\s*\(([^)]+)\)', text)
    
    if party_line:
        header_text = party_line.group(1)
        pg_match = re.search(r'(\d+)\s*PG\s*lv\s*(\d+)', header_text)
        if pg_match:
            pg_count = int(pg_match.group(1))
            pg_level = int(pg_match.group(2))
            module_party = [(pg_count, pg_level)]
            # Parse companions: "Name CR3" or "Name lv3"
            parts = header_text.split('+')
            for part in parts[1:]:
                part = part.strip()
                cr_match = re.search(r'CR\s*(\d+(?:/\d+)?)', part, re.IGNORECASE)
                lv_match = re.search(r'lv\s*(\d+)', part, re.IGNORECASE)
                if cr_match:
                    cr_val = parse_cr(cr_match.group(1))
                    equiv_level = cr_to_level(cr_val)
                    module_party.append((1, equiv_level))
                elif lv_match:
                    module_party.append((1, int(lv_match.group(1))))
                else:
                    # Companion without level/CR — assume same as PG
                    module_party.append((1, pg_level))

    # Find ## Nemici section
    nemici_match = re.search(r'^## Nemici\s*\n(.*?)(?=^## |\Z)', text, re.MULTILINE | re.DOTALL)
    if not nemici_match:
        return encounters, module_party

    nemici_text = nemici_match.group(1)

    # Parse table rows: | Luogo | Nemici | N. | CR | Difficoltà |
    for line in nemici_text.splitlines():
        if not line.strip().startswith('|') or '---' in line:
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) < 5:
            continue

        location = cells[0]
        enemy = cells[1]
        count_str = cells[2]
        cr_str = cells[3]
        declared = cells[4]

        # Skip header row
        if 'Luogo' in location or 'Nemici' in enemy:
            continue
        # Skip non-combattibili
        if 'Non combattibili' in declared or ('—' == cr_str.strip() and '—' == declared.strip()):
            continue
        if '—' == cr_str.strip():
            continue

        try:
            count = int(re.search(r'\d+', count_str).group())
            cr = parse_cr(cr_str)
        except (ValueError, AttributeError):
            continue

        encounters.append({
            'location': location,
            'enemy': enemy,
            'count': count,
            'cr': cr,
            'declared': declared.strip().upper(),
        })

    return encounters, module_party


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 check-encounter-difficulty.py <NomeAvventura>")
        sys.exit(1)

    adventure_name = sys.argv[1]
    project_root = Path(__file__).resolve().parent.parent.parent
    adv_dir = project_root / "adventures" / adventure_name

    if not adv_dir.exists():
        print(f"ERRORE: {adv_dir} non esiste")
        sys.exit(1)

    # Determine language
    manifest_path = adv_dir / "manifest.json"
    lang = "it"
    if manifest_path.exists():
        lang = json.loads(manifest_path.read_text()).get("default_lang", "it")

    lang_dir = adv_dir / lang

    # Find main document
    main_doc = lang_dir / f"{adventure_name}.md"
    if not main_doc.exists():
        print(f"ERRORE: documento principale non trovato: {main_doc}")
        sys.exit(1)

    # Find modules
    modules = sorted([d for d in lang_dir.iterdir()
                      if d.is_dir() and re.match(r'\d+_', d.name)])

    # Parse party — search in main doc, DM_Prep, PlanBook, AdventureBook, modules
    party = []
    search_files = [main_doc]
    # Also check DM_Prep files and PlanBook
    for mod_dir in modules:
        dm_prep = mod_dir / "DM_Prep.md"
        if dm_prep.exists():
            search_files.append(dm_prep)
        # Also check module files themselves
        for f in mod_dir.glob("*.md"):
            if not f.name.startswith("DM_Prep"):
                search_files.append(f)
    planbook = adv_dir / "PlanBook.md"
    if planbook.exists():
        search_files.append(planbook)
    adventurebook = adv_dir / "AdventureBook.md"
    if adventurebook.exists():
        search_files.append(adventurebook)

    for f in search_files:
        party = parse_party_from_doc(f)
        if party:
            party_source = f.relative_to(adv_dir)
            break

    if not party:
        print(f"ERRORE: party non trovato in nessun documento")
        sys.exit(1)

    # Report
    report = []
    report.append(f"# Report Difficoltà Incontri — {adventure_name}")
    report.append(f"\nData: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"\n## Party")
    report.append(f"\nRilevato da `{party_source}`:")
    for count, level in party:
        report.append(f"- {count}× livello {level}")
    total_players = sum(c for c, _ in party)
    report.append(f"\n**Totale combattenti:** {total_players}")

    # Thresholds
    thresholds = [0, 0, 0, 0]
    for count, level in party:
        if level in XP_THRESHOLDS:
            for i in range(4):
                thresholds[i] += count * XP_THRESHOLDS[level][i]
    report.append(f"\n**Soglie XP:** Easy {thresholds[0]} | Medium {thresholds[1]} | Hard {thresholds[2]} | Deadly {thresholds[3]}")

    problems = []
    report.append(f"\n## Moduli\n")

    for mod_dir in modules:
        # Find module .md (not DM_Prep)
        mod_files = [f for f in mod_dir.glob("*.md")
                     if not f.name.startswith("DM_Prep")]
        if not mod_files:
            continue

        mod_file = mod_files[0]
        encounters, module_party = parse_encounters_from_module(mod_file)

        if not encounters:
            continue

        # Use per-module party if available, otherwise global
        effective_party = module_party if module_party else party

        report.append(f"### {mod_dir.name}")
        if module_party and module_party != party:
            report.append(f"*Party modulo: {', '.join(f'{c}×lv{l}' for c,l in module_party)}*\n")

        # Group encounters by location (same location = combined encounter)
        from collections import OrderedDict
        grouped = OrderedDict()
        for enc in encounters:
            loc = enc['location']
            if loc not in grouped:
                grouped[loc] = {'monsters': [], 'declared': enc['declared'], 'enemies_desc': []}
            grouped[loc]['monsters'].append((enc['count'], enc['cr']))
            grouped[loc]['enemies_desc'].append(f"{enc['count']}× {enc['enemy']} CR {enc['cr']}")
            # The declared difficulty is on the first row only
            if enc['declared'] and enc['declared'] != '—':
                grouped[loc]['declared'] = enc['declared']

        for loc, data in grouped.items():
            monsters = data['monsters']
            declared = data['declared']
            enemies_str = " + ".join(data['enemies_desc'])

            calc_label, adj_xp, _ = calc_difficulty(effective_party, monsters)

            # Normalize declared: remove parenthetical notes
            declared_clean = re.sub(r'\(.*?\)', '', declared).strip()
            declared_norm = declared_clean.replace('-', '').replace(' ', '').upper()
            calc_norm = calc_label.replace('-', '').replace(' ', '').upper()

            # Skip rows with no declared difficulty (— only)
            if declared_norm == '—' or declared_norm == '':
                continue

            # Check match
            match = (calc_norm == declared_norm or
                     declared_norm in ("MEDIUMHARD",) and calc_norm in ("MEDIUM", "HARD"))

            status = "✓" if match else "✗"
            if not match:
                problems.append(f"{mod_dir.name}: {loc} — {enemies_str} — dichiarato {declared_clean}, calcolato {calc_label} ({adj_xp} XP adj.)")

            report.append(f"| {loc} | {enemies_str} | {adj_xp} XP adj. | Dichiarato: **{declared_clean}** | Calcolato: **{calc_label}** | {status} |")

        report.append("")

    # Summary
    report.append(f"\n## Riepilogo\n")
    if problems:
        report.append(f"**{len(problems)} problemi trovati:**\n")
        for p in problems:
            report.append(f"- {p}")
    else:
        report.append("✓ Tutte le difficoltà dichiarate corrispondono al calcolo.")

    # Write report
    report_dir = project_root / "tech" / "reports"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / f"ReportDifficulty_{adventure_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    report_text = "\n".join(report)
    report_path.write_text(report_text)

    # Print
    print(report_text)
    print(f"\n→ Report salvato: {report_path.relative_to(project_root)}")

    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
