# How-To: Creare un NPC

Guida per creare schede NPC nel formato standard del progetto.

Riferimenti:
- Template NPC: `adventures/AdventureTemplate/characters/NPC_NomePersonaggio.md`
- Regole contenuto NPC: `tech/rules/ContentRules.md` (sezione PNG)
- Script: `tech/scripts/new-npc.py`

---

## Lo script `new-npc.py`

### Uso

```bash
# Wizard interattivo — chiede i campi uno per uno
python3 tech/scripts/new-npc.py NomeAvventura

# Template vuoto — crea il file con placeholder da compilare a mano
python3 tech/scripts/new-npc.py NomeAvventura --template
```

### Cosa fa

1. Chiede il nome del personaggio
2. In modalità wizard: chiede ruolo, razza, allineamento, classe, tratto fisico, modo di parlare, motivazione, segreto, note al master
3. In modalità template: crea il file con sezioni vuote marcate `⚠ Da compilare`
4. Genera `characters/NPC_NomePersonaggio.md` nella directory dell'avventura

### Sezioni generate

| sezione | wizard | template |
|---------|--------|----------|
| Informazioni generali | compilata | placeholder |
| Descrizione | compilata (tratto + parlata) | placeholder |
| Motivazioni | compilata + segreto | placeholder |
| Note al master | compilata | placeholder |
| Stat Block | placeholder | placeholder |
| Agganci futuri | placeholder | placeholder |

### Limiti attuali

- Non genera stat block numerici (PF, CA, attacchi, abilità) — vanno aggiunti a mano
- Non supporta input da file o descrizione libera
- Non calcola i modificatori dalle statistiche
- Non esporta in formati esterni (XML FightClub, PDF)

---

## Workflow alternativo: AI + descrizione libera

Per NPC complessi (antagonisti con stat block, abilità speciali, tattiche), il workflow più efficiente è:

1. **Descrivi l'NPC all'AI in linguaggio naturale** — nome, ruolo, razza, classe, livello, personalità, abilità speciali, stat block se lo hai
2. **L'AI genera il file** `characters/NPC_Nome.md` nel formato standard con tutti i dettagli meccanici
3. **Verifica** con `check-adventure.py`

Questo workflow è più veloce del wizard per NPC con stat block complessi, perché l'AI può:
- Calcolare modificatori dalle statistiche
- Formattare attacchi e abilità nel formato tabellare standard
- Generare tattiche di combattimento coerenti con le abilità
- Aggiungere le sezioni narrative (motivazioni, segreti, agganci)

### Quando usare cosa

| situazione | strumento |
|-----------|-----------|
| NPC secondario senza stat block | `new-npc.py --template` + compilare a mano |
| NPC con pochi tratti da definire | `new-npc.py` (wizard interattivo) |
| Antagonista con stat block completo | AI + descrizione libera |
| Batch di NPC simili | `new-npc.py --template` × N |

---

## Flow di lavoro

### Flow A — PG da FightClub

Un giocatore esporta il suo PG dall'app FightClub. Serve il markdown e lo stat block stampabile.

```
1. Ricevi il file XML dal giocatore
   → salvalo in characters/fightclub/

2. Genera il markdown
   python3 tech/fightclub/fightclub-to-md.py characters/fightclub/NomePC.xml \
       -o characters/markdown/PG_NomePC.md

3. Genera lo stat block (PDF + PNG)
   node tech/fightclub/md-to-statblock-pdf.js characters/fightclub/NomePC.xml \
       -o characters/statblock/NomePC.pdf
   node tech/fightclub/md-to-statblock-pdf.js characters/fightclub/NomePC.xml \
       -o characters/statblock/NomePC.png

4. (Opzionale) Aggiungi la foto
   → metti l'immagine in characters/img/NomePC.png
   → rigenera con --image:
   node tech/fightclub/md-to-statblock-pdf.js characters/fightclub/NomePC.xml \
       -o characters/statblock/NomePC.pdf --image characters/img/NomePC.png

5. Completa il markdown generato
   → le sezioni narrative (Motivazioni, Note al master) sono marcate ⚠ Da compilare
   → compilale a mano o con l'AI
```

### Flow B — NPC/mostro da descrizione

Descrivi un NPC o mostro all'AI (o a mano). Serve il FightClub XML e lo stat block stampabile.

```
1. Crea il markdown
   → descrivi l'NPC all'AI, che genera characters/markdown/NPC_Nome.md
   → oppure usa lo script: python3 tech/scripts/new-npc.py NomeAvventura
   → oppure scrivi a mano seguendo il formato in tech/rules/NPCFormat.md

2. (Opzionale) Aggiungi la foto
   → metti l'immagine in characters/img/Nome.png

3. Genera il FightClub XML
   python3 tech/fightclub/md-to-fightclub.py characters/markdown/NPC_Nome.md \
       -o characters/fightclub/NPC_Nome.xml

4. Genera lo stat block (PDF + PNG)
   node tech/fightclub/md-to-statblock-pdf.js characters/fightclub/NPC_Nome.xml \
       -o characters/statblock/NPC_Nome.pdf --image characters/img/Nome.png
   node tech/fightclub/md-to-statblock-pdf.js characters/fightclub/NPC_Nome.xml \
       -o characters/statblock/NPC_Nome.png --image characters/img/Nome.png

5. Importa l'XML in FightClub
   → trasferisci NPC_Nome.xml sul dispositivo
   → FightClub → Settings → Import
```

### Riepilogo pipeline

```
Flow A (PG da app):     XML → md + stat block
Flow B (NPC da testo):  md → XML → stat block

Entrambi:
  characters/
  ├── markdown/    ← fonte narrativa (.md)
  ├── img/         ← foto personaggi
  ├── fightclub/   ← XML per l'app (.xml)
  └── statblock/   ← stampabili (.pdf, .png)
```

---

## Formato stat block

Per NPC con stat block, seguire questo formato (da `ContentRules.md`):

```markdown
## Stat Block

| FOR | DES | COS | INT | SAG | CAR |
|-----|-----|-----|-----|-----|-----|
| X (+X) | X (+X) | X (+X) | X (+X) | X (+X) | X (+X) |

- **Punti ferita**: X
- **Classe armatura**: X
- **Velocità**: Xm / Xft / Xqd
- **Iniziativa**: +X
- **Bonus competenza**: +X
- **Lingue**: ...
- **Sensi**: ...
- **Immunità/Resistenze**: ...

## Attacchi

### Nome Attacco (mischia/distanza)
- **Attacco**: +X, mischia/distanza Xm / Xft / Xqd
- **Danni**: XdX+X tipo
- **Effetto**: ...
```

---

## TODO futuri

### Export XML FightClub 5e

FightClub 5e (iOS/Android) usa un formato XML specifico per importare mostri/NPC.

**Risorse chiave:**
- **[kinkofer/FightClub5eXML](https://github.com/kinkofer/FightClub5eXML)** (733 ⭐) — repo di riferimento con tutti i sorgenti D&D ufficiali in XML. Contiene la struttura XML da seguire nella directory `Sources/`. Usa `xsltproc` per compilare collection → compendium importabile.
- **[Moonlington/5eTtoFC5](https://github.com/Moonlington/5eTtoFC5)** — tool per convertire da formato 5eTools a FightClub XML.
- **[matteraByte/5eDataParser](https://github.com/matteraByte/5eDataParser)** — parser/converter tra XML, JSON e markdown per stat block 5e.
- **[vidalvanbergen/CompendiumEditor](https://github.com/vidalvanbergen/CompendiumEditor)** — editor GUI per creare/modificare XML FightClub.

**Approccio**: creare uno script Python che legga le schede NPC markdown del progetto e generi XML nel formato FightClub. Usare i file in `Sources/` del repo kinkofer come riferimento per la struttura XML.

### Export PDF grafica WotC

Generare stat block nella grafica classica Wizard of the Coast (pergamena, bordi rossi, font serif).

**Risorse chiave:**
- **[tetra-cube.com/dnd/dnd-statblock](https://tetra-cube.com/dnd/dnd-statblock)** — generatore web. Compila i campi e esporta come immagine o "Printable Block". Basato su [Valloric/statblock5e](https://github.com/Valloric/statblock5e) (Web Component HTML/CSS). Supporta anche export Markdown.
- **[Valloric/statblock5e](https://github.com/Valloric/statblock5e)** — Web Component HTML/CSS che renderizza stat block nella grafica WotC. Usabile standalone in un browser. Potenzialmente automatizzabile con Playwright per generare screenshot/PDF.
- **[Homebrewery](https://homebrewery.naturalcrit.com/)** — editor web che genera PDF in stile WotC. Usa Markdown come input. Non ha API, ma il formato Markdown è documentato.
- **[GM Binder](https://www.gmbinder.com/)** — simile a Homebrewery, genera PDF in stile WotC da Markdown.
- **[javalent/fantasy-statblocks](https://github.com/javalent/fantasy-statblocks)** — plugin Obsidian per stat block in stile D&D. Utile se si usa Obsidian, non per automazione.

**Approccio più promettente**: usare `statblock5e` (Web Component) + Playwright per generare PNG/PDF automaticamente. Lo script legge il markdown NPC, popola il Web Component, e fa screenshot. Simile alla pipeline Watabou già presente nel progetto.
