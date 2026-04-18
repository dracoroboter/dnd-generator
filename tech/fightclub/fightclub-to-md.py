#!/usr/bin/env python3
"""
fightclub-to-md.py — Converte un XML FightClub 5e in scheda NPC markdown
Uso: python3 tech/fightclub/fightclub-to-md.py <file.xml> [-o output.md]

Se il file XML contiene più mostri, genera un file .md per ciascuno.
"""

import sys
import os
import re
from xml.etree.ElementTree import parse as parse_xml

ALIGNMENT_MAP = {
    "lawful good": "Legale Buono", "neutral good": "Neutrale Buono", "chaotic good": "Caotico Buono",
    "lawful neutral": "Legale Neutrale", "neutral": "Neutrale", "chaotic neutral": "Caotico Neutrale",
    "lawful evil": "Legale Malvagio", "neutral evil": "Neutrale Malvagio", "chaotic evil": "Caotico Malvagio",
}

SIZE_MAP = {"T": "Minuscolo", "S": "Piccolo", "M": "Medio", "L": "Grande", "H": "Enorme", "G": "Mastodontico"}

def get(el, tag, default=""):
    child = el.find(tag)
    return child.text.strip() if child is not None and child.text else default

def mod(score):
    s = int(score)
    m = (s - 10) // 2
    return f"+{m}" if m >= 0 else str(m)

def speed_to_triple(speed_text):
    """Converte '40 ft.' in '12m / 40ft / 8qd'."""
    m = re.search(r"(\d+)\s*ft", speed_text)
    if m:
        ft = int(m.group(1))
        meters = ft * 1.5 / 5
        qd = ft // 5
        return f"{meters:g}m / {ft}ft / {qd}qd"
    return speed_text

def monster_to_md(monster, etype="monster"):
    if etype == "pc":
        name = get(monster, "label") or get(monster, "name", "Unknown")
        type_text = get(monster, "name", "")  # razza+classe+livello
    else:
        name = get(monster, "name", "Unknown")
        type_text = get(monster, "type", "humanoid")
    size = get(monster, "size", "M")
    alignment = get(monster, "alignment", "neutral")
    ac = get(monster, "ac", "10")
    hp = get(monster, "hp", "1")
    speed = get(monster, "speed", "30 ft.")
    cr = get(monster, "cr", "")

    stats = {s: get(monster, s, "10") for s in ["str", "dex", "con", "int", "wis", "cha"]}

    # Razza dal type
    if etype == "monster":
        race_match = re.search(r"\((.+?)\)", type_text)
        race = race_match.group(1).capitalize() if race_match else type_text.capitalize()
    else:
        # PC format: "Race Class Level" o "Race (Subrace) Class Level"
        race = type_text
        pc_match = re.match(r"^(.+?)\s+(\w+)\s+(\d+)$", type_text)
        if pc_match:
            race = pc_match.group(1)
            pc_class = pc_match.group(2)
            pc_level = pc_match.group(3)

    align_it = ALIGNMENT_MAP.get(alignment.lower(), alignment) if alignment else ""

    lines = []
    lines.append(f"# NPC_{name} — antagonista\n")
    lines.append("## Informazioni generali\n")
    if etype == "pc" and 'pc_class' in dir():
        lines.append(f"- **Ruolo**: PG")
        lines.append(f"- **Razza**: {race}")
        lines.append(f"- **Classe**: {pc_class}")
        lines.append(f"- **Livello**: {pc_level}")
    else:
        lines.append(f"- **Ruolo**: ...")
        lines.append(f"- **Razza**: {race}")
    if align_it:
        lines.append(f"- **Allineamento**: {align_it}")
    lines.append("")

    # Descrizione
    desc = get(monster, "description")
    lines.append("## Descrizione\n")
    lines.append(desc if desc else "> ⚠ *Da compilare.*")
    lines.append("")

    # Stat Block
    lines.append("## Stat Block\n")
    lines.append("| FOR | DES | COS | INT | SAG | CAR |")
    lines.append("|-----|-----|-----|-----|-----|-----|")
    row = " | ".join(f"{stats[s]} ({mod(stats[s])})" for s in ["str", "dex", "con", "int", "wis", "cha"])
    lines.append(f"| {row} |")
    lines.append("")
    lines.append(f"- **Punti ferita**: {hp}")
    lines.append(f"- **Classe armatura**: {ac}")
    lines.append(f"- **Velocità**: {speed_to_triple(speed)}")
    if cr:
        lines.append(f"- **CR**: {cr}")

    skill = get(monster, "skill")
    if not skill:
        # PC format: multiple <skill> tags
        skill_els = monster.findall("skill")
        if skill_els:
            skill = ", ".join(s.text.strip() for s in skill_els if s.text)
    if skill:
        lines.append(f"- **Abilità**: {skill}")

    save = get(monster, "save")
    if not save:
        save_els = monster.findall("save")
        if save_els:
            save = ", ".join(s.text.strip() for s in save_els if s.text)
    if save:
        lines.append(f"- **Tiri salvezza**: {save}")

    immune = get(monster, "immune")
    if immune:
        lines.append(f"- **Immunità danni**: {immune}")

    cond_immune = get(monster, "conditionImmune")
    if cond_immune:
        lines.append(f"- **Immunità condizioni**: {cond_immune}")

    senses = get(monster, "senses")
    if senses:
        lines.append(f"- **Sensi**: {senses}")

    languages = get(monster, "languages")
    if languages:
        lines.append(f"- **Lingue**: {languages}")

    lines.append("")

    # Traits
    traits = monster.findall("trait")
    if traits:
        lines.append("## Capacità notevoli\n")
        for trait in traits:
            tname = get(trait, "name")
            ttext = get(trait, "text")
            lines.append(f"- **{tname}**: {ttext}")
        lines.append("")

    # Actions
    actions = monster.findall("action")
    if actions:
        lines.append("## Attacchi\n")
        for action in actions:
            aname = get(action, "name")
            atext = get(action, "text")
            lines.append(f"### {aname}")
            lines.append(atext)
            lines.append("")

    # Reactions
    reactions = monster.findall("reaction")
    if reactions:
        lines.append("## Reazioni\n")
        for reaction in reactions:
            rname = get(reaction, "name")
            rtext = get(reaction, "text")
            lines.append(f"### {rname}")
            lines.append(rtext)
            lines.append("")

    # Legendary
    legendaries = monster.findall("legendary")
    if legendaries:
        lines.append("## Azioni leggendarie\n")
        for leg in legendaries:
            lname = get(leg, "name")
            ltext = get(leg, "text")
            lines.append(f"### {lname}")
            lines.append(ltext)
            lines.append("")

    lines.append("## Motivazioni\n")
    lines.append("> ⚠ *Da compilare.*\n")
    lines.append("## Note al master\n")
    lines.append("> ⚠ *Da compilare.*\n")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <file.xml> [-o output.md]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None
    if "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    tree = parse_xml(input_file)
    root = tree.getroot()
    monsters = root.findall("monster")
    pcs = root.findall("pc")
    entries = [(m, "monster") for m in monsters] + [(p, "pc") for p in pcs]

    if not entries:
        print("Nessun <monster> o <pc> trovato nel file XML.")
        sys.exit(1)

    for entry, etype in entries:
        if etype == "pc":
            name = get(entry, "label") or get(entry, "name", "Unknown")
        else:
            name = get(entry, "name", "Unknown")
        md = monster_to_md(entry, etype)

        if output_file and len(monsters) == 1:
            out = output_file
        else:
            slug = re.sub(r"[^a-zA-Z0-9]", "", name)
            out = output_file or f"NPC_{slug}.md"

        with open(out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✓ {name} → {out}")


if __name__ == "__main__":
    main()
