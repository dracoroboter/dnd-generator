#!/bin/bash
# setup.sh — Installa i prerequisiti per gli script del progetto DnD
# Uso: bash tech/scripts/setup.sh

set -e

echo "=== Setup prerequisiti DnD project ==="

check_or_install() {
    local cmd="$1"
    local pkg="$2"
    if command -v "$cmd" &>/dev/null; then
        echo "  ✓ $cmd già installato ($(command -v "$cmd"))"
    else
        echo "  → Installazione $pkg..."
        sudo apt-get install -y "$pkg"
        echo "  ✓ $cmd installato"
    fi
}

echo ""
echo "Verifica dipendenze..."
check_or_install pandoc pandoc
check_or_install wkhtmltopdf wkhtmltopdf
check_or_install zip zip
check_or_install python3 python3

# Node e Playwright (per generazione mappe)
check_or_install node nodejs
if command -v node &>/dev/null; then
    if ! node -e "require('playwright')" 2>/dev/null; then
        echo "  → Installazione playwright..."
        cd "$(dirname "$0")/../.." && npm install playwright 2>/dev/null
        npx playwright install chromium 2>/dev/null
        echo "  ✓ playwright installato"
    else
        echo "  ✓ playwright già installato"
    fi
fi

echo ""
echo "=== Setup completato ==="
