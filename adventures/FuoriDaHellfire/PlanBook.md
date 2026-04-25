# PlanBook — FuoriDaHellfire

## Concept

- **Tipo**: one-shot (1-2 sessioni), con semi per saga fino a lv6
- **Livello**: 3 (milestone → lv4)
- **Party**: 3 PG lv3 + Udo Hutchinson (veterano CR3) + Fin Ditasvelte (rogue lv3)
- **Tono**: pulp adventure, camp anni '80, coerente con lo starter kit "Welcome to the Hellfire Club"
- **Ambientazione**: fogne inesplorate sotto Oakshore Docks, Greyhawkins
- **Plot in breve**: la compagnia ha sconfitto i ratti e messo in fuga Korex (elfo bardo CE, charmer musicale) nelle fogne che partono dai moli di Oakshore. I PG lo inseguono per consegnarlo vivo o morto alle autorità. L'inseguimento li porta in una sezione inesplorata delle fogne. Catturare o uccidere Korex risolve il problema immediato, ma nel processo i PG scoprono qualcosa di molto più grande — cliffhanger stile Buffy/Supernatural che lancia la "stagione 2".

## Stato generale

- [x] README.md
- [x] documento principale (FuoriDaHellfire.md)
- [x] AdventureBook.md
- [x] mappa fogne (FogneDiOakshore.md)
- [x] modulo 01 — Discesa nelle Fogne + mappa DM
- [x] modulo 02 — Tana di Korex + mappa DM
- [x] NPC_Korex.md — antagonista, stat block completo
- [x] NPC_UdoHutchinson.md — sceriffo/veterano, companion del party
- [x] NPC_FinDitasvelte.md — rogue, ex-charmato di Korex, companion del party
- [x] NPC_JasonAccordion.md — entità nell'anello, villain della saga
- [x] MON_TeppistaCharmato.md — servitori charmati di Korex (basati su Cultista)
- [x] MON_RattoCorrotto.md — ratti corrotti (basati su Giant Rat)
- [x] MON_SciameDiRatti.md — sciame (basato su Swarm of Rats)
- [x] Stat block PNG/PDF per tutti i personaggi e mostri
- [x] XML FightClub per tutti
- [x] Cheat sheet anello nel documento principale
- [x] DiscussioneNarrativa.md con cheat sheet operativo anello
- [x] PDF generato (FuoriDaHellfire_20260425.pdf)

## Difficoltà incontri (3 PG lv3 + Udo + Fin = 5 combattenti)

| incontro | nemici | difficoltà |
|----------|--------|------------|
| Nido ratti (mod.01) | 6 ratti corrotti CR 1/8 + 1 sciame CR 1/4 | EASY |
| Tana Korex (mod.02) | Korex CR 3 + 2 teppisti CR 1/8 | HARD |

## Note

- Udo Hutchinson: sceriffo di Oakshore, si unisce ai PG all'ingresso. Veterano CR3, tank del gruppo.
- Fin Ditasvelte: esce dalla fogna confuso, ex-charmato di Korex, vuole vendetta. Portatore dell'anello (scenario B).
- Korex: flauto magico (arma), liuto nella tana è bottino rubato.
- Passaggio nascosto nella tana: Korex lo ha scoperto esplorando le fogne antiche.
- Il cliffhanger Piano A (PG indossa anello) è definito. Piano B (guardia → attacco) è definito.
- Punti aperti per la saga lv4-6: vedi NPC_JasonAccordion.md sezione "Punti aperti" e DiscussioneNarrativa.md

## Da fare

- [ ] Generare stat block per guardia posseduta (Piano B cliffhanger)
- [ ] Definire cliffhanger alternativo Piano B per la saga (dopo la guardia, l'anello resta — e poi?)
- [ ] Punti aperti saga: dove è lo scheletro di Jason, chi è il mago/ordine, soglia possessione permanente
- [ ] Rileggere il PDF generato (releases/FuoriDaHellfire/FuoriDaHellfire_20260425.pdf) e verificare impaginazione
- [ ] Valutare se il nido ratti EASY è troppo facile — eventualmente aggiungere 2 ratti o un secondo sciame
- [ ] Aggiornare `NPC_Korex.md`: togliere "liuto" dallo stat block se presente, confermare che l'arma è solo il flauto
- [ ] Decidere: Fin è sempre presente o è opzionale? (attualmente: sempre presente per 3 PG)
- [ ] Rigenerare stat block Fin/Korex se si modificano le schede (usare `generate-statblocks.py FuoriDaHellfire`)

## Log sessioni di lavoro

### 2026-04-25 (sessione Kiro)

**Fatto:**
- Validatore da 10 warning a 0: rinominato MappaGenerale.md → FogneDiOakshore.md, aggiornato KNOWN_NPC_SECTIONS, riorganizzato sezioni NPC (h2→h3)
- Creato NPC_UdoHutchinson.md (sceriffo, Veterano CR3, companion)
- Creato MON_TeppistaCharmato.md (Cultista CR 1/8, charmato)
- Creato MON_RattoCorrotto.md (Giant Rat CR 1/8) e MON_SciameDiRatti.md (Swarm CR 1/4)
- Riscritto moduli 1 e 2: stile discorsivo, meno prolisso, misure solo in mappa
- Fix buchi: flauto (arma) vs liuto (bottino), passaggio segreto (Korex lo ha scoperto esplorando), Fin ex-charmato di Korex
- Nido ratti: da 4×4 a 8×8 qd con coperture (tubi, grate, macerie). Mappa DM aggiornata.
- Aggiornato FuoriDaHellfire.md: Udo + Fin negli NPC, intro riscritta, scalabilità, cheat sheet anello in appendice
- Creato cheat sheet operativo anello in DiscussioneNarrativa.md
- Creato generate-statblocks.py (pipeline .md → .xml + .pdf + .png)
- Generati tutti gli stat block (7 schede: 4 NPC + 3 MON)
- Calcolate difficoltà: nido EASY, tana HARD (per 3 PG lv3 + Udo + Fin)
- Aggiornati PlanBook, AdventureBook, README, plan-meta-dnd.md, README root
- Aggiornato check-adventure.py: sezioni meccaniche NPC, prefissi documento principale
- Aggiunto todo in plan-meta-dnd.md: calcolo automatico difficoltà incontri
- PDF finale generato: FuoriDaHellfire_20260425.pdf (1.6 MB, 7 stat block)
