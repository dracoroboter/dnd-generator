# AdventureTemplate — Struttura Standard delle Avventure

Struttura tecnica delle avventure: directory, naming, file obbligatori, formato delle sezioni, tipi di file.

---

## Orientamento

| Scopo | File |
|-------|------|
| Struttura tecnica: directory, naming, file obbligatori, formato sezioni (questo file) | `tech/rules/adventure-template.md` |
| **Storytelling e semantica**: come scrivere un'avventura che funziona al tavolo | `tech/rules/content-rules.md` |
| Stile di scrittura, formato testo, convenzioni linguistiche | `tech/rules/writing-style.md` |

---

## Struttura directory

```
adventures/
└── NomeAvventura/
    ├── manifest.json                ← lingua default, lingue disponibili
    ├── README.md                    ← descrizione pubblica senza spoiler
    ├── AdventureBook.md             ← istruzioni per l'AI
    ├── PlanBook.md                  ← stato del lavoro, todo, note DM
    ├── img/                         ← immagini condivise (cover, illustrazioni)
    │   └── NomeAvventura_COVER.png
    ├── maps/                        ← immagini mappe root (condivise tra lingue)
    │   ├── NomeMappa.png
    │   └── other/                   ← SVG sorgente, draft
    ├── characters/
    │   └── img/                     ← artwork personaggi (condiviso tra lingue)
    │       └── NomePersonaggio.png
    ├── NN_NomeModulo/               ← immagini mappe modulo (condivise)
    │   └── maps/
    │       ├── NomeMappa.png
    │       └── other/
    ├── other/                       ← file accessori
    │   └── pg/
    ├── objects/                     ← oggetti narrativi (opzionale)
    ├── meta/                        ← documenti di lavoro DM (opzionale)
    │
    ├── it/                          ← contenuto italiano (lingua default)
    │   ├── NomeAvventura.md         ← documento principale
    │   ├── maps/
    │   │   └── NomeMappa.md         ← descrizioni mappe (stesso nome del PNG)
    │   ├── NN_NomeModulo/
    │   │   ├── NomeModulo.md
    │   │   └── maps/
    │   │       └── NomeMappa.md     ← descrizioni mappe modulo
    │   └── characters/
    │       ├── markdown/            ← schede NPC in markdown
    │       │   └── NPC_NomePersonaggio.md
    │       ├── fightclub/           ← XML FightClub (generati)
    │       │   └── NPC_NomePersonaggio.xml
    │       └── statblock/           ← PDF e PNG stampabili (generati)
    │           └── NPC_NomePersonaggio.png
    │
    └── en/                          ← contenuto inglese (traduzione)
        ├── NomeAvventura.md
        ├── maps/
        │   └── NomeMappa.md
        ├── NN_NomeModulo/
        │   ├── NomeModulo.md
        │   └── maps/
        │       └── NomeMappa.md
        └── characters/
            ├── markdown/
            ├── fightclub/
            └── statblock/
```

### manifest.json

```json
{
  "adventure_name": "NomeAvventura",
  "default_lang": "it",
  "languages": ["it", "en"]
}
```

### Regole multilingua

- Le immagini (img/, maps/*.png, characters/img/) sono **condivise** tra le lingue e restano nella root
- Il testo (.md) e i file generati (XML, stat block) vanno sotto `<lang>/`
- I meta-documenti (README, PlanBook, AdventureBook, DM_Prep, ecc.) restano nella root — non sono multilingua
- I nomi propri di NPC/luoghi **non si traducono**
- Le label degli stat block usano i file i18n in `tech/i18n/<lang>.json`
- I file tradotti hanno un disclaimer in cima: `> ⚠️ Auto-translated from Italian.`

Le release (PDF + ZIP) non stanno nell'avventura ma in:
```
releases/
└── NomeAvventura/
    └── NomeAvventura_YYYYMMDD.pdf
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

#### Tipi di immagine e directory

| Tipo | Directory | Contenuto | Esempio |
|------|-----------|-----------|---------|
| **Mappe** (pianta dall'alto, griglia) | `maps/` e `NN_Modulo/maps/` | PNG/JPG per Roll20 o stampa | `maps/CasaArimano.png` |
| **Illustrazioni** (prospettiva, atmosfera) | `img/scenes/` e `NN_Modulo/img/scenes/` | Handout per giocatori, scene evocative | `img/scenes/SalaDaPranzoArimano.png` |
| **Personaggi** (ritratti NPC/PG) | `characters/img/` | Ritratti, artwork personaggi | `characters/img/ErBraccio.png` |
| **Oggetti** (item narrativi) | `objects/` | Immagini di oggetti specifici | `objects/DoppiaS.png` |
| **Cover** | `img/` (root) | Solo la copertina dell'avventura | `img/LAnelloDelConte_COVER.png` |

La directory determina il tipo — non serve prefisso nel nome file.

#### Naming

| elemento | convenzione | esempio |
|----------|-------------|---------|
| Immagini avventure | PascalCase | `FianusRomanus.png`, `SirGorimVel.png` |
| Copertina | `NomeAvventura_COVER.png` in `img/` | `LAnelloDelConte_COVER.png` |
| Versioni lowres | suffisso `-lowres` | `FianusRomanus-lowres.jpg` |
| Stat block generati | stesso prefisso del sorgente | `NPC_SirGorimVel.pdf`, `NPC_SirGorimVel.png` |
| XML FightClub generati | stesso prefisso del sorgente | `NPC_SirGorimVel.xml` |
| Prompt generazione immagine | stesso nome base + `.gemidesc` | `SirGorimVel.gemidesc` |

### File `.gemidesc` (opzionali)

Prompt testuali per la generazione di immagini con AI (Gemini, DALL-E, Midjourney). Ogni file contiene un singolo prompt in inglese, pronto per essere copiato nel tool di generazione.

**Struttura:** testo libero su una riga (o più righe), in inglese. Descrive il soggetto, l'aspetto, l'abbigliamento, la posa, lo sfondo e lo stile desiderato.

**Naming:** stesso nome base dell'immagine da generare, con estensione `.gemidesc`. Quando l'immagine viene generata, si salva con lo stesso nome ma `.png`.

**Posizione:** nella stessa directory dove andrà l'immagine finale (`characters/img/`, `img/`, `maps/`).

**Esempio:**

```
characters/img/
├── SirGorimVel.png        ← immagine generata
├── SirGorimVel.gemidesc   ← prompt usato per generarla
├── Korex.gemidesc         ← prompt (immagine non ancora generata)
```

I file `.gemidesc` non vengono inclusi nel PDF né nello ZIP di pubblicazione. Servono come documentazione del prompt usato, per poter rigenerare o iterare sull'immagine.

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
- **Preferire SVG** quando si scaricano mappe da internet: il formato vettoriale permette di modificare facilmente le scritte (nomi, etichette) senza rigenerare l'intera immagine. Per modificare: aprire con Inkscape (`inkscape file.svg`), selezionare il testo, cancellare e riscrivere, poi esportare PNG (`inkscape file.svg --export-type=png --export-filename=file.png --export-dpi=150`).

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

**Regola di non-duplicazione:** le informazioni a valenza generale — meccaniche trasversali, tabelle di riferimento, elenco NPC con ruoli e relazioni, elenco luoghi, lore del mondo — vanno scritte **solo** nel documento principale. I moduli non le ripetono: rimandano al documento principale con un riferimento esplicito (es. `→ vedi FuoriDaHellfire.md § "Appendice: Cheat Sheet Anello del Virtuoso"`). Nei moduli va solo il contenuto specifico di quel modulo.

**Regola contenuto vs pianificazione:** il documento principale contiene **decisioni prese** — la versione definitiva di plot, meccaniche, NPC. Non contiene varianti, linee di sviluppo alternative, idee da esplorare o agganci futuri speculativi. Quel materiale va nel **PlanBook** dell'avventura.

**Regola file committati:** vanno committati solo i file sorgente (non rigenerabili). I file generati dagli script (stat block PNG/PDF/HTML, XML FightClub, compendium) **non vanno committati** — sono rigenerabili con `generate-statblocks.py`. Eccezione: la directory `public/` contiene il "compilato" pubblicato e va committata. I sorgenti delle stat block sono i file `.md` in `characters/markdown/`.

Sezioni obbligatorie:
```
## Lore
## Introduzione
## NPC principali
## Luoghi
## Struttura dell'avventura
```

**Regola NPC principali:** ogni NPC nell'elenco deve indicare il modulo in cui compare per la prima volta nel titolo (es. `### Nome NPC (modulo N)`). Il corpo segue questo formato:

```markdown
### Nome NPC (modulo N)

Descrizione breve (1-2 righe): razza, ruolo, aspetto distintivo.

- **Dove:** dove si trova di solito o dove i PG lo incontrano.
- **Ruolo:** funzione nell'avventura (alleato, antagonista, quest giver, companion...).
- **Cosa sa:** informazioni che possiede, rilevanti per la trama.
- **Come si comporta:** personalità, tic, atteggiamento verso i PG.
- **Frase:** (opzionale) battuta ricorrente o frase d'apertura.

→ Scheda: NPC_NomePersonaggio
```

**Regola riferimenti a file:** nel testo dei moduli e del documento principale, non citare path di file (non hanno senso nel PDF). Citare per nome: "→ Scheda: NPC_NomePersonaggio" (senza `.md`, senza path). Il lettore sa che le schede sono in `characters/markdown/`. Nessun path deve comparire nel PDF pubblicato.

Sezioni consigliate (non obbligatorie):
```
## Plot generale
## Consigli al master
```

### Moduli (`NN_NomeModulo/NomeModulo.md`)
Un file per ogni quest, dungeon o luogo significativo.

**Convenzione directory:** `NN_` con numero progressivo (01_, 02_, ...). Le directory `XX*_` (es. `XX3_IlFinaleDiStagione/`) sono bozze di moduli futuri non ancora numerati — escluse dai check di normalizzazione.

**Titolo:** `# Puntata N: NomeModulo` — ogni modulo ha un numero progressivo nel titolo. La numerazione è un riferimento, non un ordine obbligatorio di gioco (i moduli possono essere giocati in ordine diverso a discrezione del DM).

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

### DM Prep (`DM_Prep.md`)

Documento di riferimento rapido per il DM durante la sessione. Uno per modulo, nella directory del modulo (`NN_NomeModulo/DM_Prep.md`). Contiene solo informazioni operative — niente prosa, niente testo da leggere ai giocatori.

**Sezioni obbligatorie:**

```
## Passaggi della storia
## Stat block
## Tiri chiave
## Mappe
```

**Sezioni opzionali:**

```
## Loot
## Milestone
```

**Regole di contenuto:**

- **Passaggi della storia**: lista numerata, una riga per passaggio. Solo cosa succede, non come descriverlo.
- **Stat block**: tutti i nemici e NPC rilevanti del modulo. Ogni stat block deve essere autocontenuto (non rimandare ad altri file). Include i companion del party con PF/CA/attacco.
- **Tiri chiave**: tabella con luogo, tipo di tiro, CD, effetto.
- **Mappe**: ASCII art compatte dei luoghi del modulo.

**Regole di formato:**

- Gli stat block non devono essere interrotti da cambio pagina nel PDF.
- Le tabelle non devono essere spezzate tra pagine.

**Generazione PDF:**

```bash
pandoc adventures/<Avventura>/it/NN_NomeModulo/DM_Prep.md \
  --pdf-engine=weasyprint \
  --metadata title="DM Prep — Modulo N" \
  --css tech/create-pdf-adventure/dm-prep.css \
  -o releases/<Avventura>/DM_Prep_NN_NomeModulo.pdf
```

Il CSS `tech/create-pdf-adventure/dm-prep.css` impedisce il page-break dentro stat block e tabelle.

### Schede PNG (`NPC_NomePersonaggio.md`)
- **Antagonisti principali**: scheda completa con stat block
- **PNG secondari**: scheda semplificata con stat essenziali

**Regola mostri generici:** i mostri generici (senza nome proprio né particolarità homebrew — es. Skeleton, Giant Rat, Swarm of Rats) **non vanno nel PDF pubblicato**. Le loro stat block vanno comunque create, ma in una directory comune a tutte le avventure (`adventures/data/monsters/`), non nella singola avventura. I moduli li referenziano con il nome e la pagina del Monster Manual. Se serve una versione modificata (es. "Ratto Corrotto" con Pack Tactics), quella è homebrew e va nell'avventura come `MON_NomeCreatura.md`.

**Procedura:**
1. Prima di creare uno stat block, verificare se esiste già in `adventures/data/monsters/`
2. Se esiste: referenziare. Se non esiste: creare lì.
3. Solo i mostri con nome/particolarità homebrew vanno in `adventures/<Avventura>/<lang>/characters/markdown/`

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
