#!/usr/bin/env python3
"""
new-npc.py — Crea una scheda NPC per un'avventura
Uso: python3 tech/scripts/new-npc.py <NomeAvventura> [--template]

Modalità:
  default    Wizard interattivo — chiede nome, ruolo, tratti base
  --template Crea scheda vuota con placeholder da riempire a mano
"""

import sys
import os
import re

def ask(prompt, default=None, optional=False):
    suffix = f" [{default}]" if default else (" (opzionale, Invio per saltare)" if optional else "")
    val = input(f"{prompt}{suffix}: ").strip()
    if not val:
        return default or ""
    return val

def slug(name):
    """NomePersonaggio → NomePersonaggio (rimuove spazi, PascalCase)"""
    return "".join(w.capitalize() for w in re.split(r'[\s_-]+', name))

def template_mode(adventure_dir, npc_name):
    filename = f"NPC_{slug(npc_name)}.md"
    path = os.path.join(adventure_dir, "personaggi", filename)
    content = f"""# {npc_name}

## Informazioni generali

- **Ruolo**: ...
- **Classe**: ... *(se applicabile)*
- **Razza**: ...
- **Allineamento**: ...

## Descrizione

*(aspetto fisico, modo di parlare, tratto distintivo)*

## Motivazioni

> ⚠ *Da compilare.*

## Note al master

> ⚠ *Da compilare.*

## Stat Block

*(opzionale)*

## Agganci futuri

*(opzionale)*
"""
    return path, content

def wizard_mode(adventure_dir, npc_name):
    print(f"\nCompila i campi per {npc_name} (Invio per saltare i campi opzionali)\n")

    ruolo = ask("Ruolo nell'avventura (es: antagonista, alleato, commerciante)")
    razza = ask("Razza", default="umano")
    allineamento = ask("Allineamento", default="neutrale")
    classe = ask("Classe e livello (es: Mago 5)", optional=True)
    aspetto = ask("Tratto fisico distintivo", optional=True)
    parlata = ask("Modo di parlare o frase ricorrente", optional=True)
    motivazione = ask("Cosa vuole / perché agisce così")
    segreto = ask("Segreto o informazione nascosta", optional=True)
    note = ask("Note al master (comportamento, agganci)", optional=True)

    info_lines = [f"- **Ruolo**: {ruolo}", f"- **Razza**: {razza}", f"- **Allineamento**: {allineamento}"]
    if classe:
        info_lines.insert(1, f"- **Classe**: {classe}")

    desc_parts = []
    if aspetto:
        desc_parts.append(aspetto)
    if parlata:
        desc_parts.append(f'Frase ricorrente: *"{parlata}"*')
    descrizione = "\n\n".join(desc_parts) if desc_parts else "> ⚠ *Da compilare.*"

    motivazione_text = motivazione if motivazione else "> ⚠ *Da compilare.*"
    if segreto:
        motivazione_text += f"\n\n**Segreto**: {segreto}"

    note_text = note if note else "> ⚠ *Da compilare.*"

    filename = f"NPC_{slug(npc_name)}.md"
    path = os.path.join(adventure_dir, "personaggi", filename)
    content = f"""# {npc_name}

## Informazioni generali

{chr(10).join(info_lines)}

## Descrizione

{descrizione}

## Motivazioni

{motivazione_text}

## Note al master

{note_text}

## Stat Block

*(da aggiungere se necessario)*

## Agganci futuri

*(da aggiungere se necessario)*
"""
    return path, content

def main():
    template = "--template" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if len(args) < 1:
        print(f"Uso: {sys.argv[0]} <NomeAvventura> [--template]")
        sys.exit(1)

    adventure_name = args[0]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../.."))
    adventure_dir = os.path.join(project_root, "adventures", adventure_name)

    if not os.path.isdir(adventure_dir):
        print(f"Errore: '{adventure_dir}' non trovata.")
        sys.exit(1)

    os.makedirs(os.path.join(adventure_dir, "personaggi"), exist_ok=True)

    print(f"\n=== Nuovo NPC: {adventure_name} ===")
    npc_name = ask("Nome del personaggio")
    if not npc_name:
        print("Nome obbligatorio.")
        sys.exit(1)

    filename = f"NPC_{slug(npc_name)}.md"
    path = os.path.join(adventure_dir, "personaggi", filename)

    if os.path.isfile(path):
        print(f"Errore: '{filename}' esiste già in personaggi/.")
        sys.exit(1)

    if template:
        path, content = template_mode(adventure_dir, npc_name)
    else:
        path, content = wizard_mode(adventure_dir, npc_name)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✓ Creato: personaggi/{filename}")
    print(f"  Verifica: python3 tech/scripts/check-adventure.py {adventure_name}")

if __name__ == "__main__":
    main()
