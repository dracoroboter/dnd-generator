# Dungeon & Dragon

**Versione**: 0.2
**Ultimo aggiornamento**: 2026-04-18
**Repository**: [github.com/dracoroboter/dnd-generator](https://github.com/dracoroboter/dnd-generator)

Raccolta di avventure D&D 5e (2014) con toolchain di automazione dedicata.
Uso personale, con intenzione di pubblicare su GitHub (CC BY-SA 4.0) quando la qualità lo giustifica.

---

## I due piani del progetto

Questo repository vive su due piani paralleli che si alimentano a vicenda.

### Piano umanistico — scrivere avventure

Scrivere, strutturare e rilasciare avventure D&D in italiano. Il prodotto finale è un PDF leggibile e una ZIP condivisibile. Il lavoro è narrativo: trama, NPC, incontri, mappe, descrizioni.

### Piano tecnico — costruire strumenti

Costruire gli strumenti che rendono il piano umanistico più efficiente: generatori di dungeon, pipeline di rendering mappe, linguaggi intermedi per descrivere l'arredamento delle stanze, script di validazione e pubblicazione.

Entrambi i piani sono assistiti da AI.

---

## Avventure in corso

| Avventura | Tipo | Stato | Note |
|-----------|------|-------|------|
| `AvventuraDiProva` | One-shot (3 moduli) | Normalizzata | Riferimento per la struttura corretta |
| `LAnelloDelConte` | Saga puntata 1 | Normalizzata | Prima avventura completa |
| `FuoriDaHellfire` | One-shot (2 moduli) | In corso | Continuazione "Ballad of the Rat King" (Hellfire Club starter set), lv3→4 |
| `IlReSpezzato` | Saga puntata 2 | Da migrare | Draft in `legacy/` formato `.odt` |
| `LoScettroDityr` | Saga puntate 3–6 (A/B/C/D) | Da migrare | In `legacy/` formato `.odt` |

La saga "Lo Scettro di Tyr" copre `LAnelloDelConte` → `IlReSpezzato` → `LoScettroDityr` in sequenza narrativa.

---

## Sottoprogetti tecnici in corso

### 1. Generatore dungeon procedurale

Genera mappe dungeon in PNG + JSON con algoritmo BSP (Binaray Space Partition) e cell-grid.

**Script attivi:** `generate-dungeon.py` (versione corrente), versioni archiviate `*-0.x.py`
**Piano:** `tech/rules/PlanMaps.md`
**Documenti:** `tech/rules/Maps.md`, `tech/rules/MapsPipelineDocs.md`

### 2. Pipeline di rendering SVG

Converte il JSON del dungeon in SVG con stili visivi diversi. Supporta un layer di enrichment (oggetti, gate).

**Script attivi:** `json-to-svg-oldschool.py`, `json-to-svg-blueprint.py`, `json-to-svg-kenney.py`, `json-to-svg-iso.py`, `json-to-svg-stone.py` — condividono `dungeon_svg_core.py`

### 3. Linguaggi intermedi DDL / RTL ← *lavoro in corso*

Sistema a due livelli per descrivere l'arredamento di un dungeon già generato senza scrivere coordinate a mano.

```
testo naturale  →  .ddl (DungeonDressLang)  →  dungeon_enrichment.json  →  SVG
template .rtl   →  .json (via rtl-to-json.py)  ↗
```

- **RTL (RoomTemplateLang):** definisce archetipi di stanza (camera da letto, cappella…). File `.rtl` compilati in `.json` da `rtl-to-json.py`.
- **DDL (DungeonDressLang):** descrive l'arredamento di un dungeon specifico. File `.ddl` compilati in `dungeon_enrichment.json` da `ddl-to-enrichment.py`.

**Piano e decisioni architetturali:** `tech/rules/PlanIntermediateRepresentation.md`
**Specifiche:** `tech/rules/RTL-spec.md`, `tech/rules/DDL-spec.md`
**Template stanze disponibili:** `bedroom`, `chapel` — `demonic_shrine`, `treasury` da creare

---

## Struttura del repository

```
dungeonandragon/
├── README.md                    # questo file
├── meta-dnd.md                  # regole generali del progetto (lingua, naming, struttura)
├── plan-meta-dnd.md             # todo list operativa
│
├── adventures/                  # avventure
│   ├── AdventureTemplate/       # scaffold vuoto (usato da new-adventure.sh)
│   ├── AvventuraDiProva/        # riferimento normalizzato
│   └── LAnelloDelConte/         # saga puntata 1
│
├── legacy/                      # .odt originali — sola lettura
│
├── releases/                    # PDF + ZIP generati (non editare)
│
└── tech/
    ├── scripts/                 # tutti gli script (vedi indice sotto)
    ├── rules/                   # specifiche e piani (vedi indice sotto)
    ├── how-to/                  # guide procedurali passo-passo
    ├── templates/               # template JSON per oggetti e stanze
    │   ├── objects/             # definizioni oggetto (bed, chest, altar…)
    │   ├── rooms/               # template stanze RTL (.rtl) e compilati (.json)
    │   └── gates/               # plugin rendering gate per stile SVG
    ├── assets/                  # asset grafici (tileset DCSS)
    └── reports/                 # output generati da script (non editare)
```

---

## Indice documentazione

### Regole generali del progetto

| File | Scopo |
|------|-------|
| `meta-dnd.md` | Visione, struttura directory, naming convention, regole generali — fonte di verità del progetto |
| `plan-meta-dnd.md` | Todo list operativa derivata da meta-dnd.md — stato avanzamento in tempo reale |

### Struttura avventure

| File | Scopo |
|------|-------|
| `tech/rules/AdventureTemplate.md` | Specifica completa della struttura di un'avventura: file obbligatori, convenzioni, esempi |
| `tech/rules/ContentRules.md` | Standard di contenuto: come dichiarare difficoltà incontri, linee guida NPC, formato modulare |
| `tech/rules/Glossary.md` | Definizioni dei termini usati nel progetto (one-shot, campagna, saga, modulo, sessione, puntata) |
| `tech/rules/Normalization.md` | Manuale per normalizzare avventure legacy al formato standard |

### Mappe e generazione dungeon

| File | Scopo | Relazione |
|------|-------|-----------|
| `tech/rules/Maps.md` | Documentazione degli script per mappe Watabou (browser automation) | Usa `generate-watabou-*.js` |
| `tech/rules/PlanMaps.md` | Piano di sviluppo del generatore dungeon custom: criteri qualità, gap aperti, iterazioni | Governa `generate-dungeon.py` e i renderer SVG |
| `tech/rules/MapsPipelineDocs.md` | Documentazione tecnica della pipeline mappe: formato JSON dungeon_base, formato enrichment, convention renderer | Riferimento per chi estende la pipeline |
| `tech/rules/DungeonIterationWorkflow.md` | Processo iterativo AI+DM per migliorare il generatore: critica oggettiva, verifica coerenza PNG/MD/JSON | Processo, non specifica |

### Linguaggi intermedi DDL / RTL

| File | Scopo | Relazione |
|------|-------|-----------|
| `tech/rules/PlanIntermediateRepresentation.md` | Decisioni architetturali DDL/RTL, limiti attuali del motore, sequenza di implementazione — documento vivente | Fonte di verità per l'intero sottoprogetto |
| `tech/rules/RTL-spec.md` | Specifica sintattica di RoomTemplateLang: grammatica, notazione, posizioni disponibili, esempi | Compila con `rtl-to-json.py` |
| `tech/rules/DDL-spec.md` | Specifica sintattica di DungeonDressLang v0.3: struttura a blocchi, direttive `is a` / `has` / `door to` | Compila con `ddl-to-enrichment.py` |

### Guide procedurali

| File | Scopo |
|------|-------|
| `tech/how-to/HowToNewAdventure.md` | Creare una nuova avventura da zero con `new-adventure.sh` e `adventure-wizard.py` |
| `tech/how-to/HowToNewNPC.md` | Creare NPC: script `new-npc.py`, workflow AI, formato stat block, export FightClub/PDF |
| `tech/how-to/HowToRelease.md` | Generare PDF + ZIP con `release.sh` e pubblicare |
| `tech/how-to/HowToEncounterDifficulty.md` | Calcolare difficoltà incontri con `encounter-difficulty.py` |
| `tech/how-to/HowToClaudeCode.md` | Usare un AI coding agent in questo progetto: configurazione, separazione ruoli narrativa vs tecnica |

---

## Indice script

### Gestione avventure

| Script | Linguaggio | Scopo |
|--------|-----------|-------|
| `new-adventure.sh` | Bash | Scaffolding nuova avventura da `AdventureTemplate/` |
| `adventure-wizard.py` | Python | Wizard interattivo per impostare/aggiornare metadati README di un'avventura |
| `check-adventure.py` | Python | Valida struttura e genera report in `tech/reports/` |
| `release.sh` | Bash | Genera PDF (via pandoc + wkhtmltopdf) e ZIP in `releases/<NomeAvventura>/` |
| `new-npc.py` | Python | Crea scheda NPC interattivamente |
| `encounter-difficulty.py` | Python | Calcola difficoltà incontro D&D 5e (XP soglia, CR multipli) |
| `setup.sh` | Bash | Installa dipendenze (pandoc, wkhtmltopdf, zip, python3, Node.js, Playwright) |
| `backup.sh` | Bash | Backup del progetto (esclude `legacy/`) |

### Generazione dungeon

| Script | Linguaggio | Scopo |
|--------|-----------|-------|
| `generate-dungeon.py` | Python | Generatore dungeon procedurale (cell-grid) → PNG + JSON + MD |
| `generate-dungeon-bsp-0.1.py` | Python | Versione archiviata BSP — solo riferimento |
| `generate-dungeon-cell-grid-0.2.py` | Python | Versione archiviata cell-grid 0.2 — solo riferimento |
| `generate-dungeon-cell-grid-0.3.py` | Python | Versione archiviata cell-grid 0.3 — solo riferimento |
| `generate-watabou-dungeon.js` | Node.js | Genera una mappa dungeon via browser Watabou (Playwright) |
| `generate-watabou-dungeon-batch.js` | Node.js | Genera N mappe Watabou con seed diversi |
| `generate-watabou-maps.js` | Node.js | Genera mappe city/world via altri generatori Watabou |

### Rendering SVG

| Script | Linguaggio | Scopo |
|--------|-----------|-------|
| `dungeon_svg_core.py` | Python | Modulo condiviso: carica JSON, ricostruisce griglia, espone `get_passages()` |
| `json-to-svg-oldschool.py` | Python | Stile oldschool (tratteggio muri, icone hand-drawn) — stile principale |
| `json-to-svg-blueprint.py` | Python | Stile blueprint (sfondo blu, linee bianche) |
| `json-to-svg-kenney.py` | Python | Stile tileset Kenney |
| `json-to-svg-iso.py` | Python | Stile isometrico |
| `json-to-svg-stone.py` | Python | Stile pietra/texture |
| `json-to-svg.py` | Python | Renderer generico (legacy) |
| `json-to-tmx.py` | Python | Esporta in formato TMX (Tiled Map Editor) |

### Pipeline DDL / RTL ← *in sviluppo*

| Script | Linguaggio | Scopo |
|--------|-----------|-------|
| `rtl-to-json.py` | Python | Compila file `.rtl` (RoomTemplateLang) in `.json` template stanza |
| `template-apply.py` | Python | Motore di placement: applica un template JSON a una stanza specifica |
| `ddl-to-enrichment.py` | Python | Compila file `.ddl` (DungeonDressLang) in `dungeon_enrichment.json` |

### Script di test / debug

| Script | Linguaggio | Scopo |
|--------|-----------|-------|
| `corridor-test.py` | Python | Test generazione corridoi |
| `door-test.py` | Python | Test rendering porte |
| `test-object-bed.py` | Python | Test placement oggetto bed |
| `test-object-pentacle.py` | Python | Test placement oggetto pentacle |
| `test-object-table.py` | Python | Test placement oggetto table |

---

## Flusso tipico — piano umanistico

```
1. new-adventure.sh NomeAvventura     # scaffolding
2. adventure-wizard.py NomeAvventura  # metadati README
3. (scrittura contenuto in Markdown)
4. check-adventure.py NomeAvventura   # validazione
5. release.sh NomeAvventura v1.0      # PDF + ZIP
```

## Flusso tipico — pipeline mappe

```
1. generate-dungeon.py --seed 42 --rooms 10 --output map.png
   → produce map.png, map.json, map.md

2. rtl-to-json.py tech/templates/rooms/chapel.rtl
   → produce chapel.json

3. (scrivere avventura.ddl)

4. ddl-to-enrichment.py avventura.ddl --dungeon map.json --output enrichment.json

5. json-to-svg-oldschool.py map.json --enrichment enrichment.json --output map.svg
```

---

## Fonti e ringraziamenti

| progetto | autore | licenza | uso nel progetto |
|----------|--------|---------|-----------------|
| [FightClub5eXML](https://github.com/kinkofer/FightClub5eXML) | kinkofer + community | MIT | Compendium XML di tutte le fonti D&D 5e ufficiali per FightClub/Game Master 5e. Include schema XSD e script di merge. Riferimento per il formato XML dei nostri NPC homebrew. |
| [statblock5e](https://github.com/Valloric/statblock5e) | Valloric | Apache-2.0 | Web Component HTML/CSS per stat block nella grafica WotC. Template per l'export PDF/PNG. |
| [tetra-cube.com](https://tetra-cube.com/dnd/dnd-statblock) | Tetra-cube | — | Generatore web di stat block basato su statblock5e. Riferimento per il formato. |

Il file `tech/data/compendium/Sources/SystemReferenceDocument/all-srd.xml` contiene l'SRD 5.1 in formato FightClub XML, rilasciato da Wizards of the Coast sotto [Creative Commons Attribution 4.0 International (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/). Lo schema `tech/data/compendium/compendium.xsd` è parte del repo kinkofer (MIT).

---

## Licenze

| contenuto | licenza |
|-----------|---------|
| Script e software (`tech/scripts/`) | [GNU General Public License v2 (GPLv2)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) |
| Avventure, how-to e documentazione | [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/) |

---

## Autore

In rete sono **dracoroboter** da più tempo di quanto vorrei ammettere. Gioco a Dungeons & Dragons da quasi altrettanto.

Per contatti: `dracoroboter(at)gmail.com` — nell'improbabile caso qualcuno scriva, aggiungete `[dnd-generator]` nell'oggetto così riesco a distinguervi dallo spam.
