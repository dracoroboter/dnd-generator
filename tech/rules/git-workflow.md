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

### Configurare SSH per evitare di inserire credenziali ogni volta

Il remote attuale usa HTTPS, che chiede un Personal Access Token a ogni push. Per evitarlo, passare a SSH:

```bash
# 1. Verifica se hai già una chiave SSH
ls ~/.ssh/id_*.pub

# 2. Se non ce l'hai, generala
ssh-keygen -t ed25519 -C "tua-email@esempio.com"
# Premi Invio per accettare il percorso default e scegli una passphrase (o lascia vuota)

# 3. Copia la chiave pubblica
cat ~/.ssh/id_ed25519.pub
# Copia l'output

# 4. Aggiungi la chiave su GitHub
#    → github.com → Settings → SSH and GPG keys → New SSH key → incolla

# 5. Testa la connessione
ssh -T git@github.com
# Deve rispondere: "Hi dracoroboter! You've successfully authenticated..."

# 6. Cambia il remote da HTTPS a SSH
git remote set-url origin git@github.com:dracoroboter/dnd-generator.git

# 7. Verifica
git remote -v
# Deve mostrare: git@github.com:dracoroboter/dnd-generator.git
```

Dopo questa configurazione, `git push` non chiederà più credenziali.

### Alternativa: credential helper (HTTPS)

Se preferisci restare su HTTPS senza passare a SSH:

```bash
# Salva le credenziali in cache per 1 settimana (604800 secondi) — solo per questo repo
git config credential.helper 'cache --timeout=604800'

# Oppure: salva permanentemente su disco (meno sicuro) — solo per questo repo
git config credential.helper store
```

Con `cache`: al primo push inserisci il PAT, poi non lo chiede più per 8 ore.
Con `store`: lo salva in `~/.git-credentials` in chiaro — non lo chiede mai più, ma il token è leggibile sul disco.

Al prossimo `git push`, inserisci come username il tuo utente GitHub e come password il **Personal Access Token** (non la password dell'account). Per generare un PAT: GitHub → Settings → Developer settings → Personal access tokens → Generate new token (scope: `repo`).

## Workflow tipico

```bash
# 1. Verifica stato
git status

# 2. Aggiungi file specifici (preferito) o tutti
git add adventures/FuoriDaHellfire/
git add tech/how-to/how-to-new-npc.md
# oppure: git add -A

# 3. Commit
git commit -m "avventura: FuoriDaHellfire prima stesura completa"

# 4. Push
git push origin main
```

## File grandi

Le immagini (PNG, JPG) nelle avventure possono essere pesanti. Per ora sono committate normalmente. Se il repo diventa troppo grande, valutare Git LFS per `*.png`, `*.jpg`, `*.svg` sopra 1MB.
