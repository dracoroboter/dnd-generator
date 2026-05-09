# ContentRules — Regole di Storytelling per le Avventure

Regole semantiche e narrative: come scrivere un'avventura che funziona al tavolo.

---

## Orientamento

| Scopo | File |
|-------|------|
| **Storytelling e semantica** (questo file) | `tech/rules/content-rules.md` |
| Stile di scrittura, formato testo, convenzioni linguistiche | `tech/rules/writing-style.md` |
| Struttura tecnica: directory, naming, file obbligatori, formato sezioni | `tech/rules/adventure-template.md` |

---

## Avventura scritta vs avventura giocata

L'avventura scritta descrive il mondo: luoghi, personaggi, oggetti, conseguenze delle azioni. Non descrive lo stato meccanico dei PG (punti ferita, condizioni, risorse spese), che appartiene alla giocata e cambia al tavolo.

L'avventura reagisce ai comportamenti dei PG, di solito non li obbliga. Usare strutture "se... allora..." per descrivere le conseguenze, non sequenze lineari che assumono un comportamento specifico.

### Eccezioni

L'avventura può descrivere lo stato meccanico dei PG o forzare un passaggio quando:

- **La situazione iniziale lo richiede**: i PG sono stati rapiti, tramortiti, avvelenati. Il modulo può dichiarare "i PG si risvegliano legati, con 0 slot incantesimo" se è il punto di partenza della scena.
- **Un passaggio è obbligato per motivi meta**: un NPC non può morire perché serve alla saga, una porta teletrasporta i PG in un luogo specifico qualunque cosa facciano. In questi casi dichiararlo esplicitamente come nota meta, separata dal testo narrativo.

In entrambi i casi, segnalare chiaramente che si tratta di un'eccezione (es. prefisso "Meta:" o nota DM dedicata).

L'avventura non può affermare cosa faranno i PG. Al limite può presumere un comportamento probabile, usando formule condizionali:

| ❌ Non scrivere | ✅ Scrivere |
|----------------|------------|
| I PG prendono il registro e lo portano a Vellun. | Se i PG portano il registro a Vellun, lo legge in silenzio. |
| Dopo il combattimento, il PG sa che deve cercare aiuto. | Dopo il combattimento, è probabile che il PG cerchi un modo per risolvere la situazione. |
| I PG scendono nella cripta. | Se i PG decidono di scendere nella cripta... |

Il DM adatta la narrazione alle scelte dei giocatori. Il modulo fornisce contenuto e conseguenze, non una sceneggiatura.

---

## Schede personaggio

Le schede NPC/MON (`characters/markdown/`) descrivono le caratteristiche generali e permanenti del personaggio: aspetto, personalità, motivazioni, stat block, tattiche. Non descrivono cosa il personaggio ha fatto in una specifica situazione di gioco. Gli eventi situazionali vanno nel testo del modulo dove accadono.

---

## Dungeon e luoghi esplorabili

Se i PG entrano in un dungeon o in un luogo con più stanze/aree, il modulo deve fornire abbastanza dettagli per giocarlo: almeno una mappa DM (anche schematica, in formato testo) o una descrizione con dimensioni, connessioni tra le stanze e posizioni dei nemici/oggetti.

---

## Struttura narrativa

Ogni avventura deve avere almeno:
- Un incontro di combattimento
- Un incontro di esplorazione
- Un incontro di roleplay

Prevedere sempre almeno una soluzione alternativa al combattimento per ogni scontro principale.

---

## PNG — Linee guida contenuto

### Separazione stat block dal testo dell'avventura

Gli stat block completi dei personaggi non vanno inseriti nel corpo dei moduli. Devono risiedere esclusivamente nelle schede dedicate in `characters/markdown/`.

Quando un NPC o mostro compare nel testo di un modulo, riferirsi a lui per nome con una breve descrizione inline delle caratteristiche essenziali, seguita dal rimando alla scheda.

Nelle tabelle nemici dei moduli, indicare i dati minimi per il combattimento (nome, n., PF, CA, attacco principale, note) e rimandare alla scheda per il dettaglio.

### Contenuto delle schede NPC

Ogni PNG deve avere (indipendentemente dal tipo di scheda):
- **Motivazione chiara**: cosa vuole, perché agisce così
- **Segreto o informazione nascosta** (opzionale ma consigliato)
- **Tratto distintivo**: un dettaglio fisico o comportamentale memorabile

### Antagonisti principali
- Scheda completa con stat block
- Non devono esistere solo per essere sconfitti; hanno un piano proprio
- Documentare il comportamento in combattimento (tattiche, condizioni di fuga/resa)

### PNG secondari
- Scheda semplificata
- Almeno un PNG ambiguo per avventura (né alleato né nemico chiaro)

---

## Difficoltà degli incontri

Ogni modulo con combattimento deve includere la difficoltà calcolata nella sezione nemici.

### Nota sul sistema CR/XP

Il sistema DMG è oggettivo ma impreciso. Affiancare sempre una nota narrativa se la difficoltà effettiva si discosta da quella calcolata (es. boss progettato per fuggire, incontro evitabile con roleplay).

### Difficoltà sospette

Gli incontri TRIVIAL e DEADLY vanno controllati e giustificati:

- **TRIVIAL**: rischia di essere noioso. Accettabile solo se ha uno scopo narrativo preciso (es. far sentire l'Exhaustion, mostrare la forza del party, introdurre un NPC). Dichiarare il motivo nelle note al master.
- **DEADLY**: rischia di uccidere i PG. Accettabile solo se c'è una via d'uscita (fuga, resa, intervento NPC) o se la morte è una possibilità accettata dal tavolo. Dichiarare la via d'uscita nelle note al master.

---

## Scalabilità degli incontri

Il numero di PG, il loro livello e la presenza di companion NPC dipendono dall'avventura e dal modulo specifico. La difficoltà va sempre calcolata per il party effettivo dichiarato nel documento principale dell'avventura (sezione "Consigli al master").

Se l'avventura è progettata per un party specifico, documentare come scalare per party diversi.

---

## Loot e ricompense

- Ogni modulo dichiara le ricompense nella sezione `## Ricompense`
- L'oro deve essere coerente con il livello del party (DMG tabelle loot)
- Oggetti magici personalizzati devono avere un costo o rischio associato
- La ricompensa principale dell'avventura va dichiarata nel documento principale

---

## Milestone

Le avventure di questo progetto usano il sistema milestone per l'avanzamento di livello (non XP).

### Regole

- Una milestone è triggerata da un evento narrativo specifico (es. "trovare la lettera di Sergius e consegnarla a Gorim") o dal completamento di un certo numero di obiettivi.
- Il trigger deve essere un momento identificabile in gioco, non generico ("completare il modulo" non è un buon trigger; "sconfiggere il boss" o "consegnare l'artefatto" sì).
- Una milestone può non essere conseguita in una sessione: se i PG non raggiungono il trigger, non avanzano.
- In una campagna multi-sessione, le milestone scandiscono il ritmo della progressione. Non è necessario che ogni modulo ne abbia una.

---

## Fonte di verità per regole e mostri

Per verificare una regola su mostri, incantesimi, oggetti o meccaniche, la fonte di verità è l'SRD 5.1 in `tech/data/compendium/Sources/SystemReferenceDocument/all-srd.xml`. Se una regola è homebrew (diversa dall'SRD), deve essere specificata esplicitamente nella scheda del mostro/oggetto o in un documento dedicato.

---

## Pianificazione vs avventura

I dubbi, le domande aperte e le decisioni da prendere vanno nei documenti di pianificazione (PlanBook, meta/), non nel testo dell'avventura. L'avventura contiene solo contenuto giocabile e definitivo.

## Debriefing post-sessione

Il debriefing è il confronto tra l'avventura scritta e quanto è successo realmente al tavolo. Serve a:

- Segnare brevemente le decisioni interessanti dei personaggi
- Segnare le modifiche fatte al volo sull'avventura scritta (improvvisazioni che la migliorano)
- Aggiornare l'avventura scritta con le correzioni emerse

Le modifiche all'avventura non devono contraddire quanto già detto ai giocatori al tavolo.

Il debriefing produce un file temporaneo in `meta/post-sessione-YYYY-MM-DD.md`. Questo file va eliminato una volta che il suo contenuto è stato riportato dove serve (modifiche all'avventura, log nel PlanBook).

### PlanBook vs DiarioSessioni

- **PlanBook**: contiene pianificazione per le sessioni future (todo, idee, punti aperti, decisioni da prendere).
- **DiarioSessioni** (`meta/DiarioSessioni.md`): contiene il racconto di cosa è successo nelle sessioni passate giocate. Serve come riferimento storico. È un file separato dal PlanBook.

---

## Foreshadowing e agganci futuri

Se l'avventura è parte di una campagna o lascia agganci aperti, documentarli in una sezione dedicata nel documento principale o nel `PlanBook.md`.
