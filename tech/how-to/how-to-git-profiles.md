# How To — Separare Profili Git su Stessa Macchina

## Situazione

Sulla stessa macchina convivono due identità GitHub:

| | Account A | Account B |
|---|-----------|-----------|
| **Username** | mario | pippo42 |
| **Email** | mario@esempio.com | pippo42@gmail.com |
| **Uso** | Repo principali | `dungeonandragon` e progetti secondari |

La config globale (`~/.gitconfig`) è impostata sull'account A. Per usare l'account B solo in questo repo, serve una config locale.

## Config locale per questo repo

```bash
cd ~/dungeonandragon
git config user.name "pippo42"
git config user.email "pippo42@gmail.com"
```

Verifica:

```bash
git config user.name   # → pippo42
git config user.email  # → pippo42@gmail.com
```

## Autenticazione per push

GitHub richiede un **Personal Access Token (PAT)**, non la password.

### Creare il PAT

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Scope: solo `repo`. Expiration: 90 days.
4. Copia il token (`ghp_...`)

### Salvare il token localmente

```bash
cd ~/dungeonandragon
# Cache per 1 settimana (solo questo repo)
git config credential.helper 'cache --timeout=604800'
```

Al primo `git push`: username = `pippo42`, password = il PAT.

Usare `credential.helper` solo nella config **locale** (senza `--global`) per non interferire con l'altro account.

## Riepilogo

```
~/.gitconfig (globale)          → mario@esempio.com (tutti gli altri repo)
~/dungeonandragon/.git/config   → pippo42@gmail.com (solo questo repo)
```
