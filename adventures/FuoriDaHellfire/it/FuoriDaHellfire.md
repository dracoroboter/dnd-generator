# Fuori da Hellfire

## Indice

- Lore
- Introduzione
- Plot generale
- Consigli al master
- NPC principali
- Luoghi
- Struttura dell'avventura
- Appendice: Cheat Sheet Anello del Virtuoso
- Appendice: Simulazione progressione Presa

---

## Lore

Greyhawkins è una città portuale dove il bizzarro è la norma, ma nessuno si aspettava quello che è successo ai moli di Oakshore. Una serie di omicidi, ratti corrotti ovunque, e dietro a tutto un elfo dal sorriso troppo largo e una melodia che ti entrava nella testa: **Korex**.

La compagnia lo ha smascherato, ha sconfitto i suoi ratti, e lo ha messo in fuga. Korex è scappato nelle fogne sotto i moli, fogne che nessuno sapeva esistessero. La Guardia di Oakshore non ha le risorse per inseguirlo nel sottosuolo. Tocca alla compagnia.

## Introduzione

> La pioggia batte sui moli di Oakshore. Lo sceriffo Udo Hutchinson vi guarda con un misto di gratitudine e impazienza. "È scappato nelle fogne. Quelle vecchie, sotto il molo est; non sapevamo nemmeno che fossero ancora aperte." Controlla la spada al fianco. "Vengo con voi. Portatelo su. Vivo o morto, non mi importa. Basta che non torni."

I PG hanno appena finito lo scontro con i ratti. Korex è fuggito attraverso una grata nel pavimento del magazzino ai moli. Udo, appena tornato a Oakshore da un viaggio personale, si è trovato il quartiere nel caos e non ha intenzione di mandare gente nelle fogne senza andarci lui stesso.

## Plot generale

- **Atto 1, La discesa**: i PG entrano nelle fogne inseguendo Korex. Tunnel bui, trappole lasciate da Korex per rallentarli, servitori rimasti a coprire la fuga. L'ambiente diventa progressivamente più strano; le fogne sono più antiche e più grandi di quanto dovrebbero essere.
- **Atto 2, La tana**: i PG raggiungono il rifugio di Korex. Scontro finale con il bardo e i suoi ultimi difensori. Korex può essere catturato vivo (se i PG resistono al charm) o ucciso.
- **Atto 3, La scoperta**: risolta la questione Korex, i PG trovano l'Anello del Virtuoso al suo dito, un artefatto maledetto che contiene l'anima di un bardo antico. Chi lo tocca rischia di indossarlo. Chi lo indossa guadagna potere, ma inizia a essere posseduto. Se nessun PG lo tocca, una guardia lo indossa e il problema esplode comunque.

## Consigli al master

- **Tono**: mantenere il camp dello starter kit. Korex è teatrale, i ratti sono grotteschi, le fogne sono esagerate. Ma il cliffhanger finale deve avere un cambio di registro, il momento in cui la commedia si ferma e i giocatori capiscono che c'è qualcosa di serio.
- **Korex in combattimento**: non combatte lealmente. Charma, scappa, manda avanti i servitori. Se messo alle strette, implora pietà. E mente.
- **Cattura vs uccisione**: entrambe le opzioni sono valide. Se catturato vivo, Korex può dare informazioni (vere e false mescolate). Se ucciso, le informazioni si trovano nei suoi appunti nella tana.
- **Il cliffhanger**: dopo la milestone, l'Anello del Virtuoso entra in gioco. L'anello era al dito di Korex, è l'origine del suo potere. Contiene l'anima di un bardo antico che vuole tornare in vita. Meccanica a tre livelli: attrazione passiva → tocco (TS Sag CD 20 o indossamento forzato) → possessione progressiva. Se nessun PG lo tocca, una guardia NPC lo indossa e attacca. Dettagli in `DiscussioneNarrativa.md`.

**Difficoltà consigliata:** 4-5 PG di livello 3 (iniziale) + Udo Hutchinson + Fin Ditasvelte (NPC companion)
**Scalabilità:** per 4+ PG, Udo resta indietro a sorvegliare l'ingresso e Fin non si unisce (il charm non si è ancora spezzato). Per 2-3 PG, tenere entrambi i companion.

## NPC principali

Schede complete in `characters/`.

### Udo Hutchinson (modulo 1)

Sceriffo di Oakshore, veterano. Uomo robusto sulla cinquantina, capelli grigi, cicatrice sul mento. Parla poco, agisce in fretta.

- **Dove:** Oakshore, quartiere portuale. Si unisce ai PG all'ingresso delle fogne.
- **Ruolo:** Tank del gruppo, NPC companion.
- **Cosa sa:** Conosce Oakshore e i suoi abitanti. Sa che Korex è arrivato da poco. Conosce Vellun di fama ("il vecchio matto nella torre").
- **Come si comporta:** Diretto, impaziente, non sopporta le perdite di tempo. Non guida il gruppo ma commenta.
- **Frase:** *"Non ho tempo per queste stronzate."*

→ Scheda: `NPC_UdoHutchinson.md`

### Korex (modulo 1-2)

Elfo bardo CE, antagonista. Alto, magro, sorriso permanente, occhi che non sorridono. Parla come se fosse sul palco. Non smette mai di canticchiare.

- **Dove:** Fogne sotto Oakshore (moduli 1-2). Nella tana al fondo.
- **Ruolo:** Antagonista dei moduli 1-2. Portatore dell'anello prima dei PG.
- **Cosa sa:** Sa dell'anello (lo indossa), sa resistere a Jason. Se catturato vivo, mescola verità e bugie.
- **Come si comporta:** Teatrale, vigliacco, manipolatore. Charma, scappa, manda avanti i servitori. Se messo alle strette, implora pietà. E mente.
- **Frase:** *"Pubblico! Finalmente!"*

→ Scheda: `NPC_Korex.md`

### Fin Ditasvelte (modulo 1)

Halfling ladro CN, ex-charmato di Korex. Basso, capelli rossi arruffati, sorriso da furbetto. Non riesce a non toccare le cose.

- **Dove:** Esce dalle fogne all'inizio del modulo 1, confuso e furioso.
- **Ruolo:** NPC companion, rogue del gruppo. Portatore dell'anello (scenario B).
- **Cosa sa:** Conosce un po' il layout delle fogne (ci è stato sotto charm). Ha sentito parlare di Vellun.
- **Come si comporta:** Veloce, curioso, impulsivo. Vuole vendetta su Korex. Tocca tutto.
- **Frase:** *"Che male può fare dare un'occhiata?"*

→ Scheda: `NPC_FinDitasvelte.md`

### Jason Accordion (modulo 2)

Bardo umano NM, anima nell'Anello del Virtuoso. Villain della saga. Manipolatore paziente che comunica telepaticamente col portatore.

- **Dove:** Nell'anello. Parla solo al portatore.
- **Ruolo:** Villain della saga lv4-6. Vuole tornare in vita prendendo il corpo del portatore.
- **Cosa sa:** Tutto sulla sua prigionia, sull'Ordine della Chiave Spezzata, sulla torre di Ashwick. Mente su quasi tutto.
- **Come si comporta:** Paziente, affabile, mai aggressivo all'inizio. Offre aiuto, crea dipendenza, poi ricatta.
- **Frase:** *"Posso aiutarti. Ho bisogno solo di un minuto."*

→ Scheda: `NPC_JasonAccordion.md`

### Aldric Vellun (modulo 3)

Studioso settantenne, discendente del Magister Vellun. Non è un mago — è un accademico. Barba grigia, occhiali rotondi, gatto arancione.

- **Dove:** Torre bassa alla periferia di Hawksbridge. I PG ci arrivano nel modulo 3.
- **Ruolo:** Alleato, esperto di maledizioni. Può eseguire rituali per ridurre la Presa.
- **Cosa sa:** Riconosce l'anello (simbolo ouroboros). Sa dell'Ordine della Chiave Spezzata. Non sa il nome "Jason" finché non legge il registro. Sa che serve lo scheletro per la rimozione definitiva.
- **Come si comporta:** Parla veloce, cambia argomento, si distrae. Genuinamente gentile.
- **Frase:** *"Vi aspettavo. No, mento. Non vi aspettavo per niente. Ma entrate, entrate. Tè?"*

→ Scheda: `NPC_AldricVellun.md`

### Barney Mezzapinta (modulo 3)

Halfling, proprietario della taverna Pint Ahoy a Greyhawkins. Calvo, nervoso, tirchio ma non cattivo.

- **Dove:** Pint Ahoy, Greyhawkins. Presente dal modulo 3.
- **Ruolo:** NPC ricorrente, base operativa dei PG.
- **Cosa sa:** Pettegolezzi locali. Sa che qualcosa è salito dalla cantina stanotte.
- **Come si comporta:** Si torce le mani, vuole che i problemi spariscano senza costargli soldi.

→ Scheda: `NPC_BarneyMezzapinta.md`

### Chef Morticcio (modulo 3)

Ghoul cuoco nella cripta sotto il Pint Ahoy. Grigio, secco, grembiule macchiato. In vita era il cuoco del rifugio dell'Ordine.

- **Dove:** Cripta sotto la taverna (modulo 3), cucina.
- **Ruolo:** Occupante della cripta, potenziale NPC ricorrente. Non ostile se non provocato.
- **Cosa sa:** Conosce la cripta. Ricordi frammentari dell'Ordine.
- **Come si comporta:** Vuole compagnia e qualcuno che apprezzi la sua cucina. Ha fame costante.

→ Scheda: `MON_ChefMorticcio.md`

### Aldric Sr. (modulo 3, stanza 6)

Spettro del Magister Aldric Vellun originale, fondatore dell'Ordine della Chiave Spezzata. Le sue spoglie sono nella cella sigillata della cripta sotto Hawksbridge.

- **Dove:** Cofanetto di piombo nella stanza 6 della cripta (modulo 3). Si manifesta se il cofanetto è aperto.
- **Ruolo:** Fonte della localizzazione della Torre di Ashwick. Avverte sui pericoli del rituale.
- **Cosa sa:** Dove sono le ossa di Jason. La regola dell'Ordine (le anime sono sacre, serve pericolo reale). La Torre di Ashwick.
- **Come si comporta:** Pragmatico, diretto. Dà le informazioni necessarie e si dissolve. Non risponde più dopo la prima volta (Persuasione CD 18 per farlo ricomparire).

### Spettri dell'Ordine (modulo 5)

Tre spiriti dei membri più importanti dell'Ordine della Chiave Spezzata. Proteggono la legge dell'Ordine: nessuna dissoluzione senza necessità.

- **Dove:** Compaiono sulla scogliera della Torre di Ashwick se qualcuno tenta il rituale senza le condizioni (Presa < 6).
- **Ruolo:** Bloccano il rituale. Non combattibili. Possono rendere muto Aldric Jr come ultima risorsa.
- **Come si comportano:** Lenti, solenni, disapprovanti. Non attaccano per uccidere. Parlano poco e con autorità.

### Titus Gambasvelta (side quest, modulo 5)

Halfling corriere, nervoso e sudato. Deve consegnare un pacco sigillato a un alchimista ma viene attaccato ogni volta sulla strada. Non sa che il contenuto attira creature.

- **Dove:** Arriva dai PG ovunque si trovino.
- **Ruolo:** Quest giver della side quest "La Consegna Maledetta". Li accompagna nel viaggio.
- **Come si comporta:** Parla veloce, si guarda alle spalle, si asciuga la fronte. Più spaventato dell'Owlbear che dei lupi.

### Prosperus Fiaschetti (side quest, modulo 5)

Alchimista umano anziano in un villaggio a mezza giornata da Hawksbridge. Distratto, entusiasta, circondato da boccette e fumi.

- **Dove:** Villaggio a mezza giornata da Hawksbridge.
- **Ruolo:** Destinatario del pacco. Paga la ricompensa (pergamena + pozione).
- **Come si comporta:** Apre il pacco con gioia infantile. Paga senza discutere. Non capisce perché il corriere abbia avuto problemi ("Ma è solo un cristallino!").

### Mostri

- **Teppisti charmati** — servitori di Korex, gente del porto sotto incantesimo. → `MON_TeppistaCharmato.md`
- **Ratti corrotti** — ratti con occhi rossi e comportamento innaturale. → `MON_RattoCorrotto.md`
- **Sciame di ratti** — sciame nelle fogne. → `MON_SciameDiRatti.md`
- **Scheletri** — custodi della cripta. → `MON_Skeleton.md`
- **Ghast** — capo custode della cripta. → `MON_Ghast.md`
- **Specter** — entità sigillata nel cofanetto. → `MON_Specter.md`

## Luoghi

| Luogo | Descrizione | Moduli |
|-------|-------------|--------|
| **Greyhawkins** | Città portuale sul mare (sud), ambientazione generale | tutti |
| **Oakshore** | Quartiere portuale di Greyhawkins. Moli, magazzini, odore di pesce e guai | 1-2 |
| **Pint Ahoy** | Taverna di Barney Mezzapinta a Greyhawkins. Base operativa dei PG | 3 |
| **Fogne sotto Oakshore** | Tunnel in mattoni → sezione antica in pietra. Più grandi e antiche di quanto dovrebbero | 1-2 |
| **Tana di Korex** | Fondo delle fogne antiche. Rifugio improvvisato con bottino rubato | 2 |
| **Hawksbridge** | Città mercantile a 1 giornata dal mare (nell'entroterra, nord di Greyhawkins). Ponte di pietra, quartieri ordinati. | 3-5 |
| **Cripta sotto Hawksbridge** | Antico rifugio dell'Ordine della Chiave Spezzata. Scheletri, Chef Morticcio, registro dei sigilli | 3 |
| **Torre di Vellun** | Torre bassa a due piani, periferia di Hawksbridge. Casa/laboratorio di Aldric | 3-5 |
| **Torre di Ashwick** | Costa nord-ovest, 3 giorni da Hawksbridge (1 giorno al mare + 2 giorni lungo la costa). In rovine. Sede dell'Ordine. Scheletro di Jason. | 4-5 |

## Struttura dell'avventura

| # | nome | tipo | file |
|---|------|------|------|
| 1 | Discesa nelle Fogne | dungeon / esplorazione | [01_DiscesaNelleFogne/DiscesaNelleFogne.md](01_DiscesaNelleFogne/DiscesaNelleFogne.md) |
| 2 | Tana di Korex | dungeon / scontro finale | [02_TanaDiKorex/TanaDiKorex.md](02_TanaDiKorex/TanaDiKorex.md) |
| 3 | La Cripta sotto la Taverna | dungeon / esplorazione + roleplay | [03_LaCriptaSottoLaTaverna/LaCriptaSottoLaTaverna.md](03_LaCriptaSottoLaTaverna/LaCriptaSottoLaTaverna.md) |
| 4 | La Torre di Ashwick | dungeon / esplorazione + finale | [04_LaTorreDiAshwick/LaTorreDiAshwick.md](04_LaTorreDiAshwick/LaTorreDiAshwick.md) |
| 5 | Le Anime Sacre | roleplay / combattimento + scelta | [05_LeAnimeSacre/LeAnimeSacre.md](05_LeAnimeSacre/LeAnimeSacre.md) |

---

## Appendice: Cheat Sheet Anello del Virtuoso

Riferimento rapido per il DM. Dettagli completi in `NPC_JasonAccordion.md` e `DiscussioneNarrativa.md`.

**Aspetto**: anello d'argento annerito, incisione ouroboros musicale. È al dito di Korex.

### Attivazione: 3 livelli

1. **Attrazione** (passiva, narrativa): quando Korex cade, chiunque veda l'anello sente curiosità. Nessun tiro.
2. **Tocco**: chi tocca l'anello → TS Saggezza CD 20. Fallimento = obbligato a indossarlo. Successo = riesce a posarlo, attrazione resta.
3. **Indossato**: l'anello si stringe, non si toglie. Sintonia automatica.

### Effetti immediati

| vantaggi | malus |
|----------|-------|
| +2 a una caratteristica (per classe) | L'anello non si toglie |
| 1 cantrip da bardo 1/giorno senza slot (fisso per classe, vedi `OBJ_AnelloDelVirtuoso.md`) | Incubi la prima notte (niente riposo lungo) |
| Vantaggio TS contro charm | Freddo costante alla mano |
| Jason può offrire un suo incantesimo da bardo lv1-5 (sceglie lui quale e quando — Presa +1) | Vulnerabilità danni psichici |

### Possessione: meccanica della Presa

**Scala: 0-10.** La Presa misura quanto Jason è intrecciato al portatore.

| Presa | Stato | Effetto |
|-------|-------|---------|
| 0 | Indossato | Freddo alla mano, incubi, vulnerabilità danni psichici. L'anello non si toglie. |
| 1-4 | Sussurri | Jason parla, suggerisce, ricatta. Incubi ogni notte: TS Sag CD 15, fallimento = 1 livello exhaustion (prima notte automatica, niente TS). Nessun effetto meccanico aggiuntivo. |
| 5-8 | Influenza | Jason può tentare di prendere il controllo all'inizio di un combattimento o prima di una decisione importante (TS Sag CD 10+Presa). Visioni involontarie. |
| 9 | Dominio | Jason tenta di prendere il controllo 1/giorno (TS Sag CD 10+Presa per resistere). Se fallisce il TS: Jason controlla il personaggio. Il portatore può ripetere il TS durante un riposo breve. Il controllo termina automaticamente durante un riposo lungo. Dolore fisico per forzarlo fuori. Il portatore perde ricordi dei momenti di possessione. |
| 10 | Punto di non ritorno | Jason non esce più. Il rituale a questo livello infligge 10d6 danni psichici al portatore (nessun TS). |

**Come sale la Presa:**

| Evento | Presa |
|--------|-------|
| Cedere a una richiesta di Jason (lasciarlo uscire, fare qualcosa per lui) | +1 |
| Usare il potere minore dell'anello (cantrip da bardo per classe, vedi `OBJ_AnelloDelVirtuoso.md`) | +1 (solo su risultato 1 al d8) |
| Lasciare che Jason usi un suo incantesimo da bardo attraverso il portatore (Jason sceglie quale, lv1-5) | +1 |
| Credere a un'influenza di Jason / agire sulla base di una sua menzogna | +1 |

**Esempi di menzogne di Jason** (il DM sceglie quando inserirle):

| Menzogna | Contesto | Perché il portatore ci casca |
|----------|----------|------------------------------|
| *"Quel tipo mente. Lo sento dalla voce."* | NPC alleato che dà informazioni vere | Jason vuole isolare il portatore dal gruppo |
| *"L'anello ti protegge. Senza di me saresti già morto nella cripta."* | Dopo un combattimento vinto | Crea dipendenza psicologica |
| *"Io ero come te. Mi hanno tradito. Non fidarti del mago."* | Quando i PG vanno da Vellun | Sabota il rituale di rimozione |
| *"Se mi togli, muori anche tu. Siamo legati."* | Quando il portatore parla di rimuovere l'anello | Falso — ma il portatore non può verificarlo |
| *"Ti ho salvato stanotte. Non te ne sei accorto, ma qualcosa è entrato nella stanza."* | Al mattino dopo un riposo | Crea gratitudine per qualcosa che non è successo |
| *"Sento un pericolo avanti. Lasciami guardare."* | Prima di una stanza/porta | Pretesto per prendere il controllo |

**Come scende la Presa:**

| Evento | Presa |
|--------|-------|
| Resistere a una tentazione di Jason in un momento critico (TS Sag riuscito quando Jason offre aiuto in combattimento) | -1 |
| Rituale di Vellun — riduzione Presa (costo: 30 mo × Presa attuale, richiede 1 giorno) | -1 |
| Musica dissonante suonata vicino al portatore (Jason era un bardo, la stonatura lo destabilizza) | -1 |
| Pronunciare il nome completo di Jason ad alta voce (forza Jason fuori per 1d4 ore) | -1 (solo la prima volta) |
| *Lesser Restoration* | -1 |
| *Greater Restoration* | -2 |

**Soglia per il rituale di dissoluzione:** Presa deve essere ≥ 6. Sotto il 6, il rituale fallisce — non c'è abbastanza legame da spezzare, il portatore non è in pericolo reale. A Presa 10: il rituale infligge 10d6 danni psichici al portatore (nessun TS).

**I tre rituali di Vellun** (sono cose diverse):

| Rituale | Effetto | Costo | Note |
|---------|---------|-------|------|
| Rituale del sonno | Protegge dagli incubi per 1d6+1 giorni. Il portatore può dormire. | Vedi tabella sotto | Funziona solo a Presa 1-4. A Presa 5+ non ha effetto. |

**Scala del rituale del sonno:**

| # | Costo | Tempo di esecuzione |
|---|-------|---------------------|
| 1ª volta | 3 mo | Qualche minuto |
| 2ª volta | 30 mo | Un'ora |
| 3ª volta | 300 mo | Molte ore |
| 4ª volta | 3.000 mo | Qualche giorno |
| 5ª volta | 30.000 mo | Una settimana |
| Rituale di riduzione Presa | Presa -1 | 30 mo × Presa attuale, 1 giorno | Richiede componenti e studio |
| Rituale di dissoluzione | Distrugge Jason definitivamente | Ossa + anello + fuoco + parole + rituale dal pavimento | Richiede Presa ≥ 6. Serve essere mago + settimane di studio per capire il rituale. |

**Stato attuale:** La Presa parte da 1 per imposizione narrativa (Jason esce per 1 minuto senza che il portatore possa impedirlo, per introdurre la meccanica della possessione al tavolo).

**Ricatto di Jason:** Jason usa la Presa come leva. A Presa 1-4 ricatta con l'insonnia ("fammi uscire o non dormi"). A Presa 5+ offre aiuto in combattimento ("lasciami combattere per te, sei in pericolo"). Ogni cedimento è +1. Il giocatore deve scegliere: soffrire o cedere.

### Rimozione

*Remove Curse* allenta l'anello per 1d4 ore, poi torna. Rimozione definitiva: trovare lo scheletro di Jason + bruciarlo con sale + mago che conosce il rituale originale.

### Piano A vs Piano B

- **A** (PG tocca): possessione progressiva del PG.
- **B variante** (Fin tocca): SAG 10, Jason lo possiede facilmente.
- **B base** (nessuno tocca): guardia lo indossa → attacco → i PG la sconfiggono → l'anello resta.

**"Libero"** = nuovo ospite senza difese, non uscita dall'anello. Korex sapeva resistergli.

---

## Appendice: Simulazione progressione Presa

Stima del ritmo di crescita della Presa, assumendo:
- 1 combattimento per modulo
- 3 usi del cantrip per modulo
- Il giocatore cede all'insonnia ~1 volta ogni 2 moduli
- Il giocatore accetta il potere maggiore di Jason ~1 volta ogni 2 moduli

### Fonti di aumento per modulo

| Fonte | Presa | Frequenza media | Media/modulo |
|-------|-------|-----------------|--------------|
| Cantrip (risultato 1 al d8, su 3 usi) | +1 | P(almeno un 1) = 1-(7/8)³ ≈ 33% | +0.33 |
| Cedere all'insonnia (TS Sag CD 15 fallito, cedere a Jason per dormire) | +1 | ~1 ogni 2 moduli | +0.5 |
| Potere maggiore (Jason lancia spell) | +1 | ~1 ogni 2 moduli | +0.5 |
| Menzogne di Jason / eventi narrativi | +1 | ~1 ogni 2 moduli | +0.5 |

**Media Presa 1-4:** ~1.8/modulo (tutte le fonti attive)
**Media Presa 5+:** ~1.3/modulo (gli incubi cessano, fonte insonnia sparisce)
**Se i PG accelerano volontariamente** (dopo modulo 5, sanno che serve ≥6): possono cedere a Jason deliberatamente, +2-3/modulo.

### Progressione stimata

| Modulo | Presa inizio | Presa fine | Fase | Note |
|--------|-------------|------------|------|------|
| 4 | 1 | ~2 | Sussurri | |
| 5 | 2 | ~4 | Sussurri | Viaggio lungo (più notti = più incubi) |
| 6 | 4 | ~6 | Sussurri → Influenza | Se accelerano: raggiungibile in 1 modulo |
| 7 | 6 | ~7 | Influenza | Rituale possibile! |
| 8 | 7 | ~8 | Influenza | |
| 9 | 8 | ~9 | Influenza → Dominio | |
| 10 | 9 | 10 | Dominio → Punto di non ritorno | |

### Finestra per il rituale di dissoluzione

Con soglia ≥ 6, il rituale diventa possibile intorno al **modulo 6-7**. Dopo il modulo 5 i PG sanno che devono arrivare a Presa 6 — possono accelerare volontariamente. Se accelerano, il rituale è possibile già al modulo 6.

Se i PG riducono la Presa (rituale di Vellun -1, Lesser Restoration -1), ritardano il momento — ma si proteggono dal Dominio.

### Conclusione

La saga ha una tensione narrativa a doppio taglio: la Presa deve salire per permettere il rituale, ma salire troppo è pericoloso. Il DM può accelerare con eventi narrativi (+1 Presa) o rallentare con rituali di Vellun. Il punto critico è Presa 6-7: abbastanza per il rituale, non ancora Dominio (9).