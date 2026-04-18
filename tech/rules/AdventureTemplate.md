# AdventureTemplate — Struttura Standard delle Avventure

Documento di riferimento per la struttura delle avventure del progetto.
Per le istruzioni operative (sezioni obbligatorie, formato file) vedere `adventures/AdventureTemplate/AdventureBook.md`.
Per le regole di contenuto vedere `tech/rules/ContentRules.md`.

---

## Struttura directory

```
adventures/
└── NomeAvventura/
    ├── README.md                    ← descrizione pubblica senza spoiler
    ├── AdventureBook.md             ← istruzioni per l'AI
    ├── PlanBook.md                  ← stato del lavoro, todo, note DM
    ├── NomeAvventura.md             ← documento principale
    ├── mappe/
    │   ├── MappaGenerale.md         ← descrizione testuale luoghi e connessioni
    │   └── *.png / *.svg            ← immagini mappe (opzionale)
    ├── personaggi/
    │   ├── markdown/                ← schede NPC in markdown
    │   │   └── NPC_NomePersonaggio.md
    │   ├── img/                     ← artwork personaggi (opzionale)
    │   │   └── NomePersonaggio.png
    │   ├── fightclub/               ← XML FightClub (generati da md-to-fightclub.py)
    │   │   └── NPC_NomePersonaggio.xml
    │   └── statblock/               ← PDF e PNG stampabili (generati da md-to-statblock-pdf.js)
    │       ├── NPC_NomePersonaggio.pdf
    │       └── NPC_NomePersonaggio.png
    └── NN_NomeModulo/               ← un modulo per subdirectory
        ├── NomeModulo.md
        └── mappe/                   ← mappe specifiche del modulo (opzionale)
```

Le release (PDF + ZIP) non stanno nell'avventura ma in:
```
releases/
└── NomeAvventura/
    └── NomeAvventura_vX.Y_YYYY-MM-DD_HHMM.zip
```

---

## Convenzioni di naming

| elemento | convenzione | esempio |
|----------|-------------|---------|
| File `.md` | PascalCase | `NomeAvventura.md`, `NPC_IlConte.md` |
| Directory | minuscolo | `personaggi/`, `mappe/` |
| Moduli | `NN_PascalCase` | `01_IndagineAPanciaverde/` |
| Immagini | PascalCase | `MappaRegione.png`, `NPC_Cattivone.png` |
| Nome avventura | PascalCase | `AvventuraDiProva/`, `LAnelloDelConte/` |
| Sottodirectory personaggi | minuscolo | `markdown/`, `img/`, `fightclub/`, `statblock/` |

---

## File obbligatori

| file | scopo |
|------|-------|
| `README.md` | Presentazione pubblica — niente spoiler. Livello, durata, tono. |
| `AdventureBook.md` | Istruzioni per l'AI — struttura, convenzioni, note specifiche dell'avventura |
| `PlanBook.md` | Stato avanzamento, todo, note narrative riservate al DM |
| `NomeAvventura.md` | Documento principale: lore, plot, NPC, consigli master |
| `mappe/MappaGenerale.md` | Luoghi, connessioni, distanze |

---

## Tipi di file

### Documento principale
Contiene tutto ciò che serve per capire l'avventura: lore, introduzione, plot, NPC principali (con rimandi alle schede), consigli al master, tabella dei moduli con link.

Sezioni obbligatorie:
```
## Lore
## Introduzione
## NPC principali
## Struttura dell'avventura
```

Sezioni consigliate (non obbligatorie):
```
## Plot generale
## Consigli al master
```

### Moduli (`NN_NomeModulo/NomeModulo.md`)
Un file per ogni quest, dungeon o luogo significativo.

Sezioni obbligatorie:
```
## Descrizione
## Obiettivo
## Ricompense
## Note al master
```

Sezioni opzionali:
```
## Luoghi interni
## Nemici
## Indizi chiave
## Finale
## Milestone     ← livello raggiunto dopo questo modulo (solo se applicabile)
```

### Schede PNG (`NPC_NomePersonaggio.md`)
- **Antagonisti principali**: scheda completa con stat block
- **PNG secondari**: scheda semplificata con stat essenziali

Sezioni obbligatorie (tutti i PNG):
```
## Informazioni generali
## Descrizione
## Motivazioni
## Note al master
```

Sezioni opzionali:
```
## Stat Block
## Agganci futuri
```

### Schede PG
Non fanno parte dell'avventura base. Se necessarie per una sessione con PG predefiniti, vanno in una directory separata fuori da `adventures/` (es. `sessions/NomeAvventura_NomeGruppo/`).

---

## Razionale delle scelte

- **PascalCase per i file**: coerente con `LAnelloDelConte` (avventura più matura del progetto), leggibile senza separatori
- **Minuscolo per le directory**: convenzione Unix standard, evita problemi su filesystem case-sensitive
- **Subdirectory per moduli**: scala bene quando un modulo ha mappe e immagini proprie; rende la navigazione più chiara nelle campagne multi-sessione
- **`AdventureBook.md` separato da `README.md`**: `README.md` è per lettori umani (anche giocatori), `AdventureBook.md` è contesto tecnico per l'AI
- **Release fuori dall'avventura**: i PDF/ZIP sono artefatti generati, non sorgente; non appartengono al repository dell'avventura

---

## Riferimento rapido: creare una nuova avventura

```bash
# 1. Copia il template
cp -r adventures/AdventureTemplate adventures/NomeMiaAvventura

# 2. Rinomina i file placeholder
cd adventures/NomeMiaAvventura
mv NomeAvventura.md NomeMiaAvventura.md
mv personaggi/NPC_NomePersonaggio.md personaggi/NPC_NomePNG.md
mv 01_NomeModulo 01_NomePrimoModulo
mv 01_NomePrimoModulo/NomeModulo.md 01_NomePrimoModulo/NomePrimoModulo.md

# 3. Crea la directory releases
mkdir -p releases/NomeMiaAvventura
```

Per la guida completa: `tech/how-to/HowToNewAdventure.md` *(da creare)*
