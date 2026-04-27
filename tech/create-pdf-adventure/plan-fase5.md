# Piano Fase 5 — Generalizzazione create-pdf-adventure.py

**Stato**: in corso
**Obiettivo**: lo script deve funzionare con qualsiasi avventura normalizzata, non solo FuoriDaHellfire
**Primo test**: `LAnelloDelConte`

---

## Analisi delle differenze strutturali

| Aspetto | FuoriDaHellfire | LAnelloDelConte |
|---------|----------------|-----------------|
| Mappe root `maps/` | Solo `MappaGenerale.md` | `MappaGenerale.md` + SVG/PNG (RealmOfAmrog, FianusRomanus) |
| Mappe moduli `NN_*/maps/` | Solo `MappaDM.md` (testo) | Solo PNG (LeFogneDiFianus.png, LeFogneDiFianusAlt.png), niente MappaDM.md |
| Stat block naming | Tutti `NPC_*.png` | Mix: `NPC_*.png` + `*_GM.png` (Barbara_GM, Maria_Biscanna_GM) |
| Stat block ordine | Hardcoded (Korex→Fin→Jason) | Nessun ordine definito |
| Moduli | 2 (01_, 02_) | 1 (01_) |

---

## Decisioni prese

### D1. Versione canonica vs versione di lavoro

Il file con il **nome canonico** (es. `LeFogneDiFianus.png`) è la versione buona (grafica) → inclusa nel PDF.
Le versioni di lavoro, schematiche o draft vanno nella directory `other/` → escluse dal PDF e dal check.

Esempio:
- `01_LeFogneDiFianus/maps/LeFogneDiFianus.png` ← versione bella (rinominata da `Alt`)
- `01_LeFogneDiFianus/maps/other/LeFogneDiFianus_draft.png` ← versione schematica

### D2. PNG preferito su SVG

Se esistono sia PNG che SVG della stessa mappa, il **PNG va nel PDF** (più affidabile per stampa).
L'SVG va in `other/` come sorgente/backup.

Esempio:
- `maps/FianusRomanus.png` ← nel PDF
- `maps/other/FianusRomanus.svg` ← sorgente, esclusa

### D3. Naming: mappa descrittiva = mappa grafica

La descrizione markdown di una mappa ha lo **stesso nome** della mappa grafica corrispondente.

| Mappa grafica | Mappa descrittiva |
|---------------|-------------------|
| `FianusRomanus.png` | `FianusRomanus.md` |
| `RealmOfAmrog.png` | `RealmOfAmrog.md` |

Questo sostituisce il vecchio `MappaGenerale.md` (che descriveva tutte le mappe in un unico file).

### D4. Mappe markdown = schede DM con nome specifico

Le mappe `.md` sono **schede DM**: combinano mappa testuale e descrizione con informazioni segrete. Si usano quando la mappa grafica è assente o insufficiente.

Il nome generico `MappaDM.md` è deprecato. Ogni mappa `.md` ha un **nome specifico PascalCase**.

| Vecchio | Nuovo |
|---------|-------|
| `01_DiscesaNelleFogne/maps/MappaDM.md` | `01_DiscesaNelleFogne/maps/DiscesaNelleFogne.md` |
| `02_TanaDiKorex/maps/MappaDM.md` | `02_TanaDiKorex/maps/TanaDiKorex.md` |

### D5. Stat block nel PDF: solo NPC e mostri

Solo `NPC_*.png` e `MON_*.png` in `characters/statblock/` vengono inclusi nel PDF.

I file `*_GM.png` (stat block PG) non sono contenuto dell'avventura → vanno in `other/pg/`.
Ordinamento: alfabetico (rimuove l'ordine hardcoded di FuoriDaHellfire).

### D6. Directory `other/` organizzata per tipo

```
other/
├── pg/          ← stat block PG (*_GM.png/pdf/html, fightclub xml)
└── maps/        ← mappe draft, SVG sorgente, versioni di lavoro
```

La directory `other/` è a livello di avventura (root). Le `other/` dentro `maps/` dei moduli sono per le mappe di lavoro di quel modulo specifico.

### D7. Directory strutturali in inglese

I nomi delle directory strutturali devono essere in inglese. Due directory vanno rinominate ovunque:

| Attuale (italiano) | Nuovo (inglese) |
|---|---|
| `maps/` | `maps/` |
| `characters/` | `characters/` |

Le sottodirectory di `characters/` sono già in inglese (`markdown/`, `img/`, `fightclub/`, `statblock/`).

Impatto: tutte le avventure, il template, tutti gli script, tutta la documentazione, e i riferimenti inline nei testi delle avventure (es. `maps/LeFogneDiFianus.png` → `maps/LeFogneDiFianus.png`).

---

## Riepilogo regole per lo script

### Cosa include nel PDF

| Sorgente | Inclusione | Posizione nel PDF |
|----------|-----------|-------------------|
| `maps/*.png` | ✅ | Dopo documento principale, prima dei moduli |
| `maps/*.md` (con PNG corrispondente) | ✅ | Prima dell'immagine corrispondente |
| `maps/*.md` (senza PNG) | ✅ | Scheda DM testuale, stessa posizione |
| `NN_*/maps/*.png` | ✅ | Dopo il contenuto del modulo |
| `NN_*/maps/*.md` | ✅ | Prima dell'immagine corrispondente (o da sola se no PNG) |
| `characters/statblock/NPC_*.png` | ✅ | Appendice stat block |
| `characters/statblock/MON_*.png` | ✅ | Appendice stat block |
| `maps/other/*` | ❌ | — |
| `NN_*/maps/other/*` | ❌ | — |
| `other/*` | ❌ | — |
| `characters/statblock/*_GM.*` | ❌ | — |
| `maps/MappaGenerale.md` | ❌ | Deprecato |
| `MappaDM.md` | ❌ | Deprecato (rinominato con nome specifico) |

### Struttura PDF risultante

```
1. Copertina (img/*_COVER.png)
2. Frontespizio
3. Documento principale (NomeAvventura.md)
4. Mappe generali (maps/*.md + *.png, una per pagina)
5. Per ogni modulo NN_*:
   a. Contenuto modulo (NomeModulo.md)
   b. Mappe del modulo (maps/*.md + *.png)
6. Appendice — Stat Block (NPC_*.png + MON_*.png, alfabetico)
```

---

## Task di normalizzazione file

### Tutte le avventure + template — Rename directory (D7)

| # | Operazione | Avventure impattate |
|---|-----------|---------------------|
| N0a | Rinominare `maps/` → `maps/` | LAnelloDelConte, FuoriDaHellfire, AdventureTemplate (root + ogni modulo) |
| N0b | Rinominare `characters/` → `characters/` | LAnelloDelConte, FuoriDaHellfire, AdventureTemplate |
| N0c | Aggiornare riferimenti nei testi `.md` | Tutti i file che referenziano `maps/` o `characters/` (avventure, moduli, docs, script) |

### LAnelloDelConte

| # | Operazione | Da | A |
|---|-----------|-----|---|
| N1 | Spostare in other | `01_*/maps/LeFogneDiFianus.png` (schematica) | `01_*/maps/other/LeFogneDiFianus_draft.png` |
| N2 | Rinominare | `01_*/maps/LeFogneDiFianusAlt.png` | `01_*/maps/LeFogneDiFianus.png` |
| N3 | Spostare in other | `maps/FianusRomanus.svg` | `maps/other/FianusRomanus.svg` |
| N4 | Spostare in other | `maps/RealmOfAmrog.svg` | `maps/other/RealmOfAmrog.svg` |
| N5 | Splittare | `maps/MappaGenerale.md` | `maps/FianusRomanus.md` + `maps/RealmOfAmrog.md` |
| N6 | Spostare in other | `characters/statblock/Barbara_GM.*` | `other/pg/Barbara_GM.*` |
| N7 | Spostare in other | `characters/statblock/Maria_Biscanna_GM.*` | `other/pg/Maria_Biscanna_GM.*` |
| N8 | Spostare in other | `characters/fightclub/Barbara GM.xml` | `other/pg/Barbara_GM.xml` |
| N9 | Spostare in other | `characters/fightclub/Maria Biscanna GM.xml` | `other/pg/Maria_Biscanna_GM.xml` |

### FuoriDaHellfire

| # | Operazione | Da | A |
|---|-----------|-----|---|
| N10 | Rinominare | `01_*/maps/MappaDM.md` | `01_*/maps/DiscesaNelleFogne.md` |
| N11 | Rinominare | `02_*/maps/MappaDM.md` | `02_*/maps/TanaDiKorex.md` |

---

## Aggiornamento regole di normalizzazione

### `tech/rules/adventure-template.md` — modifiche

1. **Struttura directory**: aggiungere `other/` con sottodirectory per tipo
2. **Mappe**: documentare la convenzione nome mappa `.md` = nome mappa `.png`
3. **Deprecare** `MappaGenerale.md` come file obbligatorio → sostituire con "un `.md` per ogni mappa grafica"
4. **Deprecare** `MappaDM.md` → nome specifico PascalCase
5. **Stat block**: esplicitare che solo `NPC_*` e `MON_*` sono contenuto dell'avventura

### `tech/rules/normalization.md` — modifiche

1. **Fase 3 (mapping)**: aggiornare tabella con regole mappe (nome specifico, SVG in other, draft in other)
2. **Fase 4 (rinomina)**: aggiungere regola `MappaDM.md` → nome specifico
3. Aggiungere nota su `other/` e cosa ci va

### `tech/scripts/check-adventure.py` — modifiche

1. **Deprecare check `MappaGenerale.md`**: non più obbligatorio. Warning se presente (suggerire split).
2. **Deprecare check `MappaDM.md`**: warning se trovato (suggerire rinomina con nome specifico).
3. **Check mappe**: per ogni `.png` in `maps/`, verificare che esista un `.md` corrispondente (warning se manca).
4. **Check SVG duplicati**: warning se esiste `.svg` accanto a `.png` con lo stesso nome (suggerire spostamento in `other/`).
5. **Check stat block naming**: warning se in `characters/statblock/` ci sono file che non matchano `NPC_*` o `MON_*`.
6. **Check file orfani**: segnalare file in posizioni inattese o con naming non riconosciuto (es. `*_GM.*` in statblock, `*Alt.*` in mappe). Messaggio: "File non riconosciuto — verificare se va spostato in other/ o rinominato".
7. **Check `other/`**: non validare il contenuto di `other/` (è una zona libera), ma segnalare se `other/` non esiste e ci sono file candidati allo spostamento.

---

## Sequenza di lavoro

| # | Task | Tipo | Dipendenze |
|---|------|------|------------|
| 1 | ✅ Analisi differenze strutturali | Analisi | — |
| 2 | ✅ Decisioni normalizzazione mappe (D1–D7) | Design | — |
| 3 | Aggiornare `adventure-template.md` con nuove regole | Docs | D1–D7 |
| 4 | Aggiornare `normalization.md` con nuove regole | Docs | D1–D7 |
| 5 | Rename directory `maps/` → `maps/`, `characters/` → `characters/` (tutte le avventure + template) | File ops | 3, 4 |
| 6 | Aggiornare riferimenti `maps/` e `characters/` in tutti i file .md e script | File ops | 5 |
| 7 | Eseguire normalizzazione file LAnelloDelConte (N1–N9) | File ops | 5 |
| 8 | Eseguire normalizzazione file FuoriDaHellfire (N10–N11) | File ops | 5 |
| 9 | Aggiornare `check-adventure.py` con nuovi check e nuovi path | Code | 5, 6 |
| 10 | Verificare check su LAnelloDelConte e FuoriDaHellfire | Test | 7, 8, 9 |
| 11 | Modificare `create-pdf-adventure.py`: nuovi path + inclusione mappe moduli | Code | 7, 8 |
| 12 | Modificare `create-pdf-adventure.py`: inclusione mappe generali | Code | 11 |
| 13 | Modificare `create-pdf-adventure.py`: generalizzare stat block | Code | 11 |
| 14 | Aggiungere CSS `.map-page` | Code | 11 |
| 15 | Testare PDF con LAnelloDelConte | Test | 11–14 |
| 16 | Verificare non-regression PDF con FuoriDaHellfire | Test | 15 |
| 17 | Aggiornare `docs-create-pdf-adventure.md` | Docs | 16 |
| 18 | Aggiornare `plan-create-pdf-adventure.md` (fase 5 completata) | Docs | 17 |
