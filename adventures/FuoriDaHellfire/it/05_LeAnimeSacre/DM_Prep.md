# DM Prep — Modulo 5: Le Anime Sacre

Party: 3 PG lv5 + Udo (CR 3) + Fin (lv3).


## Passaggi della storia

1. **Prologo** — Aldric Jr avverte: "distruggere un'anima è cosa da farsi solo in condizioni estreme"
2. **Viaggio** — 3 giorni. Se portatrice protetta dal rituale del sonno: saltare. Altrimenti: meccanica mod.4
3. **Torre (seconda visita)** — Accesso libero alla cella 4. Aldric memorizza il rituale dal pavimento (1 ora)
4. **Scoperta** — Il rituale va eseguito all'aperto. Aldric identifica il cimitero sulla scogliera (10 min)
5. **Preparazione** — Aldric traccia cerchio (30 min), ossa al centro, portatrice nel cerchio, fuoco
6. **Avvertimento** — Le iscrizioni si illuminano: "serve Presa ≥7". Aldric conferma: non funziona
7. **Se insistono** — Spettri (3, invincibili) + Scheletri (15, ondate da 5). Maledizione Aldric se uccidono tutti
8. **Chiusura** — Il dilemma: peggiorare per guarire, o convivere per sempre. Jason ride: "Ve l'avevo detto, folli."


## Stat block

→ Schede complete in `it/characters/statblock/` (PDF stampabili).

### Scheletro (Custode dell'Ordine) × 15

Scheda: `MON_Skeleton`. Particolarità: portano frammenti di armatura dell'Ordine e spade arrugginite. Compaiono a ondate dal terreno.

**Ondate:**

| Ondata | Round | N. | Da dove |
|--------|-------|----|---------|
| 1 | 1 | 5 | Tombe vicine al cerchio |
| 2 | 3 | 5 | Tombe ai lati |
| 3 | 5 | 5 | Tombe ai bordi mappa |

**Difficoltà:** HARD (3 PG lv5 + Udo + Fin)


### NPC companion

| NPC | Scheda | Ruolo in combattimento |
|-----|--------|----------------------|
| Udo Hutchinson | `NPC_UdoHutchinson` | Tank, Multiattack ×2 |
| Fin Ditasvelte | `NPC_FinDitasvelte` | Sneak Attack, posizionamento |


### Teppista Charmato (banditi viaggio) × 1d6

Scheda: `MON_TeppistaCharmato`. Intimidazione CD 13 li fa scappare (primo giorno). 1d20 mr se perquisiti.


### Spettri dell'Ordine × 3

Non combattibili. Bloccano il cerchio (Silence su Aldric, forza che respinge). Se attaccati diventano incorporei e tornano. Svaniscono dopo aver parlato/maledetto.


### Jason Accordion (incantesimi disponibili per la Presa)

Scheda: `NPC_JasonAccordion`. CD 16, attacco +8. Lancia solo attraverso il portatore (Presa +1 per ogni uso).

| Livello | Incantesimo |
|---------|-------------|
| 1 | *Healing Word*, *Dissonant Whispers* |
| 2 | *Hold Person*, *Invisibility* |
| 3 | *Hypnotic Pattern*, *Fear* |
| 4 | *Greater Invisibility* |
| 5 | *Hold Monster* |


## Tiri chiave

| Luogo | Tiro | CD | Effetto |
|-------|------|----|---------|
| Prologo | Persuasione (Aldric Sr.) | 18 | Farlo manifestare per spiegare la regola |
| Scogliera | Persuasione (Spettri) | 14 | Ottenere indizio sulla condizione (Presa ≥7) |
| Scogliera | — | — | Iscrizioni: informazione automatica |


## Mappe

### Cimitero sulla scogliera (17×17 quadretti, 5ft/qd)

```
    N (scogliera — caduta nel vuoto)
    ═══════════════════════════════════
    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    .  .  .  ▪  .  .  .  ▪  .  .  ▪  .  .  .  ▪  .  .
    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    .  ▪  .  .  .  ▪  .  .  .  ▪  .  .  .  ▪  .  .  .
    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    .  .  ▪  .  .  .  .  .  .  .  .  .  .  ▪  .  .  .
    .  .  .  .  .  .  ╔═══╗  .  .  .  .  .  .  .  .  .
    .  .  .  .  .  .  ║ C ║  .  .  .  .  .  .  .  .  .
    .  .  .  .  .  .  ╚═══╝  .  .  .  .  .  .  .  .  .
    .  .  ▪  .  .  .  .  .  .  .  .  .  ▪  .  .  .  .
    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    .  ▪  .  .  ▪  .  .  .  .  .  ▪  .  .  ▪  .  .  .
    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    .  .  .  ▪  .  .  .  .  .  ▪  .  .  ▪  .  .  .  .
    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    .  .  .  .  .  .  .  ▲  .  .  .  .  .  .  .  .  .
    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    ═══════════════════════════════════
    S (sentiero dalla torre, largo 2qd)

    C = Cerchio del rituale (3×3)
    ▪ = Lapide (copertura mezza) — spawn scheletri
    ▲ = Ingresso sentiero
    N = Scogliera (caduta mortale)
```

**Per disegno su quadrettata:**
- 17×17 quadretti
- Nord: linea irregolare (scogliera, caduta = morte)
- Centro: cerchio 3×3 (Aldric + portatrice + ossa)
- ~15 lapidi sparse 1×1 (simbolo chiave spezzata) — gli scheletri escono da sotto
- Sud: sentiero largo 2qd dalla torre
- Aldric si nasconde dietro una lapide durante il combattimento


## Loot

Nessuno.


## Milestone

Nessun level-up. I PG restano lv5.
