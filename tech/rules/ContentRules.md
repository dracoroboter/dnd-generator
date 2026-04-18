# ContentRules — Regole di Contenuto per le Avventure

Regole e convenzioni per il contenuto delle avventure D&D 5e del progetto.
Complementa le convenzioni strutturali in `adventures/AdventureTemplate/AdventureBook.md`.

---

## Difficoltà dell'avventura

Ogni avventura deve dichiarare nel `README.md`:

```
*Sistema: D&D 5e (2014) — Livello consigliato: X — Durata: one-shot / X sessioni*
```

E nel documento principale (`NomeAvventura.md`), nella sezione `## Consigli al master`:

```
**Difficoltà consigliata:** X PG di livello Y
**Difficoltà incontri:** Easy / Medium / Hard / Deadly (vedi singoli moduli)
**Scalabilità:** note su come adattare se il party è diverso
```

---

## Difficoltà degli incontri

Ogni modulo con combattimento deve includere nella sezione `## Nemici` la difficoltà calcolata:

```markdown
## Nemici

**Difficoltà incontro:** HARD (4 PG lv3) — calcolata con `encounter-difficulty.py`

| nome | numero | PF | CA | attacco | note |
...
```

Per calcolare la difficoltà:
```bash
python3 tech/scripts/encounter-difficulty.py -p <N> <LVL> -m <N> <CR> [...]
```

Riferimento: `tech/how-to/HowToEncounterDifficulty.md`

### Nota sul sistema CR/XP

Il sistema DMG è oggettivo ma impreciso. Affiancare sempre una nota narrativa se la difficoltà effettiva si discosta da quella calcolata (es. boss progettato per fuggire, incontro evitabile con roleplay, ecc.).

---

## Scalabilità degli incontri

Se l'avventura è progettata per un party specifico, documentare come scalare per party diversi. Formato suggerito nella sezione `## Note al master` del modulo:

```markdown
**Scalabilità:**
- Party più piccolo (2-3 PG): rimuovere X nemici comuni
- Party più grande (5-6 PG): aggiungere X nemici comuni o aumentare PF del boss di Y
- Party di livello superiore: aumentare CR dei nemici principali di 1-2
```

---

## PNG — Linee guida contenuto

Ogni PNG deve avere (indipendentemente dal tipo di scheda):
- **Motivazione chiara**: cosa vuole, perché agisce così
- **Segreto o informazione nascosta** (opzionale ma consigliato)
- **Tratto distintivo**: un dettaglio fisico o comportamentale memorabile

### Antagonisti principali
- Scheda completa con stat block (vedi template)
- Non devono esistere solo per essere sconfitti — hanno un piano proprio
- Documentare il comportamento in combattimento (tattiche, condizioni di fuga/resa)

### PNG secondari
- Scheda semplificata
- Almeno un PNG ambiguo per avventura (né alleato né nemico chiaro)

---

## Struttura narrativa

Ogni avventura deve avere almeno:
- **Un incontro di combattimento**
- **Un incontro di esplorazione**
- **Un incontro di roleplay**

Prevedere sempre almeno una soluzione alternativa al combattimento per ogni scontro principale.

---

## Loot e ricompense

- Ogni modulo dichiara le ricompense nella sezione `## Ricompense`
- L'oro deve essere coerente con il livello del party (DMG tabelle loot)
- Oggetti magici personalizzati devono avere un costo o rischio associato
- La ricompensa principale dell'avventura va dichiarata nel documento principale

---

## Testo da leggere ai giocatori

Usare blockquote per il testo da leggere ad alta voce:

```markdown
> Davanti a voi si apre una sala buia. L'aria odora di muffa e pietra bagnata.
> Al centro, una figura incappucciata vi volta le spalle.
```

---

## Distanze e unità di misura

Le distanze vanno espresse in formato triplo: **metri / feet / qd** (quadretti).

| qd | ft | m |
|----|----|---|
| 1 | 5ft | 1,5m |
| 2 | 10ft | 3m |
| 4 | 20ft | 6m |
| 6 | 30ft | 9m |
| 8 | 40ft | 12m |
| 12 | 60ft | 18m |
| 24 | 120ft | 36m |

**qd** = quadretto (square) — l'unità base delle battle map D&D (5ft × 5ft / 1,5m × 1,5m).

Esempio: `12m / 40ft / 8qd`

---

## Foreshadowing e agganci futuri

Se l'avventura è parte di una campagna o lascia agganci aperti, documentarli in una sezione dedicata nel documento principale o nel `PlanBook.md`:

```markdown
## Agganci futuri
- [elemento] → può essere sviluppato in [avventura futura]
```
