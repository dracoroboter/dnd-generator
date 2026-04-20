#!/bin/bash
# release.sh — Crea una release di un'avventura DnD
# Uso: ./release.sh <NomeAvventura> <versione>
# Esempio: ./release.sh AvventuraDiProva 1.0
#
# Struttura attesa dell'avventura:
#   adventures/<NomeAvventura>/
#     *.md, */*.md          → convertiti in PDF
#     maps/*.png|svg       → copiati nella release
#     characters/*.png|jpg  → copiati nella release
#     cover.png             → copertina (opzionale)
#
# Output:
#   releases/<NomeAvventura>/<NomeAvventura>_v<versione>_<data>.zip

set -e

ADVENTURE="$1"
VERSION="$2"

if [ -z "$ADVENTURE" ] || [ -z "$VERSION" ]; then
    echo "Uso: $0 <NomeAvventura> <versione>"
    echo "Esempio: $0 AvventuraDiProva 1.0"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ADVENTURE_DIR="$PROJECT_ROOT/adventures/$ADVENTURE"
RELEASES_DIR="$PROJECT_ROOT/releases/$ADVENTURE"

if [ ! -d "$ADVENTURE_DIR" ]; then
    echo "Errore: directory '$ADVENTURE_DIR' non trovata."
    exit 1
fi

DATE=$(date +%Y-%m-%d_%H%M)
RELEASE_NAME="${ADVENTURE}_v${VERSION}_${DATE}"
BUILD_DIR="/tmp/${RELEASE_NAME}"

echo "=== $ADVENTURE — Release v${VERSION} (${DATE}) ==="

# Pulizia e setup
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/pdf" "$BUILD_DIR/mappe" "$BUILD_DIR/personaggi"

# Converti tutti i .md in PDF (esclusi README, kiro, PlanBook)
echo ""
echo "Conversione MD → PDF..."
find "$ADVENTURE_DIR" -name "*.md" \
    ! -name "README.md" \
    ! -name "AdventureBook.md" \
    ! -name "PlanBook.md" \
    | sort | while read -r md; do
    name=$(basename "$md" .md)
    dest="$BUILD_DIR/pdf/${name}.pdf"
    echo "  $(realpath --relative-to="$ADVENTURE_DIR" "$md") → pdf/${name}.pdf"
    pandoc "$md" -o "$dest" --pdf-engine=wkhtmltopdf --metadata title="$name" 2>/dev/null \
        || echo "  WARN: conversione fallita per $md"
done

# Copia mappe
echo ""
echo "Copia mappe..."
find "$ADVENTURE_DIR" -path "*/maps/*.png" -o -path "*/maps/*.svg" | sort | while read -r f; do
    cp "$f" "$BUILD_DIR/maps/" && echo "  $(basename "$f")"
done

# Copia artwork personaggi
echo ""
echo "Copia artwork personaggi..."
find "$ADVENTURE_DIR/personaggi" -name "*.png" -o -name "*.jpg" 2>/dev/null | sort | while read -r f; do
    cp "$f" "$BUILD_DIR/characters/" && echo "  $(basename "$f")"
done

# Copia copertina
if [ -f "$ADVENTURE_DIR/Cover.png" ]; then
    cp "$ADVENTURE_DIR/Cover.png" "$BUILD_DIR/"
    echo "  Cover.png"
fi

# Crea file di versione
cat > "$BUILD_DIR/RELEASE.txt" <<EOF
$ADVENTURE
Versione: $VERSION
Data: $DATE

Contenuto:
- pdf/          Documenti dell'avventura in formato PDF
- maps/        Mappe (immagini)
- characters/   Artwork personaggi

Sistema: D&D 5e (2014)
EOF

# Crea ZIP
echo ""
mkdir -p "$RELEASES_DIR"
ZIPFILE="$RELEASES_DIR/${RELEASE_NAME}.zip"
cd /tmp
zip -r "$ZIPFILE" "$RELEASE_NAME" -x "*.log" > /dev/null
cd "$PROJECT_ROOT"

# Pulizia
rm -rf "$BUILD_DIR"

echo ""
echo "=== Release creata: releases/$ADVENTURE/${RELEASE_NAME}.zip ==="
ls -lh "$ZIPFILE"
