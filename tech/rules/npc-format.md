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
- Posizione: `adventures/<NomeAvventura>/characters/markdown/`

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
