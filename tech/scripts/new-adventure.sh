#!/bin/bash
# new-adventure.sh — Crea lo scheletro di una nuova avventura dal template
# Uso: bash tech/scripts/new-adventure.sh <NomeAvventura>
# Esempio: bash tech/scripts/new-adventure.sh CriptaDiMalachar

set -e

ADVENTURE="$1"

if [ -z "$ADVENTURE" ]; then
    echo "Uso: $0 <NomeAvventura>"
    echo "Esempio: $0 CriptaDiMalachar"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEMPLATE_DIR="$PROJECT_ROOT/adventures/AdventureTemplate"
DEST_DIR="$PROJECT_ROOT/adventures/$ADVENTURE"
RELEASES_DIR="$PROJECT_ROOT/releases/$ADVENTURE"

if [ -d "$DEST_DIR" ]; then
    echo "Errore: '$DEST_DIR' esiste già."
    exit 1
fi

echo "=== Nuova avventura: $ADVENTURE ==="

# Copia template
cp -r "$TEMPLATE_DIR" "$DEST_DIR"

# Rinomina file placeholder
mv "$DEST_DIR/NomeAvventura.md" "$DEST_DIR/${ADVENTURE}.md"
mv "$DEST_DIR/personaggi/NPC_NomePersonaggio.md" "$DEST_DIR/personaggi/NPC_NomePersonaggio.md.placeholder"
mv "$DEST_DIR/01_NomeModulo/NomeModulo.md" "$DEST_DIR/01_NomeModulo/${ADVENTURE}_Modulo01.md"

# Sostituisce [NomeAvventura] nei file
find "$DEST_DIR" -name "*.md" | xargs sed -i "s/\[NomeAvventura\]/$ADVENTURE/g; s/NomeAvventura/$ADVENTURE/g"

# Crea directory releases
mkdir -p "$RELEASES_DIR"

echo ""
echo "Struttura creata in: adventures/$ADVENTURE/"
echo "Release directory:   releases/$ADVENTURE/"
echo ""
echo "Prossimi passi:"
echo "  1. Esegui il wizard: python3 tech/scripts/adventure-wizard.py $ADVENTURE"
echo "  2. Rinomina i moduli: adventures/$ADVENTURE/01_NomeModulo/"
echo "  3. Rinomina/compila: adventures/$ADVENTURE/personaggi/NPC_NomePersonaggio.md.placeholder"
