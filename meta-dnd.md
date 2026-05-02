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
├── tech/how-to/how-to-aws-profile-switch.md  # Documentazione switch profilo AI CLI
│
├── adventures/              # Avventure create
│   ├── AdventureTemplate/   # Template di riferimento
│   ├── LAnelloDelConte/     # Saga puntata 1 (normalizzata)
│   ├── FuoriDaHellfire/     # One-shot (normalizzata)
│   └── LoScettroDityr/      # Saga 4 moduli (normalizzata)
│
├── releases/                # PDF + ZIP generati (non editare, in .gitignore)
│   └── NomeAvventura/
│
├── tech/                    # Script, tool e regole tecniche
│   ├── scripts/             # Script di automazione
│   ├── rules/               # Regole di riferimento
│   ├── how-to/              # Guide procedurali passo-passo
│   ├── i18n/                # Label multilingua (it.json, en.json)
│   └── tests/               # Test di non regressione
│
├── public/                  # PDF pubblicati (tracciata da git)
├── other/                   # File accessori generali (stat block PG, ecc.)
│
└── legacy/                  # Materiale originale non modificato
    └── DracoAvventure/      # Copia dell'archivio Windows originale
```

---

## Regole Generali

### Lingua e naming

- Contenuto avventure e documentazione: **italiano** (lingua primaria). Traduzioni in **inglese** disponibili per le avventure normalizzate — il contenuto viene scritto in italiano e poi tradotto
- Commenti nel codice sorgente: **inglese**

Per le convenzioni di naming complete (4 categorie: PascalCase avventure, kebab-case tech, UPPER_SNAKE_CASE meta, kebab-case script) vedere **`tech/rules/adventure-template.md` § Convenzioni di naming** — fonte di verità unica.

### File obbligatori per ogni avventura

| file | contenuto |
|------|-----------|
| `manifest.json` | Configurazione avventura: lingue disponibili, titolo e sottotitolo per lingua |
| `README.md` | Descrizione pubblica senza spoiler (per lettori umani) |
| `AdventureBook.md` | Contesto e istruzioni specifiche per Kiro su questa avventura |
| `PlanBook.md` | Todo list, stato avanzamento, note riservate al DM |
| `NomeAvventura.md` | Documento principale: lore, plot, NPC, consigli master |

### Struttura moduli
Ogni modulo/quest in subdirectory `NN_NomeModulo/` con risorse proprie:
```
NN_NomeModulo/
├── NomeModulo.md
└── maps/        ← opzionale
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

## Multilingua

Il progetto supporta avventure in più lingue (attualmente italiano e inglese). La struttura multilingua è:

### manifest.json

Ogni avventura ha un `manifest.json` nella root che dichiara le lingue disponibili e i metadati per lingua (titolo, sottotitolo per la copertina).

### Directory per lingua

Il contenuto testuale e i file generati vanno sotto `it/` e `en/` nella directory dell'avventura:

```
NomeAvventura/
├── manifest.json            # lingue, titolo/sottotitolo per lingua
├── README.md                # meta-documento (root, condiviso)
├── AdventureBook.md         # meta-documento (root, condiviso)
├── PlanBook.md              # meta-documento (root, condiviso)
├── img/                     # immagini condivise tra lingue
├── it/                      # contenuto italiano
│   ├── NomeAvventura.md
│   ├── characters/          # NPC/MON .md, .xml, stat block
│   └── NN_NomeModulo/
└── en/                      # contenuto inglese
    ├── NomeAvventura.md
    ├── characters/
    └── NN_NomeModulo/
```

### Cosa è condiviso, cosa è per lingua

- **Condiviso** (root): immagini (`img/`, `maps/*.png`, `characters/img/`), meta-documenti (README, PlanBook, AdventureBook, DM_Prep), `manifest.json`
- **Per lingua** (`it/`, `en/`): testo `.md`, schede NPC/MON `.md`, file generati (`.xml`, stat block `.pdf`/`.png`)

### Label i18n

Le etichette usate negli script (copertina PDF, sezioni, appendice) sono in `tech/i18n/it.json` e `tech/i18n/en.json`.

### Flag --lang

Gli script principali supportano `--lang <codice>` per operare sulla lingua desiderata:
- `create-pdf-adventure.py NomeAvventura --lang en`
- `generate-statblocks.py NomeAvventura --lang en`
- `md-to-fightclub.py ... --lang en`

Default: `it` (italiano).

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
Guida: `tech/how-to/how-to-encounter-difficulty.md`
