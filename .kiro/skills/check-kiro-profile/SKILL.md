# Check Kiro Profile - Verifica profilo hobby

Verifica che la sessione Kiro CLI attiva sia quella personale (hobby, Builder ID / Google), non quella aziendale (Pro, IAM Identity Center).

Usa questa skill quando vuoi assicurarti di essere sul profilo corretto prima di lavorare su progetti hobby in `~/dungeonandragon`.

## Come usarla

Chiedi a Kiro: "controlla il profilo" oppure "sono sul profilo giusto?"

## Procedura

1. Esegui `kiro-cli whoami`
2. Controlla l'output:
   - ✅ **Profilo hobby corretto** se l'output contiene `Logged in with Builder ID` e l'email è quella Gmail personale (`[tua-email-gmail]`)
   - ⚠️ **ATTENZIONE** se l'output contiene `Logged in with IAM Identity Center` — sei sul profilo aziendale, non su quello hobby

## Warning

Se sei sul profilo aziendale, avvisa l'utente con questo messaggio:

> ⚠️ **Sei loggato con il profilo AZIENDALE (Pro/IAM Identity Center).**
> Stai lavorando in `~/dungeonandragon` che è un progetto hobby.
> Per passare al profilo hobby esegui:
> ```bash
> kiro-cli logout
> kiro-cli login --license free
> ```
> ⚠️ Fallo da un terminale separato, NON da dentro questa sessione Kiro CLI.
