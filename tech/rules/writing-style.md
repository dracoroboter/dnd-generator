---
name: writing-style
description: Convenzioni formali e linguistiche. Punteggiatura, emoji, boxed text, distanze, multilingua. Regole di prolissita e forma (HR, dialogo diretto, heading, metriche target).
---

# WritingStyle — Convenzioni Formali e Linguistiche

Regole di formato, punteggiatura e convenzioni linguistiche per il testo delle avventure.

---

## Orientamento

| Scopo | File |
|-------|------|
| Stile di scrittura, formato testo, convenzioni linguistiche (questo file) | `tech/rules/writing-style.md` |
| **Storytelling e semantica**: come scrivere un'avventura che funziona al tavolo | `tech/rules/content-rules.md` |
| Struttura tecnica: directory, naming, file obbligatori, formato sezioni | `tech/rules/adventure-template.md` |

---

## Punteggiatura

Non usare il trattino lungo (—) nel testo delle avventure. Sostituire con virgola, punto, punto e virgola, o riformulare la frase.

---

## Emoji

Non usare emoji nel testo delle avventure e nei documenti di progetto. Unica eccezione: ✅ nelle checklist del PlanBook e nei documenti di lavoro.

---

## Testo da leggere ai giocatori

Usare blockquote per il testo da leggere ad alta voce:

```markdown
> Davanti a voi si apre una sala buia. L'aria odora di muffa e pietra bagnata.
> Al centro, una figura incappucciata vi volta le spalle.
```

**Suggerimento:** mantenere il boxed text breve (3-5 frasi). Descrivere solo ciò che i PG percepiscono (vista, udito, olfatto), non le loro emozioni né azioni che non hanno scelto. Le informazioni che richiedono un tiro vanno dopo il blockquote, non dentro.

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

**qd** = quadretto (square), l'unità base delle battle map D&D (5ft × 5ft / 1,5m × 1,5m).

Esempio: `12m / 40ft / 8qd`

### Capienza delle stanze

Se una stanza contiene creature (mostri, NPC, PG), verificare che lo spazio sia sufficiente per contenerle tutte. Ogni creatura Medium occupa 1 quadretto (1,5m / 5ft). Considerare anche mobili e ostacoli che riducono lo spazio disponibile.

Regola pratica: contare i quadretti disponibili (area totale meno ingombri fissi) e verificare che siano almeno pari al numero di creature previste + spazio per muoversi.

---

## Prolissita e forma

Regole per mantenere i file concisi e leggibili al tavolo. Verificabili con `python3 tech/scripts/measure-prose.py <NomeAvventura>`.

### Linee divisorie (HR)

Non usare `---` come separatore orizzontale. La struttura e data dai titoli (`##`, `###`). Le HR non aggiungono informazione e sporcano il sorgente.

### Boxed text (testo da leggere ai giocatori)

- Max **5 righe** per blocco blockquote
- Solo percezioni sensoriali (vista, udito, olfatto) e battute chiave
- Non includere azioni o emozioni dei PG
- Eccezioni consentite solo per effetto comico/drammatico voluto (documentare il perche nel file)

### Dialogo diretto

Limite: le righe con dialogo diretto (`*"..."*`) non devono superare il **20%** delle righe contenuto di un modulo (ideale: < 15%).

Se un modulo supera il 20%:
- Convertire battute ripetitive in bullet point di stile: `Gorim: impaziente, evasivo, tirchio. Frase tipica: "Dai dai dai."`
- Tenere come dialogo scritto solo le battute plot-critical o con forte effetto comico
- Le risposte a domande probabili dei PG vanno in tabella, non come dialogo

### Heading e frammentazione

- Ogni heading (`##`, `###`) deve avere almeno **5 righe di contenuto** sotto di se prima del prossimo heading (ideale: > 7)
- Se una sezione ha meno di 3 righe, valutare se fonderla con la precedente o successiva
- Non creare heading per ogni singolo passaggio: un elenco puntato sotto un heading unico e piu leggibile

### Dati strutturati sopra prosa

Preferire sempre formati strutturati per informazioni operative:

| Informazione | Formato corretto | Formato da evitare |
|-------------|-----------------|-------------------|
| Nemici in una stanza | Tabella (nome, N, PF, CA, attacco) | Paragrafo descrittivo |
| CD e conseguenze | `Se X, allora Y` oppure tabella | Frase discorsiva lunga |
| Ricompense | Lista puntata | Paragrafo |
| Tattiche combattimento | `Round 1: X. Round 2: Y. Se PF < 50%: Z.` | Prosa narrativa |
| Comportamento NPC | Bullet point (cosa sa, come reagisce) | Descrizione in prosa |

### Non-duplicazione

Un'informazione deve esistere in un solo posto:

| Informazione | Dove va | Nei moduli |
|-------------|---------|-----------|
| Background NPC, motivazioni, relazioni | Doc principale § NPC principali | Solo "Vedi §X" |
| Lore del mondo, antefatti | Doc principale § Lore | Mai ripetere |
| Regole di gioco (economia, milestone) | Doc principale | Reminder breve in DM_Prep |
| Comportamento specifico di una scena | Nel modulo dove accade | — |
| Stat block | `characters/markdown/` | Solo dati minimi in tabella Nemici |

### Metriche target

| Metrica | Soglia warning | Ideale |
|---------|---------------|--------|
| Rapporto prosa/dati | > 2.0 | < 1.5 |
| Densita informativa | < 0.35 | > 0.45 |
| Blocchi boxed > 5 righe | > 0 | 0 (eccezioni documentate) |
| Dialogo diretto | > 20% | < 15% |
| Righe per heading | < 5 | > 7 |
| HR (`---`) | > 0 | 0 |

## Multilingua

Le avventure possono essere tradotte in più lingue. La versione italiana è la fonte di verità; le traduzioni sono derivate.

### Disclaimer

Ogni file tradotto in inglese deve iniziare con:

```markdown
> ⚠️ Auto-translated from Italian. The Italian version is the source of truth.
```

### Cosa si traduce e cosa no

| Elemento | Tradotto? | Esempio |
|----------|-----------|---------|
| Nomi propri (NPC) | No | SirGorimVel, Korex, Fin Ditasvelte |
| Titoli descrittivi | Sì | Il Conte → The Count, Teppista Charmato → Charmed Thug |
| Nomi di mostri | Sì, usare nomi ufficiali SRD WotC dove disponibili | Ratto Corrotto → Corrupted Rat |
| Label stat block | Sì, definite in `tech/i18n/<lang>.json` | Punti ferita → Hit Points |
| Distanze | No, formato triplo mantenuto in entrambe le lingue | `12m / 40ft / 8qd` |
| Testo narrativo | Sì | Traduzione completa del contenuto |

### File i18n

Le label localizzate per intestazioni di sezione e campi degli stat block sono in:

```
tech/i18n/it.json
tech/i18n/en.json
```

Questi file sono usati dal parser `md-to-fightclub.py` e dagli script di generazione PDF.
