# Meta DnD - Struttura e Regole del Progetto

## Contesto

Raccolta di avventure D&D 5e (2014) gestita come progetto strutturato con versionamento, template e automazione.

- Uso personale, con intenzione di pubblicare su GitHub (licenza CC BY-SA 4.0) quando la qualità lo giustifica — la valutazione è soggettiva e affidata a feedback di community esterne (es. r/DnDBehindTheScreen, gdr-online.com)
- PDF ottimizzati per condivisione digitale
- Avventure di tipo misto: saga multi-campagna (LoScettroDityr), campagna multi-sessione (LAnelloDelConte), one-shot future
- Il template di riferimento è una one-shot (caso più semplice, estendibile)
- Tutte le avventure legacy verranno migrate in Markdown, non necessariamente subito

---

## Struttura Directory

```
dungeonandragon/
├── meta-dnd.md              # Questo file — struttura e regole generali
├── plan-meta-dnd.md         # Todo list operativa per attuare meta-dnd.md
├── aws-profile-switch.md    # Documentazione switch profilo AI CLI
│
├── adventures/              # Avventure create
│   ├── AdventureTemplate/   # Template di riferimento (one-shot esempio)
│   ├── AvventuraDiProva/    # Prima avventura normalizzata (esempio concreto)
│   ├── LAnelloDelConte/     # Da normalizzare da legacy
│   ├── IlReSpezzato/        # Da normalizzare da legacy
│   └── LoScettroDityr/      # Da normalizzare da legacy
│
├── releases/                # Release generate (PDF + ZIP), una dir per avventura
│   └── NomeAvventura/
│
├── tech/                    # Script, tool e regole tecniche
│   ├── scripts/             # Script di automazione
│   ├── rules/               # Regole di riferimento
│   └── how-to/              # Guide procedurali passo-passo
│
└── legacy/                  # Materiale originale non modificato
    └── DracoAvventure/      # Copia dell'archivio Windows originale
```

---

## Regole Generali

### Lingua
- Nomi file e directory: PascalCase italiano (eccezione: titoli propri delle avventure)
- Contenuto delle avventure: italiano

### Naming Convention File
- File `.md`: **PascalCase** (es. `NomeAvventura.md`, `NPC_IlConte.md`)
- Directory: **minuscolo** (es. `personaggi/`, `mappe/`)
- Moduli: prefisso numerico a due cifre + PascalCase (es. `01_LeFogneDiFianus/`)
- NPC: `NPC_<NomePersonaggio>.md`
- Mappe immagini: PascalCase (es. `MappaRegione.png`)
- Copertina: `Cover.png`

### File obbligatori per ogni avventura

| file | contenuto |
|------|-----------|
| `README.md` | Descrizione pubblica senza spoiler (per lettori umani) |
| `AdventureBook.md` | Contesto e istruzioni specifiche per Kiro su questa avventura |
| `PlanBook.md` | Todo list, stato avanzamento, note riservate al DM |
| `NomeAvventura.md` | Documento principale: lore, plot, NPC, consigli master |
| `mappe/MappaGenerale.md` | Luoghi, connessioni, distanze |

### Struttura moduli
Ogni modulo/quest in subdirectory `NN_NomeModulo/` con risorse proprie:
```
NN_NomeModulo/
├── NomeModulo.md
└── mappe/        ← opzionale
```

### Schede personaggio
- **PNG antagonisti**: scheda completa con stat block
- **PNG secondari**: scheda semplificata
- **Schede PG**: opzionali, non parte dell'avventura base; se presenti per sessione ad hoc, in directory separata fuori da `adventures/`

### Formato Avventure
- Tutto in Markdown
- Blockquote (`>`) per testo da leggere ai giocatori
- Tabelle per statistiche mostri e loot
- Difficoltà incontro dichiarata nella sezione `## Nemici` di ogni modulo

### Versionamento e Release
- Git per versionamento (repository GitHub)
- Tag per release (`v0.1`, `v1.0`, ecc.)
- Release generate con `tech/scripts/release.sh <NomeAvventura> <versione>`
- PDF generati via Pandoc + wkhtmltopdf
- Release salvate in `releases/<NomeAvventura>/` — non dentro l'avventura

---

## Avventure Legacy

Materiale originale conservato intatto in `legacy/DracoAvventure/`:
- **LoScettroDityr** — saga multi-campagna (4 moduli A/B/C/D), formato `.odt`
- **IlReSpezzato** — avventura con prologo a fumetti, formato `.odt`
- **LAnelloDelConte** — già in Markdown, da normalizzare

---

## Tool Mappe

Tool già usati e approvati:
- [Inkarnate](https://inkarnate.com) — mappe geografiche/regionali
- [DungeonFog](https://app.dungeonfog.com) — battle map
- [Watabou city generator](https://watabou.itch.io/medieval-fantasy-city-generator) — mappe città
- [Watabou one-page-dungeon](https://watabou.github.io/one-page-dungeon/) — dungeon (URL con `?seed=` parametrico)
- [DungeonScrawl](https://app.dungeonscrawl.com) — dungeon

---

## Tool Difficoltà Incontri

Riferimento online: [Kobold Fight Club](https://koboldplus.club) — calcola difficoltà incontro (Easy/Medium/Hard/Deadly) dato numero/livello PG e lista nemici con CR.

Per uso locale: `tech/scripts/encounter-difficulty.py` — stesso calcolo offline.
Guida: `tech/how-to/HowToEncounterDifficulty.md`
