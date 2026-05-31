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

## Party con NPC companion

Quando il party include NPC companion (alleati che combattono), vanno inclusi nel calcolo delle soglie. Il problema è che un NPC con CR non ha un "livello" diretto.

### Conversione CR → livello equivalente (Xanathar's Guide)

Lo script `check-encounter-difficulty.py` usa questa tabella (derivata da Xanathar's Guide, matchup 1-a-1):

| CR | Livello equivalente |
|----|-------------------|
| 1/8, 1/4, 1/2 | 1 |
| 1 | 2 |
| 2 | 4 |
| 3 | 5 |
| 4 | 6 |
| 5 | 8 |
| 6 | 9 |
| 7 | 10 |
| 8 | 11 |

### Esempio con companion

Party: 3 PG lv5 + Udo (veterano CR3) + Fin (rogue lv3)

```bash
# Calcolo manuale:
python3 tech/scripts/encounter-difficulty.py -p 3 5 1 5 1 3 -m 15 1/4
#                                               ↑PG  ↑Udo(CR3≈lv5) ↑Fin
```

Udo CR3 → livello equivalente 5. Fin lv3 → livello 3.
Soglie: 3×750 + 1×750 + 1×225 = 3975 (Hard).

### Nota sull'approssimazione

La conversione CR→livello è generosa: un NPC CR3 non è forte come un PG lv5 (stat più basse, niente feature di classe). In pratica gli incontri dichiarati HARD con companion sono borderline MEDIUM/HARD. Questo è accettabile — il DM dichiara HARD come scelta conservativa.

## Verifica automatica: check-encounter-difficulty.py

Lo script `check-encounter-difficulty.py` verifica che le difficoltà dichiarate nei moduli corrispondano al calcolo XP.

```bash
python3 tech/scripts/check-encounter-difficulty.py FuoriDaHellfire
```

### Cosa fa

1. Rileva il party dall'intestazione della tabella `## Nemici` (formato: `Difficoltà (3 PG lv5 + Udo CR3 + Fin lv3)`)
2. Raggruppa i nemici per Luogo (stesso luogo = incontro combinato)
3. Calcola la difficoltà e confronta con quella dichiarata
4. Genera un report in `tech/reports/`

### Formato intestazione tabella Nemici

Il party si dichiara **una sola volta** all'inizio del modulo:

```markdown
## Descrizione

**Party:** 3 PG lv5 + Udo CR3 + Fin lv3
```

La tabella Nemici ha solo `Difficoltà` senza ripetere il party:

```markdown
| Luogo | Nemici | N. | CR | Difficoltà |
```

Lo script cerca prima `**Party:**` nel testo del modulo. Se non lo trova, cerca `**Party:**` o il formato legacy nell'intestazione della tabella `Difficoltà (...)`. Per ogni companion indicare `CR3` (convertito con tabella Xanathar) o `lv3` (usato direttamente). Se manca il livello/CR, il companion è trattato come stesso livello dei PG.
