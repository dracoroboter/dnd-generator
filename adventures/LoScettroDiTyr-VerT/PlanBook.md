# PlanBook — Lo Scettro di Tyr (VerT)

## Stato del progetto

- [x] Scaffolding struttura directory
- [x] Normalizzazione Modulo A da variante G 2.2
- [x] Copia Moduli B/C/D da LoScettroDityr
- [ ] Uniformare Moduli B/C/D alle differenze del Modulo A VerT
- [ ] Traduzione inglese
- [ ] Verifica con check-adventure.py (zero errori)

## Prossimo passo — Condivisione asset

Dopo il porting dei contenuti, trattare LoScettroDiTyr-VerT come **variante** di LoScettroDityr: le immagini (mappe, characters/img, cover) e altri file pesanti non devono essere duplicati ma condivisi (symlink o directory comune). Obiettivo: ridurre l'occupazione complessiva del progetto.

Opzioni da valutare:
- Symlink delle directory `maps/`, `characters/img/`, `img/` verso LoScettroDityr
- Directory condivisa esterna (es. `adventures/_shared/LoScettroDityr-assets/`)
- Convenzione nel manifest.json (`"shares_assets_with": "LoScettroDityr"`)
- Aggiornare check-adventure.py per accettare il pattern `PascalCase-VerX` senza errore di naming

### Sovrapposizioni (immagini diverse/aggiuntive/in meno)

Quando la variante ha bisogno di immagini diverse dal padre (es. `LabirintoDiVecna.png` nel padre → `LabirintoDiDispater.png` nella VerT, oppure immagini aggiuntive o da escludere):

Opzioni da valutare:
- **Override locale:** la variante mette il file nella propria directory `maps/` → rimuove `maps` da `shared_from_parent` (ma perde TUTTE le mappe condivise, deve copiarle tutte)
- **Override parziale:** `resolve_asset_dir` cerca prima nella variante, poi nel padre. Se il file esiste localmente usa quello, altrimenti fallback al padre. Richiede modifica a `resolve_asset_dir` per lavorare a livello di singolo file, non di directory intera.
- **Lista esclusioni nel manifest:** `"exclude_from_parent": ["maps/LabirintoDiVecna.png"]` + file locali per le sostituzioni
- **Alias nel manifest:** `"asset_aliases": {"maps/LabirintoDiVecna.png": "maps/LabirintoDiDispater.png"}` — la variante usa un nome diverso per lo stesso slot

Da decidere quale approccio. L'override parziale (cerca prima locale, poi padre) è il più flessibile e richiede meno configurazione manuale.

## Problemi aperti

### Cosa è successo al tavolo (formalizzato)

Sequenza confermata:

1. PG rapiti, collari, lanciati sull'isola
2. Esplorano le fazioni, trovano la pergamena nel castro
3. Vanno alla Torre di Torth, completano il rituale, aprono il portale
4. **Rifiutano il patto con Dispater**
5. Rivelano ai capi dell'isola (Wildforge + altri) come uscire tramite il portale
6. Usano la pergamena di messaggio per avvertire Malebranche
7. Malebranche indica il punto di recupero
8. **Retcon:** escono da dove sono entrati (porta nella cupola), con il permesso della guardia di Malebranche. Vengono recuperati lì (da decidere: barca o nave volante)
9. Collari rimossi durante il recupero. Portati al palazzo di Malebranche sul continente
10. Consegnano la pergamena. Malebranche vuole tenerla per mostrarla ai vassalli (potere politico)
11. Dal portale della Torre arrivano Wildforge e i capi di Orcastle
12. I PG scelgono di attaccare (potevano andarsene)
13. Malebranche fugge con portale dimensionale ("ci rivedremo") — protezione narrativa
14. Palazzo consegnato a Wildforge

**Decisioni prese:**
- Zikle: saltato. Le immagini (`Mappa_zikle_DM.png`) restano come possibile approfondimento futuro
- Uscita dall'isola: retcon — escono dalla porta nella cupola (da dove sono entrati), non dal portale della Torre né da grotta/insenatura
- Dispater: ha usato i PG per eliminare Malebranche senza che lo sapessero (i corvi/IMP li hanno spiati). Aggancio per modulo B
- Malebranche: fuggito, non morto. Torna nel modulo D

**Domande ancora aperte:**

- Punto di recupero: barca o nave volante? (da decidere)
- Zikle: se in futuro si vuole aggiungere, scrivere la scena. Mappa DM esiste in legacy (`Mappa_zikle_DM.png`)

### Conseguenze per i moduli successivi

- **Modulo B — Nessun patto con Dispater:** non c'è debito, Dispater non può ordinare nulla. Serve un aggancio alternativo. Proposta: Dispater li contatta comunque (sogno) come manipolatore/datore di lavoro, non come creditore. Tabella d6 maledizioni come pressione se rifiutano.
- **Modulo D — Malebranche morto:** il modulo D si basa sul ritorno di Malebranche come antagonista. Con Malebranche ucciso nel modulo A, serve un antagonista sostitutivo. Opzioni da valutare:
  - Un vassallo di Malebranche prende il suo posto
  - Malebranche ritorna come non morto (coerente col tema necromante)
  - Altro antagonista completamente diverso
- **Kurzum:** non presente nel modulo A della VerT. Se serve nel modulo D, va introdotta lì.

### Vecna → Dispater (completato)

### Checkpoint narrativi (regola di design)

Per evitare l'esplosione combinatoriale delle scelte, ogni modulo parte da uno **stato garantito** (checkpoint). Il modulo non gestisce tutte le varianti di come ci si è arrivati — assume il checkpoint e basta. Le varianti vanno solo nel preludio (1-2 paragrafi adattabili dal DM). Prerequisito implicito: i PG sono vivi.

| Checkpoint | Stato garantito | Tra |
|-----------|----------------|-----|
| **C1** | I PG sono sul continente, liberi dai collari, con 2500 mo. Malebranche è fuggito. Wildforge controlla il palazzo. Dispater li ha osservati. | Fine Mod A → Inizio Mod B |
| **C2** | I PG hanno lo Scettro (o l'hanno distrutto/consegnato). Dispater è stato servito o sfidato. Alaric è sconfitto. | Fine Mod B → Inizio Mod C |
| **C3** | Lo Scettro è stato riconsegnato a Tyr (o distrutto). Othran è sconfitto. I PG tornano verso sud. | Fine Mod C → Inizio Mod D |
| **C4** | Malebranche è sconfitto definitivamente. La maledizione è spezzata. | Fine Mod D |

**Regole:**
- Ogni modulo assume il checkpoint di ingresso senza spiegare come ci si è arrivati
- Il preludio del modulo gestisce le varianti con "se X / se Y" in 1-2 paragrafi — poi converge
- Se la partita giocata non porta al checkpoint (es. TPK, scelta radicalmente diversa), il DM adatta — ma il modulo scritto non cambia

- Il Modulo A VerT usa **Dispater** nella Torre di Torth, mentre la versione Draco usa **Vecna**. I moduli B/C/D fanno riferimento a Vecna. Serve decidere se uniformare tutto a Dispater o mantenere Vecna nei moduli successivi.
- Il palazzo di Malebranche è nel Modulo A (VerT) ma anche nel Modulo D (Draco). Serve decidere se rimuoverlo dal D o se il D ha un secondo confronto con Malebranche.
- Il livello di partenza è 7 (VerT) vs 8 (Draco). I moduli B/C/D sono calibrati per lv9-10. Serve una milestone nel Modulo A per portare i PG a lv8-9 prima del Modulo B.

## Note sulla variante G 2.2

- Fonte: PDF 21 pagine, datato 10 febbraio 2025
- Avventura per 5-6 PG di livello 7
- Include il palazzo di Malebranche come finale (non presente nella versione Draco del modulo A)
- Personaggi: Frankie Partenope, Lord Cedric Malebranche, Malachias Ombrascura, Axel Ruby, Miranda Emerald, Kreig Wildforge, Mesusu Merconè, Dispater, Zikzle l'Illuminato
