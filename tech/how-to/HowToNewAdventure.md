# How-To: Creare una Nuova Avventura

Guida completa per progettare, strutturare e scrivere un'avventura D&D 5e nel formato del progetto.

Riferimenti:
- Struttura directory e file obbligatori: `tech/rules/AdventureTemplate.md`
- Regole di contenuto: `tech/rules/ContentRules.md`
- Terminologia: `tech/rules/Glossary.md`
- Avventura di riferimento: `adventures/AvventuraDiProva/`

---

## Panoramica del processo

```
1. Concept        — decidere cosa si scrive (tipo, livello, tono, agganci)
2. Scaffolding    — creare la struttura directory con new-adventure.sh
3. Metadati       — compilare README.md con adventure-wizard.py
4. Struttura      — rinominare moduli, creare NPC, impostare la mappa
5. Scrittura      — compilare i file in ordine
6. Verifica       — validare con check-adventure.py
7. Release        — generare PDF + ZIP con release.sh
```

---

## Fase 0 — Concept

Prima di toccare qualsiasi file, rispondere a queste domande:

| domanda | esempio |
|---------|---------|
| Che tipo di avventura è? | one-shot, campagna, saga |
| Per che livello? | Livello 3-4 |
| Quanti moduli? | 3 |
| Struttura narrativa? | lineare, sandbox, mista |
| Tono? | pulp adventure, camp anni '80 |
| È una continuazione? | Sì — segue "Welcome to the Hellfire Club" |
| Ambientazione? | Greyhawkins (esistente) / nuova |

Scrivere un **plot generale** in 5-10 righe: chi sono i PG, cosa è successo prima, qual è il conflitto, come si risolve. Non serve che sia definitivo — serve come bussola per la struttura.

**Esempio** (Fuori da Hellfire):

> I PG tornano a Greyhawkins dopo il gauntlet nei Nine Hells. Ma l'incursione ha lasciato una cicatrice tra i piani: corruzione infernale si espande dalla zona dei moli di Oakshore. Tre moduli: ritorno e scoperta, indagine sulla fonte, scontro finale per sigillare la breccia. Tono camp/pulp coerente con lo starter kit.

Questo concept guiderà tutte le scelte successive: quanti moduli creare, quali NPC servono, che tipo di mappa disegnare.

Dopo lo scaffolding (Fase 1), riportare il concept nella sezione `## Concept` del `PlanBook.md`.

---

## Fase 1 — Scaffolding

### Prerequisiti

```bash
bash tech/scripts/setup.sh   # solo la prima volta
```

### Creare la struttura

```bash
bash tech/scripts/new-adventure.sh NomeMiaAvventura              # 1 modulo (default)
bash tech/scripts/new-adventure.sh NomeMiaAvventura --modules 3  # 3 moduli
```

Lo script:
- Copia `adventures/AdventureTemplate/` in `adventures/NomeMiaAvventura/`
- Rinomina `NomeAvventura.md` → `NomeMiaAvventura.md`
- Rinomina il modulo placeholder `01_NomeModulo/NomeModulo.md` → `01_NomeModulo/NomeMiaAvventura_Modulo01.md`
- Crea il placeholder NPC `personaggi/NPC_NomePersonaggio.md.placeholder`
- Sostituisce `[NomeAvventura]` nei file `.md`
- Crea `releases/NomeMiaAvventura/`

### Risultato

```
adventures/NomeMiaAvventura/
├── README.md
├── AdventureBook.md
├── PlanBook.md
├── NomeMiaAvventura.md
├── mappe/
│   └── MappaGenerale.md
├── personaggi/
│   └── (vuota — usare new-npc.py per creare NPC)
│       ├── markdown/      ← schede NPC_*.md
│       ├── img/           ← artwork personaggi (opzionale)
│       ├── fightclub/     ← XML FightClub (generati)
│       └── statblock/     ← PDF e PNG stampabili (generati)
└── 01_NomeModulo/
    ├── NomeModulo.md                        ← placeholder generico, da rinominare subito
    └── mappe/
```

> **Nota**: il modulo `01_NomeModulo/NomeModulo.md` è un placeholder generico. Il primo passo dopo lo scaffolding è rinominare directory e file del modulo e crearne altri se servono (vedi Fase 3).

---

## Fase 2 — Metadati (README.md)

```bash
python3 tech/scripts/adventure-wizard.py NomeMiaAvventura
```

Il wizard chiede interattivamente: sistema, livello, durata, struttura, tono, saga (se applicabile), descrizione breve. Rilanciabile: salta i campi già compilati.

### Formato README.md risultante

```markdown
# Nome Avventura

**Sistema**: D&D 5e (2014)
**Livello consigliato**: X
**Durata**: one-shot / X sessioni
**Struttura**: lineare / sandbox / mista
**Tono**: ...

Descrizione breve senza spoiler.

---

## Ambientazione

## Personaggi principali

## Tono e temi
```

Se l'avventura è parte di una saga, aggiungere i metadati saga:

```markdown
**Saga**: Nome della Saga
**Posizione**: Puntata N di M
**Segue**: NomeAvventuraPrecedente (o —)
**Precede**: NomeAvventuraSuccessiva (o —)
```

---

## Fase 3 — Struttura: moduli, NPC, mappa

### Rinominare i moduli

Il template crea un solo modulo placeholder. Rinominarlo e crearne altri secondo il concept:

```bash
cd adventures/NomeMiaAvventura

# Rinomina il primo modulo
mv 01_NomeModulo 01_NomePrimoModulo
mv 01_NomePrimoModulo/NomeMiaAvventura_Modulo01.md 01_NomePrimoModulo/NomePrimoModulo.md

# Crea altri moduli copiando la struttura
cp -r 01_NomePrimoModulo 02_NomeSecondoModulo
mv 02_NomeSecondoModulo/NomePrimoModulo.md 02_NomeSecondoModulo/NomeSecondoModulo.md

cp -r 01_NomePrimoModulo 03_NomeTerzoModulo
mv 03_NomeTerzoModulo/NomePrimoModulo.md 03_NomeTerzoModulo/NomeTerzoModulo.md
```

### Naming convention moduli

| elemento | formato | esempio |
|----------|---------|---------|
| Directory modulo | `NN_PascalCase` | `01_RitornoAGreyhawkins` |
| File modulo | `PascalCase.md` | `RitornoAGreyhawkins.md` |
| Sottodirectory mappe | `mappe/` (minuscolo) | `01_RitornoAGreyhawkins/mappe/` |

### Creare NPC

**Modalità wizard** (NPC principali — chiede interattivamente nome, ruolo, stats):
```bash
python3 tech/scripts/new-npc.py NomeMiaAvventura
```

**Modalità template** (NPC secondari — crea il file vuoto da compilare a mano):
```bash
python3 tech/scripts/new-npc.py NomeMiaAvventura --template
```

### Naming convention NPC

| elemento | formato | esempio |
|----------|---------|---------|
| File NPC markdown | `NPC_PascalCase.md` | `personaggi/markdown/NPC_Korex.md` |
| File NPC XML | `NPC_PascalCase.xml` | `personaggi/fightclub/NPC_Korex.xml` |
| File NPC stat block | `NPC_PascalCase.pdf/.png` | `personaggi/statblock/NPC_Korex.pdf` |
| Artwork NPC | `PascalCase.ext` | `personaggi/img/Korex.png` |

### Naming convention generale

| elemento | formato | esempio |
|----------|---------|---------|
| File `.md` | PascalCase | `FuoriDaHellfire.md` |
| Directory | minuscolo | `personaggi/`, `mappe/` |
| Immagini | PascalCase | `MappaOakshore.png` |
| Copertina | `Cover.png` | `Cover.png` |

---

## Fase 4 — Scrittura

### Ordine consigliato

Compilare i file in quest'ordine — ogni passo si appoggia sul precedente:

#### 1. Documento principale (`NomeMiaAvventura.md`)

Il cuore dell'avventura. Sezioni obbligatorie:

```markdown
## Lore
## Introduzione
## NPC principali
## Struttura dell'avventura
```

Sezioni consigliate:

```markdown
## Plot generale
## Consigli al master
```

La sezione `## Struttura dell'avventura` contiene la tabella dei moduli con link:

```markdown
| # | nome | tipo | file |
|---|------|------|------|
| 1 | Ritorno a Greyhawkins | esplorazione / roleplay | [01_RitornoAGreyhawkins/RitornoAGreyhawkins.md](...) |
| 2 | La Cicatrice | dungeon / mystery | [02_LaCicatrice/LaCicatrice.md](...) |
```

#### 2. Mappa generale (`mappe/MappaGenerale.md`)

Luoghi, connessioni, distanze. Formato:

```markdown
## Luoghi principali

- **Greyhawkins** — hub di partenza, città portuale
- **Moli di Oakshore** — a 20 minuti dal centro

## Connessioni

Greyhawkins ---(strada costiera, 20min)---> Moli di Oakshore

## Note geografiche

*(terreno, visibilità, pericoli ambientali)*
```

#### 3. Moduli (`NN_NomeModulo/NomeModulo.md`)

Un file per modulo. Sezioni obbligatorie:

```markdown
## Descrizione
## Obiettivo
## Ricompense
## Note al master
```

Sezioni opzionali:

```markdown
## Luoghi interni
## Nemici
## Indizi chiave
## Finale
## Milestone
```

Se il modulo ha combattimenti, la sezione `## Nemici` deve dichiarare la difficoltà:

```markdown
## Nemici

**Difficoltà incontro:** HARD (4 PG lv3) — calcolata con `encounter-difficulty.py`

| nome | numero | PF | CA | attacco | note |
|------|--------|----|----|---------|------|
```

Per calcolare:
```bash
python3 tech/scripts/encounter-difficulty.py -p 4 3 -m 2 1 1 3
```

Guida dettagliata: `tech/how-to/HowToEncounterDifficulty.md`

#### 4. Schede NPC (`personaggi/NPC_*.md`)

Sezioni obbligatorie per tutti i PNG:

```markdown
## Informazioni generali
## Descrizione
## Motivazioni
## Note al master
```

**Antagonisti principali**: aggiungere `## Stat Block` e `## Capacità notevoli`.
**PNG secondari**: scheda semplificata, senza stat block completo.

Ogni NPC deve avere: motivazione chiara, tratto distintivo, e idealmente un segreto.

#### 5. AdventureBook.md

Istruzioni per l'AI specifiche dell'avventura. Cosa sa, cosa non deve rivelare, note strutturali:

```markdown
# AdventureBook.md — Istruzioni per l'AI

Questa avventura segue la struttura standard definita in `tech/rules/AdventureTemplate.md`.

## Note specifiche

- [tipo avventura, numero moduli]
- [tono e stile]
- [NPC chiave e loro ruolo]
- [agganci con altre avventure se applicabile]
```

#### 6. PlanBook.md

Stato del lavoro, todo, note riservate al DM:

```markdown
# PlanBook — NomeMiaAvventura

## Stato generale

- [x] README.md
- [x] documento principale
- [ ] mappa generale
- [ ] modulo 01
- [ ] modulo 02
- [ ] personaggi PNG

## Note

*(tono, scelte narrative, problemi aperti, agganci futuri)*
```

### Testo da leggere ai giocatori

Usare blockquote per il testo da leggere ad alta voce:

```markdown
> L'aria puzza di zolfo e cenere. Davanti a voi, i moli di Oakshore sono avvolti
> in una nebbia rossastra che non avevate mai visto prima.
```

### Agganci futuri

Se l'avventura lascia fili aperti, documentarli:

```markdown
## Agganci futuri
- [elemento] → può essere sviluppato in [avventura futura]
```

---

## Fase 5 — Verifica

```bash
python3 tech/scripts/check-adventure.py NomeMiaAvventura
```

Il report viene salvato in `tech/reports/`. Iterare fino a zero errori. I warning sono accettabili.

**Criteri di completamento:**
- Zero errori nel check
- Tutti i file obbligatori presenti
- Tutte le sezioni obbligatorie presenti
- Naming convention rispettata
- Difficoltà incontri calcolata per ogni modulo con combattimento

---

## Fase 6 — Release

```bash
bash tech/scripts/release.sh NomeMiaAvventura 0.1
```

Output in `releases/NomeMiaAvventura/`. Il PDF viene generato via pandoc + wkhtmltopdf.

Guida dettagliata: `tech/how-to/HowToRelease.md`

---

## Riepilogo file obbligatori

| file | scopo |
|------|-------|
| `README.md` | Presentazione pubblica senza spoiler |
| `AdventureBook.md` | Istruzioni per l'AI |
| `PlanBook.md` | Stato lavoro, todo, note DM |
| `NomeMiaAvventura.md` | Documento principale: lore, plot, NPC, struttura |
| `mappe/MappaGenerale.md` | Luoghi, connessioni, distanze |
| `NN_NomeModulo/NomeModulo.md` | Un file per modulo (almeno uno) |

---

## Checklist rapida

```
[ ] Concept definito (tipo, livello, tono, plot in 5-10 righe)
[ ] Scaffolding: new-adventure.sh
[ ] Metadati: adventure-wizard.py
[ ] Moduli rinominati e creati
[ ] NPC creati (wizard o template)
[ ] Placeholder NPC eliminato
[ ] Documento principale compilato
[ ] Mappa generale compilata
[ ] Moduli compilati
[ ] Schede NPC compilate
[ ] AdventureBook.md compilato
[ ] PlanBook.md aggiornato
[ ] Difficoltà incontri calcolata
[ ] check-adventure.py: zero errori
[ ] Release generata (quando pronta)
```
