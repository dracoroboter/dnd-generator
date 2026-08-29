#!/usr/bin/env python3
"""
validate-syntax.py — Valida la sintassi di uno o più file YAML/JSON.

Nasce per eliminare un problema ricorrente: validare YAML/JSON con
`python3 -c "..."` inline dentro `wsl bash -c "..."` rompe l'escape delle
virgolette (PowerShell -> wsl -> bash). La soluzione affidabile è NON usare
codice inline: si esegue questo script già su disco, passando i file come
argomenti. Nessuna virgoletta annidata, nessun escape.

Uso:
  python3 tech/scripts/validate-syntax.py file1.yaml file2.json ...
  python3 tech/scripts/validate-syntax.py --agents      # valida i due agenti .json
  python3 tech/scripts/validate-syntax.py --narrative   # valida i due YAML narrativi

Exit code 0 se tutti validi, 1 se almeno uno è rotto.
"""
import sys
import os
import json

try:
    import yaml
except ImportError:
    yaml = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

PRESETS = {
    "--agents": [
        ".kiro/agents/narratore.json",
        ".kiro/agents/meta-narratore.json",
    ],
    "--narrative": [
        "tech/data/references/narrative-stereotypes.yaml",
        "tech/data/references/narrative-grammar.yaml",
    ],
}


def validate_one(path):
    """Ritorna (ok: bool, messaggio: str)."""
    if not os.path.exists(path):
        return False, f"file non trovato: {path}"
    ext = os.path.splitext(path)[1].lower()
    try:
        with open(path, encoding="utf-8") as f:
            if ext in (".yaml", ".yml"):
                if yaml is None:
                    return False, "pyyaml non installato (pip install pyyaml)"
                yaml.safe_load(f)
            elif ext == ".json":
                json.load(f)
            else:
                # prova YAML (superset di JSON) se disponibile, altrimenti JSON
                data = f.read()
                if yaml is not None:
                    yaml.safe_load(data)
                else:
                    json.loads(data)
        return True, "valido"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def main(argv):
    if not argv:
        print(__doc__)
        return 1

    files = []
    for arg in argv:
        if arg in PRESETS:
            files.extend(PRESETS[arg])
        else:
            files.append(arg)

    all_ok = True
    for rel in files:
        path = rel if os.path.isabs(rel) else os.path.join(PROJECT_ROOT, rel)
        # se lanciato dalla root del progetto, rel funziona anche così
        if not os.path.exists(path) and os.path.exists(rel):
            path = rel
        ok, msg = validate_one(path)
        mark = "OK  " if ok else "FAIL"
        print(f"[{mark}] {rel}: {msg}")
        all_ok = all_ok and ok

    print("-" * 50)
    print("Tutti validi." if all_ok else "Almeno un file ha errori di sintassi.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
