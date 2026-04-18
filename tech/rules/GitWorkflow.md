# Git Workflow

Convenzioni git per il progetto dungeonandragon.

**Repository**: `https://github.com/dracoroboter/dnd-generator.git`
**Branch principale**: `main`

---

## Struttura

Mono-repo: tutto il progetto (avventure, script, regole, template) in un unico repository.

## .gitignore

| path | motivo |
|------|--------|
| `tech/reports/` | Output generati da `check-adventure.py` — rigenerabili |
| `releases/` | PDF + ZIP generati da `release.sh` — rigenerabili |
| `legacy/` | File `.odt` originali — pesanti, sola lettura, non modificati |
| `tech/data/srd/` | SRD clonato da repo esterno |
| `tech/build/` | Artefatti di build |
| `node_modules/`, `__pycache__/` | Dipendenze e cache |

## Commit

### Quando committare

- Dopo una sessione di lavoro coerente (nuova avventura, fix tooling, nuova feature)
- Prima di cambiare contesto (es. da narrativa a tecnica)
- Non committare lavoro a metà senza motivo

### Formato commit message

```
<cosa>: <descrizione breve>

[corpo opzionale con dettagli]
```

Esempi:
```
avventura: FuoriDaHellfire prima stesura completa
tooling: fix new-adventure.sh (P1-P4) + --modules N
docs: HowToNewAdventure riscritto, HowToNewNPC creato
template: PlanBook con sezione Concept, placeholder saga fix
```

Prefissi:
| prefisso | uso |
|----------|-----|
| `avventura` | contenuto narrativo (moduli, NPC, mappe) |
| `tooling` | script in `tech/scripts/` |
| `docs` | how-to, regole, guide in `tech/` |
| `template` | modifiche a `AdventureTemplate/` |
| `fix` | correzioni a file esistenti |
| `meta` | README root, meta-dnd.md, plan-meta-dnd.md, gitignore |

### Cosa NON committare

- File in `tech/reports/` (gitignore)
- File in `releases/` (gitignore)
- File in `legacy/` (gitignore)
- Segreti, credenziali, file `.env`

## Branch

Per ora si lavora su `main` (progetto personale, singolo contributore). Se serve isolare un esperimento:

```bash
git checkout -b esperimento/nome-descrittivo
# ... lavoro ...
git checkout main
git merge esperimento/nome-descrittivo
git branch -d esperimento/nome-descrittivo
```

## Push

```bash
git push origin main
```

Non usare `--force` senza motivo.

## Workflow tipico

```bash
# 1. Verifica stato
git status

# 2. Aggiungi file specifici (preferito) o tutti
git add adventures/FuoriDaHellfire/
git add tech/how-to/HowToNewNPC.md
# oppure: git add -A

# 3. Commit
git commit -m "avventura: FuoriDaHellfire prima stesura completa"

# 4. Push
git push origin main
```

## File grandi

Le immagini (PNG, JPG) nelle avventure possono essere pesanti. Per ora sono committate normalmente. Se il repo diventa troppo grande, valutare Git LFS per `*.png`, `*.jpg`, `*.svg` sopra 1MB.
