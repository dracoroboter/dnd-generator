# Normalization.md — Procedura di Normalizzazione

Guida per portare un'avventura legacy (qualsiasi formato) allo standard del progetto.
Riferimento struttura: `tech/rules/AdventureTemplate.md`
Riferimento contenuto: `tech/rules/ContentRules.md`
Riferimento termini: `tech/rules/Glossary.md`

---

## Fase 0 — Analisi del materiale legacy

Prima di toccare nulla, capire cosa c'è.

1. Aprire la directory legacy corrispondente in `legacy/CordaAvventure/`
2. Elencare tutti i file e annotare:
   - Formato (`.odt`, `.md`, `.pdf`, `.png`, ecc.)
   - Contenuto presunto (avventura principale, NPC, mappa, immagine, ecc.)
   - Quante avventure distinte contiene la directory
3. Decidere la struttura target:
   - È una one-shot, campagna o saga?
   - Quanti moduli ha?
   - È lineare o sandbox?
   - Appartiene a una saga esistente?

---

## Fase 1 — Conversione in Markdown

### Da `.odt`

```bash
pandoc input.odt -o Output.md
```

Il risultato va sempre revisionato: pandoc converte bene il testo ma può produrre formattazione spuria (asterischi, backslash, heading sbagliati). Aprire il file e fare una pulizia manuale.

Immagini incorporate nell'`.odt`: pandoc le estrae in una directory `media/` — spostarle in `mappe/` o `personaggi/` secondo il tipo.

### Da `.pdf`

Preferire sempre il `.odt` sorgente se disponibile — la conversione da PDF è molto più rumorosa. Se non c'è alternativa:

```bash
pandoc input.pdf -o Output.md
```

Aspettarsi molto rumore da rimuovere manualmente.

### File già in Markdown

Nessuna conversione necessaria — procedere direttamente alla Fase 2.

---

## Fase 2 — Creazione struttura directory

```bash
# Creare la directory dell'avventura
mkdir -p adventures/NomeAvventura/{mappe,personaggi}
mkdir -p adventures/NomeAvventura/01_NomeModulo/mappe
mkdir -p releases/NomeAvventura
```

Oppure usare `tech/scripts/new-adventure.sh` quando disponibile.

---

## Fase 3 — Mapping contenuti → file standard

Per ogni file legacy, decidere dove va nella struttura normalizzata:

| contenuto legacy | file normalizzato |
|-----------------|-------------------|
| Documento principale avventura | `NomeAvventura.md` |
| Scheda NPC | `personaggi/NPC_NomePersonaggio.md` |
| Modulo/dungeon/episodio | `NN_NomeModulo/NomeModulo.md` |
| Mappa generale | `mappe/MappaGenerale.md` + immagine |
| Mappa specifica di un modulo | `NN_NomeModulo/mappe/NomeMappa.png` |
| Artwork personaggio | `personaggi/NomePersonaggio.png` |
| Copertina | `Cover.png` |
| Note di lavoro, todo | `PlanBook.md` |
| File di versione/release | ignorare (non migrato) |
| Script legacy | ignorare (sostituito da `tech/scripts/release.sh`) |

---

## Fase 4 — Rinomina secondo le convenzioni

- File `.md`: **PascalCase** (es. `NomeFile.md`)
- Directory: **minuscolo** (es. `personaggi/`, `mappe/`)
- Moduli: prefisso numerico a due cifre (es. `01_NomeModulo/`)
- Immagini: PascalCase (es. `MappaRegione.png`)
- Copertina: `Cover.png`
- Nomi con spazi o caratteri speciali: rimuovere (es. `La fogna di Fianus.png` → `LeFogneDiFianus.png`)

---

## Fase 5 — Adeguamento sezioni

### Documento principale `NomeAvventura.md`

Sezioni obbligatorie da verificare/aggiungere:
- `## Lore`
- `## Introduzione`
- `## NPC principali`
- `## Struttura dell'avventura` (tabella con link ai moduli)

Se una sezione esiste con nome diverso, rinominarla (es. `## Intro` → `## Introduzione`, `## Ambientazione` → `## Lore`).

Se una sezione manca completamente, aggiungerla con il tag:
```markdown
## Lore

> ⚠ *Da rivedere dall'autore.*
```

### Moduli `NN_NomeModulo/NomeModulo.md`

Sezioni obbligatorie: `## Descrizione`, `## Obiettivo`, `## Ricompense`, `## Note al master`

Se mancano, aggiungerle con il tag `⚠ Da rivedere dall'autore` e un contenuto sintetico ricavato dal testo esistente.

### Schede NPC `personaggi/NPC_NomePersonaggio.md`

Sezioni obbligatorie: `## Informazioni generali`, `## Descrizione`, `## Motivazioni`, `## Note al master`

Rinominare sezioni non standard:
- `## Ruolo narrativo` → `## Informazioni generali`
- `## Personalità` → `## Descrizione`
- `## Foreshadowing` / `## Arco narrativo` → `## Agganci futuri`
- `## Statistiche` → `## Stat Block`

### README.md

Creare ex novo con:
- Titolo, sistema, livello, durata
- `**Struttura**: lineare` o `sandbox`
- Metadati saga se applicabile
- Descrizione breve senza spoiler

### AdventureBook.md

Creare ex novo con rimando a `tech/rules/AdventureTemplate.md` e note specifiche dell'avventura.

### PlanBook.md

Creare ex novo o adattare le note legacy. Includere:
- Stato del progetto (cosa è fatto, cosa manca)
- Problemi aperti
- Idee per sviluppi futuri

---

## Fase 6 — Verifica con check-adventure.py

```bash
python3 tech/scripts/check-adventure.py NomeAvventura
```

Il report viene salvato in `tech/reports/`. Iterare fino a zero errori (i warning sono accettabili).

**Criteri di normalizzazione completata:**
- Zero errori nel check
- Tutti i file obbligatori presenti
- Tutte le sezioni obbligatorie presenti (con o senza tag `⚠`)
- Naming convention rispettata

---

## Note specifiche per le avventure legacy

### LAnelloDelConte
Già normalizzata. Riferimento per casi dubbi.

### LoScettroDityr
Formato `.odt`, 4 moduli (A: FugaDaOrcastle, B: LoScettroDiTyr, C: RitornoACasa, D: LaFineNonAppartieneAiMorti). Saga "Lo Scettro di Tyr", puntate 3-6. Normalizzare un modulo alla volta.

### IlReSpezzato
Formato `.odt` + prologo a fumetti (tavole PNG). Draft incompleto. Normalizzare dopo LoScettroDityr.
