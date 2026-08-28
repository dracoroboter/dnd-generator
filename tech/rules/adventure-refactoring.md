---
name: adventure-refactoring
description: Piano operativo per migliorare la forma delle avventure esistenti senza alterarne il contenuto. Checklist in 4 fasi, regole di cosa non fare, metriche target.
---

# Refactoring Avventure: Piano Operativo

Piano generale per migliorare la forma delle avventure esistenti senza alterarne il contenuto narrativo. Obiettivo: rendere i documenti piu operativi al tavolo, meno prolissi, meglio strutturati.

---

## Principi guida

1. **Non cambiare la storia**, cambia come e presentata
2. **Sposta, non cancella**: il contenuto "di troppo" va in un posto piu adatto, non nel cestino
3. **Un'informazione, un posto**: eliminare duplicazioni tra doc principale e moduli
4. **Il test del DM**: ogni frase deve servire al DM in quel momento

---

## Checklist di refactoring (applicabile a qualsiasi avventura)

### Fase 1: Documento principale

| # | Azione | Criterio |
|---|--------|----------|
| 1.1 | Identificare backstory dump (sezioni > 50 righe di prosa esplicativa) | Se il contenuto spiega *perche* le cose sono cosi ma non serve al tavolo, va condensato |
| 1.2 | Condensare backstory in schema a punti (chi/cosa/perche/quando/dove) | Max 20 righe per la verita nascosta piu complessa |
| 1.3 | Spostare prosa esplicativa nel PlanBook (sezione "Razionale di design") | Il DM che vuole capire il *perche* la trova li |
| 1.4 | Spostare Concept/meta-informazioni nell'AdventureBook | Info per l'autore/AI, non per il DM al tavolo |
| 1.5 | Verificare che ogni NPC nella sezione "NPC principali" segua il formato standard | Nome, Dove, Ruolo, Cosa sa, Come si comporta, Frase. Niente prosa. |
| 1.6 | Eliminare informazioni duplicate dalla sezione Luoghi (se gia nei moduli) | Il doc principale ha la tabella riassuntiva; i dettagli stanno nei moduli |

### Fase 2: Moduli

| # | Azione | Criterio |
|---|--------|----------|
| 2.1 | Misurare: ogni modulo sta in 3 pagine stampate (escluse mappe)? | Se no, tagliare o splittare |
| 2.2 | Ridurre boxed text a max 5 frasi | Eccezioni solo se l'effetto comico/drammatico lo richiede (documentare il perche) |
| 2.3 | Convertire dialoghi preconfezionati in bullet point di stile | "Gorim: impaziente, evasivo, tirchio" + 1-2 frasi esempio. Il DM improvvisa |
| 2.4 | Sostituire risposte a domande probabili con una tabella sintetica | Domanda / Risposta breve / CD (se serve) |
| 2.5 | Eliminare ripetizioni dal doc principale | Se un'info e nel doc principale, il modulo dice "Vedi §X" e basta |
| 2.6 | Verificare che ogni modulo abbia un arco interno | Problema locale + sviluppo + risoluzione (anche minimo) |
| 2.7 | Convertire tattiche nemici in bullet point | "Round 1: X. Round 2: Y. Se sotto meta PF: Z." |
| 2.8 | Mettere dati meccanici in tabella, non in prosa | Nemici, CD, distanze, ricompense |

### Fase 3: DM_Prep

| # | Azione | Criterio |
|---|--------|----------|
| 3.1 | Verificare che ogni modulo giocabile abbia un DM_Prep | Se manca, crearlo |
| 3.2 | Aggiungere reminder meccaniche ricorrenti | Es. "Tiro sfighe d6 a inizio sessione" |
| 3.3 | Verificare autosufficienza degli stat block nel DM_Prep | Non deve rimandare ad altri file durante il gioco |

### Fase 4: Verifica finale

| # | Azione | Criterio |
|---|--------|----------|
| 4.1 | Rileggere il doc principale dall'inizio: si capisce la storia in 5 minuti? | Se no, la struttura non e chiara |
| 4.2 | Rileggere ogni modulo: il DM trova quello che gli serve in 10 secondi? | Se deve cercare, il formato e sbagliato |
| 4.3 | Controllare che nessun contenuto sia andato perso | Confrontare col backup |
| 4.4 | Eseguire `check-adventure.py` | Zero errori |

---

## Cosa NON fare durante il refactoring

- Non riscrivere la trama
- Non aggiungere contenuto nuovo (nuovi NPC, nuove scene)
- Non cambiare nomi, CD, stat block, ricompense
- Non eliminare running gag o elementi di tono
- Non toccare le schede NPC in `characters/markdown/` (sono gia nel formato giusto)
- Non modificare i file tradotti (EN) fino a che il refactoring IT non e stabile

---

## Esempio applicato

Per un esempio completo di piano di refactoring applicato a un'avventura specifica, vedi:
`adventures/LAnelloDelConte/meta/refactoring-plan.md`
