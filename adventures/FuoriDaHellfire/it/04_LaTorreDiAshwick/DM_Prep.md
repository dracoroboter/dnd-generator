# DM Prep — Modulo 4: La Torre di Ashwick

Party: 3 PG lv4 + Udo (CR 3) + Fin (lv3).


## Passaggi della storia

1. **Prologo** — Aldric Sr. rivela: ossa di Jason nella Torre di Ashwick, costa nord, 2-3 giorni
2. **Viaggio** — Jason tenta di dissuadere (giorno 1: "non c'è fretta", giorno 2: "è pericoloso", giorno 3: silenzio ostile, possibile Presa +1)
3. **Piano 1** — Sala in rovine, mosaico chiave spezzata, armeria laterale (registro turni, indizio chiave al 2°)
4. **Piano 2** — Studio pericolante (1d20 ogni round, 1 = pavimento cede). Cassetto: chiave + nota "Cella 4, il bardo"
5. **Sotterraneo** — Corridoio 7 celle. Cella 4 = ouroboros musicale. 2 Custodi (Wight) davanti
6. **Custodi** — Negoziazione (Persuasione CD 16, CD 12 con registro/nome Aldric) oppure combattimento HARD
7. **Cella di Jason** — Scheletro nel sarcofago. Jason urla, tenta TS Sag CD 14 per prendere il controllo. Poi silenzio
8. **Ritorno** — 2-3 giorni, Jason muto. Consegnare ossa a Vellun. Milestone lv5


## Stat block

→ Schede complete in `it/characters/statblock/` (PDF stampabili).

### Wight (Custode) × 2

Scheda: MM p.300 (non homebrew — stat standard). Particolarità: indossano cotte dell'Ordine, compaiono quando si tenta di aprire una porta del sotterraneo. Life Drain è il pericolo principale (riduce PF max).

**Tattiche:** Multiattack (spada + Life Drain). Puntano il PG più debole (meno PF). Non inseguono oltre il sotterraneo.


### NPC companion

| NPC | Scheda | Ruolo in combattimento |
|-----|--------|----------------------|
| Udo Hutchinson | `NPC_UdoHutchinson` | Tank, Multiattack ×2 |
| Fin Ditasvelte | `NPC_FinDitasvelte` | Sneak Attack, posizionamento |

### Jason Accordion (entità nell'anello)

Scheda: `NPC_JasonAccordion`. CD 16, attacco +8. Lancia solo attraverso il portatore quando ha il controllo.

**Incantesimi disponibili per la Presa** (Jason offre questi al portatore, Presa +1 per ogni uso):

| Livello | Incantesimo | Uso tipico di Jason |
|---------|-------------|---------------------|
| 1 | *Healing Word* | "Sei ferito, lasciami curarti" |
| 1 | *Dissonant Whispers* | "Quel nemico ti sta per colpire, lasciami" |
| 2 | *Hold Person* | "Lo fermo io, fidati" |
| 2 | *Invisibility* | "Ti nascondo, nessuno ti vedrà" |
| 3 | *Hypnotic Pattern* | "Li addormento tutti, un attimo" |
| 3 | *Fear* | "Li faccio scappare, è facile" |
| 4 | *Greater Invisibility* | "Combatti invisibile, io ti copro" |
| 5 | *Hold Monster* | "Anche quello grosso, lo fermo" |

**Conflitto mentale (cella 4):** TS Sag CD 14. Fallimento: Jason prende il controllo, tenta di fuggire dalla stanza.

**Debolezza:** dolore fisico lo forza fuori dal controllo.


## Tiri chiave

| Luogo | Tiro | CD | Effetto |
|-------|------|----|---------|
| Piano 1 | Percezione | 12 | Rumori dal sotterraneo |
| Piano 1 (mosaico) | Investigazione | 10 | Iscrizione "Il Custode veglia dall'alto" |
| Armeria | Investigazione | 12 | Leggere registro turni |
| Piano 2 | Ogni round: 1d20 | 1 = cede | TS Des CD 12 o 1d6 danni caduta |
| Piano 2 (cassetto) | Forza / Scassinare | 14 / 12 | Aprire cassetto sigillato |
| Sotterraneo | Persuasione (Custodi) | 16 (12 con registro) | Evitare combattimento |
| Sotterraneo | Inganno (Custodi) | 18 | Alternativa alla persuasione |
| Cella Jason | TS Saggezza (portatore) | 14 | Resistere a possessione disperata |
| Cella Jason | Arcano | 12 | Leggere simboli sigillatura |


## Mappe

### Sezione verticale

```
         ┌─────────┐
    3°   │ CROLLATO│
         ├────┬────┤
    2°   │ STUDIO  │  ← chiave + nota
         ├────┴────┤
    1°   │  SALA   │  ← armeria, porta ferro
    ═════╧═════════╧═════
         ┌─────────┐
    -1   │ SIGILLI │  ← 7 celle, Custodi
         └─────────┘
```

### Piano 1

```
  ╔════════╦═══════════════════╗
  ║ARMERIA ║  ▲ scale su (2°)  ║
  ║registro║                   ║
  ╠════════╣   SALA INGRESSO   ║
  ║        ║  [mosaico chiave] ║
  ╚════════╣  [⚷] porta ferro  ║
     ══════╝                   ╚══════
           PORTONE (marcio)
```

### Sotterraneo -1

```
    ┌───┐ ┌───┐ ┌─────┐ ┌───┐ ┌───┐
    │ 1 │ │ 2 │ │     │ │ 5 │ │ 6 │
    └─┬─┘ └─┬─┘ │scale│ └─┬─┘ └─┬─┘
  ════╧═════╧═══╧═════╧═══╧═════╧════  CORRIDOIO
    ┌─┴─┐ ┌─┴─┐         ┌─┴─┐
    │ 3 │ │ 4*│         │ 7 │
    └───┘ │ ☠☠│         └───┘
          └───┘
    * = Cella di Jason (ouroboros)
    ☠☠ = 2 Wight (Custodi)
```


## Loot

| Oggetto | Dove |
|---------|------|
| Pugnale cerimoniale (simbolo chiave, non magico) | Armeria |
| Chiave di ferro nero | Cassetto 2° piano |
| Scheletro di Jason | Cella 4 |


## Milestone

Livello 5 dopo aver recuperato lo scheletro.
