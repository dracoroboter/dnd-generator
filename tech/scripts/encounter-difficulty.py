#!/usr/bin/env python3
"""
encounter-difficulty.py — Calcola la difficoltà di un incontro D&D 5e
Basato sul sistema XP del Dungeon Master's Guide (2014)

Uso:
  python3 encounter-difficulty.py --players 4 5 --monsters 2 1 3 1
  python3 encounter-difficulty.py -p 4 5 -m 2 1 3 1

  -p / --players   : coppie <numero> <livello> (es: 4 5 = 4 PG di livello 5)
  -m / --monsters  : coppie <numero> <CR> (es: 2 1 = 2 nemici CR 1)
                     CR può essere: 0, 0.125, 0.25, 0.5, 1, 2, ... 30
                     oppure: 0, 1/8, 1/4, 1/2, 1, 2, ... 30
"""

import argparse
import sys
from fractions import Fraction

# Soglie XP per livello PG (DMG p.82)
# [Easy, Medium, Hard, Deadly]
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

# XP per CR (DMG p.274)
XP_BY_CR = {
    0:    10,
    0.125: 25,
    0.25: 50,
    0.5:  100,
    1:    200,
    2:    450,
    3:    700,
    4:    1100,
    5:    1800,
    6:    2300,
    7:    2900,
    8:    3900,
    9:    5000,
    10:   5900,
    11:   7200,
    12:   8400,
    13:   10000,
    14:   11500,
    15:   13000,
    16:   15000,
    17:   18000,
    18:   20000,
    19:   22000,
    20:   25000,
    21:   33000,
    22:   41000,
    23:   50000,
    24:   62000,
    25:   75000,
    26:   90000,
    27:   105000,
    28:   120000,
    29:   135000,
    30:   155000,
}

# Moltiplicatori per numero di mostri (DMG p.82)
def encounter_multiplier(n_monsters, n_players):
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
    # Aggiustamento per party piccolo/grande
    if n_players < 3:
        # party piccolo: un livello più alto
        thresholds = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
        idx = thresholds.index(mult)
        mult = thresholds[min(idx + 1, len(thresholds) - 1)]
    elif n_players >= 6:
        # party grande: un livello più basso
        thresholds = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
        idx = thresholds.index(mult)
        mult = thresholds[max(idx - 1, 0)]
    return mult

def parse_cr(s):
    """Converte stringa CR in float: '1/8' -> 0.125, '2' -> 2.0"""
    try:
        return float(Fraction(s))
    except (ValueError, ZeroDivisionError):
        raise argparse.ArgumentTypeError(f"CR non valido: '{s}'. Usa valori come 0, 1/8, 1/4, 1/2, 1, 2, ...")

def parse_pairs(values, label):
    """Converte lista piatta [n1, v1, n2, v2, ...] in lista di (count, value)"""
    if len(values) % 2 != 0:
        print(f"Errore: {label} richiede coppie <numero> <valore>")
        sys.exit(1)
    return [(int(values[i]), values[i+1]) for i in range(0, len(values), 2)]

def main():
    parser = argparse.ArgumentParser(
        description="Calcola difficoltà incontro D&D 5e (DMG 2014)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  %(prog)s -p 4 5 -m 2 1 3 1
    → 4 PG livello 5 vs 2 nemici CR1 + 3 nemici CR1

  %(prog)s -p 3 3 1 4 -m 1 0.5 2 2
    → party misto (3 PG lv3 + 1 PG lv4) vs 1 CR1/2 + 2 CR2
        """
    )
    parser.add_argument("-p", "--players", nargs="+", required=True,
                        metavar="N LVL",
                        help="coppie <numero> <livello> (es: 4 5)")
    parser.add_argument("-m", "--monsters", nargs="+", required=True,
                        metavar="N CR",
                        help="coppie <numero> <CR> (es: 2 1 o 1 1/4)")
    args = parser.parse_args()

    # Parse players
    player_pairs = parse_pairs(args.players, "--players")
    players = []
    for count, lvl in player_pairs:
        lvl = int(lvl)
        if lvl < 1 or lvl > 20:
            print(f"Errore: livello PG deve essere 1-20, trovato {lvl}")
            sys.exit(1)
        players.extend([lvl] * count)

    # Parse monsters
    monster_pairs = parse_pairs(args.monsters, "--monsters")
    monsters = []
    for count, cr_str in monster_pairs:
        cr = parse_cr(str(cr_str))
        if cr not in XP_BY_CR:
            print(f"Errore: CR {cr_str} non valido. CR supportati: 0, 1/8, 1/4, 1/2, 1-30")
            sys.exit(1)
        monsters.extend([cr] * count)

    n_players = len(players)
    n_monsters = len(monsters)

    # Soglie party
    party_thresholds = [0, 0, 0, 0]
    for lvl in players:
        for i, t in enumerate(XP_THRESHOLDS[lvl]):
            party_thresholds[i] += t

    # XP mostri
    raw_xp = sum(XP_BY_CR[cr] for cr in monsters)
    mult = encounter_multiplier(n_monsters, n_players)
    adjusted_xp = raw_xp * mult

    # Difficoltà
    labels = ["Easy", "Medium", "Hard", "Deadly"]
    difficulty = "Trivial"
    for i, label in enumerate(labels):
        if adjusted_xp >= party_thresholds[i]:
            difficulty = label

    # Output
    print()
    print(f"  Party:    {n_players} PG (livelli: {', '.join(str(l) for l in sorted(players))})")
    print(f"  Nemici:   {n_monsters} totali (CR: {', '.join(str(Fraction(cr).limit_denominator(8)) for cr in sorted(monsters))})")
    print()
    print(f"  XP nemici (raw):      {raw_xp:>7}")
    print(f"  Moltiplicatore:       {mult:>7.1f}×  ({n_monsters} mostri)")
    print(f"  XP aggiustati:        {adjusted_xp:>7.0f}")
    print()
    print(f"  Soglie party:")
    for i, label in enumerate(labels):
        marker = " ◄" if difficulty == label else ""
        print(f"    {label:<8} {party_thresholds[i]:>6} XP{marker}")
    print()
    print(f"  ══════════════════════════")
    print(f"  Difficoltà: {difficulty.upper()}")
    print()

if __name__ == "__main__":
    main()
