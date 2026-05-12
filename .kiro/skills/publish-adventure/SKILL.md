# Publish Adventure - Pubblica l'ultima versione di un'avventura

Genera i PDF lowres di un'avventura (IT + EN), il compendium XML FightClub, e li copia nella cartella `public/` per la pubblicazione.

Usa questa skill quando l'utente dice "pubblica X", "pubblica l'ultima versione di X", "metti in public X", o varianti simili.

## Release vs Pubblicazione

- **Release** (`releases/`): generazione dei PDF e asset. I file in `releases/` sono in `.gitignore` — sono artefatti di lavoro, non tracciati da git. Si generano con `create-pdf-adventure.py`. Il vecchio script `release.sh` (pandoc + ZIP) è deprecato.
- **Pubblicazione** (`public/`): copia dei file finali in `public/`, che è tracciata da git. È il passo che rende i PDF disponibili nel repository. Dopo la pubblicazione, l'utente deve committare.

Il flusso completo è: **stat block → compendium → PDF lowres → mappe → copia in public/**.

## Come usarla

Chiedi a Kiro: "pubblica LoScettroDityr" oppure "pubblica tutte le avventure"

Per pubblicare anche la versione fullres: "pubblica LoScettroDityr in alta risoluzione"

## Procedura per una singola avventura

Per ogni lingua presente nel `manifest.json` (tipicamente `it` e `en`):

1. Esegui `python3 tech/fightclub/generate-statblocks.py <NomeAvventura> [--lang <lang>]` per rigenerare stat block (XML + PDF + PNG + Compendium)
2. Esegui `python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> --lowres [--lang <lang>]`
3. Se richiesta alta risoluzione: esegui anche senza `--lowres`

Dopo aver generato per tutte le lingue:

4. Rimuovi da `public/` le vecchie versioni: `rm -f public/<NomeAvventura>_*.pdf public/<NomeAvventura>_Compendium*.xml`
5. Copia i PDF lowres (IT + EN) e i compendium XML in `public/`:
   - `<NomeAvventura>_YYYYMMDD_lowres.pdf` (IT)
   - `<NomeAvventura>_YYYYMMDD_lowres_en.pdf` (EN)
   - `<NomeAvventura>_Compendium.xml` (IT)
   - `<NomeAvventura>_Compendium_en.xml` (EN)
6. Copia le mappe PNG/JPG in `public/maps/<NomeAvventura>/` (per uso diretto in Roll20):
   - `rm -rf public/maps/<NomeAvventura>/`
   - `mkdir -p public/maps/<NomeAvventura>/`
   - Copia tutti i file `.png`, `.jpg`, `.jpeg` da `adventures/<NomeAvventura>/maps/` e da `adventures/<NomeAvventura>/*/maps/` (mappe dei moduli)
   - Se non esistono mappe, salta questo passo
7. Se richiesta alta risoluzione, copia anche i fullres
8. Mostra il riepilogo: nome file, dimensione, data

## Procedura per "pubblica tutte"

Ripeti la procedura sopra per ogni avventura presente in `adventures/` che ha contenuto (escludi `AdventureTemplate`). Le avventure attualmente normalizzate sono:

- FuoriDaHellfire
- LAnelloDelConte
- LoScettroDityr

## Note

- La directory di lavoro deve essere `~/dungeonandragon`
- I PDF in `public/` sono tracciati da git (a differenza di `releases/` che è in `.gitignore`)
- Il naming dei PDF è automatico: `<NomeAvventura>_YYYYMMDD_lowres.pdf` e `<NomeAvventura>_YYYYMMDD_lowres_en.pdf`
- Per default si pubblicano solo i PDF **lowres**. I fullres si pubblicano solo su richiesta esplicita.
- Le lingue disponibili si leggono dal `manifest.json` dell'avventura
- I compendium XML vanno copiati da `<lang>/characters/fightclub/<NomeAvventura>_Compendium.xml`
- Se l'avventura non ha immagini `-lowres`, il PDF lowres sarà simile al fullres. Per generare le versioni lowres delle immagini, eseguire prima `python3 tech/create-pdf-adventure/optimize-images.py <NomeAvventura>`
- Dopo la pubblicazione, suggerire all'utente di committare i cambiamenti in `public/`

---

# Rilascia Modulo - Genera PDF stampabile di un singolo modulo

Genera un PDF con un singolo modulo di un'avventura, le sue mappe e gli stat block. A differenza della pubblicazione (che genera il PDF completo e lo mette in `public/`), il rilascio modulo è per uso personale/stampa e resta in `releases/`.

## Come usarla

Chiedi a Kiro: "rilascia modulo 3 di FuoriDaHellfire", "stampa modulo 2", "rilascia modulo X"

## Procedura

1. Esegui `python3 tech/fightclub/generate-statblocks.py <NomeAvventura>` per rigenerare stat block
2. Esegui `python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> --only <NN>,maps,statblocks`
3. Mostra il path del PDF generato e la dimensione

## Output

`releases/<NomeAvventura>/<NomeAvventura>_YYYYMMDD_only-<NN>_maps_statblocks.pdf`

## Note

- Il file resta in `releases/` (non va in `public/`, non è tracciato da git)
- Include tutte le mappe dell'avventura e tutti gli stat block, non solo quelli del modulo specifico
- Per avere solo gli stat block rilevanti al modulo, usare `--only <NN>,statblocks` (senza maps)
