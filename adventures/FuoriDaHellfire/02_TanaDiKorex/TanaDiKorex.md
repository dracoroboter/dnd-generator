# Tana di Korex

## Descrizione

> Il tunnel si apre in una sala circolare, alta almeno sei metri. Al centro, una cisterna asciutta trasformata in un palcoscenico improvvisato: candele, tappeti rubati, strumenti musicali appoggiati alle pareti. E lì, seduto su una sedia come se vi stesse aspettando, c'è Korex. Sorride. Le sue dita sfiorano le corde di un liuto.
>
> "Ah, i miei fan preferiti. Accomodatevi — lo spettacolo sta per cominciare."

La tana di Korex è una cisterna antica riconvertita. Korex ha avuto tempo di prepararsi: il terreno è a suo vantaggio.

## Obiettivo

Catturare o uccidere Korex. Esplorare la tana dopo lo scontro.

## Luoghi interni

### La cisterna (arena principale)
- Sala circolare, 12m / 40ft / 8qd di diametro, soffitto a cupola.
- Korex al centro, su un rialzo di 1,5m / 5ft / 1qd (la vecchia cisterna). Copertura parziale dietro le colonne.
- Due servitori nascosti dietro le colonne laterali — si rivelano al primo round di combattimento.
- Possibile prova: Percezione CD 14 per notare i servitori prima che attacchino.

### L'alcova di Korex
- Dietro un tendaggio: un giaciglio, appunti sparsi, una cassa chiusa.
- Gli appunti sono in parte in Comune, in parte in un codice personale.
- Possibile prova: Indagare CD 12 per trovare gli appunti utili. Arcano CD 14 per decifrare il codice.
- La cassa contiene il bottino di Korex (monete, gioielli rubati).
- **L'Anello del Virtuoso** è al dito di Korex (vivo o morto), non nella cassa. Vedi sezione Finale.

### Il passaggio nascosto
- Dietro una colonna crollata, un tunnel stretto che prosegue più in profondità.
- Korex lo usa come via di fuga se le cose vanno male (Percezione CD 16 per trovarlo durante il combattimento, CD 12 dopo).
- Il tunnel prosegue nel buio. Non è mappato. Da qui parte la "stagione 2".

## Nemici

**Difficoltà incontro:** DEADLY (4 PG lv3) — calcolata con `encounter-difficulty.py`

| nome | numero | PF | CA | attacco | note |
|------|--------|----|----|---------|------|
| Korex | 1 | 52 | 13 | +5 2d4+3 perf. + 2d6 veleno / Flauto 4d6 psy CD12 Sag | vedi scheda `NPC_Korex.md` |
| Teppista charmato | 2 | 22 | 13 | +4 1d8+2 mazza | charmati da Korex, si arrendono se Korex cade |

### Tattiche di Korex
- **Round 1**: tenta di charmare il PG più pericoloso (guerriero/barbaro). I servitori escono dalle colonne.
- **Round 2-3**: usa incantesimi di controllo e si tiene a distanza. Manda avanti i servitori.
- **Se sotto metà PF**: implora pietà, offre informazioni, mente. Se i PG non abboccano, tenta la fuga verso il passaggio nascosto.
- **Se catturato**: collabora (a modo suo). Mescola verità e bugie. Conferma che "qualcuno più in alto" gli ha dato il compito di stabilirsi nelle fogne, ma non dice chi.

## Indizi chiave

1. Gli appunti di Korex — rivelano che non agiva da solo. Qualcuno (o qualcosa) gli ha dato il potere.
2. L'Anello del Virtuoso al dito di Korex — anello d'argento annerito con ouroboros musicale inciso. Emana un'attrazione sottile quando Korex cade.
3. Il passaggio nascosto — le fogne continuano. Molto più in profondità di quanto chiunque sospetti.

## Ricompense

- Bottino di Korex: 120 mo in monete e gioielli rubati
- Liuto di Korex (strumento musicale di qualità, non magico — o forse sì?)
- Taglia dalla Guardia di Oakshore: 50 mo per Korex (vivo: 75 mo)

## Milestone

- **Livello 4** dopo aver catturato o sconfitto Korex.

## Finale

### Se Korex è catturato vivo
> Lo trascinate fuori dalle fogne, le mani legate e la bocca imbavagliata — avete imparato la lezione. Il capitano della Guardia lo prende in consegna con un sorriso soddisfatto. "Ben fatto. Oakshore vi deve un favore."

Korex ha l'anello al dito. Se i PG lo notano (Percezione CD 10 — è vistoso), possono provare a toglierlo. L'anello scivola via facilmente dal dito di Korex (l'entità *vuole* cambiare ospite). Chi lo tocca: vedi cliffhanger.

### Se Korex è ucciso
> Il silenzio nelle fogne è quasi peggio della musica. Portate su le prove — gli appunti, il bottino, il liuto.

L'anello è al dito del cadavere. Si allenta da solo — l'entità cerca un nuovo ospite. L'attrazione (Livello 1) è attiva: chiunque veda l'anello sente un impulso sottile a prenderlo.

### Il cliffhanger — L'Anello del Virtuoso

**Se un PG tocca l'anello**: TS Saggezza CD 20. Fallimento: il PG è obbligato a indossarlo.

> Appena l'anello scivola al dito, il mondo si ferma per un istante. Un calore sale dal dito, al braccio, al petto. Poi una risata — bassa, profonda, soddisfatta — risuona nelle fogne. Non viene dall'anello. Viene da ovunque.
>
> *"Libero. Finalmente libero."*
>
> L'anello si stringe. Non si toglie più. E per un istante — solo un istante — vedete qualcosa nei vostri occhi riflessi in una pozza d'acqua. Non il vostro volto. Quello di qualcun altro. Che sorride.

**Effetti meccanici**: +2 Carisma (max 22), vantaggio ai TS contro charm. Maledizione: possessione progressiva (vedi `DiscussioneNarrativa.md`).

**Se nessun PG lo tocca**: l'anello viene consegnato alla Guardia con il bottino. Jason prende il controllo della guardia immediatamente — nessuna resistenza.

> Tornate alla superficie, consegnate Korex e il bottino. Il capitano della Guardia vi paga. Tutto sembra finito. Ma mentre vi allontanate dai moli, sentite un urlo dietro di voi. Vi girate: una delle guardie è in piedi, immobile, con l'anello al dito. I suoi occhi sono diversi. Sorride — un sorriso che non è il suo.
>
> *"Libero! Finalmente libero! E voi, feccia, scomparite prima che vi faccia scomparire dalla faccia della terra!"*
>
> La guardia estrae la spada.

In questo scenario la quest diventa combattere la guardia posseduta (guerriero con +2 FOR, *Heroism*). Dopo averla sconfitta, l'anello resta — e il problema con esso. Serve un nuovo cliffhanger per lanciare la saga (da definire).

## Note al master

- Lo scontro con Korex è il climax dell'avventura. Deve sentirsi come un boss fight, anche se Korex non è un combattente diretto — è un manipolatore.
- I teppisti charmati non sono malvagi: sono gente del porto che Korex ha incantato. Se Korex cade, si risvegliano confusi. Questo può creare un momento di roleplay interessante.
- Il cliffhanger deve arrivare DOPO la milestone, quando i giocatori si sentono soddisfatti. Il cambio di tono è intenzionale.
- Se Korex fugge nel passaggio nascosto, non inseguirlo in questa avventura — diventa un aggancio per la stagione 2.
- Il passaggio nascosto è il seme principale: dove porta? Chi ha costruito queste fogne? Perché Korex è stato mandato qui?
