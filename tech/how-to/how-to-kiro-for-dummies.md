# Guida a Kiro CLI — Per chi non ha mai aperto un terminale

Questa guida è per chi non programma, non ha mai usato una riga di comando, e vuole usare Kiro CLI come assistente personale per organizzare materiale, studiare, scrivere.

---

## 1. Cos'è una shell (e perché ti serve)

Una **shell** è un programma dove scrivi comandi in testo. Niente finestre, niente bottoni — solo testo. Scrivi qualcosa, premi Invio, succede qualcosa.

Perché usarla? Perché Kiro CLI funziona lì dentro. È come una chat, ma nel terminale.

**Come aprirla:**

- **Windows:** premi il tasto Windows, scrivi `PowerShell`, clicca su "Windows PowerShell"
- **Mac:** apri Spotlight (Cmd+Spazio), scrivi `Terminal`, premi Invio

Quello che si apre è la shell. Una finestra nera (o bianca) con un cursore che lampeggia.

**Quale shell usi per cosa:**

| Azione | Windows | Mac |
|--------|---------|-----|
| Installare WSL | PowerShell (come admin) | — |
| Installare Kiro CLI | PowerShell o Windows Terminal | Terminal |
| Usare Kiro CLI | PowerShell, Windows Terminal, o WSL | Terminal |
| Comandi Linux (`ls`, `cd`, `mkdir`...) | Solo dentro WSL | Terminal (sono nativi) |

**In questa guida**, ogni blocco di codice indica dove scriverlo: **(cmd)** = PowerShell/Windows Terminal, **(wsl)** = dentro WSL, **(mac)** = Mac Terminal, **(*)** = qualsiasi (funziona ovunque).

---

## 2. Installare WSL (solo Windows)

Su Windows, Kiro CLI funziona dentro **WSL** (Windows Subsystem for Linux) — un mini-Linux che vive dentro Windows. Non ti cambia niente nel computer, è solo una "stanza in più".

**Ci vogliono 10 minuti e non puoi rompere niente.** Se qualcosa va storto, puoi disinstallare WSL senza conseguenze.

**Come installarlo:**

1. Apri PowerShell **come amministratore** (tasto destro → "Esegui come amministratore")
2. Scrivi questo e premi Invio ((cmd)):
   ```
   wsl --install
   ```
3. Aspetta che finisca (scarica Ubuntu, ci mette un po')
4. Riavvia il computer quando te lo chiede
5. Dopo il riavvio, si apre una finestra che ti chiede nome utente e password — scegli qualcosa di semplice, non serve che sia sicura

Fatto. Ora hai Linux dentro Windows.

**Per aprire WSL in futuro:** apri PowerShell e scrivi `wsl`, oppure cerca "Ubuntu" nel menu Start.

---

## 3. Dove sono i tuoi file (Windows visto da WSL)

Quando sei dentro WSL (Linux), i file del tuo Windows sono qui:

```
/mnt/c/Users/IL_TUO_NOME/
```

Per esempio:
- Il Desktop: `/mnt/c/Users/Mario/Desktop/`
- I Documenti: `/mnt/c/Users/Mario/Documents/`
- I Download: `/mnt/c/Users/Mario/Downloads/`

Se non sai il tuo nome utente Windows, scrivi nella shell ((wsl)):
```
ls /mnt/c/Users/
```
Ti mostra la lista delle cartelle utente — il tuo nome è lì.

**Su Mac** non serve WSL. I tuoi file sono dove sono sempre: `/Users/IL_TUO_NOME/`.

**⚠️ Attenzione (solo Windows):** dentro WSL hai **due cartelle personali**:

| Cartella | Cos'è | Dove la vedi da Windows |
|----------|-------|------------------------|
| `/home/NOME/` | La tua home **Linux** (dentro WSL) | Non visibile normalmente da Esplora File |
| `/mnt/c/Users/NOME/` | La tua home **Windows** (il tuo Desktop, Documenti, ecc.) | È la solita cartella utente di Windows |

**Consiglio pratico:** lavora sempre in `/mnt/c/Users/NOME/` — così i file li vedi anche da Windows (Desktop, Esplora File, ecc.). Se lavori in `/home/NOME/` i file esistono solo dentro WSL e non li trovi facilmente da Windows.

---

## 4. Installare Kiro CLI

### Su Mac

Apri il Terminal e scrivi ((mac)):
```
curl -fsSL https://cli.kiro.dev/install | bash
```

Un solo comando e basta. Si installa da solo.

### Su Windows — Due opzioni

**Opzione A — Installare su Windows direttamente ((cmd)):**
```
irm 'https://cli.kiro.dev/install.ps1' | iex
```
Kiro CLI funziona in PowerShell/Windows Terminal. Non serve WSL. Serve Windows 11.

**Opzione B — Installare dentro WSL ((wsl)):**
```
curl -fsSL https://cli.kiro.dev/install | bash
```
Kiro CLI funziona dentro WSL (Linux). Utile se vuoi lavorare in ambiente Linux.

**Quale scegliere?**
- Se non sai cos'è WSL o non ti interessa Linux → **Opzione A**
- Se hai già installato WSL (sezione 2) e vuoi lavorare lì → **Opzione B**
- ⚠️ Sono installazioni separate: se installi su Windows NON lo hai dentro WSL, e viceversa

**Nota:** serve Windows 11. Usa Windows Terminal o PowerShell, NON il vecchio "Prompt dei comandi".

### Primo avvio — Creare un account e fare login

Kiro CLI ha una versione gratuita. Per usarla serve un **AWS Builder ID** — è un account gratuito di Amazon (non serve carta di credito, non è Amazon Prime, non costa niente).

**Passo 1 — Avvia il login ((*) qualsiasi shell dove hai installato Kiro):**
```
kiro-cli login --license free
```

**Passo 2 — Si apre il browser:**
Kiro ti dà un link e un codice. Si apre il browser automaticamente (se non si apre, copia il link e incollalo tu).

**Passo 3 — Crea l'account Builder ID:**
- Clicca "Create AWS Builder ID"
- Inserisci la tua email personale
- Scegli una password
- Conferma il codice che ti arriva via email
- Accetta i termini

**Passo 4 — Autorizza Kiro:**
Il browser ti chiede di autorizzare "Kiro CLI" — clicca "Allow".

**Passo 5 — Torna al terminale:**
Il terminale dice qualcosa come "Logged in successfully". Sei dentro.

**Da ora in poi:** non devi più fare login ogni volta. La sessione resta attiva per settimane. Se scade, riesegui `kiro-cli login --license free`.

### Avviare una sessione

Per lavorare con Kiro, devi prima entrare nella cartella dove vuoi che lavori. Si fa con il comando `cd` ("change directory" = cambia cartella) ((*) qualsiasi shell dove hai Kiro):

```
cd ~/mio-progetto
```

- `cd` = vai nella cartella
- `~` = la tua cartella personale (su Mac: `/Users/NOME`, su WSL: `/home/NOME`)

Poi avvia Kiro:
```
kiro-cli chat
```

Sei dentro. Scrivi in italiano, Kiro risponde in italiano. È una chat.

### ✅ Checkpoint: ce l'hai fatta?

Se vedi il prompt di Kiro che aspetta il tuo testo (un cursore dopo il suo saluto), hai finito l'installazione. Scrivi "Ciao, funzioni?" e guarda cosa risponde. **Complimenti, sei operativo.**

---

## 5. Cos'è Markdown (e perché è meglio del PDF)

**Markdown** (file `.md`) è testo normale con qualche simbolo per la formattazione. I file con estensione `.md` sono file Markdown — li puoi aprire con qualsiasi editor di testo (anche il Blocco Note), ma per vederli "belli" serve un programma che li renderizzi (vedi sotto).

```markdown
# Titolo grande
## Titolo medio
### Titolo piccolo

Testo normale. **Grassetto.** *Corsivo.*

- Elenco puntato
- Un altro punto

| Colonna 1 | Colonna 2 |
|-----------|-----------|
| dato      | dato      |
```

**Perché è meglio del PDF:**

| PDF | Markdown |
|-----|----------|
| Bello da stampare, impossibile da modificare | Brutto da stampare, facilissimo da modificare |
| Kiro non può modificarlo | Kiro può leggerlo E modificarlo |
| Non si può cercare facilmente | Si cerca con Ctrl+F ovunque |
| Pesante (immagini, font) | Leggerissimo (solo testo) |
| Formato chiuso | Formato aperto, funziona ovunque |

In pratica: il PDF è un prodotto finito (come una stampa), il Markdown è un foglio di lavoro (come un quaderno). Con Kiro lavori in Markdown, quando vuoi stampare converti in PDF.

### Come leggere un Markdown "bello" (renderizzato)

Un file `.md` aperto col Blocco Note è brutto — vedi i simboli `#`, `**`, `|`. Per vederlo formattato:

| Strumento | Come | Gratis? |
|-----------|------|---------|
| **MarkText** | App semplicissima: apri il file .md e lo vedi subito formattato. Niente altro da fare. | Sì |
| **VS Code** | Apri il file → tasto destro → "Open Preview" (o Ctrl+Shift+V) | Sì |
| **Obsidian** | App desktop per Markdown, lo mostra bello in tempo reale | Sì |
| **GitHub** | Carica il file su GitHub → lo renderizza automaticamente | Sì |
| **StackEdit** | Sito web (stackedit.io), incolla il testo e lo vedi formattato | Sì |

**Consiglio per chi vuole solo leggere:** installa **MarkText** — è il più semplice, apri il file e lo vedi bello. Se vuoi anche modificare e lavorarci seriamente, installa **VS Code**.

### Come trasformare un Markdown in PDF

**Metodo 1 — Chiedi a Kiro:**
> "Converti il file appunti.md in PDF"

Kiro usa un tool interno (se disponibile) o ti guida nell'installazione di quello che serve.

**Metodo 2 — VS Code:**
1. Installa VS Code
2. Installa l'estensione "Markdown PDF" (nel menu estensioni, cerca "Markdown PDF")
3. Apri il file .md
4. Tasto destro → "Markdown PDF: Export (PDF)"
5. Il PDF appare nella stessa cartella

**Metodo 3 — Pandoc (da terminale):**
```
sudo apt install pandoc    # installa pandoc (una volta sola)
pandoc appunti.md -o appunti.pdf
```
Se ti chiede di installare anche `texlive`, scrivi sì — è grosso ma funziona.

**Metodo 4 — Obsidian:**
Apri il file → menu "..." → "Export to PDF".

---

## 6. Bootstrap: organizzare il tuo materiale con Kiro

Una volta che hai Kiro CLI funzionante, ecco come partire:

### Passo 1 — Crea una cartella di lavoro

Nel terminale, scrivi queste 3 righe (una alla volta, premendo Invio dopo ciascuna) ((*) qualsiasi shell dove hai Kiro):

```
mkdir ~/mio-progetto
cd ~/mio-progetto
kiro-cli chat
```

- `mkdir` = crea una cartella nuova
- `cd` = entra nella cartella
- `kiro-cli chat` = avvia Kiro

### Passo 2 — Fai leggere i tuoi PDF a Kiro

Non devi copiare niente a mano. Basta dire a Kiro dove si trovano i file. Scrivi nella chat:

> "Leggi il PDF che si trova in /mnt/c/Users/Mario/Downloads/appunti-storia.pdf e trasformalo in un file Markdown"

(Sostituisci "Mario" col tuo nome utente Windows — vedi sezione 3 per trovarlo.)

Kiro lo legge, estrae il testo, lo riformatta in Markdown. Ripeti per ogni PDF.

### Passo 3 — Organizza in cartelle tematiche

> "Organizza i file che abbiamo creato in cartelle per argomento. Crea una struttura che abbia senso."

Kiro creerà cartelle tipo:
```
mio-progetto/
├── storia/
│   ├── roma-antica.md
│   └── medioevo.md
├── filosofia/
│   └── illuminismo.md
└── README.md
```

### Passo 4 — Crea un README

> "Crea un README.md che riassuma tutto il materiale che abbiamo organizzato e i miei obiettivi di studio"

Il README diventa la tua "mappa" del progetto.

---

## 7. Come porre le domande a Kiro

**Buone domande:**
- Sii specifico: "Riassumi il capitolo 3 del file storia/roma-antica.md in 10 punti"
- Dai contesto: "Sto preparando un esame di storia. Fammi delle domande sul file X"
- Chiedi un formato: "Fammi una tabella con date e eventi principali"

**Domande meno efficaci:**
- Troppo vaghe: "Parlami di storia" (non sa dove cercare)
- Senza contesto: "È giusto?" (giusto cosa?)

**Consigli pratici:**
- Scrivi in italiano normale, come parleresti a una persona
- Se la risposta non ti piace, dì cosa non va: "Troppo lungo, riduci a metà"
- Se non capisci qualcosa che ha fatto, chiedi: "Spiegami cosa hai appena fatto"
- Puoi sempre dire: "Annulla, non fare niente"

---

## 8. Trust / Only this time / No — cosa significano

Quando Kiro vuole fare qualcosa (creare un file, eseguire un comando), ti chiede il permesso. Le opzioni sono:

| Scelta | Significato |
|--------|-------------|
| **Trust** | "Sì, fai questa cosa. E se in futuro vuoi fare cose simili, fai pure senza chiedere." |
| **Only this time** | "Sì, fai questa cosa adesso. Ma la prossima volta chiedimi di nuovo." |
| **No** | "No, non farlo." |

**Regola pratica:**
- Se capisci cosa sta facendo → **Trust** (per non dover rispondere ogni volta)
- Se non sei sicuro → **Only this time** (ti richiede la prossima volta, puoi valutare)
- Se ti sembra pericoloso o strano → **No**

Non puoi rompere niente con "No". Nel dubbio, dì No.

---

## 9. Dove approfondire Kiro

- **Documentazione ufficiale:** https://kiro.dev/docs
- **Dentro Kiro stesso:** scrivi "Cosa sai fare?" o "Quali comandi hai?" — ti risponde
- **Aiuto contestuale:** se sei bloccato, scrivi "Non so come procedere, aiutami"

---

## 10. Comandi Linux da riconoscere (non devi usarli, devi capirli)

Quando Kiro ti chiede il permesso di eseguire un comando, è utile sapere cosa fa. Ecco i più comuni:

### Comandi SICURI (lettura, non modificano niente)

| Comando | Cosa fa | Esempio |
|---------|---------|---------|
| `ls` | Elenca i file in una cartella | `ls ~/documenti` |
| `cat` | Mostra il contenuto di un file | `cat appunti.md` |
| `grep` | Cerca testo dentro i file | `grep "Roma" storia.md` |
| `pwd` | Mostra dove sei (cartella attuale) | `pwd` |
| `find` | Cerca file per nome | `find . -name "*.pdf"` |
| `head` / `tail` | Mostra inizio/fine di un file | `head -20 file.md` |

### Comandi di SCRITTURA (creano o modificano, ma reversibili)

| Comando | Cosa fa | Esempio |
|---------|---------|---------|
| `mkdir` | Crea una cartella | `mkdir appunti` |
| `cp` | Copia un file | `cp file.md copia.md` |
| `mv` | Sposta/rinomina un file | `mv vecchio.md nuovo.md` |
| `echo "..." > file` | Scrive testo in un file | `echo "ciao" > nota.md` |
| `sed` | Modifica il contenuto di un file (cerca e sostituisci) | `sed -i 's/vecchio/nuovo/g' file.md` |

### ⚠️ Comandi PERICOLOSI (cancellano, difficili da annullare)

| Comando | Cosa fa | Quando preoccuparsi |
|---------|---------|---------------------|
| `rm` | **Cancella un file** | Sempre controllare COSA cancella |
| `rm -r` | **Cancella una cartella intera** | ⚠️ Molto pericoloso |
| `rm -rf /` | **Cancella TUTTO** | 🚨 Mai dire sì a questo |

**Regola d'oro:** se vedi `rm` nel comando che Kiro vuole eseguire, leggi BENE cosa vuole cancellare. Se è un file temporaneo o di test, ok. Se è una cartella con i tuoi documenti, dì No.

### Il freno d'emergenza: Ctrl+C

Se Kiro sta facendo qualcosa e vuoi fermarlo subito, premi **Ctrl+C**. Interrompe quello che sta succedendo, immediatamente. Non rompe niente — è come premere "Stop". Funziona sempre.

### Come leggere un comando

Un comando si legge così:
```
comando  opzioni  su-cosa
```

Esempio: `cp -r /mnt/c/Users/Mario/Downloads/pdf/ ./materiale/`
- `cp` = copia
- `-r` = ricorsivo (tutta la cartella, non solo un file)
- Da dove: `/mnt/c/Users/Mario/Downloads/pdf/`
- A dove: `./materiale/` (qui, nella cartella corrente)

Se non capisci un comando, chiedi a Kiro: "Spiegami cosa fa questo comando" — te lo spiega in italiano.

---

## Riepilogo rapido

1. Installa WSL (Windows) o apri Terminal (Mac)
2. Installa Kiro CLI
3. Fai login (`kiro-cli login --license free`)
4. Crea una cartella, entra, avvia la chat (`kiro-cli chat`)
5. Chiedi a Kiro di leggere i tuoi PDF e trasformarli in Markdown
6. Organizza, studia, chiedi — Kiro è il tuo assistente

In caso di dubbio: chiedi a Kiro. È fatto per rispondere.

---

## Differenze Windows vs Mac — Riferimento rapido

| Cosa | Windows (con WSL) | Mac |
|------|-------------------|-----|
| **Aprire la shell** | Tasto Windows → "PowerShell". Per WSL: scrivi `wsl` | Cmd+Spazio → "Terminal" |
| **Installare Kiro** | In PowerShell: `irm 'https://cli.kiro.dev/install.ps1' \| iex` | `curl -fsSL https://cli.kiro.dev/install \| bash` |
| **Dove sono i tuoi file** | `/mnt/c/Users/NOME/` (dentro WSL) | `/Users/NOME/` |
| **Creare una cartella** | `mkdir` (uguale) | `mkdir` (uguale) |
| **Scorciatoia Ctrl** | Ctrl+C (interrompi), Ctrl+V (incolla in PowerShell: tasto destro) | Cmd+C, Cmd+V (nel Terminal: Ctrl+C interrompe) |
| **Incollare nel terminale** | In WSL/PowerShell: tasto destro del mouse | Cmd+V |
| **Anteprima MD in VS Code** | Ctrl+Shift+V | Cmd+Shift+V |
| **Pandoc** | Si installa dentro WSL con `sudo apt install pandoc` | Si installa con `brew install pandoc` |
| **VS Code / Obsidian** | Si installano su Windows normalmente (non dentro WSL) | Si installano normalmente |
| **Aprire file WSL da Windows** | Da Esplora File: scrivi `\\wsl$` nella barra indirizzi | Non serve (tutto è nativo) |

**Nota importante per Windows:** VS Code e Obsidian si installano su Windows (non dentro WSL). I file li lavori dentro WSL con Kiro, ma li puoi aprire anche da Windows per leggerli. VS Code ha un'estensione "WSL" che collega i due mondi automaticamente.

---

## Appendice — Installazione dei tool suggeriti

### MarkText (Windows e Mac) — il più semplice

1. Vai su https://github.com/marktext/marktext/releases
2. Scarica il file per il tuo sistema (`.exe` per Windows, `.dmg` per Mac)
3. Installa con doppio clic
4. Apri un file .md con MarkText — lo vedi formattato immediatamente, senza configurare nulla

Nota: MarkText non è più aggiornato dal 2022 ma funziona perfettamente.

### VS Code (Windows e Mac)

1. Vai su https://code.visualstudio.com/
2. Clicca "Download" (riconosce da solo se sei su Windows o Mac)
3. Installa con doppio clic sul file scaricato
4. Per l'anteprima Markdown: apri un file .md → premi Ctrl+Shift+V (Windows) o Cmd+Shift+V (Mac)
5. Per esportare in PDF: vai nella barra delle estensioni (icona quadratini a sinistra) → cerca "Markdown PDF" → clicca "Install"

### Obsidian (Windows e Mac)

1. Vai su https://obsidian.md/
2. Clicca "Get Obsidian" → scarica per il tuo sistema
3. Installa con doppio clic
4. Al primo avvio: "Open folder as vault" → scegli la cartella dove hai i tuoi file .md
5. I file appaiono renderizzati automaticamente nella barra laterale

### Pandoc (dentro WSL / Linux / Mac)

Pandoc è un convertitore universale da terminale. Si usa da dentro WSL (Windows) o Terminal (Mac).

**Su WSL / Ubuntu:**
```
sudo apt update
sudo apt install pandoc texlive-latex-recommended
```

**Su Mac (con Homebrew):**
```
brew install pandoc
brew install --cask mactex-no-gui
```

Dopo l'installazione, converti con:
```
pandoc file.md -o file.pdf
```

### StackEdit (nessuna installazione)

1. Vai su https://stackedit.io/
2. Clicca "Start writing"
3. Incolla il tuo testo Markdown nella metà sinistra
4. La metà destra mostra il risultato renderizzato
5. Per esportare: menu "..." → "Export as PDF" (richiede login Google, gratuito)

---

## Fonti

| Informazione | Fonte |
|-------------|-------|
| Installazione Kiro CLI (Mac/Windows/Linux) | https://kiro.dev/docs/cli/installation/ |
| Download Kiro CLI | https://kiro.dev/downloads |
| Documentazione Kiro CLI | https://kiro.dev/docs/cli/ |
| FAQ Kiro (account, pricing) | https://kiro.dev/faq/ |
| VS Code | https://code.visualstudio.com/ |
| Obsidian | https://obsidian.md/ |
| MarkText | https://github.com/marktext/marktext |
| Pandoc | https://pandoc.org/ |
| StackEdit | https://stackedit.io/ |
| WSL (Microsoft) | https://learn.microsoft.com/en-us/windows/wsl/install |
