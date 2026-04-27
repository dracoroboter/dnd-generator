# How-To: Calcolare la Difficoltà di un Incontro

Guida per usare `encounter-difficulty.py`, che calcola la difficoltà di un incontro D&D 5e seguendo il sistema XP del Dungeon Master's Guide (2014).

## Prerequisiti

```bash
bash tech/scripts/setup.sh
```

Richiede solo `python3` (già incluso in Ubuntu/WSL di default).

## Concetti base

Lo script implementa il sistema DMG p.82:

1. Calcola le **soglie XP** del party (Easy/Medium/Hard/Deadly) sommando le soglie di ogni PG per livello
2. Calcola gli **XP totali** dei nemici in base al loro CR
3. Applica un **moltiplicatore** in base al numero di nemici (più nemici = incontro più difficile)
4. Confronta gli XP aggiustati con le soglie del party

Riferimento online equivalente: [Kobold Fight Club](https://koboldplus.club)

## Sintassi

```bash
python3 tech/scripts/encounter-difficulty.py -p <N> <LVL> [<N> <LVL> ...] -m <N> <CR> [<N> <CR> ...]
```

- `-p` / `--players`: coppie `<numero PG> <livello>` — si possono specificare più gruppi
- `-m` / `--monsters`: coppie `<numero nemici> <CR>` — CR può essere `0`, `1/8`, `1/4`, `1/2`, `1`...`30`

## Esempi

**Party omogeneo (4 PG livello 3) vs 3 goblin CR1/4 + 1 bugbear CR1:**
```bash
python3 tech/scripts/encounter-difficulty.py -p 4 3 -m 3 1/4 1 1
```

**Party misto (2 PG lv2 + 2 PG lv3) vs 2 scheletri CR1/4:**
```bash
python3 tech/scripts/encounter-difficulty.py -p 2 2 2 3 -m 2 1/4
```

**Verifica boss fight (4 PG lv5 vs mago CR7):**
```bash
python3 tech/scripts/encounter-difficulty.py -p 4 5 -m 1 7
```

## Output

```
  Party:    4 PG (livelli: 3, 3, 3, 3)
  Nemici:   4 totali (CR: 1/4, 1/4, 1/4, 1)

  XP nemici (raw):          275
  Moltiplicatore:           2.0×  (4 mostri)
  XP aggiustati:            550

  Soglie party:
    Easy        300 XP
    Medium      600 XP
    Hard        900 XP ◄
    Deadly     1600 XP

  ══════════════════════════
  Difficoltà: HARD
```

Il `◄` indica la soglia raggiunta.

## Limiti del sistema

Il sistema CR/XP del DMG è **oggettivo ma impreciso**: sovrastima la difficoltà con molti nemici deboli, sottostima con nemici con capacità speciali (incantatori, controllo). Usarlo come punto di partenza, non come verdetto definitivo.

Per una valutazione più completa, affiancare al risultato una nota narrativa nel file del modulo (es. *"incontro pensato come HARD ma Cattivone è progettato per fuggire — difficoltà effettiva MEDIUM"*).
