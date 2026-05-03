# DM Prep — Fuori da Hellfire

Riepilogo incontri e NPC per configurare Roll20 / FightClub / Game Master 5e.
One-shot (1-2 sessioni). Party: 3 PG lv3 + Udo Hutchinson (CR 3) + Fin Ditasvelte (lv3).

---

## Modulo 1 — Discesa nelle Fogne

### Incontri

| # | Luogo | Tipo | Nemici | Difficoltà |
|---|-------|------|--------|------------|
| 1 | Galleria d'ingresso | Trappola | Filo teso: Percezione CD 12, Destrezza CD 12 per disarmare. 1d6 perforanti + allerta ratti | — |
| 2 | Nido di ratti | Combattimento | 6× Ratto Corrotto (CR 1/8) + 1× Sciame di Ratti (CR 1/4) | Easy |

### NPC per luogo

#### Moli di Oakshore (ingresso fogne)

| NPC | Stat block | Note |
|-----|-----------|------|
| Udo Hutchinson | Custom (Veterano, CR 3) | Sceriffo, si unisce all'ingresso. Tank del gruppo. |
| Fin Ditasvelte | Custom (Rogue 3) | Ex-charmato di Korex, esce dalla grata confuso. Vuole vendetta. |

#### Fogne

| Nemico | Stat block | Note |
|--------|-----------|------|
| 6× Ratto Corrotto | Custom (Giant Rat, CR 1/8) | Occhi rossi, Pack Tactics |
| 1× Sciame di Ratti | MM p. 339, CR 1/4 | Resistenza armi |

### Tiri chiave

| Luogo | Tiro | CD | Effetto |
|-------|------|----|---------|
| Galleria | Percezione | 12 | Notare filo trappola |
| Galleria | Destrezza (arnesi) | 12 | Disarmare trappola |
| Bivio | Sopravvivenza | 13 | Distinguere tracce vere da false |
| Bivio | Indagare | 14 | Notare che le false sono troppo regolari |
| Nido | Natura | 10 | Capire che i ratti sono corrotti |
| Soglia | Storia | 15 | Pietra più antica della città |

---

## Modulo 2 — Tana di Korex

### Incontri

| # | Luogo | Tipo | Nemici | Difficoltà |
|---|-------|------|--------|------------|
| 1 | Cisterna | Combattimento (boss) | 1× Korex (CR 3) + 2× Teppista Charmato (CR 1/8) | Hard |

### NPC per luogo

#### Cisterna (arena)

| NPC | Stat block | Note |
|-----|-----------|------|
| Korex | Custom (Bardo, CR 3) | Antagonista. Charma, scappa, manda avanti i teppisti. |
| 2× Teppista Charmato | Custom (Cultista, CR 1/8) | Nascosti dietro colonne. Percezione CD 14 per notarli. Charm si spezza se Korex cade. |

### Tattiche Korex

| Round | Azione |
|-------|--------|
| 1 | Charma il PG più pericoloso (o Udo — SAG +0) |
| 2-3 | Incantesimi di controllo, distanza, teppisti avanti |
| Sotto metà PF | Implora pietà, offre info, mente. Se non abboccano → fuga verso passaggio nascosto |

### Tiri chiave

| Luogo | Tiro | CD | Effetto |
|-------|------|----|---------|
| Cisterna | Percezione | 14 | Notare teppisti nascosti |
| Alcova | Indagare | 12 | Trovare appunti di Korex |
| Alcova | Arcano | 14 | Decifrare codice personale |
| Cisterna | Percezione | 16 (combattimento) / 12 (dopo) | Trovare passaggio nascosto |

### Loot

| Oggetto | Dove |
|---------|------|
| 120 mo (monete + gioielli) | Cassa nell'alcova |
| Liuto di qualità (non magico) | Parete della cisterna |
| Taglia: 50 mo (morto) / 75 mo (vivo) | Guardia di Oakshore |
| Anello del Virtuoso | Dito di Korex |

---

## Il Cliffhanger — Anello del Virtuoso

**Percezione CD 10** per notare l'anello al dito di Korex (è vistoso).

| Scenario | Cosa succede |
|----------|-------------|
| PG tocca l'anello | TS Saggezza CD 20. Fallimento → indossa. Successo → posa, attrazione resta. |
| Nessun PG lo tocca | Guardia NPC lo indossa → posseduta → combattimento |

Effetti immediati se indossato: +2 caratteristica (per classe), vantaggio TS charm, 1 spell bardo 1/giorno. Maledizione: non si toglie, incubi, freddo, vulnerabilità psichici.

Dettagli completi: `DiscussioneNarrativa.md` e `NPC_JasonAccordion.md`.

---

## Stat block da preparare

| Stat block | Quanti | File |
|-----------|--------|------|
| Udo Hutchinson (custom Veterano CR 3) | 1 | `NPC_UdoHutchinson.md` |
| Fin Ditasvelte (custom Rogue 3) | 1 | `NPC_FinDitasvelte.md` |
| Korex (custom Bardo CR 3) | 1 | `NPC_Korex.md` |
| Ratto Corrotto (custom Giant Rat CR 1/8) | 6 | `MON_RattoCorrotto.md` |
| Sciame di Ratti (CR 1/4) | 1 | `MON_SciameDiRatti.md` |
| Teppista Charmato (custom Cultista CR 1/8) | 2 | `MON_TeppistaCharmato.md` |
| Jason Accordion (anima nell'anello) | — | `NPC_JasonAccordion.md` (solo riferimento) |

Tutti gli stat block sono già generati (XML + PDF + PNG) in `characters/`.

---

## Milestone

Livello 4 dopo aver catturato o sconfitto Korex.
