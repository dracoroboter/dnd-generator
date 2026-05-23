# Ciclo di sessione: dalla pianificazione al retrofitting

Regola generale per il flusso di lavoro attorno a una sessione di gioco.

---

## I quattro momenti

| Momento | Cosa | Dove va |
|---------|------|---------|
| **1. Pianificazione** | Preparare la sessione: cosa succederà, NPC coinvolti, incontri, mappe | `DM_Prep.md` del modulo (o `meta/DM_prep_*.md` per prep specifiche) |
| **2. Avventura scritta** | Il materiale pubblicato: moduli, documento principale, schede NPC | `it/NomeModulo.md`, `it/NomeAvventura.md`, `characters/` |
| **3. Giocata + Debriefing** | Cosa è successo al tavolo + analisi + modifiche necessarie | `meta/post-sessione-YYYY-MM-DD.md` |
| **4. Retrofitting** | Applicare le modifiche all'avventura scritta | Moduli, documento principale, PlanBook |

---

## 1. Pianificazione (`DM_Prep.md`)

Documento operativo per il DM durante la sessione. Formato definito in `adventure-template.md` § "DM Prep".

Contiene: passaggi della storia, stat block, tiri chiave, mappe ASCII. Non contiene prosa o testo da leggere ai giocatori.

---

## 2. Avventura scritta

Il materiale "canonico" — ciò che è pubblicabile e rigiocabile da altri gruppi. Contiene tutte le possibilità previste, non solo ciò che è successo in una specifica giocata.

---

## 3. Post-sessione (`meta/post-sessione-YYYY-MM-DD.md`)

Un file per sessione. Contiene tutto: log della giocata, decisioni prese, analisi, modifiche necessarie, checklist retrofitting.

**Formato:**

```markdown
# Post-sessione DATA: AVVENTURA Sessione N

## Sessione N - Puntata X: NomeModulo

**Giocatori:** N PG di livello X
**Livello finale:** X (se milestone raggiunta)

---

## Cosa è successo

- Elenco puntato degli eventi principali in ordine cronologico
- Improvvisazioni del DM (da retrofittare)
- Momenti memorabili

---

## Decisioni prese al tavolo

| # | Decisione | Risultato |
|---|-----------|-----------|
| D1 | ... | ... |

---

## Modifiche all'avventura scritta

### A1. Titolo breve della modifica
Descrizione. Cosa cambia, perché, dove va applicata.

### A2. ...

---

## Punti aperti

1. **Domanda** — contesto, opzioni, decisione parziale se c'è.

---

## Retrofitting da applicare

- [ ] Modifica 1 (riferimento a A1)
- [ ] Modifica 2 (riferimento a A2)
- [x] Modifica già applicata
```

**Regole:**
- Le decisioni prese al tavolo sono numerate progressivamente (D1, D2, ...) per riferimento tra sessioni.
- Ogni modifica in sezione "Modifiche" ha un codice (A1, A2, ...) per la checklist di retrofitting.
- Le modifiche applicate vanno nell'avventura scritta; il post-sessione resta come storico.
- Se una modifica è complessa, va prima nel PlanBook come todo.

---

## Flusso completo

```
Pianificazione (DM_Prep)
    ↓
Giocata al tavolo
    ↓
Post-sessione (log + analisi + modifiche + retrofitting checklist)
    ↓
Retrofitting (applicare modifiche all'avventura scritta)
    ↓
Aggiornamento PlanBook (todo rimanenti, stato avanzamento)
```

---

## Relazione tra avventura scritta e avventura giocata

L'avventura scritta prevede **tutte le possibilità ragionevoli** (es. Piano A e Piano B per l'anello). L'avventura giocata segue **un solo percorso**. Il debriefing:

1. Conferma quale percorso è stato preso (es. "Piano A attivo, il paladino ha l'anello")
2. Identifica cosa va aggiunto/modificato nell'avventura scritta
3. **Non rimuove** i percorsi non presi — restano per rigiocabilità
4. Segna nel PlanBook quale percorso è attivo per la campagna corrente

**Retrofitting strutturale:** quando la giocata cambia la struttura dell'avventura (un NPC muore, un luogo viene distrutto, un percorso narrativo si chiude), l'avventura scritta va aggiornata per riflettere il nuovo stato. Il retrofitting non deve creare contraddizioni con quanto già accaduto nelle sessioni precedenti. In pratica: si aggiunge, si modifica il futuro, ma non si riscrive il passato.

---

## Dove va ogni tipo di informazione

| Informazione | Dove |
|-------------|------|
| "Korex è morto" (fatto della giocata) | DiarioSessioni + PlanBook (decisioni prese) |
| "Korex se catturato vivo dà info X" (possibilità scritta) | Resta nel modulo (non rimuovere) |
| "La meccanica della Presa non funziona, va cambiata" | Post-sessione (sezione A) → retrofitting → documento principale |
| "La prossima sessione inizia con X" | Post-sessione (sezione C) + DM_Prep del modulo successivo |
| "Stato Presa: 1" | PlanBook (stato campagna) + documento principale (stato attuale) |
