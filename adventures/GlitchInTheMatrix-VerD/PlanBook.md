# PlanBook — Glitch in the Matrix (VerD)

## Stato del progetto

- [x] Struttura directory e manifest
- [x] README, AdventureBook, PlanBook
- [x] Documento principale (GlitchInTheMatrix-VerD.md) con Lore, NPC, Luoghi, Struttura, Appendice Background PG
- [x] Moduli 00-17 in formato avventura giocabile
- [x] Stat block PG: John Connor (other/pg/PG_JohnConnor.md + PDF)
- [x] Script stat block Carbon 2185 (tech/fightclub/carbon-statblock-pdf.js)
- [x] Copertina con autore e licenza OGL
- [x] Sito FAQ (docs/) con NPC, Luoghi, Fazioni, Piste aperte, PG
- [x] Carbon 2185 rulebook indicizzato (tech/data/compendium/Sources/Carbon2185/)
- [x] Pubblicato in public/
- [ ] Stat block PG: Glitch, T.S. Eliot, Kruna, Nyx
- [ ] Schede NPC principali (characters/markdown/)
- [ ] Bilanciamento incontri (tabelle Nemici con CR Carbon 2185)
- [ ] Mappe

## Approccio

Ogni modulo della versione narrativa (GlitchInTheMatrix) viene riscritto come modulo giocabile:
1. **Descrizione** — setting, contesto, cosa succede (istruzioni DM, non prosa)
2. **Obiettivo** — cosa devono fare i PG
3. **Incontri** — nemici, CD, meccaniche
4. **Ricompense** — Wonlongs, oggetti, informazioni, alleati
5. **Note al master** — come gestire NPC, scelte dei giocatori, complicazioni

## Note

- Il documento principale può essere condiviso con la versione base (stessi NPC, Luoghi, Struttura) con aggiunta di dettagli meccanici.
- I moduli sono il vero lavoro: trasformare ogni episodio narrativo in qualcosa di giocabile al tavolo.

## Sito FAQ (docs/)

Sito statico HTML+JS hostato su GitHub Pages dalla directory `docs/`. Navigabile per sezioni: Riassunto, NPC, Luoghi, Fazioni, Piste Aperte, PG. Ricerca testuale.

### Da valutare (NEXT)

- **Accesso giocatori e spoiler:** decidere se il sito deve essere visibile ai giocatori o solo al DM. Se visibile, implementare un sistema di sezioni nascoste (piste aperte, segreti NPC). Possibile soluzione: due viste (giocatore/DM) con toggle o URL separati.
- **Hosting separato:** il sito è nella directory `docs/` dello stesso repo delle avventure. Valutare se spostarlo in un repo dedicato (es. `dnd-faq`) per separare contenuto pubblico da sorgenti.
- **Estensione ad altre avventure:** se il formato funziona, valutare di generare automaticamente il `data.js` dal documento principale dell'avventura (script di export).
