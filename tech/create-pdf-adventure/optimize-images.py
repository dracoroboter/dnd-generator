#!/usr/bin/env python3
"""
optimize-images.py — Genera versioni -lowres delle immagini di un'avventura.

Uso:
    python3 tech/create-pdf-adventure/optimize-images.py <NomeAvventura> [--threshold MB] [--max-width PX] [--png]

Per ogni immagine sopra la soglia (default 1 MB), genera una versione -lowres
ridimensionata e compressa. Default: output JPG. Con --png: output PNG (pngquant).
Non modifica gli originali.

Richiede: ImageMagick (convert, identify). Con --png richiede anche pngquant.
"""

import argparse, subprocess, sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

THRESHOLD_MB = 1.0
MAX_WIDTH = 1500
JPG_QUALITY = 85
PNGQUANT_QUALITY = "80-95"
LOWRES_SUFFIX = "-lowres"

SKIP_DIRS = {"other"}
SKIP_PATTERNS = {LOWRES_SUFFIX}


def find_images(adventure_dir):
    """Find all PNG/JPG images in the adventure, excluding other/ and -lowres files."""
    images = []
    for f in sorted(adventure_dir.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue
        if any(skip in f.stem for skip in SKIP_PATTERNS):
            continue
        if any(d.name in SKIP_DIRS for d in f.relative_to(adventure_dir).parents):
            continue
        images.append(f)
    return images


def get_dimensions(img_path):
    """Get image width x height via identify."""
    r = subprocess.run(["identify", "-format", "%wx%h", str(img_path)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None, None
    w, h = r.stdout.strip().split("x")
    return int(w), int(h)


def optimize_jpg(img_path, max_width, quality):
    """Create a -lowres.jpg version."""
    lowres = img_path.with_stem(img_path.stem + LOWRES_SUFFIX).with_suffix(".jpg")
    w, _ = get_dimensions(img_path)
    if w is None:
        return None

    cmd = ["convert", str(img_path), "-strip"]
    if w > max_width:
        cmd += ["-resize", f"{max_width}x"]
    cmd += ["-quality", str(quality), str(lowres)]
    subprocess.run(cmd, check=True)
    return lowres


def optimize_png(img_path, max_width, quality):
    """Create a -lowres.png version via pngquant."""
    lowres = img_path.with_stem(img_path.stem + LOWRES_SUFFIX)
    w, _ = get_dimensions(img_path)
    if w is None:
        return None

    if w > max_width:
        tmp = img_path.with_stem(img_path.stem + "-tmp")
        subprocess.run(["convert", str(img_path), "-resize", f"{max_width}x", "-strip",
                        str(tmp)], check=True)
        subprocess.run(["pngquant", f"--quality={quality}", "--force",
                        "--output", str(lowres), str(tmp)], check=True)
        tmp.unlink()
    else:
        subprocess.run(["pngquant", f"--quality={quality}", "--force",
                        "--output", str(lowres), str(img_path)], check=True)
    return lowres


def main():
    parser = argparse.ArgumentParser(description="Genera versioni -lowres delle immagini di un'avventura")
    parser.add_argument("adventure", help="Nome dell'avventura")
    parser.add_argument("--threshold", type=float, default=THRESHOLD_MB,
                        help=f"Soglia in MB (default {THRESHOLD_MB})")
    parser.add_argument("--max-width", type=int, default=MAX_WIDTH,
                        help=f"Larghezza massima in px (default {MAX_WIDTH})")
    parser.add_argument("--png", action="store_true",
                        help="Output PNG (pngquant) invece di JPG")
    args = parser.parse_args()

    adventure_dir = PROJECT_ROOT / "adventures" / args.adventure
    if not adventure_dir.exists():
        print(f"Errore: {adventure_dir} non trovata.")
        sys.exit(1)

    # Check dependencies
    deps = ["convert", "identify"]
    if args.png:
        deps.append("pngquant")
    for cmd in deps:
        r = subprocess.run(["which", cmd], capture_output=True)
        if r.returncode != 0:
            print(f"Errore: {cmd} non trovato.")
            sys.exit(1)

    fmt = "PNG" if args.png else "JPG"
    ext = ".png" if args.png else ".jpg"
    print(f"=== optimize-images: {args.adventure} (soglia {args.threshold} MB, max {args.max_width}px, {fmt}) ===\n")

    images = find_images(adventure_dir)
    threshold_bytes = args.threshold * 1024 * 1024

    optimized = 0
    skipped = 0
    for img in images:
        size_mb = img.stat().st_size / (1024 * 1024)
        rel = img.relative_to(adventure_dir)
        lowres = img.with_stem(img.stem + LOWRES_SUFFIX).with_suffix(ext)

        if img.stat().st_size < threshold_bytes:
            print(f"  SKIP {rel} ({size_mb:.1f} MB < soglia)")
            skipped += 1
            continue

        if lowres.exists():
            print(f"  ESISTE {rel} → {lowres.name}")
            skipped += 1
            continue

        if args.png:
            result = optimize_png(img, args.max_width, PNGQUANT_QUALITY)
        else:
            result = optimize_jpg(img, args.max_width, JPG_QUALITY)

        if result:
            new_mb = result.stat().st_size / (1024 * 1024)
            print(f"  OK {rel} ({size_mb:.1f} MB → {new_mb:.1f} MB)")
            optimized += 1

    print(f"\n=== {optimized} ottimizzate, {skipped} saltate ===")


if __name__ == "__main__":
    main()
