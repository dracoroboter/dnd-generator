#!/usr/bin/env python3
"""
md-to-fightclub.py — Converte una scheda NPC markdown in XML FightClub 5e
Uso: python3 tech/fightclub/md-to-fightclub.py <file.md> [-o output.xml]
"""

import sys
import re
import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

# Mapping italiano → inglese per allineamenti
ALIGNMENT_MAP = {
    "legale buono": "lawful good", "neutrale buono": "neutral good", "caotico buono": "chaotic good",
    "legale neutrale": "lawful neutral", "neutrale": "neutral", "caotico neutrale": "chaotic neutral",
    "legale malvagio": "lawful evil", "neutrale malvagio": "neutral evil", "caotico malvagio": "chaotic evil",
}

SIZE_MAP = {
    "minuscolo": "T", "tiny": "T", "piccolo": "S", "small": "S",
    "medio": "M", "medium": "M", "grande": "L", "large": "L",
    "enorme": "H", "huge": "H", "mastodontico": "G", "gargantuan": "G",
}

RACE_TO_SIZE = {
    "halfling": "S", "gnomo": "S", "gnome": "S",
    "umano": "M", "human": "M", "elfo": "M", "elf": "M",
    "nano": "M", "dwarf": "M", "mezzelfo": "M", "half-elf": "M",
    "mezzorco": "M", "half-orc": "M", "tiefling": "M", "dragonborn": "M",
}

def parse_md(filepath):
    """Parse un file NPC markdown e restituisce un dict con i dati estratti."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    data = {}
    # Nome dal titolo
    m = re.search(r"^# (?:NPC_)?(.+?)(?:\s*—.*)?$", text, re.MULTILINE)
    data["name"] = m.group(1).strip() if m else os.path.basename(filepath).replace("NPC_", "").replace(".md", "")

    # Informazioni generali
    for key, xml_key in [("Ruolo", "role"), ("Classe", "class"), ("Livello", "level"),
                          ("Razza", "race"), ("Allineamento", "alignment")]:
        m = re.search(rf"\*\*{key}\*\*:\s*(.+)", text)
        if m:
            data[xml_key] = m.group(1).strip()

    # Stat block - tabella
    m = re.search(r"\|\s*(\d+)\s*\([+-]?\d+\)\s*\|\s*(\d+)\s*\([+-]?\d+\)\s*\|\s*(\d+)\s*\([+-]?\d+\)\s*\|\s*(\d+)\s*\([+-]?\d+\)\s*\|\s*(\d+)\s*\([+-]?\d+\)\s*\|\s*(\d+)\s*\([+-]?\d+\)\s*\|", text)
    if m:
        data["str"], data["dex"], data["con"] = m.group(1), m.group(2), m.group(3)
        data["int"], data["wis"], data["cha"] = m.group(4), m.group(5), m.group(6)

    # CR — dal campo Sfida nel markdown, fallback stima dal livello
    cr_match = re.search(r"\*\*Sfida\*\*:\s*(\S+)", text)
    if cr_match:
        cr_val = cr_match.group(1).strip()
        # Accetta formati: "1", "1/2", "1/4", "1/8", "0"
        data["cr"] = cr_val

    # Campi stat block
    for key, xml_key in [("Punti ferita", "hp"), ("Classe armatura", "ac"),
                          ("Bonus competenza", "pb"), ("Percezione", "perception"),
                          ("Performance", "performance"), ("Furtività", "stealth"),
                          ("Immunità", "immune"), ("Sensi", "senses"),
                          ("Lingue", "languages"), ("CD tiro salvezza magia", "spelldc"),
                          ("Bonus attacco magia", "spellattack")]:
        m = re.search(rf"\*\*{key}\*\*:\s*(.+)", text)
        if m:
            data[xml_key] = m.group(1).strip()

    # Velocità — estrai solo i feet
    m = re.search(r"\*\*Velocità\*\*:\s*(.+)", text)
    if m:
        speed_text = m.group(1).strip()
        ft_match = re.search(r"(\d+)\s*ft", speed_text)
        if ft_match:
            data["speed"] = ft_match.group(1) + " ft."
        else:
            m2 = re.search(r"(\d+)\s*m", speed_text)
            if m2:
                data["speed"] = str(int(float(m2.group(1)) / 1.5 * 5)) + " ft."

    # Attacchi (sezione ## Attacchi)
    data["actions"] = []
    attack_section = re.search(r"## Attacchi\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if attack_section:
        attacks = re.split(r"### ", attack_section.group(1))
        for atk in attacks:
            if not atk.strip():
                continue
            lines = atk.strip().split("\n")
            name = lines[0].strip()
            atk_bonus = ""
            damage = ""
            desc_parts = []
            for line in lines[1:]:
                line = line.strip("- ").strip()
                if not line:
                    continue
                m_atk = re.search(r"\*\*Attacco\*\*:\s*\+(\d+)", line)
                if m_atk:
                    atk_bonus = "+" + m_atk.group(1)
                m_dmg = re.search(r"\*\*Danni\*\*:\s*(.+)", line)
                if m_dmg:
                    damage = m_dmg.group(1).strip()
                desc_parts.append(re.sub(r"\*\*(.+?)\*\*:\s*", r"\1: ", line))

            action = {"name": name, "text": " ".join(desc_parts)}
            if atk_bonus and damage:
                # Estrai prima formula danni per il tag <attack>
                dmg_match = re.search(r"(\d+d\d+[+-]?\d*)", damage)
                if dmg_match:
                    action["attack"] = f"{name}|{atk_bonus}|{dmg_match.group(1)}"
            data["actions"].append(action)

    # Azioni bonus
    bonus_section = re.search(r"## Azioni bonus\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if bonus_section:
        for line in bonus_section.group(1).strip().split("\n"):
            line = line.strip("- ").strip()
            if not line:
                continue
            m = re.match(r"\*\*(.+?)\*\*:\s*(.+)", line)
            if m:
                data.setdefault("traits", []).append({"name": m.group(1), "text": m.group(2)})

    # Capacità notevoli
    data.setdefault("traits", [])
    cap_section = re.search(r"## Capacità notevoli\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if cap_section:
        cap_text = cap_section.group(1).strip()
        # Incantesimi
        if "Incantesimi" in cap_text or "Trucchetti" in cap_text:
            spell_lines = []
            for line in cap_text.split("\n"):
                line = line.strip("- ").strip()
                if line and not line.startswith("**Arcane") and not line.startswith("**Sigillo"):
                    spell_lines.append(re.sub(r"\*\*(.+?)\*\*", r"\1", line))
            if spell_lines:
                data["actions"].append({"name": "Spellcasting", "text": "\n".join(spell_lines)})
        # Altri tratti
        for line in cap_text.split("\n"):
            line = line.strip("- ").strip()
            m = re.match(r"\*\*(.+?)\*\*\s*(?:\([^)]*\)\s*)?:\s*(.+)", line)
            if m and "Incantesimi" not in m.group(1) and "Trucchetti" not in m.group(1):
                trait_name = m.group(1)
                # Includi il contenuto tra parentesi nel nome se presente
                paren = re.search(r"\*\*(.+?)\*\*\s*(\([^)]*\))", line)
                if paren:
                    trait_name = f"{paren.group(1)} {paren.group(2)}"
                data["traits"].append({"name": trait_name, "text": m.group(2)})

    # Descrizione
    desc_section = re.search(r"## Descrizione\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if desc_section:
        data["description"] = desc_section.group(1).strip()

    return data


def build_xml(data):
    """Costruisce l'XML FightClub da un dict di dati NPC."""
    compendium = Element("compendium", version="5", auto_indent="NO")
    monster = SubElement(compendium, "monster")

    SubElement(monster, "name").text = data.get("name", "Unknown")

    # Size
    race = data.get("race", "").lower()
    size = RACE_TO_SIZE.get(race, "M")
    SubElement(monster, "size").text = size

    # Type
    race_display = data.get("race", "humanoid")
    cls = data.get("class", "")
    type_text = f"humanoid ({race_display.lower()})"
    SubElement(monster, "type").text = type_text

    # Alignment
    align = data.get("alignment", "neutral").lower()
    SubElement(monster, "alignment").text = ALIGNMENT_MAP.get(align, align)

    # Stats
    ac = data.get("ac", "10")
    # Prendi solo il numero base
    ac_num = re.match(r"(\d+)", ac)
    SubElement(monster, "ac").text = ac.strip() if ac_num else "10"
    SubElement(monster, "hp").text = data.get("hp", "1")
    SubElement(monster, "speed").text = data.get("speed", "30 ft.")

    for stat in ["str", "dex", "con", "int", "wis", "cha"]:
        SubElement(monster, stat).text = data.get(stat, "10")

    # Skills
    skills = []
    for key, label in [("perception", "Perception"), ("performance", "Performance"),
                        ("stealth", "Stealth")]:
        if key in data:
            skills.append(f"{label} +{data[key].lstrip('+')}")
    if skills:
        SubElement(monster, "skill").text = ", ".join(skills)

    # Immunities
    if "immune" in data:
        immune_text = data["immune"].lower()
        SubElement(monster, "immune").text = immune_text
        if "veleno" in immune_text or "poison" in immune_text:
            SubElement(monster, "conditionImmune").text = "poisoned"

    # Senses
    if "senses" in data:
        senses = data["senses"]
        if "scurovisione" in senses.lower():
            senses = senses.replace("scurovisione", "darkvision 60 ft.")
        SubElement(monster, "senses").text = senses
    elif "senses" not in data:
        # Check for scurovisione in raw text
        pass

    # Languages
    if "languages" in data:
        langs = data["languages"]
        langs = langs.replace("Comune", "Common").replace("Elfico", "Elvish")
        SubElement(monster, "languages").text = langs

    # CR — usa valore dal markdown se presente, altrimenti stima dal livello
    if "cr" in data:
        cr = data["cr"]
    else:
        level = int(data.get("level", "1"))
        cr = str(max(1, level - 1))
    SubElement(monster, "cr").text = cr

    # Traits
    for trait in data.get("traits", []):
        t = SubElement(monster, "trait")
        SubElement(t, "name").text = trait["name"]
        SubElement(t, "text").text = trait["text"]

    # Actions
    for action in data.get("actions", []):
        a = SubElement(monster, "action")
        SubElement(a, "name").text = action["name"]
        SubElement(a, "text").text = action["text"]
        if "attack" in action:
            SubElement(a, "attack").text = action["attack"]

    # Description
    if "description" in data:
        SubElement(monster, "description").text = data["description"]

    xml_str = tostring(compendium, encoding="unicode")
    pretty = parseString(xml_str).toprettyxml(indent="    ", encoding=None)
    # Rimuovi la dichiarazione XML duplicata da minidom
    lines = pretty.split("\n")
    lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    return "\n".join(line for line in lines if line.strip())


def main():
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <file.md> [-o output.xml]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None
    if "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    if not output_file:
        output_file = os.path.splitext(input_file)[0] + ".xml"

    data = parse_md(input_file)
    xml = build_xml(data)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"✓ {input_file} → {output_file}")


if __name__ == "__main__":
    main()
