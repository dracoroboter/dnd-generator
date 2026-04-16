# How To — Separare Git Aziendale e Personale

## Situazione

Sulla stessa macchina convivono due identità GitHub:

| | Aziendale | Personale |
|---|-----------|-----------|
| **Username** | rcorda | dracoroboter |
| **Email** | roberto.corda@vivaticket.com | roberto.ilcorda@gmail.com |
| **Account GitHub** | (aziendale) | dracoroboter |
| **Uso** | Repo di lavoro | `dungeonandragon` e progetti hobby |

La config globale (`~/.gitconfig`) è impostata sull'account aziendale. Questo è corretto — la maggior parte dei repo sono di lavoro.

## Config locale per questo repo

Per committare con l'identità personale solo in `dungeonandragon`:

```bash
cd ~/dungeonandragon
git config user.name "dracoroboter"
git config user.email "roberto.ilcorda@gmail.com"
```

Questo scrive in `.git/config` (locale). Git usa sempre la config locale se presente, altrimenti cade sulla globale.

Verifica:

```bash
git config user.name   # → dracoroboter
git config user.email  # → roberto.ilcorda@gmail.com
```

## Autenticazione per push

GitHub non accetta password per `git push` dal 2021. Serve un **Personal Access Token (PAT)**.

### Creare il PAT

1. Logga su https://github.com con l'account `dracoroboter`
2. Vai su https://github.com/settings/tokens (oppure: icona profilo → Settings → Developer settings → Personal access tokens → Tokens (classic))
3. Clicca **"Generate new token"** → **"Generate new token (classic)"**
4. Compila:
   - **Note**: `dungeonandragon-wsl` (nome descrittivo)
   - **Expiration**: scegli la durata (consigliato: 90 days, poi rinnovare)
   - **Scopes**: seleziona solo `repo` (accesso completo ai repository)
5. Clicca **"Generate token"**
6. **Copia il token** (inizia con `ghp_...`) — non sarà più visibile dopo

### Salvare il token localmente

Per non reinserirlo ogni volta:

```bash
cd ~/dungeonandragon
git config credential.helper store
```

Al primo `git push` inserisci:
- Username: `dracoroboter`
- Password: il PAT copiato sopra

Verrà salvato in `~/.git-credentials` (testo in chiaro).

Alternativa più sicura (tiene in memoria per 1 ora, poi lo richiede):

```bash
git config credential.helper 'cache --timeout=3600'
```

### Conflitto credenziali con account aziendale

Se anche i repo aziendali usano `credential.helper store`, le credenziali di `robertocorda` potrebbero sovrascrivere quelle aziendali in `~/.git-credentials`. Per evitarlo, usa `store` solo nella config **locale** di questo repo (come sopra, senza `--global`).

## Recupero password account personale

Se non ricordi la password dell'account `robertocorda`:

1. Vai su https://github.com/password_reset
2. Inserisci la tua email Gmail
3. Segui il link di reset ricevuto via email
4. Dopo il login, crea il PAT come descritto sopra

## Riepilogo

```
~/.gitconfig (globale)          → vivaticket (tutti i repo di lavoro)
~/dungeonandragon/.git/config   → roberto.ilcorda@gmail.com + dracoroboter (solo questo repo)
```

Ogni `git commit` in `dungeonandragon` userà l'identità personale. Tutti gli altri repo restano invariati.
