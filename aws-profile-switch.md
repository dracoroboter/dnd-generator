# Switch Profilo Kiro CLI: Pro (lavoro) ↔ Free (hobby)

## Obiettivo

Usare **due account separati** per Kiro CLI:
- **Account aziendale** (IAM Identity Center) → piano **Pro** → progetti di lavoro → ⚠️ NON TOCCARE
- **Account personale** (Google login) → piano **Free** → progetti hobby (es. `~/dungeonandragon`)

> ⚠️ **REGOLA D'ORO**: nessuna modifica deve impattare il profilo di lavoro.

---

## Profilo di Lavoro (riferimento)

```
Logged in with IAM Identity Center (https://vivaticket.awsapps.com/start#/)
Profile: QDefaultProfile
arn:aws:codewhisperer:us-east-1:654297655744:profile/H77P7DGP77NV
```

## Profilo Hobby (riferimento)

```
Logged in with Builder ID
Email: [tua-email-gmail]
```

**Verifica da dentro Kiro CLI:** chiedere a Kiro di eseguire `kiro-cli whoami`, oppure invocare la skill `check-kiro-profile`.

---

## Comandi di Switch (riferimento rapido)

```bash
# Passare al Free (hobby)
kiro-cli logout
kiro-cli login --license free

# Tornare al Pro (lavoro)
kiro-cli logout
kiro-cli login --license pro
```

> Se il re-login al pro non trova automaticamente Identity Center:
> ```bash
> kiro-cli login --license pro --identity-provider https://vivaticket.awsapps.com/start#/
> ```

---

## Procedura - Primo Setup e Test

> ⚠️ Fai questo da un **terminale separato**, NON da dentro una sessione Kiro CLI attiva.
> ⚠️ Fallo in un momento in cui **non stai lavorando** — richiede logout dal profilo aziendale.

### Prerequisiti
- Un account Google personale (Gmail)

### Step 1 — Logout dal pro

```bash
kiro-cli logout
```

### Step 2 — Login con Google (piano free)

```bash
kiro-cli login --license free
```

Si aprirà automaticamente il browser. Se non si apre, il terminale mostrerà un URL da copiare e incollare manualmente. In alternativa:
```bash
kiro-cli login --license free --use-device-flow
```
Questo mostra un codice da inserire su una pagina web (utile se il redirect del browser non funziona).

Nella pagina di login:
1. Scegli **"Continue with Google"**
2. Seleziona il tuo **account Gmail personale** (NON quello aziendale)
3. Autorizza l'accesso a Kiro
4. Se è il primo accesso con Google, potrebbe chiederti di:
   - Accettare i **termini di servizio** di Kiro/Amazon Q
   - Confermare la creazione di un profilo
   - Accettare queste cose è normale — stai creando il tuo account free
5. Il browser confermerà il login ("You can close this window") — torna al terminale

### Step 3 — Verifica login free

```bash
kiro-cli whoami
```
Deve mostrare il tuo account Google personale. Il piano Free si attiva automaticamente.
Al primo accesso ricevi **500 crediti bonus** utilizzabili entro 30 giorni.

### Step 4 — Torna al pro

```bash
kiro-cli logout
kiro-cli login --license pro
```
Si aprirà il browser → login via Identity Center (`vivaticket.awsapps.com`).

### Step 5 — Verifica ritorno al pro

```bash
kiro-cli whoami
```
Deve mostrare:
```
Logged in with IAM Identity Center (https://vivaticket.awsapps.com/start#/)
```

Se non funziona → vedi "Piano di Emergenza" sotto.

---

## Piano di Emergenza

Se il re-login al pro non funziona:

```bash
# Tentativo 1: specificare l'identity provider
kiro-cli login --license pro --identity-provider https://vivaticket.awsapps.com/start#/

# Tentativo 2: specificare anche la regione
kiro-cli login --license pro --identity-provider https://vivaticket.awsapps.com/start#/ --region us-east-1

# Tentativo 3: diagnostica
kiro-cli doctor
```

Se nulla funziona, il profilo aziendale non è stato cancellato — è solo un problema di re-autenticazione. Contattare il supporto IT aziendale con le informazioni del profilo salvate sopra.

---

## Possibile Automazione (dopo aver verificato che lo switch funziona)

Alias da aggiungere a `~/.bashrc`:

```bash
alias kiro-hobby='kiro-cli logout && kiro-cli login --license free'
alias kiro-work='kiro-cli logout && kiro-cli login --license pro'
```

> ⚠️ Questi alias richiedono interazione browser — non sono completamente automatici.

### TODO: wrapper `kiro` con warning automatico

Idea non ancora implementata: uno script `~/bin/kiro` che, se la directory corrente è sotto `~/dungeonandragon`, esegue `kiro-cli whoami` e stampa un warning se non sei sul profilo hobby, poi lancia `kiro-cli "$@"`. Richiederebbe di usare `kiro` invece di `kiro-cli` direttamente — valutare se vale la complessità.

---

## Domande Aperte

- [ ] **Le sessioni/contesti in `~/.kiro/sessions/` sopravvivono al cambio account?** Verificare durante il test
- [ ] **Il re-login al pro richiede `--identity-provider`?** Verificare allo Step 4
- [ ] **50 crediti/mese bastano per il progetto hobby?** Monitorare l'uso nei primi mesi
- [ ] **Il `.envrc` e direnv servono ancora?** Per Kiro CLI no. Potrebbero servire se in futuro si usano servizi AWS classici (S3, Lambda, ecc.) dal progetto hobby. Per ora si possono ignorare

---

## Confronto Piani Kiro

| Piano | Costo | Crediti/mese | Overage |
|-------|-------|-------------|---------|
| **Free** | $0 | 50 | No |
| **Pro** | $20/mese | 1.000 | $0.04/credito |
| **Pro+** | $40/mese | 2.000 | $0.04/credito |
| **Power** | $200/mese | 10.000 | $0.04/credito |

### Dettagli crediti

- 1 credito ≈ 1 prompt (semplici < 1, complessi > 1)
- Modelli diversi consumano a rate diverse (Sonnet 4 ≈ 1.3x Auto)
- Minimo: 0.01 crediti per task
- Crediti non cumulabili, reset mensile
- Free: nessun overage, finiti i 50 → stop fino al mese dopo
- Tutti i modelli disponibili su tutti i piani (Auto, Sonnet 4, Sonnet 4.5, Haiku 4.5, Opus 4.5, Opus 4.6)
- Powers incluse su tutti i piani

### Stima per il progetto D&D

~30-50 interazioni semplici/mese con 50 crediti. Per un hobby da weekend dovrebbe bastare.

> Fonte: [kiro.dev/pricing](https://kiro.dev/pricing/)

---

## Checklist Operativa

- [x] Indagine autenticazione (Fase 0)
- [ ] Primo login con Google e test switch completo (Step 1-5)
- [ ] Verificare che sessioni/contesti sopravvivano al cambio
- [ ] Opzionale: aggiungere alias `kiro-hobby` / `kiro-work` a `~/.bashrc`
- [ ] TODO: valutare automazione warning all'avvio — possibile tramite script bash/alias che esegue `kiro-cli whoami` e stampa un avviso prima di aprire Kiro, da eseguire manualmente prima di ogni sessione hobby (non realizzabile come hook automatico dentro Kiro CLI)
