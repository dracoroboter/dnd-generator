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

Riferimento: `tech/how-to/how-to-encounter-difficulty.md`

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

### Separazione stat block dal testo dell'avventura

Gli stat block completi dei personaggi **non vanno inseriti nel corpo dei moduli**. Devono risiedere esclusivamente nelle schede dedicate in `characters/markdown/` (formato: `NPC_Nome.md`, `MON_Nome.md`).

Quando un NPC o mostro compare nel testo di un modulo, riferirsi a lui per **nome** con una breve descrizione inline delle caratteristiche essenziali, seguita dal rimando alla scheda:

```markdown
I PG affrontano **Alaric il Giusto** (umano, mago corrotto, CA 15, PF 90 —
stat block completo: vedi `characters/markdown/NPC_SirAlaric.md`).
```

Nelle tabelle nemici dei moduli, indicare i dati minimi per il combattimento (nome, n., PF, CA, attacco principale, note) e rimandare alla scheda per il dettaglio:

```markdown
| nome | n. | PF | CA | attacco | note |
|------|-----|----|----|---------|------|
| Alaric il Giusto | 1 | 90 | 15 | vedi scheda | `NPC_SirAlaric.md` |
```

**Razionale**: i moduli devono essere leggibili e scorrevoli al tavolo. Gli stat block completi interrompono il flusso narrativo e sono difficili da consultare nel mezzo di una descrizione. Tenerli separati permette anche di stamparli come schede singole e di generare stat block grafici (PDF/PNG) con la pipeline FightClub.

### Contenuto delle schede NPC

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

## Milestone

Le avventure di questo progetto usano il sistema **milestone** per l'avanzamento di livello (non XP). La milestone è un dato strutturale opzionale del modulo — non tutti i moduli ne hanno una.

### Regole

- Una milestone è triggerata da un **evento narrativo specifico** (es. "trovare la lettera di Sergius e consegnarla a Gorim") o dal **completamento di un certo numero di obiettivi** (es. "completati almeno 3 dei 5 obiettivi secondari").
- Il trigger deve essere un momento **identificabile in gioco**, non generico ("completare il modulo" non è un buon trigger — "sconfiggere il boss" o "consegnare l'artefatto" sì).
- Una milestone può **non essere conseguita** in una sessione: se i PG non raggiungono il trigger, non avanzano.
- In una campagna multi-sessione, le milestone scandiscono il ritmo della progressione. Non è necessario che ogni modulo ne abbia una.

### Formato nel modulo

```markdown
## Milestone

**Livello raggiunto:** X
**Trigger:** [evento o condizione]
```

Per la posizione e il formato strutturale, vedere `tech/rules/adventure-template.md`.

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
