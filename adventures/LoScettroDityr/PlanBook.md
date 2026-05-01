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
- [ ] Mappe DM
- [x] Asset grafici copiati dal legacy (29 file)
- [x] Validazione con check-adventure.py (0 errori, 16 warning accettabili)

## Versione

Questa è la versione **"Draco"** — porting fedele del materiale legacy. Una versione **"Trust"** è prevista in futuro.

## Problemi aperti

### Generali

- Il materiale legacy ha livelli di completezza diversi: A è il più dettagliato (giocato), D ha due versioni (v0.1 e v0.3)
- Mancano stat block formali per molti NPC — il legacy usa riferimenti al Manuale dei Mostri (es. "Veterano pag 344")
- Le mappe sono descritte testualmente nei .odt ma non ci sono battle map grafiche per tutti i moduli
- La continuità tra moduli ha qualche buco narrativo (es. come i PG passano da A a B)

### Modulo A — Fuga da Orcastle

- Collari esplosivi: la meccanica di rimozione ha 4 opzioni ma nessuna è completamente definita
- Ombrascura: il suo piano per usare la pergamena non è chiaro (non può attivarla, sta cercando alternative)
- Manca una mappa dell'isola di Orcastle
- Le fazioni (Ruby, Emerald, Highlander) hanno interazioni complesse — serve una tabella riassuntiva

### Modulo B — Lo Scettro di Tyr

- Il dungeon del Tempio di Lumina ha una mappa (immagine nel .odt) ma la descrizione delle sale è incompleta
- La transizione verso Erythale (piano etereo) è poco definita meccanicamente
- Alaric il Giusto: lo stat block è una variante del Mago ma con incongruenze (CA 15 senza spiegazione)
- Le prove di purezza nel tempio sono narrative — servono meccaniche più precise

### Modulo C — Ritorno a Casa

- Il viaggio via nave è molto lungo (35+ giorni) — rischio di noia per i giocatori
- Zalhara (la spia): le meccaniche di scoperta sono dettagliate ma la timeline è confusa
- Othran Vorash: appare troppe volte (Luskan, Bryn Shander, Svoalbard) — valutare se ridurre
- La famiglia Dawnshield e la Lanterna dell'Aurora sono introdotte tardi

### Modulo D — La fine non appartiene ai morti

- La maledizione di Malebranche è molto potente (cure dimezzate, non morti ovunque) — rischio di frustrazione
- Il Santuario di Ostegard: la prova morale con gli spiriti è narrativamente forte ma meccanicamente vaga
- Malebranche: manca uno stat block completo (il legacy dice "mago necromante" senza dettagli)
- L'epilogo (matrimonio di Tungsten) è divertente ma scollegato dal tono del resto del modulo

## Idee per sviluppi futuri

- Creare una tabella riassuntiva degli NPC che attraversano più moduli con il loro stato in ogni modulo
- Definire le milestone di livello per ogni modulo (attualmente: A→lv9, B→lv10, C e D restano lv10?)
- Valutare se il Modulo A può funzionare come avventura standalone

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

Le mappe attuali sono PNG generiche. Per Roll20 servono due versioni per ogni mappa:
- **Player** — senza segreti (porte segrete, trappole, note DM rimossi)
- **DM** — con tutti i dettagli (per il GM Info Overlay layer)

Mappe da ottimizzare per Roll20:

| Mappa | Modulo | Stato |
|-------|--------|-------|
| Isola di Orcastle (MappaGenerale_County) | A | PNG presente, serve split player/DM |
| Fortezza di Orcastle | A | PNG presente (2 versioni: normale e master) |
| Torre di Torth (3 livelli) | A | PNG presenti, servono versioni player |
| Labirinto di Vecna | A | PNG presente |
| Tempio di Lumina (dungeon) | B | PNG presente (2 versioni) |
| Lumina town | B | PNG presente |
| Mappa geografica viaggio | B | JPEG presente |
| Svoalbard | C | JPG presente |

**Blocco**: manca l'export SVG→PNG automatico nel progetto (vedi Fase 1 roadmap in `plan-meta-dnd.md`). Le mappe attuali sono già PNG quindi utilizzabili su Roll20 così come sono — ma senza la separazione player/DM.

### Stat block FightClub per import in Game Master 5e

Gli XML FightClub sono già generati per tutti i 16 NPC/mostri in `characters/fightclub/`. Per importarli in FightClub 5e o Game Master 5e:

- [ ] Testare l'import dei 16 XML in Game Master 5e (verificare che i campi siano corretti)
- [ ] Verificare che gli NPC senza stat block completo (quelli con solo riferimento MM) siano utili o se servono stat block custom
- [ ] Valutare se creare un file XML unico con tutti gli NPC dell'avventura (merge) per import singolo

---

*Ultimo aggiornamento: Maggio 2026*
