---
name: adventure-design
description: Struttura narrativa e design di avventure D&D. Contiene Vogler 12 stadi, Propp 31 funzioni, Booker 7 plot, Three Clue Rule, 8 step Lazy DM, livello di dettaglio, differenza scritto/giocato, plot base.
---

# Adventure Design: struttura, dettaglio e narrazione

Come progettare un'avventura che funziona al tavolo. Principi di struttura narrativa, livello di dettaglio, differenza tra scritto e giocato, plot base.

---

## Orientamento

| Scopo | File |
|-------|------|
| **Struttura narrativa e design** (questo file) | `tech/rules/adventure-design.md` |
| Storytelling e semantica: regole operative per scrivere moduli | `tech/rules/content-rules.md` |
| Struttura tecnica: directory, naming, file obbligatori | `tech/rules/adventure-template.md` |
| Stile di scrittura e convenzioni linguistiche | `tech/rules/writing-style.md` |

---

## Principio fondamentale: scrivi per il DM, non per il lettore

Un'avventura D&D non e un romanzo, non e una sceneggiatura, non e un worldbuilding document. E un **materiale di riferimento operativo** che il DM consulta al tavolo mentre i giocatori aspettano.

Ogni frase deve superare il test: **"Il DM ha bisogno di questa informazione in questo momento?"**

Se la risposta e no, la frase non serve. Il DM puo improvvisare il colore, l'atmosfera, i dettagli ambientali. Non puo improvvisare i dati: nomi, numeri, connessioni tra fatti, conseguenze meccaniche.

---

## Parte I: Avventura scritta vs avventura giocata

### Cosa sono

L'**avventura scritta** e il documento markdown che produciamo. L'**avventura giocata** e quello che succede realmente al tavolo.

La distanza tra le due e enorme e irriducibile. Nessun testo puo catturare la totalita di una sessione, perche i giocatori fanno scelte imprevedibili, il DM improvvisa, i dadi cambiano tutto.

### Il ruolo del testo

Il testo serve a tre cose:

1. **Dare al DM abbastanza contesto** da improvvisare in modo coerente
2. **Fornire i dati meccanici** che non si possono inventare al volo (stat block, CD, distanze, contenuti di stanze)
3. **Suggerire il tono e l'atmosfera** tramite boxed text brevi e indicazioni sintetiche

Il testo NON serve a:

- Raccontare una storia completa (la storia la fanno i giocatori)
- Prevedere ogni possibile scelta dei PG
- Descrivere emozioni, pensieri o azioni dei PG
- Spiegare il background del mondo a un lettore esterno
- Impressionare per la qualita letteraria della prosa

### La regola dell'improvvisazione

Tutto cio che il DM puo ragionevolmente improvvisare **non va scritto**. Il DM sa descrivere una taverna, sa fare la voce di un mercante, sa inventare il nome di una via secondaria. Quello che il DM non puo improvvisare sono le informazioni strutturali: chi sa cosa, cosa c'e dentro la stanza, quali sono le conseguenze di un'azione specifica, qual e la CD di un tiro.

### Tabella: cosa scrivere e cosa no

| Scrivi | Non scrivere |
|--------|-------------|
| Nome NPC, razza, ruolo, motivazione | Descrizione fisica dettagliata (1 tratto basta) |
| Cosa sa l'NPC (informazioni per la trama) | Dialoghi preconfezionati lunghi |
| Layout della stanza (dimensioni, uscite, contenuti) | Descrizione poetica dell'atmosfera |
| CD dei tiri e conseguenze | Cosa fanno i PG |
| Stat block nemici, PF, CA, attacchi | Backstory irrilevante dei nemici generici |
| Connessioni tra indizi e nodi | Riassunti di cosa e successo prima |
| Ricompense specifiche | Elenco esaustivo del mobilio |

### Indicatore pratico: la regola di una pagina

Ogni incontro/stanza/scena dovrebbe stare in **una pagina** (o meno). Se servono due pagine, il contenuto e probabilmente troppo denso o troppo prolisso. Condensare o splittare.

---

## Parte II: Il livello di dettaglio giusto

### Il problema della prolissita

Le avventure pubblicate da WotC (Curse of Strahd, Waterdeep, ecc.) soffrono di prolissita sistematica: paragrafi di backstory prima di ogni stanza, descrizioni di quattro righe per un corridoio vuoto, ripetizione di informazioni gia note.

Il risultato: il DM non trova quello che gli serve, si perde nel testo, rallenta il gioco.

### Principio: dati sopra prosa

| Tipo di informazione | Formato ideale |
|---------------------|---------------|
| Nemici in una stanza | Tabella (nome, numero, PF, CA, attacco) |
| Layout | Elenco puntato di aree + mappa |
| NPC | Nome, 1 tratto, motivazione, cosa sa |
| Indizi | Lista numerata |
| Conseguenze di azioni | "Se X, allora Y" |
| Testo da leggere | Blockquote, max 3-5 frasi |
| Backstory/lore | Solo nel documento principale, mai nei moduli |

### Boxed text (testo da leggere ai giocatori)

Il boxed text funziona quando e breve (3-5 frasi), descrive solo percezioni sensoriali (vista, udito, olfatto), e non presume azioni o emozioni dei PG. Oltre le 5 frasi il DM smette di leggerlo e riassume a parole sue, rendendo il testo inutile.

### Anti-pattern: il backstory dump

Il backstory dump e l'errore piu comune: spiegare nel modulo la storia di un luogo, la genealogia di un NPC, o gli antefatti della situazione. Queste informazioni servono al DM per capire il mondo, non ai giocatori al tavolo. Vanno nel **documento principale** dell'avventura (sezione Lore o NPC principali), non nel modulo dove si gioca.

Nel modulo va solo: **situazione attuale, cosa succede, cosa possono fare i PG.**

### Anti-pattern: la duplicazione

Se un'informazione e nel documento principale, non va ripetuta nel modulo. Un rimando basta: "Vedi NPC principali nel documento principale."

### Anti-pattern: la descrizione esaustiva

Non serve descrivere ogni mobile, ogni pietra, ogni dettaglio di una stanza. Descrivi solo cio che:
- I PG possono interagire con (leve, porte, oggetti)
- E pericoloso (trappole, terreno difficile)
- Contiene informazioni (libri, lettere, simboli)
- Stabilisce il tono (un singolo dettaglio evocativo)

Tutto il resto il DM lo inventa se i giocatori chiedono.

---

## Parte III: Il plot base

### La struttura fondamentale

Il plot base di ogni avventura e elementare:

> Un messaggero dice che una persona o un oggetto va recuperato, e che ci sara una ricompensa.

Tutto il resto (complicazioni, tradimenti, dilemmi morali, colpi di scena) e cio che rende la storia interessante. Ma il nucleo e sempre: **qualcuno ha bisogno di qualcosa, i PG vanno a prenderlo**.

L'oggetto o la persona non devono necessariamente avere importanza in se. Quando non ce l'hanno si parla di **MacGuffin**: un pretesto per far muovere i personaggi e far succedere cose lungo la strada.

### Varianti del plot base

| Variante | Esempio |
|----------|---------|
| **Recupero** | Trova l'artefatto, salva il prigioniero |
| **Difesa** | Proteggi il villaggio dall'assalto |
| **Indagine** | Scopri chi ha avvelenato il conte |
| **Fuga** | Scappa dalla prigione/dungeon |
| **Viaggio** | Porta X da A a B |
| **Eliminazione** | Ferma il rituale, uccidi il mostro |
| **Esplorazione** | Mappa il territorio sconosciuto |

### Il problema urgente

Un'avventura che funziona presenta un **problema urgente** che richiede azione immediata. Se i PG possono rimandare senza conseguenze, l'avventura non ha tensione.

Modi per creare urgenza:
- Timer (il rituale si compie a mezzanotte)
- Minaccia progressiva (il villaggio viene attaccato ogni notte)
- Perdita personale (ti hanno rubato qualcosa)
- Opportunita che scade (il mercante parte domani)

---

## Parte IV: Strutture narrative classiche

### Il Viaggio dell'Eroe (Campbell / Vogler)

Joseph Campbell (*The Hero with a Thousand Faces*, 1949) identifico una struttura comune nei miti eroici di tutte le culture. Christopher Vogler la adatto per la sceneggiatura in *The Writer's Journey* (1992), condensandola in 12 stadi organizzati in 3 atti.

#### I 12 stadi di Vogler

**Atto I: Separazione**

| # | Stadio | In D&D |
|---|--------|--------|
| 1 | **Mondo Ordinario** | I PG nella loro vita quotidiana (taverna, citta, routine) |
| 2 | **Chiamata all'avventura** | L'hook: qualcuno chiede aiuto, qualcosa va storto |
| 3 | **Rifiuto della chiamata** | I PG esitano (opzionale: i giocatori scelgono) |
| 4 | **Incontro con il mentore** | NPC che fornisce informazioni, oggetti, direzione |

**Atto II: Iniziazione**

| # | Stadio | In D&D |
|---|--------|--------|
| 5 | **Attraversamento della prima soglia** | I PG lasciano la zona sicura (entrano nel dungeon, partono) |
| 6 | **Prove, alleati, nemici** | Il corpo dell'avventura: incontri, sfide, NPC |
| 7 | **Avvicinamento alla caverna piu interna** | Si avvicinano al boss/obiettivo finale |
| 8 | **Prova suprema (Ordeal)** | Il boss fight, la crisi, il momento di massima tensione |
| 9 | **Ricompensa** | I PG ottengono cio che cercavano |

**Atto III: Ritorno**

| # | Stadio | In D&D |
|---|--------|--------|
| 10 | **Via del ritorno** | Fuga dal dungeon, inseguimento, conseguenze |
| 11 | **Resurrezione** | Ultima prova, trasformazione dell'eroe |
| 12 | **Ritorno con l'elisir** | I PG tornano cambiati, con il bottino/conoscenza |

#### Applicazione al GDR

La struttura di Vogler NON va usata come binario. E un **modello di riferimento**, non una checklist obbligatoria. Nel GDR:

- I giocatori non rifiutano la chiamata (o l'avventura non parte)
- Il mentore puo essere ridotto a un quest giver
- La "resurrezione" e spesso il livello successivo
- L'Atto III (ritorno) e spesso il piu debole nelle avventure D&D, spesso ridotto a "tornate in citta"

Il valore del modello e strutturale: assicura che ci sia un **arco** (partenza, crescita di tensione, climax, risoluzione) e non una sequenza piatta di incontri scollegati.

#### Limiti del modello

- Non si applica bene alle avventure sandbox (nessun arco predefinito)
- I PG sono multipli (non un singolo eroe)
- Il GDR e collaborativo, non autoriale: la struttura emerge, non si impone
- Campbell stesso non riusciva a trovare un mito che contenesse tutti gli stadi

### Le 31 funzioni di Propp

Vladimir Propp (*Morfologia della fiaba*, 1928) analizzo centinaia di fiabe russe e identifico 31 funzioni narrative ricorrenti, raggruppate in 4 sfere.

#### Le 4 sfere

| Sfera | Funzioni | Contenuto |
|-------|----------|-----------|
| **Introduzione** | 1-7 | Presentazione della situazione e dei personaggi |
| **Corpo della storia** | 8-11 | Il conflitto principale emerge, l'eroe parte |
| **Sequenza del donatore** | 12-19 | L'eroe viene messo alla prova, ottiene un aiuto, affronta il villain |
| **Ritorno dell'eroe** | 20-31 | Inseguimento, prove finali, riconoscimento, punizione del villain |

#### Le funzioni piu utili per D&D

Non tutte le 31 funzioni si applicano. Le piu produttive per il game design:

| # | Funzione | Uso in D&D |
|---|----------|-----------|
| 1 | **Allontanamento** | Qualcuno scompare, l'equilibrio si rompe |
| 2 | **Divieto** | "Non andate nel bosco di notte" (i PG ci andranno) |
| 4 | **Ricognizione** | Il villain cerca informazioni sui PG |
| 6 | **Inganno** | Il villain o un NPC ambiguo mente ai PG |
| 8 | **Mancanza** | L'hook: qualcosa e stato rubato, qualcuno e sparito |
| 12 | **Prova** | Il donatore testa l'eroe prima di aiutarlo |
| 14 | **Acquisizione** | L'eroe riceve l'oggetto magico/informazione chiave |
| 16 | **Lotta** | Il combattimento principale |
| 18 | **Vittoria** | Il villain e sconfitto |
| 24 | **Pretese del falso eroe** | Un NPC prende il merito (ottimo per colpi di scena) |

#### I 7 archetipi di Propp

| Archetipo | In D&D |
|-----------|--------|
| **Villain** | L'antagonista principale |
| **Dispatcher** | Il quest giver |
| **Helper** | Il companion NPC |
| **Prize** | La principessa/l'oggetto da recuperare (il MacGuffin) |
| **Donor** | L'NPC che da informazioni/oggetti dopo una prova |
| **Hero** | I PG |
| **False Hero** | L'NPC che tradisce o prende il merito |

#### Uso pratico di Propp

Propp non va usato come sequenza lineare. La tecnica suggerita:

1. **Scegli 4-5 funzioni** da sfere diverse
2. **Combinale** in un ordine interessante
3. **Associa** ogni funzione a un incontro/scena
4. Il risultato e una struttura che "suona giusta" perche attiva pattern narrativi universali

Esempio: Mancanza (8) + Divieto (2) + Prova (12) + Inganno (6) + Lotta (16) = Un oggetto e stato rubato (mancanza), i PG sono avvertiti di non fidarsi di nessuno (divieto), devono superare una prova per ottenere informazioni (prova), un alleato li tradisce (inganno), combattono il vero responsabile (lotta).

---

## Parte V: Strutture specifiche per il GDR

### Il Node-Based Design (Alexandrian)

Justin Alexander propone di strutturare le avventure come grafi di nodi, non come sequenze lineari.

**Principi:**

- Ogni nodo e un luogo, un NPC, o un evento
- I nodi sono collegati da **indizi** (non da un percorso obbligato)
- I PG possono attraversare il grafo in qualsiasi ordine
- Ogni nodo deve contenere almeno 2-3 indizi che puntano ad altri nodi

**Quando usarlo:** avventure investigative, sandbox, mystery. Meno adatto per dungeon crawl lineari.

### La Three Clue Rule (Alexandrian)

Per ogni informazione critica che deve essere scoperta per far avanzare l'avventura, prevedere **almeno 3 indizi** in punti diversi. Se ne esiste solo uno e i PG lo mancano, l'avventura si blocca.

Questo non significa 3 indizi identici. Significa 3 vie diverse per arrivare alla stessa conclusione:
- Un NPC che sa la verita
- Un documento trovabile in un altro luogo
- Un dettaglio ambientale che il DM puo offrire
- Un incantesimo di divinazione che funziona

### Gli 8 Step del Lazy DM (Sly Flourish)

Mike Shea propone 8 passi di preparazione rapida per ogni sessione:

| # | Step | Cosa produce |
|---|------|-------------|
| 1 | **Review Characters** | Ricordare chi sono i PG, cosa vogliono |
| 2 | **Strong Start** | Una scena d'apertura che inizia in medias res |
| 3 | **Secrets & Clues** | 10 informazioni che i PG possono scoprire (non legate a un modo specifico) |
| 4 | **Scenes** | 5 scene che potrebbero accadere (~1 per 45 min di gioco) |
| 5 | **Locations** | Luoghi fantastici dove le scene accadono |
| 6 | **NPCs** | NPC con nome, motivazione, tratto |
| 7 | **Monsters** | Stat block e tattiche |
| 8 | **Treasure** | Ricompense (mo, oggetti, informazioni) |

**Principio chiave:** questi 8 step sono **materiale flessibile**. Non sono una sceneggiatura. Secrets & Clues possono essere rivelati in qualsiasi scena. Le scene non hanno un ordine fisso. E il DM che assembla al tavolo in base alle scelte dei giocatori.

**Applicazione al progetto:** gli 8 step sono il formato ideale per il **DM_Prep.md** di ogni modulo. Il modulo scritto contiene la struttura completa; il DM_Prep contiene il distillato operativo.

### Il metodo Arcane Library (Kelsey Dionne)

Kelsey Dionne propone un approccio basato sugli **ostacoli** (hurdles):

1. Definisci un **problema urgente** che solo i PG possono risolvere
2. Definisci il **finale**: cosa succede se vincono, cosa se perdono
3. Immagina di giocare l'avventura: a ogni punto, chiediti "cosa faccio dopo?"
4. Ogni volta che colpisci un **ostacolo**, quello e un incontro
5. Alterna tipi di incontro (combattimento, roleplay, esplorazione)
6. Assicurati che ogni tipo di personaggio abbia almeno un momento per brillare
7. Ogni incontro sta in **una pagina massimo**

**Principio della rilevanza:** "Cio che sto descrivendo aiuta a risolvere il problema dell'avventura? Se no, non scriverlo."

---

## Parte VI: La struttura a tre atti applicata a D&D

La struttura a tre atti e il minimo sindacale per un'avventura che funzioni narrativamente:

### Atto I: Setup (25% del tempo)

- Hook: il problema urgente
- Contesto: dove siamo, chi ci ha mandato
- Prima soglia: i PG si impegnano (entrano nel dungeon, accettano la quest)

### Atto II: Confronto (50% del tempo)

- Prove crescenti: incontri di difficolta progressiva
- Complicazioni: il piano non funziona, emergono nuove informazioni
- Punto di non ritorno: i PG scoprono la verita, la posta si alza

### Atto III: Risoluzione (25% del tempo)

- Climax: lo scontro finale, la scelta decisiva
- Risoluzione: conseguenze, ricompense
- Aggancio: un filo aperto per il futuro (opzionale)

### Nota sui moduli

Ogni modulo non deve necessariamente contenere tutti e tre gli atti. In un'avventura multi-modulo:
- Il primo modulo e l'Atto I dell'intera avventura
- I moduli centrali sono l'Atto II
- L'ultimo modulo e l'Atto III

Ma ogni singolo modulo dovrebbe avere un proprio **arco interno** (anche minimo): problema locale, sviluppo, risoluzione.

---

## Parte VII: Regole pratiche per questo progetto

### Gerarchia dell'informazione

| Dove va | Cosa contiene |
|---------|-------------|
| **Documento principale** | Lore, plot complessivo, NPC con descrizione estesa, luoghi, backstory, mappa generale |
| **Modulo** | Situazione attuale, cosa succede, incontri, dati meccanici, indizi, ricompense |
| **DM_Prep** | Distillato operativo: passaggi, stat block inline, tiri chiave, mappe ASCII |
| **Scheda NPC** | Solo stat block meccanico + 1 riga di ruolo |
| **PlanBook** | Pianificazione, dubbi, alternative, agganci futuri |

### Checklist anti-prolissita

Prima di committare un modulo, verificare:

- [ ] Ogni paragrafo supera il test "il DM ne ha bisogno al tavolo?"
- [ ] Nessuna informazione e duplicata dal documento principale
- [ ] I boxed text sono max 3-5 frasi
- [ ] Le descrizioni delle stanze contengono solo interazioni e pericoli
- [ ] I dati meccanici sono in tabella, non in prosa
- [ ] L'intero modulo sta in meno di 3 pagine stampate (escluse mappe)
- [ ] Le tattiche dei nemici sono bullet point, non paragrafi
- [ ] Non ci sono backstory dump: la storia va nel doc principale

### Pattern del buon modulo (da TanaDiKorex)

```
# Puntata N: NomeModulo

## Descrizione                 ← boxed text + 2-3 frasi di contesto DM
## Obiettivo                   ← 1 frase
## Luoghi interni              ← per ogni area: dimensioni, contenuto, CD
## Nemici                      ← tabella + tattiche bullet point
## Indizi chiave               ← lista
## Ricompense                  ← lista
## Milestone                   ← trigger specifico (opzionale)
## Finale                      ← 2-3 esiti possibili con boxed text
## Note al master              ← consigli operativi
```

---

## Fonti

| Fonte | Autore | Concetto chiave |
|-------|--------|-----------------|
| *The Hero with a Thousand Faces* (1949) | Joseph Campbell | Monomito: 17 stadi in 3 fasi (Partenza, Iniziazione, Ritorno) |
| *The Writer's Journey* (1992) | Christopher Vogler | Adattamento del monomito in 12 stadi per sceneggiatura |
| *Morfologia della fiaba* (1928) | Vladimir Propp | 31 funzioni narrative + 7 archetipi delle fiabe |
| [The Alexandrian](https://thealexandrian.net) | Justin Alexander | Node-based design, Three Clue Rule, Don't Prep Plots |
| *Return of the Lazy Dungeon Master* (2018) | Mike Shea | 8 step per prep efficiente: Strong Start, Secrets & Clues |
| [The Arcane Library](https://thearcanelibrary.com) | Kelsey Dionne | Hurdles-based design, una pagina per incontro, problema urgente |
| [On Writing Adventures](https://slyflourish.com/on_writing_adventures.html) | Mike Shea | Riassunto WotC freelancer guidelines |
| [Nerds on Earth](https://nerdsonearth.com/2017/09/propps-31-functions-getting-better-at-dnd/) | Clave Jones | Applicazione delle 31 funzioni di Propp a D&D |
