#!/usr/bin/env python3
"""
measure-prose.py — Misura prolissità e chiarezza dei file di un'avventura.

Metriche:
  - Righe totali, righe vuote, righe di contenuto
  - Parole totali
  - Boxed text: numero blocchi, righe totali, media righe per blocco, blocchi >5 righe
  - Tabelle: numero, righe totali
  - Bullet point: numero righe
  - Prosa pura: righe che non sono heading, tabella, bullet, boxed text, vuote
  - Rapporto prosa/dati (prosa pura / (tabelle + bullet + heading))
  - Densità informativa stimata: (tabelle + bullet + heading) / righe contenuto
  - Heading: numero per livello (##, ###)

Uso:
  python3 measure-prose.py <NomeAvventura>
  python3 measure-prose.py <NomeAvventura> --file it/LAnelloDelConte.md
  python3 measure-prose.py <NomeAvventura> --verbose
"""

import os
import sys
import re
import argparse
from pathlib import Path

# Resolve project root
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # tech/scripts/ -> project root


def classify_line(line):
    """Classify a line into a category."""
    stripped = line.strip()

    if not stripped:
        return "blank"
    if stripped in ("---", "***", "___"):
        return "hr"
    if stripped.startswith("#"):
        return "heading"
    if stripped.startswith("|") or stripped.startswith("|-"):
        return "table"
    if stripped.startswith(">"):
        return "boxed_text"
    if stripped.startswith("- ") or stripped.startswith("* ") or re.match(r'^\d+\.\s', stripped):
        return "bullet"
    if stripped.startswith("```"):
        return "code_fence"
    if stripped.startswith("**") and stripped.endswith("**"):
        return "bold_line"  # counted as structured data
    return "prose"


def count_words(line):
    """Count words in a line, ignoring markdown formatting."""
    # Remove markdown syntax
    clean = re.sub(r'[#*>|`\-]', ' ', line)
    return len(clean.split())


def has_direct_dialogue(line):
    """Check if a line contains direct dialogue (quoted speech outside boxed text)."""
    stripped = line.strip()
    if stripped.startswith(">"):
        return False  # boxed text handled separately
    # Match *"..."* or "..." patterns
    return bool(re.search(r'\*"[^"]+"\*', stripped) or
                re.search(r'\*\'[^\']+\'\*', stripped) or
                re.search(r'"[^"]{10,}"', stripped))


def measure_file(filepath):
    """Measure metrics for a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    metrics = {
        "file": str(filepath),
        "total_lines": len(lines),
        "blank_lines": 0,
        "content_lines": 0,
        "total_words": 0,
        "heading_lines": 0,
        "heading_h2": 0,
        "heading_h3": 0,
        "table_lines": 0,
        "table_count": 0,
        "bullet_lines": 0,
        "boxed_text_lines": 0,
        "boxed_text_blocks": 0,
        "boxed_text_blocks_over5": 0,
        "prose_lines": 0,
        "code_lines": 0,
        "bold_lines": 0,
        "dialogue_lines": 0,
        "dialogue_in_boxed": 0,
        "hr_lines": 0,
    }

    in_code_block = False
    in_boxed_block = False
    in_table = False
    current_boxed_len = 0

    for line in lines:
        stripped = line.strip()
        metrics["total_words"] += count_words(line)

        # Handle code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            metrics["code_lines"] += 1
            continue
        if in_code_block:
            metrics["code_lines"] += 1
            continue

        category = classify_line(line)

        # Detect direct dialogue
        if has_direct_dialogue(line):
            metrics["dialogue_lines"] += 1
        # Detect dialogue inside boxed text
        if category == "boxed_text" and re.search(r'\*"[^"]+"\*', stripped):
            metrics["dialogue_in_boxed"] += 1

        if category == "blank":
            metrics["blank_lines"] += 1
            # End boxed text block
            if in_boxed_block:
                in_boxed_block = False
                if current_boxed_len > 5:
                    metrics["boxed_text_blocks_over5"] += 1
                current_boxed_len = 0
            # End table
            if in_table:
                in_table = False
        elif category == "hr":
            metrics["hr_lines"] += 1
            # Don't count as content
        elif category == "heading":
            metrics["heading_lines"] += 1
            metrics["content_lines"] += 1
            if stripped.startswith("## ") and not stripped.startswith("### "):
                metrics["heading_h2"] += 1
            elif stripped.startswith("### "):
                metrics["heading_h3"] += 1
        elif category == "table":
            metrics["table_lines"] += 1
            metrics["content_lines"] += 1
            if not in_table:
                in_table = True
                metrics["table_count"] += 1
        elif category == "boxed_text":
            metrics["boxed_text_lines"] += 1
            metrics["content_lines"] += 1
            if not in_boxed_block:
                in_boxed_block = True
                metrics["boxed_text_blocks"] += 1
                current_boxed_len = 0
            current_boxed_len += 1
        elif category == "bullet":
            metrics["bullet_lines"] += 1
            metrics["content_lines"] += 1
        elif category == "bold_line":
            metrics["bold_lines"] += 1
            metrics["content_lines"] += 1
        elif category == "prose":
            metrics["prose_lines"] += 1
            metrics["content_lines"] += 1

    # Close open boxed block at end of file
    if in_boxed_block and current_boxed_len > 5:
        metrics["boxed_text_blocks_over5"] += 1

    # Derived metrics
    structured = metrics["table_lines"] + metrics["bullet_lines"] + metrics["heading_lines"] + metrics["bold_lines"]
    metrics["structured_lines"] = structured
    metrics["prose_ratio"] = (
        round(metrics["prose_lines"] / structured, 2) if structured > 0 else float('inf')
    )
    metrics["density"] = (
        round(structured / metrics["content_lines"], 2) if metrics["content_lines"] > 0 else 0
    )
    metrics["boxed_text_avg"] = (
        round(metrics["boxed_text_lines"] / metrics["boxed_text_blocks"], 1)
        if metrics["boxed_text_blocks"] > 0 else 0
    )
    # Dialogue density: dialogue lines (outside boxed) as % of content
    metrics["dialogue_density"] = (
        round(metrics["dialogue_lines"] / metrics["content_lines"] * 100, 1)
        if metrics["content_lines"] > 0 else 0
    )
    # Total dialogue (inside + outside boxed text)
    metrics["dialogue_total"] = metrics["dialogue_lines"] + metrics["dialogue_in_boxed"]
    metrics["dialogue_total_pct"] = (
        round(metrics["dialogue_total"] / metrics["content_lines"] * 100, 1)
        if metrics["content_lines"] > 0 else 0
    )
    # Heading fragmentation: avg content lines per heading
    total_headings = metrics["heading_h2"] + metrics["heading_h3"]
    metrics["lines_per_heading"] = (
        round(metrics["content_lines"] / total_headings, 1)
        if total_headings > 0 else float('inf')
    )

    return metrics


def print_metrics(metrics, verbose=False):
    """Print metrics for a file."""
    name = os.path.basename(metrics["file"])
    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")
    print(f"  Righe totali:          {metrics['total_lines']}")
    print(f"  Righe contenuto:       {metrics['content_lines']}")
    print(f"  Parole:                {metrics['total_words']}")
    print()
    print(f"  Prosa pura:            {metrics['prose_lines']} righe")
    print(f"  Dati strutturati:      {metrics['structured_lines']} righe "
          f"(tab:{metrics['table_lines']} bul:{metrics['bullet_lines']} "
          f"head:{metrics['heading_lines']} bold:{metrics['bold_lines']})")
    print(f"  Boxed text:            {metrics['boxed_text_lines']} righe "
          f"in {metrics['boxed_text_blocks']} blocchi "
          f"(media {metrics['boxed_text_avg']} righe/blocco)")
    print(f"  Blocchi boxed >5 righe:{metrics['boxed_text_blocks_over5']}")
    print()
    print(f"  Dialogo diretto:       {metrics['dialogue_lines']} righe fuori boxed "
          f"+ {metrics['dialogue_in_boxed']} in boxed = "
          f"{metrics['dialogue_total']} tot ({metrics['dialogue_total_pct']}%)")
    print(f"  Heading (h2+h3):       {metrics['heading_h2']}+{metrics['heading_h3']} "
          f"= {metrics['heading_h2']+metrics['heading_h3']} "
          f"({metrics['lines_per_heading']} righe/heading)")
    if metrics['hr_lines'] > 0:
        print(f"  HR (---):              {metrics['hr_lines']} (inutili, da rimuovere)")
    print()
    print(f"  RAPPORTO PROSA/DATI:   {metrics['prose_ratio']}")
    print(f"  DENSITÀ INFORMATIVA:   {metrics['density']}")
    print()

    # Suggerimenti azionabili (cosa migliorare al prossimo giro)
    suggerimenti = build_suggestions(metrics)
    if suggerimenti:
        print("  SUGGERIMENTI (cosa migliorare):")
        for s in suggerimenti:
            print(f"    - {s}")


def build_suggestions(metrics):
    """Traduce le metriche fuori target in suggerimenti concreti e azionabili.
    Ritorna una lista di stringhe (vuota se tutto in target)."""
    s = []
    name = os.path.basename(metrics["file"])
    if metrics['prose_ratio'] > 2.0:
        s.append(
            f"Rapporto prosa/dati {metrics['prose_ratio']} (target < 2.0): "
            f"accorcia la prosa discorsiva o convertila in tabelle/bullet "
            f"(tattiche NPC, esiti, ricompense in elenco)."
        )
    if metrics['boxed_text_blocks_over5'] > 0:
        s.append(
            f"{metrics['boxed_text_blocks_over5']} boxed text oltre 5 righe: "
            f"accorciali tenendo solo le percezioni sensoriali; sposta i dettagli "
            f"logici nelle Note per il DM. Usa find-long-boxed.py per le righe esatte."
        )
    if metrics['density'] < 0.35:
        s.append(
            f"Densità informativa {metrics['density']} (target > 0.35): "
            f"poca sostanza per riga. Aggiungi dati strutturati (CD, tabelle, "
            f"esiti) o taglia la prosa di riempimento."
        )
    if metrics['dialogue_total_pct'] > 20:
        s.append(
            f"Dialogo diretto {metrics['dialogue_total_pct']}% (target < 20%): "
            f"il modulo tende al copione. Converti le battute non essenziali in "
            f"bullet di intenzione ('Gorim spiega che...')."
        )
    if metrics['lines_per_heading'] < 5:
        s.append(
            f"Frammentazione heading ({metrics['lines_per_heading']} righe/heading, "
            f"target > 5): accorpa sezioni troppo corte sotto un titolo comune."
        )
    if metrics['hr_lines'] > 0:
        s.append(
            f"{metrics['hr_lines']} separatori HR (---): rimuovili, la struttura "
            f"la danno i titoli."
        )
    return s


def print_summary(all_metrics):
    """Print aggregate summary."""
    total_lines = sum(m["content_lines"] for m in all_metrics)
    total_prose = sum(m["prose_lines"] for m in all_metrics)
    total_structured = sum(m["structured_lines"] for m in all_metrics)
    total_boxed = sum(m["boxed_text_lines"] for m in all_metrics)
    total_boxed_over5 = sum(m["boxed_text_blocks_over5"] for m in all_metrics)
    total_words = sum(m["total_words"] for m in all_metrics)
    total_dialogue = sum(m["dialogue_total"] for m in all_metrics)
    total_headings = sum(m["heading_h2"] + m["heading_h3"] for m in all_metrics)

    print(f"\n{'#' * 60}")
    print(f"  RIEPILOGO AVVENTURA")
    print(f"{'#' * 60}")
    print(f"  File analizzati:       {len(all_metrics)}")
    print(f"  Righe contenuto tot:   {total_lines}")
    print(f"  Parole totali:         {total_words}")
    print(f"  Prosa pura totale:     {total_prose} ({round(total_prose/total_lines*100)}%)")
    print(f"  Strutturato totale:    {total_structured} ({round(total_structured/total_lines*100)}%)")
    print(f"  Boxed text totale:     {total_boxed} ({round(total_boxed/total_lines*100)}%)")
    print(f"  Blocchi boxed >5 righe:{total_boxed_over5}")
    print(f"  Dialogo diretto tot:   {total_dialogue} ({round(total_dialogue/total_lines*100)}%)")
    print(f"  Heading tot (h2+h3):   {total_headings} "
          f"({round(total_lines/total_headings, 1) if total_headings > 0 else 'inf'} righe/heading)")
    print()
    overall_ratio = round(total_prose / total_structured, 2) if total_structured > 0 else float('inf')
    overall_density = round(total_structured / total_lines, 2) if total_lines > 0 else 0
    print(f"  RAPPORTO PROSA/DATI GLOBALE:   {overall_ratio}")
    print(f"  DENSITÀ INFORMATIVA GLOBALE:   {overall_density}")
    print()

    # Targets
    print(f"  Target consigliati:")
    print(f"    Rapporto prosa/dati:  < 2.0 (ideale < 1.5)")
    print(f"    Densità informativa:  > 0.35 (ideale > 0.45)")
    print(f"    Blocchi boxed >5:     0 (eccezioni documentate)")
    print(f"    Dialogo diretto:      < 20% (ideale < 15%)")
    print(f"    Righe per heading:    > 5 (ideale > 7)")

    # Suggerimenti aggregati: cosa migliorare al prossimo giro, per file
    per_file = [(os.path.basename(m["file"]), build_suggestions(m)) for m in all_metrics]
    con_problemi = [(n, sg) for n, sg in per_file if sg]
    print()
    print(f"{'#' * 60}")
    if con_problemi:
        print(f"  DA MIGLIORARE AL PROSSIMO GIRO ({len(con_problemi)} file)")
        print(f"{'#' * 60}")
        for nome, sugg in con_problemi:
            print(f"\n  {nome}:")
            for s in sugg:
                print(f"    - {s}")
    else:
        print(f"  NESSUN SUGGERIMENTO: tutti i file sono nei target di stile.")
        print(f"{'#' * 60}")


def main():
    parser = argparse.ArgumentParser(description="Misura prolissità/chiarezza dei file avventura")
    parser.add_argument("adventure", help="Nome dell'avventura")
    parser.add_argument("--file", help="Analizza un singolo file (path relativo alla root avventura)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mostra dettagli per ogni file")
    parser.add_argument("--modules-only", action="store_true", help="Analizza solo i moduli (NN_*)")
    args = parser.parse_args()

    adventure_dir = PROJECT_ROOT / "adventures" / args.adventure
    if not adventure_dir.exists():
        print(f"Errore: directory {adventure_dir} non trovata")
        sys.exit(1)

    it_dir = adventure_dir / "it"
    if not it_dir.exists():
        print(f"Errore: directory {it_dir} non trovata")
        sys.exit(1)

    if args.file:
        filepath = adventure_dir / args.file
        if not filepath.exists():
            print(f"Errore: file {filepath} non trovato")
            sys.exit(1)
        metrics = measure_file(filepath)
        print_metrics(metrics, args.verbose)
        return

    # Collect all .md files
    files_to_analyze = []

    if args.modules_only:
        # Only NN_* directories
        for d in sorted(it_dir.iterdir()):
            if d.is_dir() and re.match(r'^\d{2}_', d.name):
                for f in sorted(d.glob("*.md")):
                    if f.name != "DM_Prep.md" and f.name != "nemici-sessione.md":
                        files_to_analyze.append(f)
    else:
        # Main document
        main_doc = it_dir / f"{args.adventure}.md"
        if main_doc.exists():
            files_to_analyze.append(main_doc)

        # All modules
        for d in sorted(it_dir.iterdir()):
            if d.is_dir() and re.match(r'^\d{2}_', d.name):
                for f in sorted(d.glob("*.md")):
                    if f.name != "DM_Prep.md" and f.name != "nemici-sessione.md":
                        files_to_analyze.append(f)

    if not files_to_analyze:
        print("Nessun file trovato da analizzare")
        sys.exit(1)

    all_metrics = []
    for filepath in files_to_analyze:
        metrics = measure_file(filepath)
        all_metrics.append(metrics)
        print_metrics(metrics, args.verbose)

    if len(all_metrics) > 1:
        print_summary(all_metrics)


if __name__ == "__main__":
    main()
