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

### Regola dei nomi meccanici

I personaggi non conoscono i nomi degli incantesimi del manuale né le meccaniche di gioco. Nei dialoghi e nel testo da leggere ai giocatori non devono comparire termini come "Hold Person", "Healing Word", "tiro salvezza", "classe armatura". I personaggi descrivono gli effetti in modo narrativo. I nomi meccanici vanno solo nelle note DM (tra parentesi o in sezioni separate).

| ❌ Non scrivere (dialogo) | ✅ Scrivere (dialogo) |
|---------------------------|----------------------|
| *"Healing Word. Lasciami."* | *"Posso aiutarti. Fammelo fare."* |
| *"Lancia Hold Person su di lui"* | *"Lo blocco. Non si muoverà."* |
| *"Il tuo TS Saggezza è fallito"* | *"Senti la volontà che cede"* |

Le note DM possono e devono usare i termini meccanici per chiarezza: `(offre Hold Person — Presa +1 se accetta)`.

---

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

**Eventi script-bounded (⚠️):** eventi che avvengono indipendentemente dalle azioni dei PG, per ragioni di struttura narrativa. Vanno segnalati con ⚠️ e dichiarati esplicitamente come non modificabili. Usare con parsimonia: solo per momenti strutturali della saga (es. morte di un NPC chiave, catastrofe che lancia l'atto successivo).

Il DM adatta la narrazione alle scelte dei giocatori. Il modulo fornisce contenuto e conseguenze, non una sceneggiatura.

---

## Schede personaggio

Le schede NPC/MON (`characters/markdown/`) descrivono le caratteristiche generali e permanenti del personaggio: aspetto, personalità, motivazioni, stat block, tattiche. Non descrivono cosa il personaggio ha fatto in una specifica situazione di gioco. Gli eventi situazionali vanno nel testo del modulo dove accadono.

---

## Dungeon e luoghi esplorabili

Se i PG entrano in un dungeon o in un luogo con più stanze/aree, il modulo deve fornire abbastanza dettagli per giocarlo: almeno una mappa DM (anche schematica, in formato testo) o una descrizione con dimensioni, connessioni tra le stanze e posizioni dei nemici/oggetti.

---

## Brevità nei moduli

I moduli contengono solo ciò che serve al tavolo. La backstory lunga (storia del mondo, antefatti, motivazioni profonde degli antagonisti) va nel documento principale (sezione Lore o NPC principali), non ripetuta nei moduli. Nei moduli: situazione attuale, cosa succede, cosa possono fare i PG.

---

## Struttura narrativa

Ogni avventura deve avere almeno:
- Un incontro di combattimento
- Un incontro di esplorazione
- Un incontro di roleplay

Prevedere sempre almeno una soluzione alternativa al combattimento per ogni scontro principale.

### Regola degli indizi multipli

Per ogni informazione critica che i PG devono scoprire per far avanzare l'avventura, prevedere **almeno 2-3 modi** per trovarla. Se ne esiste solo uno e i PG lo mancano, l'avventura si blocca. Esempi di modi alternativi: un NPC diverso che sa la stessa cosa, un documento trovabile in un altro luogo, un incantesimo di divinazione, un indizio ambientale.

### Checkpoint narrativi (suggerimento per avventure multi-modulo)

Nelle avventure con più moduli sequenziali, le scelte dei giocatori possono creare un'esplosione combinatoriale difficile da gestire nel testo scritto. Una soluzione è definire **checkpoint**: stati garantiti tra un modulo e l'altro, indipendenti da come ci si è arrivati.

- Ogni modulo assume il checkpoint di ingresso senza spiegare tutte le varianti
- Le varianti vanno gestite nel preludio del modulo successivo (1-2 paragrafi "se X / se Y") e poi convergono
- Il corpo del modulo non cambia in base alle scelte precedenti

Questo approccio non è obbligatorio ma è consigliato quando il numero di percorsi possibili rende il testo ingestibile.

### Struttura a nodi (alternativa per avventure sandbox)

Per avventure non lineari, considerare il **node-based design**: l'avventura è un grafo di nodi (luoghi, NPC, eventi) collegati da indizi. I PG possono attraversare il grafo in qualsiasi ordine. Ogni nodo deve avere almeno 2-3 indizi che puntano ad altri nodi (coerente con la regola degli indizi multipli). Questo approccio è consigliato per avventure sandbox; le avventure lineari possono ignorarlo.

### Minacce che avanzano (opzionale)

Per dare urgenza senza forzare i PG su un percorso, considerare minacce che avanzano nel tempo indipendentemente dalle azioni dei PG (es. timer che scade, nemico che si rafforza, situazione che peggiora). Se i PG non agiscono, il mondo cambia. Documentare nel modulo cosa succede se i PG ignorano la minaccia.

---

## Hint narrativi (suggerimenti, non regole)

Suggerimenti per storie più interessanti. Non sono obbligatori — sono spunti da considerare. A volte il cattivo è cattivo e basta, e va benissimo.

### Villain con motivazione

I cattivi più interessanti sono convinti, con qualche ragione, di essere i buoni. Dare ai villain una motivazione comprensibile (anche se sbagliata) li rende più memorabili di un "malvagio generico". Non tutti i villain devono essere complessi — ma almeno l'antagonista principale dovrebbe avere un perché.

### Il companion traditore

Un alleato che ha un piano segreto è un motore narrativo potente. Il tradimento funziona meglio quando il companion è stato genuinamente utile e simpatico prima di rivelare le sue vere intenzioni. Il giocatore deve sentire la perdita, non solo la rabbia.

### Mostri con una ragione

I mostri dovrebbero avere una ragione per essere dove sono. Uno spettro è lo spettro di qualcuno (chi era? perché è ancora lì?). Un rinoceronte in un dungeon ci è stato portato da qualcuno, a meno che il dungeon non sia nella savana. Questo non significa che ogni goblin ha bisogno di un arco narrativo — ma chiedersi "perché è qui?" arricchisce la scena.

### Alleati con difetti

I buoni sono simpatici quando hanno debolezze e difetti. Un paladino perfetto è noioso — un paladino tentato dal male che dimostra la sua purezza resistendo è interessante. Gli alleati dovrebbero avere momenti di dubbio, scelte difficili, tentazioni. La virtù ha valore solo quando costa qualcosa. Con più sfumatura per le altre classi: il ladro che ruba ma ha un codice, il mago arrogante che impara l'umiltà, il chierico che dubita della sua fede.

### Il plot base

Il plot base di un'avventura è molto semplice: un messaggero dice che una persona o un oggetto va recuperato, e che ci sarà una ricompensa. Tutto il resto — complicazioni, tradimenti, dilemmi morali, colpi di scena — è ciò che rende la storia interessante. Ma il nucleo è sempre quello: qualcuno ha bisogno di qualcosa, i PG vanno a prenderlo. L'oggetto o la persona non devono necessariamente avere rilevanza in sé — quando non ce l'hanno si parla di MacGuffin: un pretesto per far muovere i personaggi e far succedere cose lungo la strada.

### Scelte difficili

Una storia interessante porta a scelte in cui tutte le opzioni hanno rischi o conseguenze negative. Fare la cosa giusta non deve essere facile — deve costare qualcosa (tempo, risorse, un alleato, un vantaggio). D'altro canto, fare la cosa sbagliata deve essere pericoloso — non solo moralmente, ma con conseguenze concrete nel mondo di gioco. Le scelte migliori sono quelle in cui i giocatori discutono al tavolo perché non c'è una risposta ovvia.

### Il rischio di morte

Ogni tanto nei combattimenti bisogna rischiare di morire. Non sempre — ma se i giocatori sanno che non possono mai perdere, la tensione scompare e i combattimenti diventano noiosi. Alternare incontri facili (dove i PG si sentono forti) a incontri dove un errore può costare la vita mantiene l'attenzione alta. I combattimenti sono pensati per essere consecutivi: i PG devono affrontarli già provati dai precedenti (slot incantesimo spesi, PF mancanti, risorse consumate). Un incontro MEDIUM dopo due incontri EASY diventa pericoloso. Un incontro HARD dopo un MEDIUM può essere letale.

### Equilibrio tra i pilastri

Un'avventura ha tre pilastri: esplorazione, investigazione (roleplay) e combattimento. In generale serve un equilibrio tra i tre — troppo combattimento stanca, troppo roleplay senza azione annoia, troppa esplorazione senza scopo disorienta. Detto questo, è del tutto legittimo che un'avventura sia sbilanciata verso uno dei pilastri per scelta di sceneggiatura (un'avventura investigativa, un dungeon crawl puro, una sessione di puro roleplay politico). Lo sbilanciamento deve essere intenzionale, non accidentale.

### Il terreno come arma

Nei combattimenti è bene usare il terreno di gioco come elemento tattico: coperture, parti pericolose (pareti da scalare, ponti stretti, fiumi che impediscono il passaggio), ostacoli che limitano il movimento, punti alti che danno vantaggio. Un combattimento in una stanza vuota 10×10 è noioso — lo stesso combattimento su un ponte stretto con un burrone sotto è memorabile. Il terreno rende gli incontri EASY interessanti e quelli HARD letali.

---

## PNG — Linee guida contenuto

### Separazione stat block dalla descrizione narrativa

Le schede in `characters/markdown/` contengono **solo lo stat block**: meccaniche, valori numerici, attacchi, capacita, e un breve accenno al ruolo (una riga). Sono quello che serve al tavolo durante il gioco.

La **descrizione estesa** del personaggio (storia, background, motivazioni, segreti, ruolo nella trama, indizi, agganci futuri, tattiche narrative) va nel testo dell'avventura: nella sezione personaggi del documento principale (`NomeAvventura.md`) o nel modulo dove il personaggio compare.

| Contenuto | Dove va |
|-----------|---------|
| Stat block, CA, PF, attacchi, capacita, abilita | `characters/markdown/NPC_*.md` |
| Ruolo breve (una riga) | `characters/markdown/NPC_*.md` |
| Aspetto fisico (breve, per lo stat block grafico) | `characters/markdown/NPC_*.md` § Descrizione |
| Tattiche di combattimento (breve) | `characters/markdown/NPC_*.md` § Note al master |
| Storia, background, motivazioni, segreti | Documento principale o modulo |
| Ruolo nella trama, come si comporta, cosa sa | Documento principale o modulo |
| Indizi, agganci futuri, note DM narrative | Documento principale o modulo |
| Tattiche narrative (come reagisce, cosa rivela) | Modulo dove compare |

**Razionale:** lo stat block si stampa come scheda singola e si genera come PDF/PNG. Non deve contenere spoiler narrativi o testo lungo. La descrizione estesa vive nel contesto della storia dove ha senso leggerla.

### Separazione stat block dal testo dei moduli

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

Ogni modulo con combattimento deve includere la difficoltà calcolata nella sezione `## Nemici`.

### Formato standard della sezione Nemici

La sezione `## Nemici` deve contenere una tabella con formato fisso:

```markdown
## Nemici

| Luogo | Nemici | N. | CR | Difficoltà (3 PG lv5 + Udo + Fin) |
|-------|--------|----|----|-----|
| Scogliera | Scheletri | 15 | 1/4 | HARD |
| Scogliera | Spettri dell'Ordine | 3 | — | Non combattibili |
```

**Colonne obbligatorie:**

| Colonna | Contenuto |
|---------|-----------|
| Luogo | Dove avviene l'incontro |
| Nemici | Nome del nemico o gruppo |
| N. | Numero di creature |
| CR | Challenge Rating (numerico: `1/4`, `1/2`, `1`, `3`). `—` se non combattibile |
| Difficoltà | Label calcolata: TRIVIAL, EASY, MEDIUM, HARD, DEADLY. `Non combattibili` se CR è `—` |

**Regole:**

- L'intestazione della colonna Difficoltà è semplicemente `Difficoltà` (senza parentesi)
- Il party di riferimento va dichiarato **una sola volta** all'inizio del modulo con il formato: `**Party:** 3 PG lv5 + Udo CR3 + Fin lv3`. Per ogni companion indicare il livello (`lv3`) o il CR (`CR3`). Lo script usa la tabella Xanathar per convertire CR → livello equivalente.
- Note aggiuntive (evitabile, tattiche) vanno tra parentesi dopo la label: `HARD (evitabile con negoziazione)`
- Lo script `check-encounter-difficulty.py` usa questa tabella per verificare automaticamente i calcoli

### Incontri combinati (più tipi di nemici)

Quando un incontro include nemici di tipo diverso (es. boss + minion), elencarli su **righe separate con lo stesso Luogo**. La difficoltà va dichiarata **solo sulla prima riga** del gruppo; le righe successive dello stesso luogo hanno `—` nella colonna Difficoltà.

Lo script raggruppa automaticamente le righe con lo stesso Luogo e calcola la difficoltà combinata.

```markdown
| Luogo | Nemici | N. | CR | Difficoltà (3 PG lv3 + Udo + Fin) |
|-------|--------|----|----|-----|
| La cisterna | Korex | 1 | 3 | HARD |
| La cisterna | Teppista charmato | 2 | 1/8 | — |
| Nido ratti | Ratto corrotto | 6 | 1/8 | EASY |
| Nido ratti | Sciame di ratti | 1 | 1/4 | — |
```

In questo esempio:
- "La cisterna" è un incontro combinato: Korex CR 3 + 2 Teppisti CR 1/8 → calcolato insieme
- "Nido ratti" è un incontro combinato: 6 Ratti + 1 Sciame → calcolato insieme
- La difficoltà dichiarata sulla prima riga si riferisce all'intero gruppo

**Questo formato è obbligatorio per tutti i moduli normalizzati.** I moduli legacy vanno aggiornati quando si toccano.

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

## Documento principale: lista personaggi e luoghi

Il documento principale di ogni avventura (`NomeAvventura.md`) deve contenere una sezione centralizzata con personaggi e luoghi. I moduli non ripetono queste informazioni — riportano solo le eccezioni specifiche della puntata.

### Lista personaggi

**Tabella riassuntiva** (formato tabellare, breve): nome, ruolo in poche parole.

**Schede estese** (formato lista, una per personaggio): per ogni NPC con nome proprio, elencare:
- Dove si trova di solito (posizione base)
- Cosa sa (conoscenze rilevanti per la trama)
- Come si comporta (temperamento, reazioni tipiche)
- Relazioni con altri personaggi (amicizie, inimicizie, debiti)
- Frasi ricorrenti o tratti distintivi (se rilevanti)

Non includere villain generici (Thug, Guard, ecc.) — quelli vanno solo nei moduli come stat block per i combattimenti.

### Lista luoghi

**Formato tabellare**: nome, dove si trova, descrizione breve (1-2 frasi che danno il contesto al DM).

Le descrizioni lunghe (layout stanze, battle map, dettagli esplorazione) restano nei moduli dove servono.

### Nei moduli

I moduli riportano solo:
- **Eccezioni** alla posizione base dei personaggi (es. "Sberluccica: rapito nell'Atto 2")
- **Informazioni aggiuntive** specifiche della puntata (es. "Gorim in questa puntata sa anche che...")
- Rimando esplicito al documento principale per il resto (es. "Vedi § NPC principali in NomeAvventura.md")

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

Gli agganci futuri (semi da piantare per avventure successive, archi narrativi a lungo termine, collegamenti con altre avventure della saga) vanno nel **PlanBook**, non nel testo dell'avventura. Sono pianificazione della scrittura, non contenuto giocabile.

Nel testo dell'avventura vanno solo gli elementi che il DM usa effettivamente al tavolo (es. una frase di Gorim che tradisce preoccupazione, una menzione di un luogo lontano). Questi vanno nelle note DM del modulo specifico dove compaiono.
