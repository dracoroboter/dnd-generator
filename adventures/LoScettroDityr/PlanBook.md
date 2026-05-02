# PlanBook — Lo Scettro di Tyr

## Stato del progetto

### Fatto

- [x] Scaffolding directory
- [x] Documento principale (`LoScettroDityr.md`)
- [x] README.md
- [x] AdventureBook.md
- [x] PlanBook.md
- [x] Modulo A: Fuga da Orcastle — porting da .odt
- [x] Modulo B: Lo Scettro di Tyr — porting da .odt
- [x] Modulo C: Ritorno a Casa — porting da .odt
- [x] Modulo D: La fine non appartiene ai morti — porting da .odt
- [x] Schede NPC principali (15 schede)
- [x] Mappe DM (3 create: TorreDiTorth, TempioDiLumina, SantuarioDiOstegard)
- [x] Asset grafici copiati dal legacy (29 file)
- [x] Validazione con check-adventure.py (0 errori, 16 warning accettabili)

## Versione

Questa è la versione **"Draco"** — porting fedele del materiale legacy. Una versione **"Trust"** è prevista in futuro.

## TODO — Problemi dalla review (maggio 2026)

### Meccaniche — Difficoltà incontri

- [x] Ricalcolare difficoltà: Cultisti di Vecna Mod A (dichiarata MEDIUM, reale TRIVIAL)
- [x] Ricalcolare difficoltà: Diavoli barbuti Mod A (dichiarata HARD, reale MEDIUM/EASY)
- [x] Ricalcolare difficoltà: Diavolo delle catene Mod A (dichiarata DEADLY, reale EASY)
- [x] Ricalcolare difficoltà: Valle del Giudizio Mod B (dichiarata MEDIUM, reale TRIVIAL). Anche: "cultisti" è flavor sbagliato per paladini di Tyr
- [x] Ricalcolare difficoltà: Yeti Mod B (dichiarata HARD, reale EASY)
- [x] Ricalcolare difficoltà: Spettri sala 9 Mod B (dichiarata HARD, reale TRIVIAL)
- [x] Battaglia finale Mod B (15 veterani + Alaric): DEADLY estremo, quasi TPK. Aggiungere piano B meccanico se il roleplay fallisce

### Meccaniche — Stat block incompleti o errati

- [x] Alaric CA 15 non giustificata (DES +2 = CA 12). Aggiungere Mage Armor o abbassare
- [x] Frankie CA 17 non giustificata (Difesa Senza Armatura = 16). Aggiungere scudo o correggere
- [x] Frankie SAG 20 anomalo per barbaro. Scambiare FOR↔SAG o giustificare
- [x] Frankie PF 40 sotto media (barbaro lv5 COS +3 = media 47). Correggere e aggiungere formula dadi vita
- [x] Othran CA 15 non giustificata (DES +3 = CA 13). Aggiungere armatura leggera nella descrizione
- [x] Ombrascura: solo "usa Sacerdote MM", aggiungere stat block custom o varianti
- [x] Miranda: solo "usa Mago MM lv basso", definire livello e incantesimi
- [x] Assassini Emerald Mod A: PF/CA/attacco tutti "—". Aggiungere riferimento MM
- [x] Soldati Highlander Mod A: PF/CA/attacco tutti "—". Aggiungere riferimento MM
- [x] Golem sala 4 Mod B: nessuna difficoltà dichiarata
- [x] Mostri marini Mod C: tabella senza PF/CA/numero. Completare o rimuovere
- [x] Banditi Waterdeep Mod C: PF/CA vuoti

### Meccaniche — Regole ambigue

- [x] Collari esplosivi Mod A: 1 naturale = esplosione non è regola 5e per prove abilità. Dichiarare homebrew
- [x] Sala del Riflesso Mod A: doppi con "stessi poteri e PF dei PG" è ingestibile. Semplificare con stat fissi
- [x] Labirinto Mod A: 2d4+2 danni senza tipo né TS. Specificare (perforante, TS Des CD 12)
- [x] Sala 12 Mod B: Ormut guida i PG ma la benedizione si ottiene lì. Chiarire sequenza
- [x] Mal di mare Mod C: CD "pari alla condizione del mare" ma le condizioni sono testo. Aggiungere mappatura → CD
- [x] Giuramento Mod D: vulnerabilità non morti permanente, troppo potente. Aggiungere durata (24h o fine modulo)
- [x] Rituale Mod D: "assistita" non è termine 5e. Chiarire: due tiri separati, entrambi devono riuscire

### Contenuto — Buchi narrativi

- [x] Mod B: Vecna dice "date lo Scettro ad Alaric" ma vuole lo Scettro per sé. Spiegare che è un inganno (Alaric è corruttibile, Vecna lo usa come tramite)
- [x] Mod D: Frankie e Ombrascura "fuggiti da Orcastle" ma nel Mod A Frankie è con i PG. Chiarire nel preludio che si sono separati dopo la fuga
- [x] Mod D: Tungsten mai presentato prima. Aggiungere riga nel preludio o nel doc principale
- [x] Mod D: Zikle "mago lv15" → Wraith CR 5, riduzione enorme. Aggiungere nota: il rituale di Malebranche lo ha indebolito
- [ ] Mod B: Sala 11 mancante (numerazione salta da 10 a 12). Rinumerare o aggiungere sala
- [x] Mod A: Cultisti di Vecna troppo facili (TRIVIAL per lv8). Valutare se aggiungere nemici o sostituire con creature più forti
- [x] Mod A: Diavolo delle catene troppo facile (EASY per lv8). Rendere più difficile — aggiungere nemici o usare versione potenziata
- [x] Mod B: Valle del Giudizio troppo facile (TRIVIAL per lv9). Dovrebbe essere DEADLY, al limite del TPK — i Custodi sono guerrieri sacri, non cultisti. Sostituire stat block e aumentare numero
- [x] Mod B: Yeti troppo facili (EASY per lv9). Rendere più difficile — aggiungere Yeti o sostituire con Abominable Yeti CR 9
- [x] Mod B: Spettri sala 9 troppo facili (TRIVIAL per lv9). Valutare se rendere più difficile

### Formale — Naming e formato

- [x] Rinominare `labirintodivecna.png` → `LabirintoDiVecna.png`
- [x] Rinominare `laPergamenaDelGiudizio.png` → `LaPergamenaDelGiudizio.png`
- [x] Rinominare `Airborne_Machine.jpg` → `AirborneMachine.jpg`
- [x] Rinominare `MappaGenerale_County.png` → `OrcastleCounty.png` (nome deprecato)
- [x] Uniformare grafia Ablundt/Ablunth (immagine vs testo)
- [x] Aggiungere sezione `## Milestone` a tutti e 4 i moduli` a tutti e 4 i moduli
- [x] Creare schede NPC minime per: Tungsten, Orlomm Glittergear, Maestro Elrin, Halassiter Arlan
- [x] Uniformare distanze al formato "m / ft / qd" nei moduli
- [x] Allineamento mancante per Ludmilla Dawnshield e Zikle

## Idee per sviluppi futuri

- Creare una tabella riassuntiva degli NPC che attraversano più moduli con il loro stato in ogni modulo
- Definire le milestone di livello per ogni modulo (attualmente: A→lv9, B→lv10, C e D restano lv10?)
- Valutare se il Modulo A può funzionare come avventura standalone

### Ottimizzazione stampa (da fare)

Il PDF attuale è troppo lungo per la stampa. Due interventi:

1. **Stat block multi-colonna**: attualmente ogni stat block occupa una pagina intera. Servono 2 stat block per pagina (layout a 2 colonne) per gli NPC con stat block brevi. Richiede modifica a `md-to-statblock-pdf.js` o al CSS di `create-pdf-adventure.py` per l'appendice stat block.

2. **Testo più compatto**: i moduli sono prolissi — molte descrizioni possono essere accorciate senza perdere informazioni. Valutare:
   - Font più piccolo per le Note al master (già grigio nel CSS?)
   - Tabelle nemici più compatte (rimuovere colonne ridondanti)
   - Sezioni collassabili nel PDF (non possibile con weasyprint — alternativa: versione "DM screen" con solo tabelle e stat)

### Release bundle (da fare)

Una **release** è l'insieme taggato (con codice identificativo univoco, es. `v1.0_20260502`) delle versioni di tutti i file che compongono l'avventura:
- Compendium XML FightClub
- Mappe PNG (player + DM quando disponibili)
- PDF comprensivo (fullres + lowres)
- Opzionalmente: PDF diviso nelle sue parti (lore, sessioni numerate, appendice mappe/stat block)
- Stat block PNG stampabili

Una **pubblicazione** è lo ZIP di tutto ciò, in un formato directory predeterminato, messo in `public/` dove può essere committato.

Formato directory dello ZIP:

```
LoScettroDityr_v1.0_20260502.zip
├── LoScettroDityr_20260502.pdf              # PDF unico fullres (senza mappe PNG inline)
├── LoScettroDityr_20260502_lowres.pdf       # PDF unico lowres
├── LoScettroDityr_Compendium.xml            # FightClub import (tutti gli NPC/MON)
├── LoScettroDityr_COVER.png                 # Copertina (per thumbnail Roll20/siti)
├── README.txt                               # versione, data, contenuto, licenza
├── pdf/                                     # PDF divisi (opzionale)
│   ├── LoScettroDityr_Lore.pdf
│   ├── LoScettroDityr_01_FugaDaOrcastle.pdf
│   ├── LoScettroDityr_02_LoScettroDiTyr.pdf
│   ├── LoScettroDityr_03_RitornoACasa.pdf
│   ├── LoScettroDityr_04_LaFineNonAppartieneAiMorti.pdf
│   └── LoScettroDityr_Appendice.pdf         # stat block multi-colonna (quando implementato)
├── maps/                                    # mappe PNG (fuori dal PDF, non dentro)
│   ├── *_player.png                         # versioni player (quando disponibili)
│   └── *_dm.png                             # versioni DM
└── statblocks/                              # stat block PNG stampabili (singoli)
    ├── NPC_*.png
    └── MON_*.png
```

**Decisioni prese:**
- Le mappe PNG vanno fuori dal PDF (nella directory `maps/`), non inline. Opzionalmente includibili nel PDF con un flag.
- Gli stat block singoli sono solo PNG (no PDF singoli). Nel PDF unico, gli stat block vanno in appendice in formato multi-colonna (2 per pagina) — da implementare.
- La copertina va inclusa come file separato.
- I sorgenti .md, AdventureBook, PlanBook, XML singoli, immagini personaggi e file in other/ sono esclusi.

**TODO:**
- [ ] Creare script `release-bundle.py` che assembla lo ZIP
- [ ] Aggiungere flag `--no-maps` a `create-pdf-adventure.py` per escludere mappe PNG inline
- [ ] Implementare `--split` in `create-pdf-adventure.py` per generare PDF divisi (lore, sessioni, appendice)
- [ ] Implementare stat block multi-colonna nell'appendice PDF (2 per pagina)
- [ ] Definire il tag di versione (manuale nel PlanBook? campo nel README.md dell'avventura? tag git?)
- [x] Generalizzare le definizioni release/pubblicazione e il formato ZIP da LoScettroDityr a plan-meta-dnd.md (valgono per tutte le avventure)

### PDF multi-file (da valutare)

Valutare la fattibilità e l'utilità di generare il PDF dell'avventura diviso in più file separati anziché un unico PDF monolitico:

| File | Contenuto |
|------|-----------|
| `LoScettroDityr_Lore.pdf` | Documento principale: lore, trama, NPC, oggetti |
| `LoScettroDityr_01_FugaDaOrcastle.pdf` | Modulo A singolo |
| `LoScettroDityr_02_LoScettroDiTyr.pdf` | Modulo B singolo |
| `LoScettroDityr_03_RitornoACasa.pdf` | Modulo C singolo |
| `LoScettroDityr_04_LaFineNonAppartieneAiMorti.pdf` | Modulo D singolo |
| `LoScettroDityr_Mappe.pdf` | Tutte le mappe raccolte |
| `LoScettroDityr_StatBlock.pdf` | Tutti gli stat block raccolti |

**Pro**: più pratico al tavolo (apri solo il modulo che stai giocando), stat block stampabili separatamente, mappe estraibili.
**Contro**: più file da gestire, richiede modifiche a `create-pdf-adventure.py` (flag `--split` o simile).
**Nota**: lo script supporta già `--only NN` per generare un singolo modulo — potrebbe bastare uno script wrapper.

### Mappe ottimizzate per Roll20

Le mappe attuali sono PNG raster. Per Roll20 servono due versioni per ogni battle map:
- **Player** — senza segreti (porte segrete, trappole, note DM rimossi)
- **DM** — con tutti i dettagli (per il GM Info Overlay layer)

#### Classificazione mappe

| Mappa | Modulo | Tipo | Roll20? | Versione player? |
|-------|--------|------|---------|-----------------|
| OrcastleCounty.png (1.4M) | A | regionale | overview | Non serve |
| FortezzaDiOrcastle.png (534K) | A | battle map | ✅ | ✅ Già player |
| FortezzaDiOrcastle_master.png (2.3M) | A | battle map DM | ✅ GM layer | È la versione DM |
| TorthTower_Entrance.png (1.2M) | A | battle map lv1 | ✅ | ❌ Serve player |
| TorthTower_MainSaloon.png (1.3M) | A | battle map lv2 | ✅ | ❌ Serve player |
| TorthTower_altarRoom.png (1.4M) | A | battle map lv3 | ✅ | ❌ Serve player |
| LabirintoDiVecna.png (1.3M) | A | battle map | ✅ | ❌ Serve player |
| LuminaDungeon.png (3.7M) | B | battle map | ✅ | ❌ Serve player |
| LuminaDungeonV2.png (124K) | B | alternativa | Da valutare | — |
| LuminaTown.png (7.4M) | B | città | overview | Non serve |
| TorreDiTorth.png (991K) | A | illustrazione | No | — |
| CerchiConcentrici.png | A | illustrazione | No | — |
| LaPergamenaDelGiudizio.png | A | illustrazione | No | — |
| AirborneMachine.jpg | A | illustrazione | No | — |
| StemmaDawnshield.png | C | stemma | No | — |
| Svoalbard.jpg | C | regionale | overview | Non serve |
| LoScettroDiTyrGeoMap.jpeg | B | viaggio | overview | Non serve |

#### TODO mappe Roll20

- [ ] Creare versione player di TorthTower_Entrance.png (rimuovere annotazioni DM)
- [ ] Creare versione player di TorthTower_MainSaloon.png (rimuovere annotazioni DM)
- [ ] Creare versione player di TorthTower_altarRoom.png (rimuovere annotazioni DM)
- [ ] Creare versione player di LabirintoDiVecna.png (rimuovere soluzione)
- [ ] Creare versione player di LuminaDungeon.png (rimuovere annotazioni DM)
- [ ] Decidere formato: le mappe attuali sono PNG raster, non modificabili programmaticamente. Opzioni: edit manuale GIMP, rigenerazione AI, o rigenerazione con pipeline dnd-maps (richiede conversione in SVG/DDL)

**Blocco**: le mappe sono PNG raster — non è possibile rimuovere automaticamente i segreti. Serve la conversione in SVG a layer (vedi workflow sotto).

#### Workflow: SVG a layer con Inkscape + export automatico

Ogni battle map viene salvata come SVG Inkscape con 3 layer:
- **`base`** — muri, pavimenti, porte normali, arredamento (sempre visibile)
- **`dm-only`** — porte segrete, trappole, note, numeri stanze, soluzioni puzzle
- **`grid`** — griglia opzionale (Roll20 ha la sua, ma utile per stampa)

Uno script esporta automaticamente:
- **Player PNG** = layer `base` + `grid` (nasconde `dm-only`)
- **DM PNG** = tutti i layer visibili

**Passi:**
1. Per ogni battle map PNG legacy, importarla in Inkscape come layer `base`
2. Aggiungere un layer `dm-only` sopra e disegnarci le annotazioni DM
3. Salvare come SVG Inkscape
4. Script di export genera `NomeMappa_player.png` e `NomeMappa_dm.png`

**Export automatico** con Inkscape CLI o script Python che rimuove il `<g inkscape:label="dm-only">` dall'SVG e converte con `cairosvg`. Tool di riferimento: [inkbatch](https://github.com/olav-st/inkbatch), [batch-export](https://github.com/StefanTraistaru/batch-export).

**Roll20 best practice**: 70×70 pixel per quadretto (140×140 per alta risoluzione). Il workflow ufficiale WotC è lo stesso: segreti su layer separato, rimosso per la versione player ([fonte](https://www.dndbeyond.com/forums/d-d-beyond-general/d-d-beyond-feedback/87160)).

Il passo 2 è lavoro manuale (Inkscape), ma va fatto una volta sola. Dopo, ogni modifica genera automaticamente entrambe le versioni.

### Stat block FightClub per import in Game Master 5e

Gli XML FightClub sono già generati per tutti i 16 NPC/mostri in `characters/fightclub/`. Per importarli in FightClub 5e o Game Master 5e:

- [ ] Testare l'import dei 16 XML in Game Master 5e (verificare che i campi siano corretti)
- [ ] Creare mappe ottimizzate per Roll20 (versioni player/DM separate per ogni mappa PNG — vedi sezione "Mappe ottimizzate per Roll20" sotto)
- [x] Verificare che gli NPC senza stat block completo (quelli con solo riferimento MM) siano utili o se servono stat block custom
- [x] Valutare se creare un file XML unico con tutti gli NPC dell'avventura (merge) per import singolo

---

*Ultimo aggiornamento: Maggio 2026*
