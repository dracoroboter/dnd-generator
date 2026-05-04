# Plan Meta DnD - Todo List

Todo list operativa per attuare la struttura descritta in `meta-dnd.md`.

---

## Obiettivo Principale

Creare nuove avventure D&D 5e per sessioni con amici, usando Kiro e gli script del progetto come acceleratori. L'obiettivo non è costruire un framework generico — è avere strumenti pratici che riducano il tempo tra "ho un'idea per un'avventura" e "la sessione è pronta da giocare su Roll20".

### Cosa serve concretamente

| # | Capacità | Descrizione | Priorità |
|---|----------|-------------|----------|
| A | **Mappe da descrizione testuale** | Descrivere un dungeon a Kiro in linguaggio naturale → ottenere una mappa giocabile. La pipeline attuale (DDL → enrichment → SVG) è il nucleo. Manca il passo "linguaggio naturale → DDL" (skill Kiro) e l'export ottimizzato per Roll20. | **Alta** |
| A1 | **Mappe ottimizzate per Roll20** | Roll20 ha layer separati: Map (sfondo visibile ai player), GM Info Overlay (solo GM), Objects (token). Servono almeno 2 PNG: uno "player" (senza segreti) per il Map layer, uno "DM" (con porte segrete, note, trappole) per il GM Info Overlay. Il flag `--view dm|players` esiste già nei renderer — manca l'export automatico SVG→PNG (serve `cairosvg` o simile). | **Alta** |
| A2 | **Mappe multi-livello (segreti nascosti)** | Porte segrete, passaggi nascosti, trappole visibili solo al DM. Il sistema `--view dm|players` + gate `secret hidden/found` esiste già. Per Roll20 basta generare le due immagini e caricarle sui layer giusti. Non serve un formato speciale — sono due PNG separati. | **Media** (già quasi funzionante) |
| B | **Creazione rapida scontri, NPC, PG** | Data una descrizione ("6 banditi nel bosco, party livello 3, difficoltà hard"), generare la lista mostri bilanciata con stat block. `encounter-difficulty.py` calcola già la difficoltà — manca la direzione inversa: dato un budget XP, suggerire combinazioni di mostri. Per NPC e PG: generazione da descrizione con stat block completo 5e. | **Alta** |
| C | ~~**Export Fight Club 5e XML**~~ | ✅ Risolto: `md-to-fightclub.py`, `fightclub-to-md.py`, `generate-statblocks.py` (pipeline completa .md → .xml + .pdf + .png). | **Completata** |
| D | **Wizard NPC/PG** | Wizard interattivo per creare NPC e PG. `new-npc.py` esiste già. `new-pc.py` è da definire (5 domande aperte in questo plan). Opzionale — Kiro con la skill DungeonMaster può già guidare la creazione conversazionalmente. | **Bassa** |
| E | **Assistenza costruzione avventura** | Skill/conoscenze per: evitare contraddizioni narrative, bilanciare scontri, suggerire tipi di mostri e svolte narrative, proporre battle map appropriate. Più "intelligenza nel processo" che script specifici. | **Media** |

### Critica — cosa funziona e cosa no

**Modalità di gioco e strumenti necessari:**

| Modalità | Avventure | Strumenti chiave | Stato |
|----------|-----------|-----------------|-------|
| **Dal vivo** (mappe improvvisate, tablet/stampa) | FuoriDaHellfire | PDF unico (`create-pdf-adventure.py`), stat block PNG, schede mappa DM testuali | ✅ Funzionante |
| **Roll20** (mappe digitali, token, layer) | LAnelloDelConte, saga Scettro di Tyr | Export SVG→PNG (player + DM), mappe ottimizzate per layer Roll20 | ❌ Manca export PNG |

Le due modalità condividono la pipeline NPC/stat block e il generatore PDF, ma divergono sulle mappe: dal vivo bastano descrizioni testuali (`MappaDM.md`), Roll20 richiede immagini PNG separate per player e DM.

**Cosa funziona già:**
- La pipeline dungeon (generazione → enrichment → SVG multi-stile) è solida
- Il sistema DM/players con gate segreti è implementato
- `encounter-difficulty.py` calcola la difficoltà
- La skill DungeonMaster ha già linee guida per bilanciamento, NPC, dungeon
- 4 template stanze RTL funzionanti

**Cosa manca davvero (gap critici):**
1. **Nessun export PNG automatico.** Senza SVG→PNG, le mappe non vanno su Roll20. È il blocco più immediato. Serve `cairosvg` (o Inkscape CLI, o `rsvg-convert`).
2. **Nessuna skill "linguaggio naturale → DDL".** La pipeline DDL→JSON→SVG funziona, ma scrivere un `.ddl` a mano è ancora da programmatore. Kiro dovrebbe poter tradurre "la stanza 3 è una cappella con un altare e due candelabri" in DDL valido.
3. ~~**Nessun generatore di scontri inverso.**~~ ✅ Risolto: `encounter-builder.py` con database SRD 327 mostri.
4. ~~**Nessun export Fight Club XML.**~~ ✅ Risolto: `md-to-fightclub.py`, `fightclub-to-md.py`, `generate-statblocks.py` (pipeline completa).
5. ~~**Nessun database mostri locale.**~~ ✅ Risolto: `tech/data/srd_5e_monsters.json`.

**Cosa è sovra-ingegnerizzato rispetto all'obiettivo:**
- Il sistema DDL/RTL è potente ma complesso. Per le prime avventure, Kiro che scrive direttamente il `dungeon_enrichment.json` da una descrizione potrebbe bastare — il DDL diventa utile quando hai molti dungeon da arredare.
- I 5 stili SVG (oldschool, blueprint, kenney, stone, iso) sono un lusso. Per Roll20 ne basta uno buono. Concentrare lo sforzo sull'oldschool (il più maturo) e sull'export PNG.

### Domande aperte

| # | Domanda | Impatto |
|---|---------|---------|
| V1 | Hai un account Roll20 Pro/Plus (per il Foreground Layer) o Free? Con Free hai solo Map + GM Info Overlay + Objects — comunque sufficienti per DM/players. | Determina se servono 2 o 3 layer di export |
| V2 | Per Fight Club: ti servono solo mostri/NPC custom, o anche PG dei giocatori? I PG di solito li gestiscono i giocatori nell'app — tu esporteresti solo i pregen per one-shot? | Scope dello script FC5 export |
| V3 | Hai già un set di mostri homebrew che usi spesso, o ti basta il SRD 5.1? | Determina se serve un sistema di mostri custom oltre al database SRD |
| V4 | Le mappe ti servono solo per dungeon interni, o anche per battle map all'aperto (foresta, strada, accampamento)? Il generatore attuale fa solo dungeon chiusi. | Scope del generatore mappe |
| V5 | Dimensione tipica delle tue sessioni: quante stanze per dungeon, quanti scontri per sessione? | Calibra la complessità degli strumenti |

### Roadmap di sviluppo

Ordinata per impatto sulla prossima sessione, non per eleganza tecnica.

```
Fase 1 — "Mappa giocabile su Roll20" (sblocca A, A1, A2)
├── 1a. Export SVG → PNG (cairosvg o rsvg-convert)
├── 1b. Script wrapper: genera PNG player + PNG DM in un colpo
└── 1c. Skill Kiro: linguaggio naturale → DDL (o direttamente → enrichment JSON)

Fase 2 — "Scontri bilanciati" (sblocca B parziale) ✅
├── 2a. ✅ Database mostri SRD 5.1 in JSON locale (tech/data/srd_5e_monsters.json, 327 mostri)
├── 2b. ✅ Script encounter-builder.py: dato budget XP + tema → lista mostri
│       Filtri: --type, --cr-range, --max-monsters, --seed, party misto
└── 2c. ✅ Usa stesse tabelle DMG di encounter-difficulty.py (XP_THRESHOLDS, XP_BY_CR, multiplier)

Fase 3 — "NPC e PG rapidi" (sblocca B completo, C, D)
├── 3a. Generazione NPC da descrizione (stat block 5e completo)
├── 3b. ✅ Export Fight Club 5e XML (mostri + NPC) — md-to-fightclub.py
├── 3c. ✅ Pipeline completa .md → .xml + .pdf + .png — generate-statblocks.py
├── 3d. Generazione PG da descrizione (pregen per one-shot)
└── 3e. Export Fight Club 5e XML (PG)

Fase 4 — "Assistente avventura" (sblocca E)
├── 4a. Skill review avventura: contraddizioni, bilanciamento, linearità
├── 4b. Suggeritore mostri/svolte dato contesto narrativo
└── 4c. enrichment-to-description.py (descrizioni stanze da oggetti reali)

Fase 5 — "Qualità di vita" (migliora tutto)
├── 5a. ✅ Git + GitHub (github.com/dracoroboter/dnd-generator)
├── 5b. Wizard PG interattivo (new-pc.py)
├── 5c. Miglioramenti motore placement (beside, L2)
└── 5d. Knowledge base SRD 5.1 ricercabile
        Scaricare SRD 5.1 CC-BY-4.0 in Markdown (repo OldManUmby/DND.SRD.Wiki) in tech/data/srd/
        Indicizzarla come knowledge base Kiro per rispondere a domande rapide sulle regole:
        durata incantesimi, condizioni per vantaggio/svantaggio, effetti di spell, ecc.
        Valutare: indicizzazione Kiro KB vs script di ricerca locale (grep strutturato)
```

**Nota:** la Fase 1 è la più urgente perché sblocca il caso d'uso primario (mappa per la sessione). Le fasi 2-4 possono procedere in parallelo. La Fase 5 è infrastruttura che non blocca nessuna sessione.

---

## Multilingua (completato 2026-05-02)

- [x] Progettazione struttura multilingua (it/ + en/ + manifest.json)
- [x] File i18n: tech/i18n/it.json, tech/i18n/en.json
- [x] Refactoring struttura tutte le avventure (FuoriDaHellfire, LAnelloDelConte, LoScettroDityr)
- [x] Aggiornamento script: create-pdf-adventure.py, generate-statblocks.py, md-to-fightclub.py, check-adventure.py, release-bundle.py
- [x] Traduzione inglese FuoriDaHellfire (7 NPC/MON, 2 moduli)
- [x] Traduzione inglese LAnelloDelConte (5 NPC, 2 moduli)
- [x] Traduzione inglese LoScettroDityr (18 NPC/MON, 4 moduli)
- [x] Copertina con titolo/sottotitolo tradotti dal manifest
- [x] Nomi mostri EN con riferimenti SRD WotC
- [x] Test di non regressione: tech/tests/test_regression.py (15 test)
- [x] Frontmatter EN: Duration, Structure, Tone tradotti via manifest
- [x] Role line aggiunta alla description degli stat block XML
- [x] Pubblicazione lowres IT+EN in public/ per tutte le avventure
- [x] Skill publish-adventure aggiornata (lowres default, multilingua)
- [x] AdventureTemplate aggiornato
- [x] Documentazione aggiornata (adventure-template.md)

---

## Struttura del progetto

- [x] Creare directory `adventures/`
- [x] Creare directory `tech/scripts/`, `tech/rules/`, `tech/how-to/`, `tech/reports/`
- [x] Creare directory `tech/assets/tilesets/` (tile per generatore dungeon) → spostata in **dnd-maps**
- [x] Creare directory `adventures/AdventureTemplate/`
- [x] Creare directory `releases/` (suddivisa per avventura)

---

## Convenzioni (decisioni prese)

- [x] Naming convention file: **PascalCase** (es. `NomeFile.md`)
- [x] Directory: **minuscolo** (es. `characters/`, `maps/`)
- [x] Struttura moduli: **subdirectory** `NN_NomeModulo/` con risorse proprie
- [x] `README.md`: descrizione pubblica senza spoiler + metadati saga opzionali
- [x] `AdventureBook.md`: istruzioni specifiche per Kiro su questa avventura
- [x] `PlanBook.md`: todo list e stato lavoro del DM
- [x] Schede PG: opzionali, fuori dall'avventura base
- [x] `versioni/` dentro le avventure: eliminata — sostituita da `releases/<NomeAvventura>/`
- [x] Copertina: `img/NomeAvventura_COVER.png`
- [x] Milestone: sezione `## Milestone` opzionale nei moduli (separata da `## Ricompense`)
- [x] Struttura avventura: campo `**Struttura**: lineare/sandbox/mista` nel `README.md`

---

## Template e normalizzazione

- [x] Analisi comparativa `avventuraprova` vs `LAnelloDelConte`
- [x] Struttura directory e file placeholder creati (`adventures/AdventureTemplate/`)
- [x] `LAnelloDelConte` normalizzata — check passa con 1 warning (Consigli al master assente)
- [x] Regole di contenuto documentate in `tech/rules/content-rules.md`
- [x] Struttura standard documentata in `tech/rules/adventure-template.md`
- [x] Glossario termini in `tech/rules/glossary.md`
- [x] Manuale di normalizzazione in `tech/rules/normalization.md`
- [x] Normalizzare **LoScettroDityr** (saga, 4 moduli A/B/C/D, da `.odt`) — versione "Draco" completata (maggio 2026): 4 moduli, 16 NPC, 1 MON, 29 asset grafici, 0 errori check
- [ ] Completare **IlReSpezzato** (draft IT creato maggio 2026: documento principale, modulo Nerrok, meccanica medaglione. Mancano: NPC schede, moduli successivi, traduzione EN)

---

## Script e manuali

- [x] `tech/scripts/setup.sh` — installa prerequisiti (pandoc, wkhtmltopdf, zip, python3, node, playwright)
- [x] `tech/scripts/backup.sh` — backup del progetto (escluso legacy/)
- [x] `tech/scripts/release.sh` — genera PDF + ZIP per una avventura
- [x] `tech/scripts/check-adventure.py` — verifica normalizzazione + genera report in `tech/reports/` (aggiornato: riconosce sezioni meccaniche NPC: Attacchi, Azioni bonus, Reazioni, Backstory, Punti aperti)
- [x] `tech/scripts/encounter-difficulty.py` — calcola difficoltà incontro D&D 5e
- [ ] **Calcolo automatico difficoltà nei moduli** — `check-adventure.py` (o script dedicato) legge il party size/livello dal documento principale e le tabelle nemici dai moduli, calcola la difficoltà (Easy/Medium/Hard/Deadly) e verifica che corrisponda a quella dichiarata. Il party va dichiarato nel documento principale (es. `**Party**: 3 PG lv3 + Udo (CR3) + Fin (lv3)`)
- [x] `tech/scripts/new-adventure.sh` — scaffolding nuova avventura da template
- [x] `tech/scripts/adventure-wizard.py` — wizard interattivo per metadati avventura (rilanciabile)
- [x] `tech/scripts/new-npc.py` — crea scheda NPC (interattivo o template vuoto)
- [ ] `tech/scripts/new-pc.py` — wizard per scheda PG (da definire scope e formato)
  - **Domande aperte**:
  - [ ] 1. Scope: PG per one-shot con personaggi predefiniti, o uso più generico?
  - [ ] 2. Cosa fa già `new-npc.py`? Leggere per capire i gap prima di procedere.
  - [ ] 3. Livello di dettaglio: scheda completa 5e (feature classe, incantesimi, ecc.) o semplificata (stat base + tratti)?
  - [ ] 4. Output: `.md` come NPC, JSON, o altro?
  - [ ] 5. Integrazione: il wizard salva nella directory giusta in automatico, o salvataggio manuale?
- [ ] Aggiungere definizioni PG e NPC in `tech/rules/glossary.md`
- [x] `tech/how-to/how-to-release.md`
- [x] `tech/how-to/how-to-encounter-difficulty.md`
- [x] `tech/how-to/how-to-new-adventure.md`
- [ ] `tech/how-to/how-to-normalization.md` — guida passo-passo normalizzazione legacy (da `.odt`)
- [ ] TODO: studiare sistema di prefissi/suffissi per sezioni libere dei moduli

---

## Generazione mappe

### Stato attuale

| tipo | tool | script | qualità | note |
|------|------|--------|---------|------|
| Dungeon | Watabou one-page-dungeon | `generate-watabou-dungeon.js` | ✅ buona | `--seed`, `--size`, `--player` |
| Dungeon batch | Watabou | `generate-watabou-dungeon-batch.js` | ✅ | genera N mappe + `seeds.txt` |
| Città | Watabou Town Generator | `generate-watabou-maps.js city` | ✅ buona | `--river`, `--walls`, `--citadel`, ecc. |
| Geografica | Watabou Perilous Shores | `generate-watabou-maps.js region` | ❌ stile non gradito | scartato |
| Geografica | Azgaar's Fantasy Map Generator | prototipo testato | ❌ troppo ampia | scartato |
| Battle map | DungeonFog, DungeonScrawl | — | solo manuale | nessuna API |
| Mappa custom | Inkarnate | — | solo manuale | nessuna API |
| Dungeon custom | `generate-dungeon.py` | `generate-dungeon.py` | 🔧 in sviluppo | BSP tree, tileset DCSS |

Documentazione tool: → repository **[dnd-maps](https://github.com/dracoroboter/dnd-maps)**

### Generatore dungeon custom (`generate-dungeon.py`)

Piano dettagliato e workflow iterativo: → repository **[dnd-maps](https://github.com/dracoroboter/dnd-maps)**

Workflow definitivo:
1. `generate-dungeon.py` → PNG strutturale (BSP tree, stanze numerate, tileset opzionale)
2. Manuale: upload PNG su Gemini web + prompt ambientazione → PNG finale professionale

Tileset disponibili nel repository **dnd-maps** (da DCSS, licenza CC):
- `floor.png` (cobble_blood), `wall.png` (brick_brown)
- Varianti: `floor_crystal.png`, `wall_stone.png`

- [x] Versione base BSP tree funzionante
- [x] Supporto tileset (`--tileset <dir>`)
- [ ] *(i TODO seguenti sono nel repository **dnd-maps**, non in questo repo)*
- [ ] Parametro `--wall-thickness N` + `--wall-mode dual|padding`
- [ ] Corridoi larghi 1-4 celle (parametro `--corridor-width N`, default 1-2)
- [ ] Stanze più grandi rispetto ai corridoi (problema visivo attuale)
- [ ] Blocchi separati con spazio aperto tra loro
- [ ] Aggiungere più varianti tileset (pietra, caverna, ecc.)

### AI e mappe

- [x] Workflow donjon → Gemini validato manualmente (risultato professionale)
- [x] Automazione Gemini via Playwright: scartata (richiede login manuale)
- [x] API Gemini gratuita: solo testo, non immagini — scartata per mappe
- [ ] Imagen 3 via API Google: a pagamento — valutare se accettabile

### Immagini NPC/luoghi

- [ ] Stable Diffusion locale (richiede GPU) — valutare hardware disponibile
- [ ] DALL-E / API cloud — valutare costo per uso hobby

---

## Git e PDF

**Priorità: da fare prima della prima pubblicazione**

- [x] Decidere struttura repository GitHub (mono-repo o repo separati per avventura)
- [x] Inizializzare repository e primo commit
- [x] Documentare workflow git in `tech/rules/git-workflow.md`
- [x] Decidere se `releases/` va in `.gitignore`
- [x] Aggiungere `tech/reports/` a `.gitignore`
- [ ] Creare GitHub Action per generazione PDF automatica al push/tag

---

## Release e Pubblicazione

### Definizioni

- **Release** = insieme taggato (con codice identificativo univoco, es. `v1.0_20260502`) delle versioni di tutti i file che compongono un'avventura. I file in `releases/` sono in `.gitignore` — artefatti di lavoro, non tracciati da git.
- **Pubblicazione** = ZIP della release in formato directory predeterminato, messo in `public/` dove può essere committato. È il passo che rende il materiale disponibile nel repository.

### Composizione di una release

Lo ZIP è pensato per **campagne online** (Roll20, VTT). Per **campagne fisiche** serve un PDF printable separato (vedi sotto).

**Obbligatori nello ZIP:**

| File | Descrizione |
|------|-------------|
| `NomeAvventura_YYYYMMDD_lowres.pdf` | PDF lowres senza mappe/stat block inline |
| `NomeAvventura_Compendium.xml` | Tutti gli NPC/MON in formato FightClub |
| `NomeAvventura_COVER.png` | Copertina |
| `maps/*.png` | Mappe PNG separate (player + DM quando disponibili) |
| `statblocks/*.png` | Stat block PNG stampabili |
| `README.txt` | Versione, data, autore, contenuto, licenza |

**Opzionali (quando implementati):**

| File | Descrizione |
|------|-------------|
| `pdf/NomeAvventura_Lore.pdf` | Documento principale separato |
| `pdf/NomeAvventura_NN_NomeModulo.pdf` | Un PDF per modulo |

**Esclusi dallo ZIP:** PDF fullres, sorgenti .md, AdventureBook, PlanBook, XML singoli, immagini personaggi, file in other/.

### PDF printable (da implementare)

Per campagne fisiche: un unico PDF hires con tutto dentro — testo, mappe inline, stat block in appendice (multi-colonna, 2 per pagina). Generato separatamente dallo ZIP.

### Script

```bash
# Pubblicazione completa (stat block → compendium → PDF → ZIP → public/)
python3 tech/scripts/release-bundle.py <NomeAvventura> [--tag vX.Y]

# Singoli passi (se serve)
python3 tech/fightclub/generate-statblocks.py <NomeAvventura>          # stat block + compendium
python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura>  # PDF fullres
python3 tech/create-pdf-adventure/create-pdf-adventure.py <NomeAvventura> --lowres  # PDF lowres
```

Il vecchio `release.sh` (pandoc + ZIP) è deprecato — spostato in `tech/scripts/old/`.

### TODO

- [ ] Aggiungere flag `--no-maps` a `create-pdf-adventure.py` per escludere mappe PNG inline
- [ ] Implementare `--split` in `create-pdf-adventure.py` per PDF divisi (lore, sessioni, appendice)
- [ ] Implementare stat block multi-colonna nell'appendice PDF (2 per pagina)
- [ ] Definire il tag di versione (manuale? campo nel README.md? tag git?)

---

## Future / opzionali

- [ ] Valutare layout PDF ottimizzato per stampa fisica (margini, formato A5/A4)
- [ ] Valutare pubblicazione su piattaforme dedicate (DMsGuild, itch.io)
- [x] Script per PDF unico pubblicabile (copertina `NomeAvventura_COVER.png` + tutti i MD + mappe + immagini, con indice, licenza, autore, data) → `create-pdf-adventure.py`

---

## Naming convention documentazione

**Priorità: bassa, da fare quando si tocca la documentazione**

Il progetto ha tre tipi di file in `tech/` ma non c'è una convenzione chiara per distinguerli dal nome:

| Tipo | Scopo | Prefisso proposto |
|------|-------|-------------------|
| Piano di sviluppo | Roadmap, decisioni, fasi, TODO | `plan-*.md` |
| Documentazione tecnica | Come funziona, formato, API, uso | `docs-*.md` o `README.md` |
| Specifica | Grammatica, formato, regole formali | `*-spec.md` |

Convenzione adottata (aprile 2026):
- **Contenuto avventure**: PascalCase (es. `LeFogneDiFianus.md`, `NPC_SirGorimVel.md`)
- **Documenti tecnici** (rules, how-to, docs): kebab-case (es. `adventure-template.md`, `how-to-release.md`)
- **File meta/progetto**: UPPER_SNAKE_CASE (es. `README.md`, `CLAUDE.md`)
- **Script**: kebab-case (es. `check-adventure.py`)
- **Commenti nel codice**: inglese. Tutto il resto: italiano.

Fonte di verità: `tech/rules/adventure-template.md` § Convenzioni di naming.

- [x] Definire convenzione naming per i tre tipi di documento
- [x] Uniformare i nomi esistenti (in dnd-generator)
- [ ] Uniformare i nomi esistenti (in dnd-maps)
- [x] Applicare la convenzione ai nuovi file (es. `plan-create-pdf-adventure.md` ✅)

---

## create-pdf-adventure

**Priorità: alta (serve per masterare FuoriDaHellfire)**

Genera un singolo PDF con tutta l'avventura: copertina, moduli, schede mappa DM, stat block in appendice. Grafica D&D-style via CSS custom.

- Piano di sviluppo: `tech/create-pdf-adventure/plan-create-pdf-adventure.md`
- Documentazione: `tech/create-pdf-adventure/docs-create-pdf-adventure.md`
- [x] Fase 1: CSS custom (`adventure.css`)
- [x] Fase 2: Script `create-pdf-adventure.py`
- [x] Fase 3: HTML → PDF (weasyprint)
- [x] Fase 4: Test con FuoriDaHellfire — `FuoriDaHellfire_20260419.pdf` (2.1 MB)
- [x] Fase 5: Generalizzare per qualsiasi avventura
