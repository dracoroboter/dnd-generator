# Publish Adventure - Pubblica l'ultima versione di un'avventura

Genera gli asset di un'avventura (IT + EN) e li copia nella cartella `public/` per la pubblicazione.

Usa questa skill quando l'utente dice "pubblica X", "pubblica l'ultima versione di X", "metti in public X", o varianti simili.

## Release vs Pubblicazione

- **Release** (`releases/`): generazione dei PDF e asset. I file in `releases/` sono in `.gitignore` - sono artefatti di lavoro, non tracciati da git.
- **Pubblicazione** (`public/`): copia dei file finali in `public/`, che e tracciata da git. E il passo che rende i file disponibili nel repository. Dopo la pubblicazione, l'utente deve committare.

## Cosa va in public/ (default)

| Tipo | Formato | Note |
|------|---------|------|
| PDF avventura | `.pdf` (lowres, solo cover come immagine) | Generato con `--lowres` (senza `--only`, include tutto tranne mappe) oppure `--only cover,frontmatter,doc,01,02,...` |
| Mappe | `.zip` (versioni lowres JPG) | ZIP unico per avventura, suffisso `_lowres` |
| Stat block | `.pdf` (tutti gli stat block PNG in un unico PDF) | PDF unico per avventura |
| Compendium | `.xml` (non zippato) | FightClub XML |

Il PDF completo con tutte le mappe incluse e una possibilita (flag `--full`), non il default.

## Regole immagini lowres

- Le immagini `-lowres.jpg/png` sono generate da `optimize-images.py` e **non vanno committate** (sono in `.gitignore`)
- Le lowres delle mappe vanno in `maps/lowres/` (directory separata dagli originali PNG)
- Lo ZIP mappe in `public/` contiene **solo le versioni lowres** (suffisso `_Maps_lowres.zip`)
- Per pubblicare le mappe full-size (PNG originali), usare il flag `--full-maps` → `_Maps.zip` (senza suffisso lowres)

## Come usarla

- "pubblica LoScettroDityr" - pubblicazione standard (PDF testo + ZIP mappe + ZIP stat block + compendium)
- "pubblica LoScettroDityr --full" - PDF completo con mappe e stat block inclusi nel PDF

## Procedura per una singola avventura

Per ogni lingua presente nel `manifest.json` (tipicamente `it` e `en`):

1. Esegui `python3 tech/fightclub/generate-statblocks.py <NomeAvventura> [--lang <lang>]` per rigenerare stat block (XML + PDF + PNG + Compendium)
2. Esegui `python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> --lowres --only cover,frontmatter,doc,01,02,03,04 [--lang <lang>]`

Dopo aver generato per tutte le lingue:

3. Rimuovi da `public/` le vecchie versioni: `rm -f public/<NomeAvventura>_*`
4. Copia i PDF in `public/`:
   - `<NomeAvventura>_YYYYMMDD_lowres_it.pdf` (IT)
   - `<NomeAvventura>_YYYYMMDD_lowres_en.pdf` (EN)
5. Genera lowres mappe (se non esistono già):
   - `python3 tech/create-pdf-adventure/optimize-images.py <NomeAvventura>`
   - Sposta le lowres delle mappe in `maps/lowres/`: `mkdir -p adventures/<NomeAvventura>/maps/lowres && mv adventures/<NomeAvventura>/maps/*-lowres.jpg adventures/<NomeAvventura>/maps/lowres/`
6. Crea ZIP mappe (lowres):
   - `zip -j public/<NomeAvventura>_Maps_lowres.zip adventures/<NomeAvventura>/maps/lowres/*-lowres.jpg`
   - Per full-size (su richiesta `--full-maps`): `zip -j public/<NomeAvventura>_Maps.zip adventures/<NomeAvventura>/maps/*.png`
6. Genera PDF stat block:
   - `python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> --lowres --only statblocks [--lang <lang>]`
   - Copia in `public/<NomeAvventura>_Statblocks_it.pdf` (e `_en.pdf` per EN)
7. Copia compendium XML:
   - `<NomeAvventura>_Compendium_it.xml` (IT)
   - `<NomeAvventura>_Compendium_en.xml` (EN)
8. Mostra il riepilogo: nome file, dimensione, data

## Procedura per "pubblica tutte"

Ripeti la procedura sopra per ogni avventura normalizzata:

- FuoriDaHellfire
- LAnelloDelConte
- LoScettroDityr

## Note

- La directory di lavoro deve essere `~/dungeonandragon`
- I file in `public/` sono tracciati da git
- Per default il PDF contiene solo testo + cover + stat block (no mappe nel PDF)
- Le mappe vanno come ZIP separato (per uso diretto in Roll20/VTT)
- Gli stat block vanno come PDF separato (per stampa)
- Il compendium XML va non zippato (per import diretto in FightClub/Game Master 5e)
- Le lingue disponibili si leggono dal `manifest.json` dell'avventura
- Dopo la pubblicazione, suggerire all'utente di committare i cambiamenti in `public/`

---

# Rilascia Modulo - Genera PDF di un singolo modulo per la sessione

Genera un PDF con il documento principale dell'avventura (contesto, NPC, plot) e un singolo modulo. Per uso personale/sessione, resta in `releases/`.

## Come usarla

Chiedi a Kiro: "rilascia modulo 3 di FuoriDaHellfire", "stampa modulo 2", "rilascia modulo X"

## Procedura

1. Esegui `python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> --only doc,<NN>`
2. Mostra il path del PDF generato e la dimensione

## Output

`releases/<NomeAvventura>/<NomeAvventura>_YYYYMMDD_only-<NN>_doc.pdf`

## Note

- Il file resta in `releases/` (non va in `public/`, non e tracciato da git)
- Contiene il documento principale (informazioni di contesto: plot, NPC, lore) + il modulo richiesto
- NON include mappe né stat block (quelli si consultano su Roll20 / FightClub separatamente)
