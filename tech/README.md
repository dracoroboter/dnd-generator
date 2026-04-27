# tech/ — Documentazione e Strumenti

Indice di tutta la documentazione tecnica del progetto `dungeonandragon`.

> **Mappe e generazione dungeon** → tutta la toolchain mappe (generatore, renderer SVG, DDL/RTL, template, asset) è nel repository separato **[dnd-maps](https://github.com/dracoroboter/dnd-maps)**.

---

## How-To — Guide procedurali

| File | Descrizione |
|------|-------------|
| [`how-to/how-to-new-adventure.md`](how-to/how-to-new-adventure.md) | Creare una nuova avventura: scaffolding, wizard metadati, moduli, NPC, verifica, release |
| [`how-to/how-to-new-npc.md`](how-to/how-to-new-npc.md) | Creare NPC: script `new-npc.py`, workflow AI, formato stat block, export FightClub/PDF |
| [`how-to/how-to-release.md`](how-to/how-to-release.md) | Generare una release PDF + ZIP con `release.sh` |
| [`how-to/how-to-encounter-difficulty.md`](how-to/how-to-encounter-difficulty.md) | Calcolare la difficoltà di un incontro con `encounter-difficulty.py` (sistema XP DMG 2014) |
| [`how-to/how-to-git-profiles.md`](how-to/how-to-git-profiles.md) | Separare profili git (account A / account B) sulla stessa macchina |
| [`how-to/how-to-claude-code.md`](how-to/how-to-claude-code.md) | Usare un AI coding agent in questo progetto: configurazione, separazione ruoli |
| [`how-to/how-to-aws-profile-switch.md`](how-to/how-to-aws-profile-switch.md) | Switch profilo AI CLI (hobby vs aziendale) |

---

## Rules — Specifiche e convenzioni

| File | Descrizione |
|------|-------------|
| [`rules/adventure-template.md`](rules/adventure-template.md) | Specifica struttura avventura, convenzioni di naming (fonte di verità), file obbligatori |
| [`rules/content-rules.md`](rules/content-rules.md) | Regole di contenuto: difficoltà incontri, NPC, struttura narrativa, loot, milestone |
| [`rules/glossary.md`](rules/glossary.md) | Definizioni: avventura, one-shot, campagna, saga, modulo, sessione, quest, puntata |
| [`rules/normalization.md`](rules/normalization.md) | Guida alla migrazione di avventure legacy (da `.odt` a Markdown normalizzato) |
| [`rules/npc-format.md`](rules/npc-format.md) | Specifica formato markdown per NPC/mostri: sezioni, naming, prefissi, pipeline |
| [`rules/git-workflow.md`](rules/git-workflow.md) | Convenzioni git: commit message, branch, push, credential helper |

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
| `scripts/encounter-builder.py` | `python3 tech/scripts/encounter-builder.py --party 4 3 --difficulty hard` | Costruisce incontri bilanciati da database SRD |
| `scripts/new-npc.py` | `python3 tech/scripts/new-npc.py <Nome>` | Crea scheda NPC (wizard o template) |
| `scripts/backup.sh` | `bash tech/scripts/backup.sh` | Backup del progetto (escluso `legacy/`) |

---

## FightClub / Stat Block

| File | Descrizione |
|------|-------------|
| [`fightclub/README.md`](fightclub/README.md) | Formato XML FightClub 5e: struttura tag, esempi, pipeline |

Script: `fightclub/md-to-fightclub.py`, `fightclub/fightclub-to-md.py`, `fightclub/md-to-statblock-pdf.js`, `fightclub/generate-statblocks.py`

---

## Create PDF Adventure

| File | Descrizione |
|------|-------------|
| [`create-pdf-adventure/docs-create-pdf-adventure.md`](create-pdf-adventure/docs-create-pdf-adventure.md) | Documentazione operativa del generatore PDF |

Script: `create-pdf-adventure/create-pdf-adventure.py`, `create-pdf-adventure/optimize-images.py`

---

## Data

| Directory | Contenuto |
|-----------|-----------|
| `data/compendium/` | Schema XSD + SRD 5.1 in formato FightClub XML |
| `data/srd_5e_monsters.json` | Database 327 mostri SRD 5.1 per `encounter-builder.py` |

---

## Reports

Output generato automaticamente da `check-adventure.py`. Non modificare manualmente.
