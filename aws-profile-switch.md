# Switch Profilo Kiro CLI: account A ↔ account B

## Obiettivo

Usare **due account separati** per Kiro CLI:
- **Account A** (IAM Identity Center) → piano **Pro** → progetti principali
- **Account B** (Google login) → piano **Free** → progetti secondari (es. `~/dungeonandragon`)

---

## Comandi di Switch

```bash
# Passare all'account B (free)
kiro-cli logout
kiro-cli login --license free

# Tornare all'account A (pro)
kiro-cli logout
kiro-cli login --license pro
```

**Verifica:** `kiro-cli whoami`

---

## Primo Setup

> ⚠️ Fai questo da un **terminale separato**, NON da dentro una sessione Kiro CLI attiva.

### Step 1 — Logout

```bash
kiro-cli logout
```

### Step 2 — Login con Google (account B)

```bash
kiro-cli login --license free
```

Si aprirà il browser. Scegli **"Continue with Google"** e seleziona l'account personale.

### Step 3 — Verifica

```bash
kiro-cli whoami
```

### Step 4 — Torna all'account A

```bash
kiro-cli logout
kiro-cli login --license pro
```

---

## Alias opzionali

```bash
alias kiro-b='kiro-cli logout && kiro-cli login --license free'
alias kiro-a='kiro-cli logout && kiro-cli login --license pro'
```

---

## Confronto Piani Kiro

| Piano | Costo | Crediti/mese |
|-------|-------|-------------|
| **Free** | $0 | 50 |
| **Pro** | $20/mese | 1.000 |
| **Pro+** | $40/mese | 2.000 |
| **Power** | $200/mese | 10.000 |

> Fonte: [kiro.dev/pricing](https://kiro.dev/pricing/)
