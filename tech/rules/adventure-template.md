# AdventureTemplate — Struttura Standard delle Avventure

Documento di riferimento per la struttura delle avventure del progetto.
Per le istruzioni operative (sezioni obbligatorie, formato file) vedere `adventures/AdventureTemplate/AdventureBook.md`.
Per le regole di contenuto vedere `tech/rules/content-rules.md`.

---

## Struttura directory

```
adventures/
└── NomeAvventura/
    ├── README.md                    ← descrizione pubblica senza spoiler
    ├── AdventureBook.md             ← istruzioni per l'AI
    ├── PlanBook.md                  ← stato del lavoro, todo, note DM
    ├── NomeAvventura.md             ← documento principale
    ├── maps/
    │   ├── NomeMappa.md             ← descrizione mappa (stesso nome del PNG)
    │   ├── NomeMappa.png            ← mappa grafica
    │   └── other/                   ← SVG sorgente, draft, versioni di lavoro
    ├── characters/
    │   ├── markdown/                ← schede NPC in markdown
    │   │   └── NPC_NomePersonaggio.md
    │   ├── img/                     ← artwork personaggi (opzionale)
    │   │   └── NomePersonaggio.png
    │   ├── fightclub/               ← XML FightClub (generati da md-to-fightclub.py)
    │   │   └── NPC_NomePersonaggio.xml
    │   └── statblock/               ← PDF e PNG stampabili (generati da md-to-statblock-pdf.js)
    │       ├── NPC_NomePersonaggio.pdf
    │       └── NPC_NomePersonaggio.png
    ├── other/                       ← file accessori non inclusi nel PDF
    │   └── pg/                      ← stat block PG (*_GM.*)
    ├── objects/                     ← oggetti narrativi: simboli, lettere, artefatti (opzionale)
    │   └── NomeOggetto.md           ← descrizione + prompt generazione immagine
    ├── meta/                        ← documenti di lavoro del DM (opzionale, non pubblicabili)
    │   └── DiarioSessioni.md        ← registro sessioni giocate
    └── NN_NomeModulo/               ← un modulo per subdirectory
        ├── NomeModulo.md
        └── maps/                    ← mappe specifiche del modulo
            ├── NomeMappa.md         ← descrizione mappa (opzionale)
            ├── NomeMappa.png        ← mappa grafica (opzionale)
            └── other/               ← draft, versioni di lavoro
```

Le release (PDF + ZIP) non stanno nell'avventura ma in:
```
releases/
└── NomeAvventura/
    └── NomeAvventura_vX.Y_YYYY-MM-DD_HHMM.zip
```

---

## Convenzioni di naming

> Questa è la **fonte di verità** per il naming del progetto. Gli altri documenti (`meta-dnd.md`, `CLAUDE.md`, `content-rules.md`) rimandano qui.

### 1. Contenuto avventure — PascalCase

File narrativi dentro `adventures/`: moduli, NPC, mappe, documento principale.

| elemento | convenzione | esempio |
|----------|-------------|---------|
| Documento principale | PascalCase | `LAnelloDelConte.md` |
| Moduli (directory) | `NN_PascalCase` | `01_LeFogneDiFianus/` |
| Moduli (file) | PascalCase | `LeFogneDiFianus.md` |
| Schede NPC/mostri | prefisso `NPC_` o `MON_` + PascalCase | `NPC_SirGorimVel.md`, `MON_DragonRosso.md` |
| Mappe (descrizione) | PascalCase, stesso nome base del PNG | `FianusRomanus.md` |
| Nome avventura (directory) | PascalCase | `LAnelloDelConte/`, `FuoriDaHellfire/` |
| File fissi dell'avventura | PascalCase | `AdventureBook.md`, `PlanBook.md` |

Lingua: **italiano**.

### 2. Documenti tecnici — kebab-case

File in `tech/rules/`, `tech/how-to/`, documentazione script.

| elemento | convenzione | esempio |
|----------|-------------|---------|
| Regole e specifiche | kebab-case | `adventure-template.md`, `content-rules.md` |
| Guide procedurali | kebab-case | `how-to-release.md`, `how-to-new-npc.md` |
| Documentazione script | kebab-case | `docs-create-pdf-adventure.md` |
| Piani di sviluppo | kebab-case | `plan-create-pdf-adventure.md` |

Lingua: **italiano**.

### 3. File meta/progetto — UPPER_SNAKE_CASE

File nella root del progetto che descrivono il progetto stesso.

| elemento | convenzione | esempio |
|----------|-------------|---------|
| File meta | UPPER_SNAKE_CASE | `README.md`, `CLAUDE.md`, `CHANGELOG.md` |
| Plan operativo | kebab-case (eccezione storica) | `plan-meta-dnd.md`, `meta-dnd.md` |

Lingua: **italiano**.

### 4. Script — kebab-case

Codice sorgente in `tech/scripts/` e sottodirectory.

| elemento | convenzione | esempio |
|----------|-------------|---------|
| Script Python/Bash | kebab-case | `check-adventure.py`, `new-npc.py` |
| Commenti nel codice | inglese | `# Validate adventure structure` |

Lingua commenti: **inglese**.

### Immagini e asset

| elemento | convenzione | esempio |
|----------|-------------|---------|
| Immagini avventure | PascalCase | `FianusRomanus.png`, `SirGorimVel.png` |
| Copertina | `NomeAvventura_COVER.png` in `img/` | `LAnelloDelConte_COVER.png` |
| Versioni lowres | suffisso `-lowres` | `FianusRomanus-lowres.jpg` |
| Stat block generati | stesso prefisso del sorgente | `NPC_SirGorimVel.pdf`, `NPC_SirGorimVel.png` |
| XML FightClub generati | stesso prefisso del sorgente | `NPC_SirGorimVel.xml` |

### Directory

| elemento | convenzione | esempio |
|----------|-------------|---------|
| Directory strutturali | minuscolo, inglese | `maps/`, `characters/`, `img/`, `other/` |
| Sottodirectory characters | minuscolo, inglese | `markdown/`, `fightclub/`, `statblock/` |
| Directory tech | minuscolo, inglese | `scripts/`, `rules/`, `how-to/` |

### Regole mappe

- Ogni mappa grafica (`.png`) può avere una descrizione markdown (`.md`) con lo **stesso nome base**.
- Le mappe `.md` sono **schede DM**: contengono mappa testuale e informazioni segrete per il master. Si usano quando la mappa grafica è assente o insufficiente.
- Se esistono sia PNG che SVG della stessa mappa, il **PNG è la versione canonica**. L'SVG va in `other/`.
- Le versioni di lavoro, draft o schematiche vanno in `other/` (con suffisso `_draft` se necessario).
- Il nome generico `MappaDM.md` è **deprecato**: usare un nome specifico PascalCase.
- Il file `MappaGenerale.md` è **deprecato**: splittare in un `.md` per ogni mappa.

### Directory `other/`

Contiene file accessori non inclusi nel PDF e non validati dal check. Organizzata per tipo:

```
other/
├── pg/          ← stat block PG (*_GM.png/pdf/html, fightclub xml)
└── maps/        ← mappe draft, SVG sorgente, versioni di lavoro
```

Le directory `other/` dentro `maps/` dei moduli contengono le mappe di lavoro di quel modulo specifico.

---

## File obbligatori

| file | scopo |
|------|-------|
| `README.md` | Presentazione pubblica — niente spoiler. Livello, durata, tono. |
| `AdventureBook.md` | Istruzioni per l'AI — struttura, convenzioni, note specifiche dell'avventura |
| `PlanBook.md` | Stato avanzamento, todo, note narrative riservate al DM |
| `NomeAvventura.md` | Documento principale: lore, plot, NPC, consigli master |
| `maps/` | Directory mappe — almeno un file `.md` o `.png` per mappa |

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
## Milestone
```

#### Milestone (dato strutturale opzionale)

La sezione `## Milestone` è un dato strutturale del modulo, non una semplice nota. Indica un avanzamento di livello dei PG, triggerato da un evento narrativo specifico o dal completamento di un certo numero di obiettivi.

**Posizione:** dopo `## Ricompense`, prima di `## Note al master`.

**Formato:**

```markdown
## Milestone

**Livello raggiunto:** X
**Trigger:** [descrizione dell'evento o condizione che attiva la milestone]
```

- **Livello raggiunto** — il livello a cui passano i PG.
- **Trigger** — l'evento specifico (es. "consegna della lettera a Gorim") o una condizione cumulativa (es. "completati almeno 3 dei 5 obiettivi secondari"). Deve essere un momento identificabile in gioco, non generico.

La milestone è **opzionale**: non tutti i moduli ne hanno una. Un modulo senza `## Milestone` significa che non c'è avanzamento di livello in quel modulo.

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
mv characters/markdown/NPC_NomePersonaggio.md characters/markdown/NPC_NomePNG.md
mv 01_NomeModulo 01_NomePrimoModulo
mv 01_NomePrimoModulo/NomeModulo.md 01_NomePrimoModulo/NomePrimoModulo.md

# 3. Crea la directory releases
mkdir -p releases/NomeMiaAvventura
```

Per la guida completa: `tech/how-to/how-to-new-adventure.md` *(da creare)*
