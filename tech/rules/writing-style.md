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
