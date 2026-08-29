#!/usr/bin/env python3
"""Regenerate narrative-stereotypes-index.md from the YAML database."""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "references"
YAML_FILE = DATA_DIR / "narrative-stereotypes.yaml"
INDEX_FILE = DATA_DIR / "narrative-stereotypes-index.md"

TIPO_ORDER = ["plot", "situazione", "personaggio", "relazione", "tecnica"]
TIPO_LABELS = {
    "plot": "PLOT",
    "situazione": "SITUAZIONI",
    "personaggio": "PERSONAGGI",
    "relazione": "RELAZIONI",
    "tecnica": "TECNICHE",
}


def parse_entries(yaml_path: Path) -> dict[str, list[str]]:
    """Parse YAML and extract nome + sottocaso_di per ogni tipo."""
    entries: dict[str, list[tuple[str, bool]]] = {t: [] for t in TIPO_ORDER}
    current_tipo = None
    current_nome = None
    is_sottocaso = False

    for line in yaml_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- tipo:"):
            current_tipo = stripped.split(":", 1)[1].strip()
            current_nome = None
            is_sottocaso = False
        elif stripped.startswith("nome:") and not stripped.startswith("nome_en:") and not stripped.startswith("nomi_alt:"):
            current_nome = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("sottocaso_di:"):
            is_sottocaso = True
        elif stripped.startswith("- tipo:") or (stripped.startswith("descrizione:") and current_tipo and current_nome):
            # Entry complete enough
            pass

        # When we hit the next entry or end, save previous
        if stripped.startswith("- tipo:") and current_nome and current_tipo:
            # Actually we need to save on transition. Let's restructure.
            pass

    # Simpler approach: two-pass
    entries = {t: [] for t in TIPO_ORDER}
    lines = yaml_path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("- tipo:"):
            tipo = line.split(":", 1)[1].strip()
            nome = None
            sottocaso = False
            # Scan forward for nome and sottocaso_di
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("- tipo:"):
                l = lines[j].strip()
                if l.startswith("nome:") and not l.startswith("nome_en:") and not l.startswith("nomi_alt:"):
                    nome = l.split(":", 1)[1].strip()
                elif l.startswith("sottocaso_di:"):
                    sottocaso = True
                j += 1
            if tipo in entries and nome:
                entries[tipo].append((nome, sottocaso))
            i = j
        else:
            i += 1

    return entries


def generate_index(entries: dict[str, list[tuple[str, bool]]]) -> str:
    """Generate the index markdown content."""
    total = sum(len(v) for v in entries.values())
    lines = [f"# Indice Stereotipi Narrativi ({total} voci)", ""]
    lines.append("Indice del database `narrative-stereotypes.yaml`.")
    lines.append("`*` = sottocaso di un altro stereotipo (vedi campo `sottocaso_di`).")
    lines.append("")
    lines.append("---")

    for tipo in TIPO_ORDER:
        items = entries[tipo]
        lines.append("")
        lines.append(f"## {TIPO_LABELS[tipo]} ({len(items)})")
        lines.append("")
        names = []
        for nome, is_sottocaso in items:
            display = f"{nome}*" if is_sottocaso else nome
            names.append(display)
        # Format as pipe-separated, ~3-4 per line
        chunk_size = 3
        for k in range(0, len(names), chunk_size):
            chunk = names[k:k + chunk_size]
            suffix = " |" if k + chunk_size < len(names) else ""
            lines.append(" | ".join(chunk) + suffix)

    lines.append("")
    return "\n".join(lines)


def main():
    if not YAML_FILE.exists():
        print(f"ERROR: {YAML_FILE} not found", file=sys.stderr)
        sys.exit(1)

    entries = parse_entries(YAML_FILE)
    content = generate_index(entries)
    INDEX_FILE.write_text(content, encoding="utf-8")

    total = sum(len(v) for v in entries.values())
    print(f"Index generated: {INDEX_FILE.name} ({total} voci)")
    for tipo in TIPO_ORDER:
        print(f"  {TIPO_LABELS[tipo]}: {len(entries[tipo])}")

    # Also update the count in the YAML header
    yaml_content = YAML_FILE.read_text(encoding="utf-8")
    import re
    yaml_content = re.sub(
        r"# INDICE: vedi narrative-stereotypes-index\.md \(\d+ voci\)",
        f"# INDICE: vedi narrative-stereotypes-index.md ({total} voci)",
        yaml_content,
    )
    YAML_FILE.write_text(yaml_content, encoding="utf-8")
    print(f"  YAML header updated to {total} voci")


if __name__ == "__main__":
    main()
