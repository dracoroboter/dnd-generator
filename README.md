# Dungeon & Dragon

**Versione**: 0.3
**Ultimo aggiornamento**: 2026-04-27
**Repository**: [github.com/dracoroboter/dnd-generator](https://github.com/dracoroboter/dnd-generator)

Raccolta di avventure D&D 5e (2014) con toolchain di automazione dedicata.
Uso personale, con intenzione di pubblicare su GitHub (CC BY-SA 4.0) quando la qualità lo giustifica.

---

## I due piani del progetto

Questo repository vive su due piani paralleli che si alimentano a vicenda.

### Piano umanistico — scrivere avventure

Scrivere, strutturare e rilasciare avventure D&D in italiano. Il prodotto finale è un PDF leggibile e una ZIP condivisibile. Il lavoro è narrativo: trama, NPC, incontri, mappe, descrizioni.

### Piano tecnico — costruire strumenti

Costruire gli strumenti che rendono il piano umanistico più efficiente: script di validazione e pubblicazione, pipeline NPC/stat block. La toolchain mappe (generatore dungeon, renderer SVG, linguaggi DDL/RTL) è nel repository separato **[dnd-maps](https://github.com/dracoroboter/dnd-maps)**.

Entrambi i piani sono assistiti da AI.

---

## Avventure in corso

| Avventura | Tipo | Stato | Note |
|-----------|------|-------|------|
| `LAnelloDelConte` | Saga puntata 1 | Normalizzata | Prima avventura completa |
| `FuoriDaHellfire` | One-shot (2 moduli) | Normalizzata | Continuazione "Ballad of the Rat King" (Hellfire Club starter set), lv3→4. PDF generato. |
| `IlReSpezzato` | Saga puntata 2 | Da migrare | Draft in `legacy/` formato `.odt` |
| `LoScettroDityr` | Saga (4 moduli A/B/C/D) | Normalizzata | Versione "Draco" — 4 moduli, 15 NPC, 29 asset grafici |

La saga "Lo Scettro di Tyr" copre `LAnelloDelConte` → `IlReSpezzato` → `LoScettroDityr` in sequenza narrativa.

---

## Sottoprogetti tecnici in corso

### Mappe e generazione dungeon → repository separato

Tutta la toolchain mappe (generatore procedurale, renderer SVG, linguaggi DDL/RTL, formato v2, script Watabou) è stata spostata nel repository dedicato:

**→ [dnd-maps](https://github.com/dracoroboter/dnd-maps)**

Include: generatore dungeon, 6 renderer SVG, pipeline DDL/RTL per arredamento, renderer v2 per mappe scritte a mano, automazione Watabou, template oggetti/stanze/gate, documentazione completa.

### Pipeline FightClub / Stat Block

Converte schede NPC markdown in XML FightClub 5e e genera stat block in PDF/PNG.

```
NPC_*.md  →  md-to-fightclub.py  →  .xml (FightClub)
NPC_*.md  →  md-to-statblock-pdf.js  →  .pdf / .png (stat block grafico)
.xml      →  fightclub-to-md.py  →  NPC_*.md (import da FightClub/Game Master 5e)

# Pipeline completa (wrapper):
generate-statblocks.py <Avventura>  →  .xml + .pdf + .png per tutti gli NPC/MON
```

**Script:** `tech/fightclub/md-to-fightclub.py`, `tech/fightclub/fightclub-to-md.py`, `tech/fightclub/md-to-statblock-pdf.js`
**Documentazione:** `tech/fightclub/README.md`

### Generatore PDF avventure

Genera un singolo PDF con tutta l'avventura: copertina, moduli, schede mappa DM, stat block in appendice. Grafica D&D-style via CSS custom + weasyprint.

```
create-pdf-adventure.py LAnelloDelConte            →  releases/LAnelloDelConte/LAnelloDelConte_20260422.pdf
create-pdf-adventure.py LAnelloDelConte --lowres    →  releases/LAnelloDelConte/LAnelloDelConte_20260422_lowres.pdf
optimize-images.py LAnelloDelConte                  →  genera versioni -lowres.jpg delle immagini
```

**Script:** `tech/create-pdf-adventure/create-pdf-adventure.py`, `tech/create-pdf-adventure/optimize-images.py`
**Documentazione:** `tech/create-pdf-adventure/docs-create-pdf-adventure.md`

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
│   ├── LAnelloDelConte/         # saga puntata 1
│   ├── FuoriDaHellfire/         # continuazione Hellfire Club starter set
│   └── LoScettroDityr/          # saga 4 moduli (versione "Draco")
│
├── legacy/                      # .odt originali — sola lettura
│
├── releases/                    # PDF + ZIP generati (non editare, in .gitignore)
│
├── public/                      # PDF pubblicati (tracciata da git)
│
└── tech/
    ├── scripts/                 # script gestione avventure (vedi indice sotto)
    ├── rules/                   # specifiche e piani (vedi indice sotto)
    ├── how-to/                  # guide procedurali passo-passo
    ├── fightclub/               # tool export FightClub 5e (XML, stat block PDF/PNG)
    ├── create-pdf-adventure/    # generatore PDF unico per avventure (CSS + script)
    ├── data/
    │   └── compendium/          # schema XSD + SRD 5.1 in formato FightClub XML
    └── reports/                 # output generati da script (non editare)
```

> **Nota:** tutta la toolchain mappe (generatore, renderer SVG, DDL/RTL, template, asset) è nel repository separato **[dnd-maps](https://github.com/dracoroboter/dnd-maps)**.

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
| `tech/rules/adventure-template.md` | Specifica completa della struttura di un'avventura: file obbligatori, convenzioni, esempi |
| `tech/rules/content-rules.md` | Standard di contenuto: come dichiarare difficoltà incontri, linee guida NPC, formato modulare |
| `tech/rules/glossary.md` | Definizioni dei termini usati nel progetto (one-shot, campagna, saga, modulo, sessione, puntata) |
| `tech/rules/normalization.md` | Manuale per normalizzare avventure legacy al formato standard |

### Mappe e generazione dungeon

| File | Scopo |
|------|-------|
| → **[dnd-maps](https://github.com/dracoroboter/dnd-maps)** | Tutta la documentazione mappe è nel repository separato |

### Guide procedurali

| File | Scopo |
|------|-------|
| `tech/how-to/how-to-new-adventure.md` | Creare una nuova avventura da zero con `new-adventure.sh` e `adventure-wizard.py` |
| `tech/how-to/how-to-new-npc.md` | Creare NPC: script `new-npc.py`, workflow AI, formato stat block, export FightClub/PDF |
| `tech/how-to/how-to-release.md` | Generare PDF + ZIP con `release.sh` e pubblicare |
| `tech/how-to/how-to-encounter-difficulty.md` | Calcolare difficoltà incontri con `encounter-difficulty.py` |
| `tech/how-to/how-to-git-profiles.md` | Separare profili git (account A / account B) sulla stessa macchina |
| `tech/how-to/how-to-claude-code.md` | Usare un AI coding agent in questo progetto: configurazione, separazione ruoli narrativa vs tecnica |
| `tech/how-to/how-to-aws-profile-switch.md` | Switch profilo AI CLI (hobby vs aziendale) |

### NPC e FightClub

| File | Scopo |
|------|-------|
| `tech/rules/npc-format.md` | Specifica formato markdown per NPC/mostri: sezioni, naming, prefissi, pipeline |
| `tech/fightclub/README.md` | Formato XML FightClub 5e: struttura tag, esempi, fonti, piano implementazione |

### Git e workflow

| File | Scopo |
|------|-------|
| `tech/rules/git-workflow.md` | Convenzioni git: commit message, branch, push, credential helper |

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
| `encounter-builder.py` | Python | Costruisce incontri bilanciati |
| `setup.sh` | Bash | Installa dipendenze (pandoc, wkhtmltopdf, zip, python3, Node.js, Playwright) |
| `backup.sh` | Bash | Backup del progetto (esclude `legacy/`) |

### Generazione dungeon

| Script | Linguaggio | Scopo |
|--------|-----------|-------|
| → **[dnd-maps](https://github.com/dracoroboter/dnd-maps)** | | Tutti gli script mappe sono nel repository separato |

### FightClub / Stat Block

| Script | Linguaggio | Scopo |
|--------|-----------|-------|
| `md-to-fightclub.py` | Python | Converte NPC markdown → XML FightClub 5e |
| `fightclub-to-md.py` | Python | Converte XML FightClub → NPC markdown |
| `md-to-statblock-pdf.js` | Node.js | Genera stat block PDF/PNG via Playwright + statblock5e |
| `generate-statblocks.py` | Python | Pipeline completa: .md → .xml + .pdf + .png (wrapper) |

---

## Flusso tipico — piano umanistico

```
1. new-adventure.sh NomeAvventura     # scaffolding
2. adventure-wizard.py NomeAvventura  # metadati README
3. (scrittura contenuto in Markdown)
4. check-adventure.py NomeAvventura   # validazione
5. release.sh NomeAvventura v1.0      # PDF + ZIP
```

→ Vedi **[dnd-maps](https://github.com/dracoroboter/dnd-maps)** per la pipeline mappe.

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
