#!/bin/bash
# new-adventure.sh — Crea lo scheletro di una nuova avventura dal template
# Uso: bash tech/scripts/new-adventure.sh <NomeAvventura> [--modules N]
# Esempio: bash tech/scripts/new-adventure.sh CriptaDiMalachar --modules 3

set -e

ADVENTURE="$1"
NUM_MODULES=1

if [ -z "$ADVENTURE" ]; then
    echo "Uso: $0 <NomeAvventura> [--modules N]"
    echo "Esempio: $0 CriptaDiMalachar --modules 3"
    exit 1
fi

# Parse --modules
shift
while [ $# -gt 0 ]; do
    case "$1" in
        --modules) NUM_MODULES="$2"; shift 2 ;;
        *) echo "Opzione sconosciuta: $1"; exit 1 ;;
    esac
done

if ! [[ "$NUM_MODULES" =~ ^[1-9][0-9]?$ ]]; then
    echo "Errore: --modules deve essere un numero da 1 a 99"
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

echo "=== Nuova avventura: $ADVENTURE ($NUM_MODULES moduli) ==="

# Copia template
cp -r "$TEMPLATE_DIR" "$DEST_DIR"

# Rinomina file placeholder
mv "$DEST_DIR/NomeAvventura.md" "$DEST_DIR/${ADVENTURE}.md"
rm "$DEST_DIR/personaggi/NPC_NomePersonaggio.md"

# Crea moduli aggiuntivi (il template ha già 01_NomeModulo)
for i in $(seq 2 "$NUM_MODULES"); do
    NUM=$(printf "%02d" "$i")
    cp -r "$DEST_DIR/01_NomeModulo" "$DEST_DIR/${NUM}_NomeModulo"
done

# Sostituisce [NomeAvventura] nei file
find "$DEST_DIR" -name "*.md" | xargs sed -i "s/\[NomeAvventura\]/$ADVENTURE/g; s/NomeAvventura/$ADVENTURE/g"

# Crea directory releases
mkdir -p "$RELEASES_DIR"

echo ""
echo "Struttura creata in: adventures/$ADVENTURE/"
echo "Release directory:   releases/$ADVENTURE/"
echo "Moduli creati:       $NUM_MODULES"
echo ""
echo "Prossimi passi:"
echo "  1. Esegui il wizard: python3 tech/scripts/adventure-wizard.py $ADVENTURE"
echo "  2. Rinomina i moduli: adventures/$ADVENTURE/01_NomeModulo/ etc."
echo "  3. Crea NPC: python3 tech/scripts/new-npc.py $ADVENTURE"
