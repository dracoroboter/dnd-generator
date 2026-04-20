# PlanBook — L'Anello del Conte

*Documento di lavoro: stato del progetto, idee, problemi aperti.*

---

## Relazione con Il Re Spezzato

L'Anello del Conte è il prologo umoristico di Il Re Spezzato. Stesso mondo, stesso cast di base, tono opposto. Il passaggio di tono è il colpo di scena finale: la morte del Conte nell'ultima puntata non è comica — è il momento in cui la commedia finisce e inizia la storia seria.

---

## Stato del progetto

### Fatto

- [x] Documento principale (`LAnelloDelConte.md`)
- [x] Puntata 1: Le Fogne di Fianus (`01_LeFogneDiFianus/`)
- [x] Schede NPC: Sir Gorim Vel, Il Conte, Sergius Sottobancus, Domina Lella
- [x] Mappe: regione, borgo, fogne
- [x] Artwork: 3 PG (Maria Biscanna, Gin Tonica, Pipinius Chennedius) + Sir Gorim Vel + copertina

### Da fare

- [ ] Definire il quarto PG
- [ ] Puntata 2: La Festa del Borgo — gare, bancarelle, l'anello di cipolla, incidente diplomatico di Pipinius
- [ ] Puntata 3: Il Rivale — gruppo di avventurieri rivali incompetenti
- [ ] Puntata 4: La Pista Vera (forse) — mercante di anelli contraffatti, indizio reale non riconosciuto
- [ ] Puntata 5: Il Finale — rivelazione dell'Anello, del Conte, cambio di tono verso Il Re Spezzato
- [ ] Definire cosa sia davvero l'Anello e perché la rivelazione finale è soddisfacente
- [ ] Definire l'esclamazione ricorrente del borgo (equivalente di "Daje!")
- [ ] Definire l'equivalente fantasy di "Smarmella tutto"
- [ ] Tabella complicazioni random per sessione

---

## Problemi aperti — Puntata 1

1. **La lettera nella stanza 5**: il cattivo misterioso (Sergius) ha trovato l'Anello e lasciato una caccia al tesoro. Va definito meglio cosa vuole e come ha saputo dell'Anello.
2. **Due incontri sociali di fila** (stanza 1 e 2): Ratti + Ermolao sono entrambi dialogo. Valutare se invertire stanza 2 e 3.
3. **Grunzio è troppo pericoloso**: anche con 30 PF, un Ogre fa 2d8+4 — one-shot su PG lv1. Abbassare il danno o rendere esplicito che non colpisce per uccidere.
4. **Manca un motivo per cui i PG accettano**: Gorim dice "ordine del Conte" ma i PG non lavorano per lui. La trattativa sul compenso è il motivo, ma va reso più esplicito.

---

## NPC da creare (ispirati a Boris)

- **Equivalente di Biascica**: qualcuno che parla in modo incomprensibile ma ha sempre ragione
- **Equivalente di Alessandro/Lopez**: nobile/funzionario che non capisce nulla ma ha il potere decisionale
- **Equivalente di Itala**: la vecchia del borgo che sa tutto di tutti
- **Equivalente di Arianna**: libero, non ancora assegnato

---

## Idee sparse

- Pochi combattimenti, molti skill check sociali (Persuasion, Deception, Performance)
- Complicazioni da tabella random per ogni puntata
- Niente morte dei PG — al massimo conseguenze comiche
- **Ermolao "Il Profondo"**: NPC ricorrente trovato in posti improbabili in ogni puntata
- **I Ratti Sindacalizzati**: running gag, tornano a protestare in piazza alla Festa del Raccolto
- **Grunzio**: potrebbe tornare come alleato improbabile nelle puntate successive
- **La canzone del borgo**: equivalente della sigla di Boris, filastrocca che tutti cantano

---

## Il cattivo misterioso — Sergius Sottobancus (da sviluppare)

Ha trovato l'Anello nelle fogne prima dei PG e lo usa per una vendetta contro il Conte. Da definire:
- In che modo è stato fregato dal Conte
- Quali traffici illeciti ha nelle fogne
- Come i PG scoprono la sua esistenza (quale puntata?)
- Chi o cosa causa l'esplosione finale

---

*Ultimo aggiornamento: Aprile 2026*

---

## TODO — PDF avventura (create-pdf-adventure)

### Cover
- [ ] La cover (`LAnelloDelConte_COVER.png`) è landscape 1408x768px — serve portrait per A4. Lo script dovrebbe adattare l'immagine: aggiungere bande nere/sfondo, centrare, sovrapporre titolo. Da implementare nello script come trasformazione automatica per cover non-portrait.

### Mappe nel PDF
- [ ] Le mappe PNG del modulo (`01_LeFogneDiFianus/maps/LeFogneDiFianus.png`, `LeFogneDiFianusAlt.png`) non sono incluse nel PDF — lo script include solo `MappaDM.md`, non mappe grafiche. Aggiungere supporto per includere PNG dalle directory `maps/` dei moduli.
- [ ] Mappe generali (`maps/FianusRomanus.png`, `maps/RealmOfAmrog.png`) non incluse — decidere se servono nel PDF

### Stat block
- [ ] Stat block con naming non-standard (`Barbara_GM.png`, `Maria_Biscanna_GM.png`) esclusi — rinominarli con prefisso `NPC_`/`PG_` per seguire la convenzione

### Schede mappa DM
- [ ] Nessun `MappaDM.md` per il modulo 01 — creare se serve per sessioni dal vivo
