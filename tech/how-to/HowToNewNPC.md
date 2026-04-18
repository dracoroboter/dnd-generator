# How-To: Creare un NPC

Guida per creare schede NPC nel formato standard del progetto.

Riferimenti:
- Template NPC: `adventures/AdventureTemplate/personaggi/NPC_NomePersonaggio.md`
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
4. Genera `personaggi/NPC_NomePersonaggio.md` nella directory dell'avventura

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
2. **L'AI genera il file** `personaggi/NPC_Nome.md` nel formato standard con tutti i dettagli meccanici
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
