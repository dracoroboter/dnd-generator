# tech/ — Documentazione e Strumenti

Indice di tutta la documentazione tecnica del progetto `dungeonandragon`.

---

## How-To — Guide procedurali

| File | Descrizione |
|------|-------------|
| [`how-to/HowToNewAdventure.md`](how-to/HowToNewAdventure.md) | Creare una nuova avventura: scaffolding, wizard metadati, moduli, NPC, verifica, release |
| [`how-to/HowToRelease.md`](how-to/HowToRelease.md) | Generare una release PDF + ZIP con `release.sh` |
| [`how-to/HowToEncounterDifficulty.md`](how-to/HowToEncounterDifficulty.md) | Calcolare la difficoltà di un incontro con `encounter-difficulty.py` (sistema XP DMG 2014) |
| [`how-to/HowToClaudeCode.md`](how-to/HowToClaudeCode.md) | Usare Claude Code in questo progetto: modelli, comandi, cambio modello |

---

## Rules — Specifiche e convenzioni

| File | Descrizione |
|------|-------------|
| [`rules/Glossary.md`](rules/Glossary.md) | Definizioni: avventura, one-shot, campagna, saga, modulo, sessione, quest, puntata |
| [`rules/AdventureTemplate.md`](rules/AdventureTemplate.md) | Specifica completa della struttura di un'avventura (file obbligatori, sezioni, formato) |
| [`rules/ContentRules.md`](rules/ContentRules.md) | Regole di contenuto: difficoltà incontri, PNG, struttura narrativa, loot, testo da leggere |
| [`rules/Normalization.md`](rules/Normalization.md) | Guida alla migrazione di avventure legacy (da `.odt` a Markdown normalizzato) |
| [`rules/Maps.md`](rules/Maps.md) | Catalogo tool mappe: Inkarnate, DungeonFog, Watabou, DungeonScrawl — valutazioni e uso |
| [`rules/MapsPipelineDocs.md`](rules/MapsPipelineDocs.md) | Documentazione tecnica completa della pipeline mappe: script, JSON format, plugin oggetti e gate, convenzioni |
| [`rules/DungeonIterationWorkflow.md`](rules/DungeonIterationWorkflow.md) | Workflow per l'iterazione e raffinamento delle mappe dungeon |
| [`rules/PlanMaps.md`](rules/PlanMaps.md) | Roadmap sviluppo della pipeline mappe dungeon |
| [`rules/DDL-spec.md`](rules/DDL-spec.md) | Specifica DungeonDressLang (DDL) — linguaggio semi-naturale per l'enrichment dei dungeon |
| [`rules/PlanIntermediateRepresentation.md`](rules/PlanIntermediateRepresentation.md) | Piano architetturale per il livello intermedio DDL tra linguaggio naturale e JSON |

---

## Scripts — Automazione

| Script | Uso | Descrizione |
|--------|-----|-------------|
| `scripts/setup.sh` | `bash tech/scripts/setup.sh` | Installa dipendenze (pandoc, wkhtmltopdf, zip, Playwright) |
| `scripts/new-adventure.sh` | `bash tech/scripts/new-adventure.sh <Nome>` | Scaffolding nuova avventura da template |
| `scripts/adventure-wizard.py` | `python3 tech/scripts/adventure-wizard.py <Nome>` | Wizard interattivo per i metadati del README |
| `scripts/check-adventure.py` | `python3 tech/scripts/check-adventure.py <Nome>` | Valida struttura avventura, genera report in `tech/reports/` |
| `scripts/release.sh` | `./tech/scripts/release.sh <Nome> <versione>` | Genera PDF + ZIP in `releases/<Nome>/` |
| `scripts/encounter-difficulty.py` | `python3 tech/scripts/encounter-difficulty.py -p 4 5 -m 1 5` | Calcola difficoltà incontro (sistema XP DMG) |
| `scripts/new-npc.py` | `python3 tech/scripts/new-npc.py <Nome>` | Crea scheda NPC (wizard o template) |
| `scripts/generate-dungeon.py` | `python3 tech/scripts/generate-dungeon.py --seed 42 --rooms 10 --output map.png` | Genera dungeon procedurale (cell-grid BFS/MST) → `dungeon_base.json` + PNG |
| `scripts/json-to-svg-oldschool.py` | `python3 tech/scripts/json-to-svg-oldschool.py dungeon_base.json --enrichment dungeon_enrichment.json` | Renderer SVG stile old-school D&D (stile principale) |
| `scripts/json-to-svg-blueprint.py` | `python3 tech/scripts/json-to-svg-blueprint.py dungeon_base.json` | Renderer SVG stile blueprint millimetrato |
| `scripts/json-to-svg-stone.py` | `python3 tech/scripts/json-to-svg-stone.py dungeon_base.json` | Renderer SVG stile texture pietra |
| `scripts/json-to-svg-kenney.py` | `python3 tech/scripts/json-to-svg-kenney.py dungeon_base.json` | Renderer SVG stile Kenney Scribble (sperimentale) |
| `scripts/json-to-svg.py` | `python3 tech/scripts/json-to-svg.py dungeon_base.json` | Renderer SVG tileset DCSS |
| `scripts/json-to-tmx.py` | `python3 tech/scripts/json-to-tmx.py dungeon_base.json` | Export formato TMX per Tiled Map Editor |
| `scripts/generate-watabou-dungeon-batch.js` | `node tech/scripts/generate-watabou-dungeon-batch.js --count 5` | Genera mappe Watabou in batch via Playwright |

---

## Templates

| Directory | Contenuto |
|-----------|-----------|
| `templates/objects/` | JSON + plugin renderer per ogni oggetto dungeon (bed, chest, altar, column, table, fountain, demonic_pentacle...) |
| `templates/gates/` | JSON + plugin renderer per ogni tipo di gate (door, portcullis, arch, secret) |

---

## Assets

| Directory | Contenuto |
|-----------|-----------|
| `assets/tilesets/dcss/` | Tileset Dungeon Crawl Stone Soup (CC) — floor, wall e varianti |

---

## Reports

Output generato automaticamente da `check-adventure.py`. Non modificare manualmente.
