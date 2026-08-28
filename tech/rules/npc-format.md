---
name: npc-format
description: Formato markdown per schede NPC/MON. Sezioni obbligatorie, stat block, attacchi, pipeline FightClub XML e stat block PDF/PNG. Naming con prefissi NPC_/MON_/PG_.
---

# Formato Markdown per NPC e Mostri

Specifica del formato `.md` usato nelle schede personaggio del progetto.
Questo formato è la fonte di verità per la generazione di XML FightClub e stat block PDF/PNG.

---

## Principi

- **Human readable**: il file deve essere leggibile e modificabile a mano
- **Machine parsable**: il parser (`md-to-fightclub.py`) estrae i dati meccanici dalle sezioni e dai campi
- **Aperto ad estensioni**: sezioni non riconosciute dal parser vengono ignorate senza errore. Nuove sezioni possono essere aggiunte in futuro senza rompere la compatibilità.

## Naming

- File: `PREFISSO_PascalCase.md`
- Posizione: `adventures/<NomeAvventura>/<lang>/characters/markdown/`

### Prefissi

| prefisso | tipo | esempio |
|----------|------|---------|
| `NPC_` | Personaggio Non Giocante (alleato, secondario, commerciante, ecc.) | `NPC_SirGorimVel.md` |
| `MON_` | Mostro o creatura con stat block da combattimento | `MON_RattoCorrotto.md` |
| `PG_` | Personaggio Giocante (se gestito nel progetto, raro) | `PG_Barbara.md` |

Il prefisso determina il tipo nel titolo e nell'export XML. Il formato del file è identico per tutti e tre — la distinzione è solo nel prefisso e nel ruolo narrativo.

La stessa convenzione si applica ai file generati:
- `characters/fightclub/NPC_SirGorimVel.xml`, `MON_RattoCorrotto.xml`
- `characters/statblock/NPC_SirGorimVel.pdf`, `MON_RattoCorrotto.pdf`

---

## Struttura

### Sezioni obbligatorie (richieste da `check-adventure.py`)

```markdown
# NPC_Nome — ruolo
## Informazioni generali
## Descrizione
## Motivazioni
## Note al master
```

### Sezioni meccaniche (richieste per export FightClub/stat block)

```markdown
## Stat Block
## Attacchi
```

### Sezioni opzionali (ignorate dal parser se assenti)

```markdown
## Capacità notevoli
## Azioni bonus
## Reazioni
## Ruolo nell'avventura
## Agganci futuri
## Da definire
```

Qualsiasi altra sezione `##` è consentita e viene ignorata dal parser.

---

## Formato dettagliato

### Titolo

```markdown
# NPC_Nome — ruolo
```

`ruolo` è uno tra: `antagonista`, `alleato`, `secondario`, `companion`.
Il parser estrae il nome rimuovendo `NPC_` e tutto dopo ` — `.

### Informazioni generali

```markdown
## Informazioni generali

- **Ruolo**: antagonista principale
- **Classe**: bardo
- **Livello**: 4
- **Razza**: elfo
- **Allineamento**: Caotico Malvagio
```

Campi riconosciuti dal parser: `Ruolo`, `Classe`, `Livello`, `Razza`, `Allineamento`.
Tutti opzionali. Il parser usa i valori per generare `<type>`, `<alignment>`, `<cr>` nell'XML.

### Descrizione

```markdown
## Descrizione

Testo libero. Aspetto fisico, modo di parlare, tratto distintivo.
```

Il parser estrae il testo per il tag `<description>` dell'XML.

### Stat Block

```markdown
## Stat Block

| FOR | DES | COS | INT | SAG | CAR |
|-----|-----|-----|-----|-----|-----|
| 13 (+1) | 16 (+3) | 14 (+2) | 8 (-1) | 12 (+1) | 15 (+2) |

- **Punti ferita**: 52
- **Classe armatura**: 13
- **Velocità**: 12m / 40ft / 8qd
- **Iniziativa**: +3
- **Bonus competenza**: +2
- **Tiri salvezza**: FOR +4, COS +4
- **Competenze**: Persuasione +4, Intuizione +3
- **Percezione**: +3
- **Performance**: +4
- **Furtività**: +5
- **Immunità**: veleno
- **Sensi**: scurovisione
- **Lingue**: Comune, Elfico
- **Sfida**: 3 (700 PE)
- **Strumenti**: Arnesi da scasso
```

**Tabella abilità**: esattamente 6 colonne, formato `valore (+mod)` o `valore(-mod)`.

**Campi**: formato `- **NomeCampo**: valore`. Il parser riconosce i campi elencati sopra.
Campi non riconosciuti vengono ignorati senza errore.

**Velocità**: formato triplo `Xm / Xft / Xqd`. Il parser estrae i feet per l'XML.

### Capacità notevoli

```markdown
## Capacità notevoli

- **Nome capacità**: descrizione della capacità
- **Altra capacità**: altra descrizione
```

Formato: lista con `- **Nome**: testo`. Ogni voce diventa un `<trait>` nell'XML.

### Attacchi

```markdown
## Attacchi

### Nome Attacco (mischia)
- **Attacco**: +5, mischia
- **Danni**: 2d4+3 perforanti + 2d6 veleno
- **Effetto**: il bersaglio è avvelenato

### Altro Attacco (distanza)
- **Attacco**: +5, distanza 36m / 120ft / 24qd
- **Tiro salvezza**: Saggezza CD 12
- **Fallimento**: 4d6 danni psichici + charmato
- **Successo**: metà dei danni
```

Ogni `###` diventa un `<action>` nell'XML. I campi `Attacco` e `Danni` generano il tag `<attack>`.

### Azioni bonus

```markdown
## Azioni bonus

- **Disengage**: descrizione
- **Dash**: descrizione
```

Formato: lista con `- **Nome**: testo`. Ogni voce diventa un `<trait>` nell'XML (FightClub non ha un tag separato per le azioni bonus).

### Reazioni

```markdown
## Reazioni

- **Parry**: +2 alla CA contro un attacco in mischia
```

Formato: lista con `- **Nome**: testo`. Ogni voce diventa un `<reaction>` nell'XML.

### Motivazioni, Ruolo, Note al master, Agganci futuri

Testo libero. Non esportati nell'XML FightClub (sono sezioni narrative, non meccaniche).

---

## Distinzione NPC / PG / Mostri

| tipo | prefisso | formato MD | fonte XML | export |
|------|----------|-----------|-----------|--------|
| **NPC** | `NPC_` | `NPC_*.md` in `characters/markdown/` | generato da `md-to-fightclub.py` | XML + stat block PDF/PNG |
| **Mostri** | `MON_` | `MON_*.md` in `characters/markdown/` | generato da `md-to-fightclub.py` | XML + stat block PDF/PNG |
| **PG** | `PG_` | raro (gestiti dall'app FightClub) | esportati dall'app in `characters/fightclub/` | stat block PDF/PNG |

---

## Pipeline

```
characters/markdown/NPC_Nome.md
    ↓ md-to-fightclub.py
characters/fightclub/NPC_Nome.xml
    ↓ md-to-statblock-pdf.js [--image characters/img/Nome.ext]
characters/statblock/NPC_Nome.pdf + NPC_Nome.png
```

---

## TODO

- [ ] Il parser `md-to-fightclub.py` non gestisce ancora `## Reazioni` — da aggiungere
- [ ] Aggiungere supporto per `## Azioni leggendarie` (mostri potenti)
- [ ] Aggiungere supporto per `## Incantesimi` come sezione separata (alternativa a metterli in Capacità notevoli)
- [ ] Valutare se servono sezioni per equipaggiamento e inventario
- [ ] Valutare formato MD per PG (attualmente non previsto — i PG vengono dall'app)
- [ ] `check-adventure.py` dovrebbe riconoscere le sezioni meccaniche (Stat Block, Attacchi) come valide senza warning

---

## Multilingua

I file NPC possono esistere in più lingue. La struttura per lingua è:

```
adventures/<NomeAvventura>/it/characters/markdown/NPC_Nome.md   # italiano (fonte)
adventures/<NomeAvventura>/en/characters/markdown/NPC_Nome.md   # inglese
```

I file generati seguono la stessa struttura:

```
adventures/<NomeAvventura>/<lang>/characters/fightclub/NPC_Nome.xml
adventures/<NomeAvventura>/<lang>/characters/statblock/NPC_Nome.pdf
adventures/<NomeAvventura>/<lang>/characters/statblock/NPC_Nome.png
```

Le immagini restano nella root dell'avventura (non dipendono dalla lingua): `characters/img/`.

### Intestazioni e campi in inglese

I file NPC in inglese usano intestazioni e label in inglese:

| Sezione IT | Sezione EN |
|------------|------------|
| `## Informazioni generali` | `## General Information` |
| `## Descrizione` | `## Description` |
| `## Motivazioni` | `## Motivations` |
| `## Note al master` | `## DM Notes` |
| `## Stat Block` | `## Stat Block` |
| `## Attacchi` | `## Attacks` |
| `## Azioni bonus` | `## Bonus Actions` |
| `## Capacità notevoli` | `## Notable Abilities` |

### Tabella abilità in inglese

```markdown
| STR | DEX | CON | INT | WIS | CHA |
```

### Campi stat block in inglese

| Campo IT | Campo EN |
|----------|----------|
| **Punti ferita** | **Hit Points** |
| **Classe armatura** | **Armor Class** |
| **Velocità** | **Speed** |
| **Sfida** | **Challenge** |
| **Sensi** | **Senses** |
| **Lingue** | **Languages** |
| **Bonus competenza** | **Proficiency Bonus** |
| **Attacco** | **Attack** |
| **Danni** | **Damage** |

### File i18n

Le label sono definite in `tech/i18n/<lang>.json`. Il parser le usa per riconoscere intestazioni e campi nella lingua corretta.

### Pipeline

```bash
python3 tech/fightclub/md-to-fightclub.py NPC_Nome.md --lang en
python3 tech/fightclub/generate-statblocks.py NomeAvventura --lang en
```

### Role line nello stat block

Il parser aggiunge automaticamente `Role: <ruolo>` in fondo al tag `<description>` dell'XML, leggendo il campo `**Ruolo**` / `**Role**` dalla sezione Informazioni generali. Questa riga è visibile anche nello stat block grafico (PDF/PNG), in corsivo sotto il sottotitolo.

### Nomi mostri in inglese

I nomi propri (Korex, Fin Ditasvelte, Sir Gorim Vel) **non si traducono**. Le descrizioni e i titoli si traducono:

| IT | EN | Nota |
|----|-----|------|
| Il Conte | The Count | descrizione, non nome proprio |
| Teppista Charmato | Charmed Thug | Thug variant, MM p.350 |
| Ratto Corrotto | Corrupted Rat | Giant Rat variant, MM p.327 |
| Sciame di Ratti | Swarm of Rats | MM p.339 |
| Guardiano Lumina | Guardian of Lumina | homebrew |

Per i mostri basati su creature SRD, aggiungere il riferimento WotC nel file EN (es. `*(Thug variant, Monster Manual p.350)*`).

---

## Variante Carbon 2185

Per le avventure che usano il sistema Carbon 2185 (basato su SRD 5.1 ma con ambientazione cyberpunk), il formato della scheda cambia nei seguenti punti:

### Ability Scores

| D&D 5e | Carbon 2185 |
|--------|-------------|
| STR, DEX, CON, INT, WIS, CHA | STR, DEX, CON, INT, TEC, PEO |

### Saving Throws

| D&D 5e | Carbon 2185 |
|--------|-------------|
| Forza, Destrezza, Costituzione, Intelligenza, Saggezza, Carisma | Fortitude (CON), Reflex (DEX), Mind (INT) |

### Campi aggiuntivi (PG)

- **Origine:** equivalente di razza (Korporate Kid, Wormer, Street Rat, Synth, ecc.)
- **Blood Toxicity:** limite di augmentations installabili (2 x CON modifier)
- **Influence (Street/Corporate):** reputazione nei due mondi
- **Wonlongs:** valuta (simbolo: ₩)
- **Augmentations:** lista con nome e slot (Eyes, Torso, Arms, Legs, Head, Spine)
- **Damage Resistance:** formato DR/X tipo (es. DR/3 Ballistic)

### Formato scheda PG (Carbon 2185)

```markdown
# PG_NomePersonaggio, classe

## Informazioni generali

- **Nome completo**: Nome "Nickname" Cognome
- **Classe**: Classe (Sottoclasse)
- **Livello**: N
- **Origine**: NomeOrigine
- **Background**: descrizione breve
- **Vice**: nome vice

## Stat Block

| STR | DEX | CON | INT | TEC | PEO |
|-----|-----|-----|-----|-----|-----|
| X (mod) | X (mod) | X (mod) | X (mod) | X (mod) | X (mod) |

- **PF:** X/max (Dado vita: NdX)
- **CA:** X (armatura)
- **Velocita:** X ft
- **Tiri salvezza:** Fortitude +X, Reflex +X, Mind +X
- **Blood Toxicity:** X/max
- **Influence:** Street X, Corporate X

## Competenze

Lista skill con bonus.

## Augmentations

| Nome | Slot | Effetto |
|------|------|---------|
| ... | ... | ... |

## Armi

| Nome | Bonus | Danno | Tipo | Note |
|------|-------|-------|------|------|
| ... | ... | ... | ... | ... |

## Equipaggiamento

Lista oggetti con peso.

## Capacita di classe

Lista feature attive al livello corrente.

## Note

Informazioni aggiuntive (manutenzione augmentations, dipendenze, ecc.)
```

### Formato stat block NPC/Nemici (Carbon 2185)

Identico al formato D&D 5e presente nel rulebook, con le sostituzioni di ability scores e saving throws sopra indicate. Esempio:

```markdown
# NPC_NomePersonaggio, ruolo

## Informazioni generali

- **Nome**: NomePersonaggio
- **Tipo**: Medium human (o machine/synthetic)
- **Ruolo**: descrizione breve

## Stat Block

- **CA:** X (armatura)
- **PF:** X (formula dadi)
- **Velocita:** X ft
- **DR:** DR/X tipo
- **Tiri salvezza:** Fortitude +X
- **Competenze:** Skill +X, Skill +X
- **Sensi:** Percezione passiva X
- **Lingue:** English, other
- **Grado di Sfida:** X (XP)

| STR | DEX | CON | INT | TEC | PEO |
|-----|-----|-----|-----|-----|-----|
| +X | +X | +X | +X | +X | +X |

## Capacita

Descrizione tratti speciali.

## Azioni

Descrizione attacchi e azioni.
```
