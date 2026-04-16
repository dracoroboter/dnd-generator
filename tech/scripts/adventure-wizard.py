#!/usr/bin/env python3
"""
adventure-wizard.py — Wizard interattivo per i metadati di un'avventura
Uso: python3 tech/scripts/adventure-wizard.py <NomeAvventura>

Legge README.md e AdventureBook.md esistenti, chiede solo i campi mancanti.
Rilanciabile: non sovrascrive campi già compilati.
"""

import sys
import os
import re

def ask(prompt, options=None, default=None):
    """Chiede input all'utente con opzioni e default."""
    if options:
        opts = "/".join(f"[{o}]" if o == default else o for o in options)
        prompt = f"{prompt} ({opts}): "
    elif default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    while True:
        val = input(prompt).strip()
        if not val and default:
            return default
        if options and val not in options:
            print(f"  Scegli tra: {', '.join(options)}")
            continue
        if val:
            return val

def field_present(content, field):
    """Controlla se un campo markdown bold è già presente e compilato."""
    pattern = rf'\*\*{re.escape(field)}\*\*:\s*(.+)'
    m = re.search(pattern, content)
    if not m:
        return False
    val = m.group(1).strip()
    # Considera non compilato se è un placeholder
    return val and val not in ("...", "—", "X", "N", "M")

def set_field(content, field, value):
    """Aggiorna o aggiunge un campo **Field**: value nel README."""
    pattern = rf'(\*\*{re.escape(field)}\*\*:).*'
    if re.search(pattern, content):
        return re.sub(pattern, rf'\1 {value}', content)
    # Aggiunge dopo la prima riga (titolo)
    lines = content.split("\n")
    lines.insert(2, f"**{field}**: {value}")
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <NomeAvventura>")
        sys.exit(1)

    adventure_name = sys.argv[1]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../.."))
    adventure_dir = os.path.join(project_root, "adventures", adventure_name)

    if not os.path.isdir(adventure_dir):
        print(f"Errore: '{adventure_dir}' non trovata. Esegui prima new-adventure.sh.")
        sys.exit(1)

    readme_path = os.path.join(adventure_dir, "README.md")
    ab_path = os.path.join(adventure_dir, "AdventureBook.md")

    readme = open(readme_path, encoding="utf-8").read() if os.path.isfile(readme_path) else ""
    ab = open(ab_path, encoding="utf-8").read() if os.path.isfile(ab_path) else ""

    print(f"\n=== Wizard: {adventure_name} ===")
    print("Premi Invio per saltare un campo già compilato o lasciarlo vuoto.\n")

    changed = False

    # --- Sistema ---
    if not field_present(readme, "Sistema"):
        val = ask("Sistema di gioco", default="D&D 5e (2014)")
        readme = set_field(readme, "Sistema", val)
        changed = True

    # --- Livello consigliato ---
    if not field_present(readme, "Livello consigliato"):
        val = ask("Livello PG consigliato (es: 1, 3-5)")
        if val:
            readme = set_field(readme, "Livello consigliato", val)
            changed = True

    # --- Durata ---
    if not field_present(readme, "Durata"):
        val = ask("Durata", options=["one-shot", "campagna", "saga"], default="one-shot")
        if val == "campagna":
            n = ask("Numero di sessioni previste (es: 3-5)")
            val = f"campagna ({n} sessioni)"
        elif val == "saga":
            val = "saga multi-campagna"
        readme = set_field(readme, "Durata", val)
        changed = True

    # --- Struttura ---
    if not field_present(readme, "Struttura"):
        val = ask("Struttura", options=["lineare", "sandbox", "mista"], default="lineare")
        readme = set_field(readme, "Struttura", val)
        changed = True

    # --- Tono ---
    if not field_present(readme, "Tono"):
        print("Tono (puoi sceglierne più di uno, separati da virgola)")
        print("  Opzioni: umoristico, horror, investigativo, combattimento, drammatico, avventura")
        val = ask("Tono", default="avventura")
        readme = set_field(readme, "Tono", val)
        changed = True

    # --- Saga ---
    if not field_present(readme, "Saga"):
        is_saga = ask("Fa parte di una saga?", options=["s", "n"], default="n")
        if is_saga == "s":
            saga_name = ask("Nome della saga")
            pos = ask("Posizione (es: Puntata 2 di 5)")
            segue = ask("Segue (nome avventura precedente, o — se prima)", default="—")
            precede = ask("Precede (nome avventura successiva, o — se ultima)", default="—")
            readme = set_field(readme, "Saga", saga_name)
            readme = set_field(readme, "Posizione", pos)
            readme = set_field(readme, "Segue", segue)
            readme = set_field(readme, "Precede", precede)
            changed = True

    # --- Descrizione breve ---
    # Controlla se c'è già testo descrittivo dopo i metadati
    desc_match = re.search(r'\n\n([^#\*\n].{20,})', readme)
    if not desc_match:
        print("\nDescrizione breve (senza spoiler, per il README pubblico):")
        val = input("> ").strip()
        if val:
            readme = readme.rstrip() + f"\n\n{val}\n"
            changed = True

    # --- Salva ---
    if changed:
        open(readme_path, "w", encoding="utf-8").write(readme)
        print(f"\n✓ README.md aggiornato.")
    else:
        print("\n✓ Nessuna modifica necessaria — tutti i campi già compilati.")

    print(f"\nProssimi passi:")
    print(f"  - Rinomina i moduli in adventures/{adventure_name}/")
    print(f"  - Aggiungi NPC: python3 tech/scripts/new-npc.py {adventure_name}")
    print(f"  - Verifica: python3 tech/scripts/check-adventure.py {adventure_name}")

if __name__ == "__main__":
    main()
