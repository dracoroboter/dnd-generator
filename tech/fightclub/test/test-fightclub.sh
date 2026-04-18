#!/bin/bash
# test-fightclub.sh — Testa gli script di conversione MD↔XML FightClub
# Uso: bash tech/fightclub/test/test-fightclub.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEST_DIR="$SCRIPT_DIR/test"

echo "=== Test MD → XML ==="

echo "--- Korex (stat block completo) ---"
python3 "$SCRIPT_DIR/md-to-fightclub.py" \
    "$PROJECT_ROOT/adventures/FuoriDaHellfire/personaggi/NPC_Korex.md" \
    -o "$TEST_DIR/korex.xml"

echo "--- Cattivone (mago con incantesimi) ---"
python3 "$SCRIPT_DIR/md-to-fightclub.py" \
    "$PROJECT_ROOT/adventures/AvventuraDiProva/personaggi/NPC_Cattivone.md" \
    -o "$TEST_DIR/cattivone.xml"

echo ""
echo "=== Test XML → MD ==="

echo "--- Korex round-trip ---"
python3 "$SCRIPT_DIR/fightclub-to-md.py" \
    "$TEST_DIR/korex.xml" \
    -o "$TEST_DIR/korex_roundtrip.md"

echo "--- Winter Wolf (SRD) ---"
python3 -c "
import re
with open('$PROJECT_ROOT/tech/data/compendium/Sources/SystemReferenceDocument/all-srd.xml') as f:
    text = f.read()
m = re.search(r'(<monster><name>Winter Wolf</name>.*?</monster>)', text)
if m:
    xml = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<compendium version=\"5\" auto_indent=\"NO\">\n' + m.group(1).replace('&#39;', \"'\") + '\n</compendium>'
    with open('$TEST_DIR/winter_wolf.xml', 'w') as out:
        out.write(xml)
    print('✓ Estratto Winter Wolf da SRD')
"
python3 "$SCRIPT_DIR/fightclub-to-md.py" \
    "$TEST_DIR/winter_wolf.xml" \
    -o "$TEST_DIR/winter_wolf.md"

echo ""
echo "=== Test XML → PDF (Playwright) ==="

echo "--- Korex PDF ---"
node "$SCRIPT_DIR/md-to-statblock-pdf.js" "$TEST_DIR/korex.xml" -o "$TEST_DIR/korex.pdf"

echo "--- Korex PNG ---"
node "$SCRIPT_DIR/md-to-statblock-pdf.js" "$TEST_DIR/korex.xml" -o "$TEST_DIR/korex.png"

echo "--- Winter Wolf PDF ---"
node "$SCRIPT_DIR/md-to-statblock-pdf.js" "$TEST_DIR/winter_wolf.xml" -o "$TEST_DIR/winter_wolf.pdf"

echo ""
echo "=== Validazione XML (se xmllint disponibile) ==="
if command -v xmllint &> /dev/null; then
    XSD="$PROJECT_ROOT/tech/data/compendium/compendium.xsd"
    for xml in "$TEST_DIR"/*.xml; do
        if xmllint --noout --schema "$XSD" "$xml" 2>/dev/null; then
            echo "✓ $(basename $xml) valido"
        else
            echo "⚠ $(basename $xml) non valido (potrebbe essere un subset)"
        fi
    done
else
    echo "xmllint non trovato — skip validazione schema"
fi

echo ""
echo "=== File generati ==="
ls -la "$TEST_DIR"
