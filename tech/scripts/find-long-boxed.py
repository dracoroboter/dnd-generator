#!/usr/bin/env python3
"""
find-long-boxed.py — Trova tutti i blocchi boxed text (>) piu lunghi di N righe.

Mostra: file, riga di inizio, numero righe, anteprima del contenuto.

Uso:
  python3 find-long-boxed.py <NomeAvventura>
  python3 find-long-boxed.py <NomeAvventura> --max 3      # soglia a 3 righe
  python3 find-long-boxed.py <NomeAvventura> --full       # mostra tutto il blocco
"""

import os
import sys
import re
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent


def find_long_boxed(filepath, max_lines=5, show_full=False):
    """Find boxed text blocks exceeding max_lines in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results = []
    in_block = False
    block_start = 0
    block_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('>'):
            if not in_block:
                in_block = True
                block_start = i + 1  # 1-indexed
                block_lines = []
            block_lines.append(stripped[1:].strip())
        else:
            if in_block and len(block_lines) > max_lines:
                results.append({
                    "start": block_start,
                    "length": len(block_lines),
                    "preview": block_lines[:2],
                    "full": block_lines,
                })
            in_block = False
            block_lines = []

    # Handle block at end of file
    if in_block and len(block_lines) > max_lines:
        results.append({
            "start": block_start,
            "length": len(block_lines),
            "preview": block_lines[:2],
            "full": block_lines,
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Trova blocchi boxed text troppo lunghi")
    parser.add_argument("adventure", help="Nome dell'avventura")
    parser.add_argument("--max", type=int, default=5, help="Soglia massima righe (default: 5)")
    parser.add_argument("--full", action="store_true", help="Mostra il contenuto completo dei blocchi")
    args = parser.parse_args()

    adventure_dir = PROJECT_ROOT / "adventures" / args.adventure
    it_dir = adventure_dir / "it"

    if not it_dir.exists():
        print(f"Errore: {it_dir} non trovata")
        sys.exit(1)

    # Collect files: main doc + modules
    files_to_check = []

    main_doc = it_dir / f"{args.adventure}.md"
    if main_doc.exists():
        files_to_check.append(main_doc)

    for d in sorted(it_dir.iterdir()):
        if d.is_dir() and re.match(r'^\d{2}_', d.name):
            for f in sorted(d.glob("*.md")):
                if f.name not in ("DM_Prep.md", "nemici-sessione.md"):
                    files_to_check.append(f)

    total_found = 0

    for filepath in files_to_check:
        results = find_long_boxed(filepath, args.max, args.full)
        if not results:
            continue

        rel_path = filepath.relative_to(it_dir)
        print(f"\n{'=' * 60}")
        print(f"  {rel_path}  ({len(results)} blocchi > {args.max} righe)")
        print(f"{'=' * 60}")

        for r in results:
            total_found += 1
            print(f"\n  [{total_found}] Riga {r['start']}, {r['length']} righe:")
            if args.full:
                for line in r['full']:
                    print(f"      > {line}")
            else:
                for line in r['preview']:
                    truncated = line[:70] + "..." if len(line) > 70 else line
                    print(f"      > {truncated}")
                if r['length'] > 2:
                    print(f"      ... ({r['length'] - 2} righe omesse)")

    print(f"\n{'#' * 60}")
    print(f"  TOTALE: {total_found} blocchi boxed text > {args.max} righe")
    print(f"{'#' * 60}")


if __name__ == "__main__":
    main()
