# How-To: Usare Claude Code in questo Progetto

Guida all'uso di Claude Code (CLI) per lavorare sul progetto `dungeonandragon`.

---

## Modelli disponibili

| Alias | Modello | Quando usarlo |
|-------|---------|---------------|
| `sonnet` | claude-sonnet-4-6 | Default per questo progetto — migrazione legacy, script, validazione struttura |
| `opus` | claude-opus-4-6 | Scrittura narrativa complessa, lore, dialoghi NPC con alta coerenza |
| `haiku` | claude-haiku-4-5 | Task semplici e veloci, bozze rapide |

**Raccomandazione:** usa `sonnet` per tutto il lavoro tecnico e strutturale. Passa a `opus` solo per generare contenuto narrativo dove qualità e coerenza contano davvero.

---

## Cambiare modello

### Durante una sessione attiva

```
/model sonnet
/model opus
```

### Al lancio (una tantum)

```bash
claude --model sonnet
```

### Persistente (settings file)

Aggiungi a `~/.claude/settings.json`:

```json
{
  "model": "claude-sonnet-4-6"
}
```

### Ordine di priorità

`/model` in sessione > `--model` al lancio > `ANTHROPIC_MODEL` env var > settings file

---

## Avviare una sessione di lavoro

Dalla root del progetto:

```bash
cd ~/dungeonandragon
claude
```

Claude Code legge automaticamente `CLAUDE.md` nella root — contiene le convenzioni del progetto e i comandi principali.

---

## Skill Kiro vs Claude Code

Questo progetto usa due strumenti AI:

| Strumento | Quando usarlo |
|-----------|---------------|
| **Claude Code** (`claude`) | Scrittura script, refactoring, generazione contenuto strutturato, debug |
| **Kiro** | Sessioni di gioco, interpretare PNG, generare contenuto narrativo guidato dalla Skill `dungeonmaster` |

La Skill Kiro per le avventure è in `.kiro/skills/dungeonmaster/SKILL.md`.

---

## Comandi utili in sessione

| Comando | Descrizione |
|---------|-------------|
| `/model <alias>` | Cambia modello |
| `/clear` | Pulisce la sessione (libera contesto) |
| `/help` | Mostra comandi disponibili |
| `! <comando>` | Esegue un comando shell direttamente nella sessione |

---

## Contesto progetto

Claude Code carica `CLAUDE.md` automaticamente. Se serve ricaricare il contesto dopo un `/clear`:

```bash
cat CLAUDE.md
```

Per dare contesto su un'avventura specifica, inizia la sessione indicando il file principale:

```
Sto lavorando su adventures/LAnelloDelConte — leggi AdventureBook.md per il contesto.
```
