#!/usr/bin/env python3
"""
encounter-builder.py — Genera scontri bilanciati D&D 5e dal database SRD

Dato un party (numero e livello PG) e una difficoltà target, suggerisce
combinazioni di mostri dal database SRD 5e che rientrano nel budget XP.

Uso:
  python3 encounter-builder.py --players 4 5 --difficulty hard
  python3 encounter-builder.py -p 4 5 -d hard --type beast
  python3 encounter-builder.py -p 4 5 -d medium --max-monsters 6 --cr-range 0.5 3
  python3 encounter-builder.py -p 3 3 1 4 -d deadly --type undead --suggestions 10

Opzioni:
  -p / --players      : coppie <numero> <livello> (es: 4 5 = 4 PG di livello 5)
  -d / --difficulty    : easy, medium, hard, deadly
  --type               : filtra per tipo creatura (beast, undead, fiend, dragon, ...)
  --cr-range           : range CR min max (es: 0.5 3)
  --max-monsters       : numero massimo di mostri nell'incontro (default: 8)
  --suggestions        : numero di suggerimenti da generare (default: 5)
  --db                 : percorso database mostri JSON (default: auto-detect)
"""

import argparse
import json
import os
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

# --- XP tables from DMG (same as encounter-difficulty.py) ---

XP_THRESHOLDS = {
    1:  [25,   50,   75,   100],
    2:  [50,   100,  150,  200],
    3:  [75,   150,  225,  400],
    4:  [125,  250,  375,  500],
    5:  [250,  500,  750,  1100],
    6:  [300,  600,  900,  1400],
    7:  [350,  750,  1100, 1700],
    8:  [450,  900,  1400, 2100],
    9:  [550,  1100, 1600, 2400],
    10: [600,  1200, 1900, 2800],
    11: [800,  1600, 2400, 3600],
    12: [1000, 2000, 3000, 4500],
    13: [1100, 2200, 3400, 5100],
    14: [1250, 2500, 3800, 5700],
    15: [1400, 2800, 4300, 6400],
    16: [1600, 3200, 4800, 7200],
    17: [2000, 3900, 5900, 8800],
    18: [2100, 4200, 6300, 9500],
    19: [2400, 4900, 7300, 10900],
    20: [2800, 5700, 8500, 12700],
}

XP_BY_CR = {
    0: 10, 0.125: 25, 0.25: 50, 0.5: 100,
    1: 200, 2: 450, 3: 700, 4: 1100, 5: 1800,
    6: 2300, 7: 2900, 8: 3900, 9: 5000, 10: 5900,
    11: 7200, 12: 8400, 13: 10000, 14: 11500, 15: 13000,
    16: 15000, 17: 18000, 18: 20000, 19: 22000, 20: 25000,
    21: 33000, 22: 41000, 23: 50000, 24: 62000, 25: 75000,
    26: 90000, 27: 105000, 28: 120000, 29: 135000, 30: 155000,
}

DIFFICULTY_INDEX = {"easy": 0, "medium": 1, "hard": 2, "deadly": 3}


def encounter_multiplier(n_monsters, n_players):
    if n_monsters <= 0:
        return 1.0
    thresholds = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
    if n_monsters == 1:
        mult = 1.0
    elif n_monsters == 2:
        mult = 1.5
    elif n_monsters <= 6:
        mult = 2.0
    elif n_monsters <= 10:
        mult = 2.5
    elif n_monsters <= 14:
        mult = 3.0
    else:
        mult = 4.0
    idx = thresholds.index(mult)
    if n_players < 3:
        mult = thresholds[min(idx + 1, len(thresholds) - 1)]
    elif n_players >= 6:
        mult = thresholds[max(idx - 1, 0)]
    return mult


def parse_cr_string(challenge_str):
    """Parse '10 (5,900 XP)' or '1/4 (50 XP)' → float CR."""
    m = re.match(r"([\d/]+)", challenge_str.strip())
    if not m:
        return None
    try:
        return float(Fraction(m.group(1)))
    except (ValueError, ZeroDivisionError):
        return None


def parse_monster_type(meta_str):
    """Parse 'Large aberration, lawful evil' → 'aberration'."""
    # Format: "Size type, alignment" or "Size type (subtype), alignment"
    m = re.match(r"\w+\s+(\w+)", meta_str)
    return m.group(1).lower() if m else ""


def load_monsters(db_path):
    """Load and index monsters by CR."""
    with open(db_path) as f:
        raw = json.load(f)
    monsters = []
    for m in raw:
        cr = parse_cr_string(m.get("Challenge", ""))
        if cr is None or cr not in XP_BY_CR:
            continue
        monsters.append({
            "name": m["name"],
            "cr": cr,
            "xp": XP_BY_CR[cr],
            "type": parse_monster_type(m.get("meta", "")),
            "meta": m.get("meta", ""),
            "ac": m.get("Armor Class", "?"),
            "hp": m.get("Hit Points", "?"),
        })
    return monsters


def cr_label(cr):
    if cr == 0.125:
        return "1/8"
    if cr == 0.25:
        return "1/4"
    if cr == 0.5:
        return "1/2"
    return str(int(cr)) if cr == int(cr) else str(cr)


def party_xp_budget(players, difficulty):
    idx = DIFFICULTY_INDEX[difficulty]
    return sum(XP_THRESHOLDS[lvl][idx] for lvl in players)


def generate_encounter(monsters, budget_low, budget_high, n_players, max_monsters, rng):
    """Try to build a random encounter within the XP budget.

    Strategy: pick a random 'anchor' CR that fits, then optionally add
    smaller monsters to fill the remaining budget.
    """
    for _ in range(200):
        group = []
        # Pick anchor monster
        anchor = rng.choice(monsters)
        group.append(anchor)
        raw_xp = anchor["xp"]
        adj_xp = raw_xp * encounter_multiplier(1, n_players)
        if adj_xp > budget_high:
            continue

        # Try adding more monsters (same or lower CR)
        eligible = [m for m in monsters if m["xp"] <= anchor["xp"]]
        attempts = 0
        while len(group) < max_monsters and attempts < 30:
            attempts += 1
            candidate = rng.choice(eligible)
            new_raw = raw_xp + candidate["xp"]
            new_adj = new_raw * encounter_multiplier(len(group) + 1, n_players)
            if new_adj <= budget_high:
                group.append(candidate)
                raw_xp = new_raw
                adj_xp = new_adj
            elif new_adj > budget_high:
                break

        adj_xp = raw_xp * encounter_multiplier(len(group), n_players)
        if budget_low <= adj_xp <= budget_high:
            return group, raw_xp, adj_xp
    return None, 0, 0


def format_encounter(group):
    """Collapse group into counts: '2× Goblin (CR 1/4), 1× Bugbear (CR 1)'."""
    counts = {}
    for m in group:
        key = (m["name"], m["cr"])
        counts[key] = counts.get(key, 0) + 1
    parts = []
    for (name, cr), count in sorted(counts.items(), key=lambda x: (-x[0][1], x[0][0])):
        parts.append(f"{count}× {name} (CR {cr_label(cr)}, {XP_BY_CR[cr]} XP)")
    return parts


def find_db_path(explicit_path):
    if explicit_path:
        return explicit_path
    # Look relative to this script
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir.parent / "data" / "srd_5e_monsters.json",
        script_dir / "srd_5e_monsters.json",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    print("Errore: database mostri non trovato. Usa --db <percorso>")
    sys.exit(1)


def parse_pairs(values, label):
    if len(values) % 2 != 0:
        print(f"Errore: {label} richiede coppie <numero> <valore>")
        sys.exit(1)
    return [(int(values[i]), values[i + 1]) for i in range(0, len(values), 2)]


def main():
    parser = argparse.ArgumentParser(
        description="Genera scontri bilanciati D&D 5e dal database SRD",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  %(prog)s -p 4 5 -d hard
    → suggerisce scontri hard per 4 PG livello 5

  %(prog)s -p 4 5 -d medium --type undead
    → solo mostri di tipo undead

  %(prog)s -p 4 3 -d deadly --cr-range 1 5 --max-monsters 4
    → scontro deadly, CR 1-5, max 4 mostri
        """,
    )
    parser.add_argument("-p", "--players", nargs="+", required=True, metavar="N LVL")
    parser.add_argument("-d", "--difficulty", required=True,
                        choices=["easy", "medium", "hard", "deadly"])
    parser.add_argument("--type", help="filtra per tipo creatura (beast, undead, fiend, ...)")
    parser.add_argument("--cr-range", nargs=2, type=float, metavar=("MIN", "MAX"),
                        help="range CR (es: 0.5 3)")
    parser.add_argument("--max-monsters", type=int, default=8)
    parser.add_argument("--suggestions", type=int, default=5)
    parser.add_argument("--seed", type=int, help="seed per riproducibilità")
    parser.add_argument("--db", help="percorso database mostri JSON")
    args = parser.parse_args()

    # Parse players
    player_pairs = parse_pairs(args.players, "--players")
    players = []
    for count, lvl_str in player_pairs:
        lvl = int(lvl_str)
        if lvl < 1 or lvl > 20:
            print(f"Errore: livello PG deve essere 1-20, trovato {lvl}")
            sys.exit(1)
        players.extend([lvl] * count)
    n_players = len(players)

    # Load monsters
    db_path = find_db_path(args.db)
    all_monsters = load_monsters(db_path)

    # Filter
    filtered = all_monsters
    if args.type:
        t = args.type.lower()
        filtered = [m for m in filtered if t in m["type"]]
        if not filtered:
            print(f"Nessun mostro di tipo '{args.type}' trovato nel database.")
            print(f"Tipi disponibili: {', '.join(sorted(set(m['type'] for m in all_monsters)))}")
            sys.exit(1)
    if args.cr_range:
        cr_min, cr_max = args.cr_range
        filtered = [m for m in filtered if cr_min <= m["cr"] <= cr_max]
        if not filtered:
            print(f"Nessun mostro nel range CR {cr_label(cr_min)}-{cr_label(cr_max)}.")
            sys.exit(1)

    # XP budget
    diff_idx = DIFFICULTY_INDEX[args.difficulty]
    budget_target = party_xp_budget(players, args.difficulty)
    # Budget window: from previous difficulty threshold to target
    if diff_idx > 0:
        prev_diff = list(DIFFICULTY_INDEX.keys())[diff_idx - 1]
        budget_low = party_xp_budget(players, prev_diff)
    else:
        budget_low = 0
    budget_high = budget_target

    # For deadly, allow up to 1.3× the threshold (deadly has no upper bound in DMG)
    if args.difficulty == "deadly":
        budget_high = int(budget_target * 1.3)

    rng = random.Random(args.seed)

    # Header
    print()
    print(f"  Party:      {n_players} PG (livelli: {', '.join(str(l) for l in sorted(players))})")
    print(f"  Difficoltà: {args.difficulty.upper()}")
    print(f"  Budget XP:  {budget_low}–{budget_high} (adjusted)")
    if args.type:
        print(f"  Filtro:     tipo={args.type}")
    if args.cr_range:
        print(f"  CR range:   {cr_label(args.cr_range[0])}–{cr_label(args.cr_range[1])}")
    print(f"  Mostri DB:  {len(filtered)} disponibili (su {len(all_monsters)} totali)")
    print()

    # Generate suggestions
    seen = set()
    results = []
    for _ in range(args.suggestions * 20):
        if len(results) >= args.suggestions:
            break
        group, raw_xp, adj_xp = generate_encounter(
            filtered, budget_low, budget_high, n_players, args.max_monsters, rng
        )
        if group is None:
            continue
        # Deduplicate by composition
        key = tuple(sorted((m["name"], m["cr"]) for m in group))
        if key in seen:
            continue
        seen.add(key)
        results.append((group, raw_xp, adj_xp))

    if not results:
        print("  Nessun incontro trovato con questi parametri.")
        print("  Prova ad allargare il range CR o aumentare --max-monsters.")
        sys.exit(0)

    # Print results
    for i, (group, raw_xp, adj_xp) in enumerate(results, 1):
        mult = encounter_multiplier(len(group), n_players)
        parts = format_encounter(group)
        print(f"  ── Opzione {i} ──  ({len(group)} mostri, {adj_xp:.0f} XP adj, ×{mult})")
        for p in parts:
            print(f"     {p}")
        print()


if __name__ == "__main__":
    main()
