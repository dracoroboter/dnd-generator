# Piano di sviluppo — create-pdf-adventure

**Stato**: v1 completata — primo PDF generato (FuoriDaHellfire, 20260419)
**Scopo**: generare un singolo PDF con tutta l'avventura, grafica D&D-style, stat block in appendice
**Primo caso d'uso**: `FuoriDaHellfire`

---

## Problema

`release.sh` produce N file PDF separati (uno per ogni `.md`) dentro uno ZIP. Per masterare serve un **documento unico** con ordine di lettura, grafica decente, e stat block in appendice.

## Versioning

Formato: `yyyymmdd`. Il file si chiama:
```
FuoriDaHellfire_20260419.pdf
```
Se servisse più granularità: `yyyymmdd_HHmm`. Per ora non serve.

## Composizione del PDF

Ordine di assemblaggio per un'avventura standard:

| # | Sorgente | Sezione nel PDF |
|---|----------|----------------|
| 1 | `img/*_COVER.png` | **Copertina** — immagine a pagina intera |
| 2 | (generata) | **Frontespizio** — titolo, livello, sistema, versione |
| 3 | `<Avventura>.md` | **Documento principale** — lore, plot, NPC, struttura, consigli |
| 4 | `01_*/modulo.md` | **Modulo 1** |
| 5 | `01_*/maps/MappaDM.md` | Scheda mappa modulo 1 |
| 6 | `02_*/modulo.md` | **Modulo 2** |
| 7 | `02_*/maps/MappaDM.md` | Scheda mappa modulo 2 |
| … | (altri moduli) | … |
| N | `characters/statblock/NPC_*.png` | **Appendice — Stat Block** |

### File esclusi dal PDF

| File | Motivo |
|------|--------|
| `README.md` | Meta-file del progetto |
| `AdventureBook.md` | Istruzioni per l'AI |
| `PlanBook.md` | Todo list di sviluppo dell'avventura |
| `DiscussioneNarrativa.md` | Todo list narrativa (file di lavoro, non contenuto giocabile) |
| `maps/MappaGenerale.md` | Contenuto già presente nei MappaDM |
| `characters/markdown/NPC_*.md` | Ridondanti con stat block PNG |

> **TODO naming convention**: servono prefissi o convenzioni per distinguere file di lavoro (Plan*, Todo*, Discussione*) da file di contenuto effettivo. Vedi `plan-meta-dnd.md` sezione "Naming convention documentazione".

## Copertina

L'immagine di copertina è in `adventures/<Avventura>/img/<Avventura>_COVER.png`.
Lo script la usa come prima pagina a immagine intera. Se non esiste, genera un frontespizio tipografico.

Per FuoriDaHellfire: `adventures/FuoriDaHellfire/img/FuoriDaHellfire_COVER.png` ✅ esiste.

## Grafica

CSS custom applicato al PDF:

- Font serif (Libre Baskerville o simile)
- Intestazioni con colore ruggine/pergamena
- Blockquote (testo read-aloud) con sfondo pergamena e bordo laterale
- Tabelle con stile pulito
- Page break tra moduli
- Frontespizio tipografico dopo la copertina

## Stat block in appendice

Gli stat block PNG già generati dalla pipeline FightClub (`characters/statblock/NPC_*.png`) vengono inclusi come immagini nell'appendice.

### NPC senza stat block PNG

Jason Accordion ha solo il markdown, niente stat block grafico. **Soluzione**: creare la scheda markdown temporanea nel formato standard (`NPCFormat.md`) e generare lo stat block PNG con la pipeline esistente prima di creare il PDF.

Pipeline per generare stat block mancanti:
```
characters/markdown/NPC_JasonAccordion.md
    → md-to-fightclub.py → characters/fightclub/NPC_JasonAccordion.xml
    → md-to-statblock-pdf.js → characters/statblock/NPC_JasonAccordion.png
```

Il formato markdown NPC è documentato in `tech/rules/NPCFormat.md`. Sezioni obbligatorie: Informazioni generali, Descrizione, Motivazioni, Note al master. Sezioni meccaniche per export: Stat Block (tabella 6 abilità + campi PF/CA/velocità/etc.), Attacchi (sottosezioni `###` con Attacco/Danni/Effetto).

## Pipeline

```
create-pdf-adventure.py <NomeAvventura>
    │
    ├── legge adventures/<NomeAvventura>/
    ├── usa img/*_COVER.png come copertina
    ├── assembla markdown in ordine (moduli, mappe DM)
    ├── genera frontespizio HTML
    ├── include stat block PNG come appendice
    ├── applica adventure.css
    │
    └── HTML → PDF (weasyprint)
            │
            └── releases/<NomeAvventura>/<NomeAvventura>_yyyymmdd.pdf
```

## Tool e dipendenze

| Tool | Stato | Uso |
|------|-------|-----|
| `pandoc` | ✅ installato | Markdown → HTML |
| `weasyprint` | ✅ installato via `apt install weasyprint` | HTML → PDF (CSS migliore di wkhtmltopdf) |
| `wkhtmltopdf` | ✅ installato | Fallback se weasyprint ha problemi |
| `md-to-fightclub.py` | ✅ esistente | Genera XML FightClub da markdown NPC |
| `md-to-statblock-pdf.js` | ✅ esistente | Genera stat block PDF/PNG da XML (`-o file.png`) |

## Directory output

```
releases/<NomeAvventura>/<NomeAvventura>_yyyymmdd.pdf
```

Coerente con `release.sh`. La directory `releases/` è già in `.gitignore`.

## Fasi di implementazione

| Fase | Cosa | Output | Stato |
|------|------|--------|-------|
| 0 | ~~Verificare weasyprint~~ | ✅ weasyprint 61.1 via apt | ✅ Fatto |
| 1 | ~~CSS custom per PDF D&D-style~~ | ✅ `tech/create-pdf-adventure/adventure.css` | ✅ Fatto |
| 2 | ~~Creare stat block mancante (Jason Accordion)~~ | ✅ PNG generato | ✅ Fatto |
| 3 | ~~Script `create-pdf-adventure.py`~~ | ✅ Script funzionante | ✅ Fatto |
| 4 | ~~Test con FuoriDaHellfire~~ | ✅ `FuoriDaHellfire_20260419.pdf` (2.1 MB) | ✅ Fatto |
| 5 | Generalizzare per qualsiasi avventura | Supporto struttura standard | Da fare |

## Punti aperti

1. **Naming convention file di lavoro vs contenuto** — da definire a livello di progetto (vedi `plan-meta-dnd.md`). Impatta quali file lo script include/esclude automaticamente. Non bloccante per la prima versione (la lista di esclusione è hardcoded).
2. **Ordine stat block in appendice** — per ordine di apparizione: Korex → Fin Ditasvelte → Jason Accordion. ✅ Deciso.
3. **Supporto mappe PNG nei moduli** — lo script include solo `MappaDM.md` (testo), non le mappe grafiche PNG/SVG nelle directory `maps/`. Da aggiungere: includere immagini da `NN_*/maps/` e `maps/` dopo il contenuto del modulo corrispondente.

## Relazione con release.sh

`create-pdf-adventure.py` **non sostituisce** `release.sh`. Sono complementari:
- `create-pdf-adventure.py` → PDF unico per masterare
- `release.sh` → ZIP con PDF separati + mappe + artwork per distribuzione

In futuro `release.sh` potrebbe chiamare `create-pdf-adventure.py` per includere il PDF unico nello ZIP.
