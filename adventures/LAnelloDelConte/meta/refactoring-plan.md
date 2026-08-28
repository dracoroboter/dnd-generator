# Refactoring Plan: L'Anello del Conte

Piano specifico di refactoring per questa avventura. Applica le regole generali di `tech/rules/adventure-refactoring.md`.

---

## Misura iniziale (2026-08-28)

```
  RAPPORTO PROSA/DATI GLOBALE:   0.58
  DENSITÀ INFORMATIVA GLOBALE:   0.55
  Blocchi boxed >5 righe:        21
  Parole totali:                 35210
```

## Interventi sul documento principale (`it/LAnelloDelConte.md`)

| # | Sezione | Intervento | Stato |
|---|---------|------------|-------|
| A1 | "La verita - chi e S" (~100 righe prosa) | Condensare in schema tabellare | FATTO |
| A2 | "Concept" (15 righe) | Spostare in AdventureBook.md | FATTO |
| A3 | "I PG" - tabella sfighe | Tenere (e regola di gioco), aggiungere cross-ref nei DM_Prep | TODO |
| A4 | "NPC principali" | Verificare formato standard, tagliare prosa eccedente | TODO |
| A5 | "Luoghi" tabella finale | Eliminare se duplica la tabella precedente | TODO |
| A6 | "Struttura dell'avventura" | OK, tenere | — |

## Interventi sui moduli (boxed text >5 righe)

| Modulo | Blocchi >5 | Intervento |
|--------|-----------|------------|
| P1 - LeFogneDiFianus | 4 | Pergamena: eccezione comica (tenere). Intro taverna: spezzare. Domande Gorim: tabella. |
| P2 - LaFestaDelGrazie | 4 | Ridurre a max 5 righe ciascuno |
| P3 - UnaPizzaInCompagnia | 6 | Ridurre a max 5 righe ciascuno |
| P4 - IlCorniciaio | 2 | Ridurre a max 5 righe ciascuno |
| P5 - RitornoAlleFogne | 4 | Ridurre + valutare split del modulo (843 righe) |
| P7 - IlFinaleDiStagione | 1 | Ridurre a max 5 righe |

## DM_Prep mancanti

| Modulo | Stato | Azione |
|--------|-------|--------|
| P1 | Assente | Creare |
| P2 | Assente | Creare |
| P3 | Assente | Creare |
| P4 | Assente | Creare |
| P5 | Presente | Verificare, aggiungere reminder sfighe |
| P6 | Presente | Verificare, aggiungere reminder sfighe |
| P7 | Assente | Creare |

## Ordine di esecuzione

1. Doc principale (A1-A6) — parzialmente fatto
2. Moduli: riduzione boxed text, da P1 a P7
3. P1: condensare dialoghi Gorim
4. DM_Prep mancanti
5. Rimisurare e confrontare

## Target post-refactoring

```
  Blocchi boxed >5 righe:  max 3-4 (eccezioni documentate)
  Rapporto prosa/dati:     < 0.55 (migliorare leggermente)
  P5 RitornoAlleFogne:     < 600 righe (da 843)
```
