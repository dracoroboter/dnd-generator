# Fuori da Hellfire

## Lore

Greyhawkins è una città portuale dove il bizzarro è la norma — ma nessuno si aspettava quello che è successo ai moli di Oakshore. Una serie di omicidi, ratti corrotti ovunque, e dietro a tutto un elfo dal sorriso troppo largo e una melodia che ti entrava nella testa: **Korex**.

La compagnia lo ha smascherato, ha sconfitto i suoi ratti, e lo ha messo in fuga. Korex è scappato nelle fogne sotto i moli — fogne che nessuno sapeva esistessero. La Guardia di Oakshore non ha le risorse per inseguirlo nel sottosuolo. Tocca alla compagnia.

## Introduzione

> La pioggia batte sui moli di Oakshore. Lo sceriffo Udo Hutchinson vi guarda con un misto di gratitudine e impazienza. "È scappato nelle fogne. Quelle vecchie, sotto il molo est — non sapevamo nemmeno che fossero ancora aperte." Controlla la spada al fianco. "Vengo con voi. Portatelo su. Vivo o morto, non mi importa. Basta che non torni."

I PG hanno appena finito lo scontro con i ratti. Korex è fuggito attraverso una grata nel pavimento del magazzino ai moli. Udo, appena tornato a Oakshore da un viaggio personale, si è trovato il quartiere nel caos e non ha intenzione di mandare gente nelle fogne senza andarci lui stesso.

## Plot generale

- **Atto 1 — La discesa**: i PG entrano nelle fogne inseguendo Korex. Tunnel bui, trappole lasciate da Korex per rallentarli, servitori rimasti a coprire la fuga. L'ambiente diventa progressivamente più strano — le fogne sono più antiche e più grandi di quanto dovrebbero essere.
- **Atto 2 — La tana**: i PG raggiungono il rifugio di Korex. Scontro finale con il bardo e i suoi ultimi difensori. Korex può essere catturato vivo (se i PG resistono al charm) o ucciso.
- **Atto 3 — La scoperta**: risolta la questione Korex, i PG trovano l'Anello del Virtuoso al suo dito — un artefatto maledetto che contiene l'anima di un bardo antico. Chi lo tocca rischia di indossarlo. Chi lo indossa guadagna potere, ma inizia a essere posseduto. Se nessun PG lo tocca, una guardia lo indossa e il problema esplode comunque.

## Consigli al master

- **Tono**: mantenere il camp dello starter kit. Korex è teatrale, i ratti sono grotteschi, le fogne sono esagerate. Ma il cliffhanger finale deve avere un cambio di registro — il momento in cui la commedia si ferma e i giocatori capiscono che c'è qualcosa di serio.
- **Korex in combattimento**: non combatte lealmente. Charma, scappa, manda avanti i servitori. Se messo alle strette, implora pietà — e mente.
- **Cattura vs uccisione**: entrambe le opzioni sono valide. Se catturato vivo, Korex può dare informazioni (vere e false mescolate). Se ucciso, le informazioni si trovano nei suoi appunti nella tana.
- **Il cliffhanger**: dopo la milestone, l'Anello del Virtuoso entra in gioco. L'anello era al dito di Korex — è l'origine del suo potere. Contiene l'anima di un bardo antico che vuole tornare in vita. Meccanica a tre livelli: attrazione passiva → tocco (TS Sag CD 20 o indossamento forzato) → possessione progressiva. Se nessun PG lo tocca, una guardia NPC lo indossa e attacca. Dettagli in `DiscussioneNarrativa.md`.

**Difficoltà consigliata:** 3 PG di livello 3 + Udo Hutchinson + Fin Ditasvelte (NPC companion)
**Scalabilità:** per 4+ PG, Udo resta indietro a sorvegliare l'ingresso e Fin non si unisce (il charm non si è ancora spezzato). Per 2 PG, tenere entrambi i companion.

## NPC principali

Schede complete in `characters/`.

- **Udo Hutchinson** — sceriffo di Oakshore, veterano. Si unisce ai PG all'ingresso delle fogne. Tank del gruppo.
- **Korex** — elfo bardo CE, antagonista. Charmer musicale, manipolatore, vigliacco.
- **Fin Ditasvelte** — halfling ladro CN, ex-charmato di Korex. Esce dalla fogna confuso e furioso, si unisce ai PG per vendetta. Portatore dell'anello (scenario B).
- **Jason Accordion** — bardo umano NM, anima nell'Anello del Virtuoso. Villain della saga.

Stat block teppisti charmati: vedi `MON_TeppistaCharmato.md`.

## Struttura dell'avventura

| # | nome | tipo | file |
|---|------|------|------|
| 1 | Discesa nelle Fogne | dungeon / esplorazione | [01_DiscesaNelleFogne/DiscesaNelleFogne.md](01_DiscesaNelleFogne/DiscesaNelleFogne.md) |
| 2 | Tana di Korex | dungeon / scontro finale | [02_TanaDiKorex/TanaDiKorex.md](02_TanaDiKorex/TanaDiKorex.md) |

## Agganci futuri

- L'Anello del Virtuoso → saga lv4-6: chi era il bardo nell'anello? Corsa contro il tempo per rimuoverlo prima della possessione totale
- Korex (se catturato vivo) → fonte di informazioni inaffidabili per avventure future
- Le fogne antiche → perché sono così grandi? Chi le ha costruite? Il passaggio nascosto nella tana porta più in profondità
- Il bardo nell'anello ha un piano proprio — non è un alleato

---

## Appendice — Cheat Sheet Anello del Virtuoso

Riferimento rapido per il DM. Dettagli completi in `NPC_JasonAccordion.md` e `DiscussioneNarrativa.md`.

**Aspetto**: anello d'argento annerito, incisione ouroboros musicale. È al dito di Korex.

### Attivazione — 3 livelli

1. **Attrazione** (passiva, narrativa): quando Korex cade, chiunque veda l'anello sente curiosità. Nessun tiro.
2. **Tocco**: chi tocca l'anello → TS Saggezza CD 20. Fallimento = obbligato a indossarlo. Successo = riesce a posarlo, attrazione resta.
3. **Indossato**: l'anello si stringe, non si toglie. Sintonia automatica.

### Effetti immediati

| vantaggi | malus |
|----------|-------|
| +2 a una caratteristica (per classe) | L'anello non si toglie |
| 1 incantesimo da bardo 1/giorno senza slot | Incubi la prima notte (niente riposo lungo) |
| Vantaggio TS contro charm | Freddo costante alla mano |
| | Vulnerabilità danni psichici |

### Possessione — tracciamento presa

Ogni uso dell'incantesimo 1/giorno → tira **d8**.
- **2-8**: funziona.
- **1**: fallisce + onda psichica 1d4+presa a tutti entro 10qd + presa +1.

| presa | narrativo | meccanico |
|-------|-----------|-----------|
| 0 | Freddo, incubi | Vulnerabilità psichica |
| 1-2 | Tic di Jason, sussurri rari | Onda 1d4+1/+2 |
| 3-4 | Jason parla spesso, ricordi altrui | Onda 1d4+3/+4, TS Sag CD 14 in stress |
| 5-6 | Jason prende il controllo 1d4 round | Onda 1d4+5/+6, TS Sag CD 15 |
| 7+ | Tentativo controllo permanente | Onda 1d4+7+, TS Sag CD 16+ |

**Ridurre presa**: TS Sag riuscito vs Jason (−1), *Lesser Restoration* (−1), *Greater Restoration* (−2).

### Rimozione

*Remove Curse* allenta l'anello per 1d4 ore, poi torna. Rimozione definitiva: trovare lo scheletro di Jason + bruciarlo con sale + mago che conosce il rituale originale.

### Piano A vs Piano B

- **A** (PG tocca): possessione progressiva del PG.
- **B variante** (Fin tocca): SAG 10, Jason lo possiede facilmente.
- **B base** (nessuno tocca): guardia lo indossa → attacco → i PG la sconfiggono → l'anello resta.

**"Libero"** = nuovo ospite senza difese, non uscita dall'anello. Korex sapeva resistergli.
