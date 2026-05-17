# Publish Adventure - Pubblica l'ultima versione di un'avventura

Genera gli asset di un'avventura (IT + EN) e li copia nella cartella `public/` per la pubblicazione.

Usa questa skill quando l'utente dice "pubblica X", "pubblica l'ultima versione di X", "metti in public X", o varianti simili.

## Release vs Pubblicazione

- **Release** (`releases/`): generazione dei PDF e asset. I file in `releases/` sono in `.gitignore` - sono artefatti di lavoro, non tracciati da git.
- **Pubblicazione** (`public/`): copia dei file finali in `public/`, che e tracciata da git. E il passo che rende i file disponibili nel repository. Dopo la pubblicazione, l'utente deve committare.

## Cosa va in public/ (default)

| Tipo | Formato | Note |
|------|---------|------|
| PDF avventura | `.pdf` (lowres, solo cover come immagine) | Generato con `--only cover,frontmatter,doc,statblocks --lowres` |
| Mappe | `.zip` (tutte le mappe PNG/JPG) | ZIP unico per avventura |
| Stat block | `.zip` (tutti i PNG stat block) | ZIP unico per avventura |
| Compendium | `.xml` (non zippato) | FightClub XML |

Il PDF completo con tutte le mappe incluse e una possibilita (flag `--full`), non il default.

## Come usarla

- "pubblica LoScettroDityr" - pubblicazione standard (PDF testo + ZIP mappe + ZIP stat block + compendium)
- "pubblica LoScettroDityr --full" - PDF completo con mappe e stat block inclusi nel PDF

## Procedura per una singola avventura

Per ogni lingua presente nel `manifest.json` (tipicamente `it` e `en`):

1. Esegui `python3 tech/fightclub/generate-statblocks.py <NomeAvventura> [--lang <lang>]` per rigenerare stat block (XML + PDF + PNG + Compendium)
2. Esegui `python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> --lowres --only cover,frontmatter,doc,statblocks [--lang <lang>]`

Dopo aver generato per tutte le lingue:

3. Rimuovi da `public/` le vecchie versioni: `rm -f public/<NomeAvventura>_*`
4. Copia i PDF in `public/`:
   - `<NomeAvventura>_YYYYMMDD_lowres_it.pdf` (IT)
   - `<NomeAvventura>_YYYYMMDD_lowres_en.pdf` (EN)
5. Crea ZIP mappe:
   - `cd adventures/<NomeAvventura>/maps && zip -j /path/public/<NomeAvventura>_Maps.zip *.png *.jpg 2>/dev/null`
6. Crea ZIP stat block:
   - `cd adventures/<NomeAvventura>/<lang>/characters/statblock && zip -j /path/public/<NomeAvventura>_Statblocks_it.zip *.png`
   - `cd adventures/<NomeAvventura>/<lang>/characters/statblock && zip -j /path/public/<NomeAvventura>_Statblocks_en.zip *.png` (per EN)
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
- Gli stat block vanno come ZIP separato (per stampa singola)
- Il compendium XML va non zippato (per import diretto in FightClub/Game Master 5e)
- Le lingue disponibili si leggono dal `manifest.json` dell'avventura
- Dopo la pubblicazione, suggerire all'utente di committare i cambiamenti in `public/`

---

# Rilascia Modulo - Genera PDF stampabile di un singolo modulo

Genera un PDF con un singolo modulo di un'avventura, le sue mappe e gli stat block. A differenza della pubblicazione (che genera il PDF completo e lo mette in `public/`), il rilascio modulo e per uso personale/stampa e resta in `releases/`.

## Come usarla

Chiedi a Kiro: "rilascia modulo 3 di FuoriDaHellfire", "stampa modulo 2", "rilascia modulo X"

## Procedura

1. Esegui `python3 tech/fightclub/generate-statblocks.py <NomeAvventura>` per rigenerare stat block
2. Esegui `python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> --only <NN>,maps,statblocks`
3. Mostra il path del PDF generato e la dimensione

## Output

`releases/<NomeAvventura>/<NomeAvventura>_YYYYMMDD_only-<NN>_maps_statblocks.pdf`

## Note

- Il file resta in `releases/` (non va in `public/`, non e tracciato da git)
- Include tutte le mappe dell'avventura e tutti gli stat block, non solo quelli del modulo specifico
- Per avere solo gli stat block rilevanti al modulo, usare `--only <NN>,statblocks` (senza maps)
