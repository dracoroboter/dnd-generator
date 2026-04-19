# create-pdf-adventure — Documentazione

Genera un singolo PDF con un'avventura D&D completa, pronta per essere masterata.

---

## Obiettivo

Produrre un documento unico che il DM tiene aperto (tablet, laptop, stampa) durante la sessione. Contiene tutto: trama, moduli, schede mappa, stat block. Niente file separati, niente ZIP, niente navigazione tra cartelle.

Non è un prodotto editoriale. È uno strumento di lavoro con una grafica abbastanza curata da non sembrare un dump di markdown.

## Cosa NON è

- Non sostituisce `release.sh` (che produce ZIP con file separati per distribuzione)
- Non è un layout da pubblicazione (Homebrewery, GMBinder, LaTeX)
- Non genera contenuto — assembla contenuto già scritto

## Uso

```bash
python3 tech/create-pdf-adventure/create-pdf-adventure.py FuoriDaHellfire
```

Output:
```
releases/FuoriDaHellfire/FuoriDaHellfire_20260419.pdf
```

## Versioning

Formato `yyyymmdd` nel nome file. Niente versioni semantiche — ogni PDF è uno snapshot della data.

## Struttura del PDF

Il PDF è composto da sezioni assemblate in ordine fisso:

### 1. Copertina

Immagine a pagina intera da `adventures/<Avventura>/img/<Avventura>_COVER.png`.
Se non esiste, la copertina viene saltata e il PDF inizia dal frontespizio.

### 2. Frontespizio

Pagina tipografica generata dallo script:
- Titolo dell'avventura (da `<Avventura>.md`, heading H1)
- Sistema: D&D 5e (2014)
- Livello, durata, struttura (dal README dell'avventura)
- Data di generazione

### 3. Documento principale

Il file `<Avventura>.md` nella root dell'avventura. Contiene lore, plot generale, NPC principali, struttura, consigli al master.

### 4. Moduli (in ordine numerico)

Per ogni directory `NN_NomeModulo/`:
- Il file `.md` principale del modulo (il contenuto giocabile)
- Il file `mappe/MappaDM.md` se presente (scheda mappa per disegno al tavolo)

I moduli sono separati da page break.

### 5. Appendice — Stat Block

Tutti i file `personaggi/statblock/NPC_*.png` inclusi come immagini, uno per pagina. Ordine di apparizione nell'avventura: Korex → Fin Ditasvelte → Jason Accordion.

Gli stat block sono già in grafica WotC (generati dalla pipeline FightClub). Non vengono ri-renderizzati.

### File esclusi

| File | Motivo |
|------|--------|
| `README.md` | Meta-file del progetto, non contenuto giocabile |
| `AdventureBook.md` | Istruzioni per l'AI |
| `PlanBook.md` | Todo list di sviluppo |
| `DiscussioneNarrativa.md` | Note di design, file di lavoro |
| `mappe/MappaGenerale.md` | Contenuto già nei MappaDM dei moduli |
| `personaggi/markdown/NPC_*.md` | Ridondanti con stat block PNG |

## Grafica

CSS custom scritto ad hoc per il progetto (`adventure.css`). Non è un template esterno.

### Scelte stilistiche

| Elemento | Stile |
|----------|-------|
| Font corpo | Serif (Libre Baskerville o sistema) |
| Font titoli | Serif bold, colore ruggine |
| Blockquote (read-aloud) | Sfondo pergamena, bordo laterale scuro |
| Tabelle | Bordi sottili, header con sfondo |
| Intestazioni H1 | Page break prima, stile capitolo |
| Intestazioni H2/H3 | Gerarchia visiva con colore e dimensione |
| Pagina | Margini generosi, numero pagina in footer |

### Perché CSS custom e non un template

- I template Homebrewery/GMBinder sono pensati per layout a due colonne stile PHB — troppo complessi per un documento di lavoro
- Il CSS è sotto il nostro controllo, modificabile, versionabile
- weasyprint supporta `@page`, margini, header/footer — sufficiente per un PDF leggibile

## Dipendenze

| Tool | Versione | Installazione | Uso |
|------|----------|---------------|-----|
| `pandoc` | qualsiasi | `apt install pandoc` | Markdown → HTML |
| `weasyprint` | qualsiasi | `apt install weasyprint` | HTML → PDF |

### Prerequisiti per gli stat block

Gli stat block PNG devono essere già generati prima di lanciare lo script. Pipeline:

```
personaggi/markdown/NPC_*.md
    → tech/fightclub/md-to-fightclub.py → personaggi/fightclub/NPC_*.xml
    → tech/fightclub/md-to-statblock-pdf.js -o *.png → personaggi/statblock/NPC_*.png
```

Lo script `create-pdf-adventure.py` non genera stat block — li include come immagini.

## Decisioni prese

| # | Decisione | Alternativa scartata | Motivo |
|---|-----------|---------------------|--------|
| D1 | weasyprint per HTML→PDF | wkhtmltopdf | CSS migliore (@page, margini, page-break affidabili) |
| D2 | CSS scritto ad hoc | Template Homebrewery/GMBinder | Troppo complessi, non servono colonne, controllo totale |
| D3 | Versioning `yyyymmdd` | Semver (1.0, 1.1) | Ogni PDF è uno snapshot, non un rilascio con breaking changes |
| D4 | Stat block come PNG in appendice | Stat block come testo markdown | I PNG sono già in grafica WotC, molto più belli del testo |
| D5 | Ordine stat block per apparizione | Ordine alfabetico | Più naturale per il DM che legge in sequenza |
| D6 | DiscussioneNarrativa esclusa | Inclusa come appendice | È un file di lavoro, non contenuto giocabile |
| D7 | Copertina da `img/*_COVER.png` | Copertina solo tipografica | L'immagine esiste, tanto vale usarla |
| D8 | Output in `releases/` | Directory dedicata | Coerente con release.sh, già in .gitignore |

## File del progetto

```
tech/create-pdf-adventure/
├── PlanCreatePdfAdventure.md      # piano di sviluppo (fasi, TODO)
├── DocsCreatePdfAdventure.md      # questo file (documentazione operativa)
├── adventure.css                  # CSS custom D&D-style
└── create-pdf-adventure.py        # script principale
```

## Output

Il PDF viene generato in `releases/<NomeAvventura>/` (in `.gitignore`).
Le versioni da pubblicare vanno copiate manualmente in `releases/public/` (tracciata da git).
