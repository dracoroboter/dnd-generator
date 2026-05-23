#!/usr/bin/env python3
"""Calcola la dimensione del progetto suddivisa per categoria (solo file tracciati da git)."""

import subprocess
import os

def get_tracked_files():
    """File tracciati da git, escludendo quelli che il .gitignore attuale escluderebbe."""
    r = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
    all_files = [f for f in r.stdout.strip().split("\n") if f]
    # Simula gitignore: escludi file che sarebbero ignorati
    ignore_patterns = [
        lambda f: "/statblock/" in f and not f.startswith("public/"),
        lambda f: "/fightclub/" in f and not f.startswith("public/"),
        lambda f: "-lowres.jpg" in f or "-lowres.png" in f,
        lambda f: f.startswith("releases/"),
        lambda f: f.startswith("legacy/"),
        lambda f: f.startswith("backup/"),
        lambda f: f.startswith("tech/build/"),
        lambda f: f.startswith("tech/reports/"),
    ]
    return [f for f in all_files if not any(p(f) for p in ignore_patterns)]

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../..")
    files = get_tracked_files()

    img_exts = {".png", ".jpg", ".jpeg", ".svg"}
    categories = {"public": 0, "images": 0, "other": 0}
    counts = {"public": 0, "images": 0, "other": 0}

    total = 0
    for f in files:
        if not os.path.isfile(f):
            continue
        size = os.path.getsize(f)
        total += size
        if f.startswith("public/"):
            categories["public"] += size
            counts["public"] += 1
        elif os.path.splitext(f)[1].lower() in img_exts:
            categories["images"] += size
            counts["images"] += 1
        else:
            categories["other"] += size
            counts["other"] += 1

    def mb(b):
        return f"{b / (1024*1024):.1f} MB"

    print(f"{'Categoria':<20} {'File':>6} {'Dimensione':>12} {'%':>6}")
    print("-" * 48)
    for cat in ["public", "images", "other"]:
        pct = categories[cat] / total * 100 if total else 0
        print(f"{cat:<20} {counts[cat]:>6} {mb(categories[cat]):>12} {pct:>5.1f}%")
    print("-" * 48)
    print(f"{'TOTALE':<20} {sum(counts.values()):>6} {mb(total):>12}")

if __name__ == "__main__":
    main()
