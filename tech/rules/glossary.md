---
name: glossary
description: Definizioni dei termini del progetto. One-shot, campagna, saga, modulo, sessione, quest, plot. Metadati saga nei README.
---

# Glossary — Termini del Progetto

## Unità narrative

**Avventura** — unità base del progetto. Ha un inizio, una fine e un arco narrativo completo. Può essere giocata in una o più sessioni. Corrisponde a una directory in `adventures/`.

**One-shot** — avventura progettata per una singola sessione.

**Campagna** — avventura multi-sessione con arco narrativo unico. Es: `LAnelloDelConte`.

**Saga** — sequenza di avventure collegate con arco narrativo comune più ampio. Non ha una directory contenitore — ogni avventura è indipendente in `adventures/`, ma dichiara la sua appartenenza nel `README.md`.

**Modulo** — unità strutturale di un'avventura. Corrisponde a una subdirectory `NN_NomeModulo/`. Può essere un dungeon, un episodio, una location significativa.

**Sessione** — una serata di gioco. Non è un'unità strutturale del progetto — una sessione può coprire mezzo modulo o due moduli. Non ha un file dedicato.

**Quest** — obiettivo narrativo all'interno di un modulo. Non è un'unità strutturale — è contenuto testuale dentro un modulo.

**Plot** — arco narrativo complessivo di un'avventura. Documentato nella sezione `## Plot generale` del documento principale.

---

## Collegamento tra avventure (saga)

Le avventure appartenenti a una saga si collegano tramite metadati nel `README.md`, non tramite naming convention delle directory.

Formato obbligatorio per avventure parte di una saga:

```markdown
**Saga**: Nome della Saga (o **Sequenza** per avventure in serie senza saga)
**Posizione**: Puntata N di M
**Precede**: NomeAvventuraSuccessiva (o —)
**Segue**: NomeAvventuraPrecedente (o —)
```

Esempio — `LAnelloDelConte/README.md`:
```markdown
**Sequenza**: LAnelloDelConte → IlReSpezzato
**Posizione**: Puntata 1 di 2
**Segue**: —
**Precede**: IlReSpezzato
```

Le avventure standalone (non parte di saga o sequenza) non includono questi campi.

---

## Saga esistenti

| Saga / Sequenza | Avventure (in ordine) |
|------|-----------------------|
| Lo Scettro di Tyr (saga) | LoScettroDityr (A→B→C→D) |
| LAnelloDelConte → IlReSpezzato (sequenza) | LAnelloDelConte → IlReSpezzato |
