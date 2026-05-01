# AdventureBook.md — Istruzioni per l'AI

Questa avventura segue la struttura standard definita in `tech/rules/adventure-template.md`.

## Note specifiche

- Campagna in 4 moduli sequenziali (A→B→C→D), livelli 8-10
- Versione "Draco" — porting dal materiale legacy in `legacy/DracoAvventure/LoScettroDityr/`
- Continuità narrativa forte: NPC ricorrenti (Frankie, Ombrascura, Kreig, Miranda, Ruby) attraversano più moduli
- Vecna è il filo conduttore: appare nel Modulo A (Torre di Torth), dà la missione nel Modulo B, insegue tramite agenti nei Moduli C-D
- Lo Scettro di Tyr è l'oggetto centrale: recuperato nel Modulo B, trasportato nel C, la sua eredità guida il D
- La Pergamena del Giudizio è l'oggetto centrale del Modulo A (abbatte la cupola di Orcastle)
- Il Monile d'Oro di Ostegard è l'oggetto centrale del Modulo D (spezza la maledizione)

## Struttura dei moduli

| Modulo | Tipo | Ambientazione principale |
|--------|------|--------------------------|
| A — Fuga da Orcastle | sandbox su isola | Orcastle (città-prigione) |
| B — Lo Scettro di Tyr | viaggio + dungeon | Baldur's Gate → Tempio di Lumina → Erythale |
| C — Ritorno a Casa | viaggio via nave + terra | Baldur's Gate → Luskan → Bryn Shander → Svoalbard |
| D — La fine non appartiene ai morti | viaggio + combat | Costa della Spada → Orcastle → Santuario di Ostegard |

## Schede personaggi e mostri

Le schede NPC/MON sono in `characters/markdown/`. I personaggi principali che attraversano più moduli:

| NPC | Ruolo | Moduli |
|-----|-------|--------|
| Frankie Partenope | alleato, barbaro | A, D |
| Malachias Ombrascura | alleato ambiguo, chierico | A, D |
| Lord Cedric Malebranche | antagonista, arcimago | A, D |
| Vecna | divinità, manipolatore | A, B |
| Tyr | divinità, giudice | B, C |
| Sir Alaric il Giusto | antagonista, sacerdote corrotto | B |
| Othran Vorash | antagonista, warlock | C, D |
| Kreig Highlander/Wildforge | neutrale → alleato | A, D |

## Fonti legacy

I file sorgente `.odt` sono in `legacy/DracoAvventure/LoScettroDityr/`. Non modificare i file legacy.
- `A_FugaDaOrcastle/Fuga_da_Orcastle.odt` (v1.0, ott 2024) + `Fuga_Da_Orcastle_Lore.odt`
- `B_LoScettroDiTyr/LoScettroDiTyr.odt` (v1.1, gen 2024)
- `C_RitornoACasa/RitornoACasa.odt` (v0.5, gen 2025)
- `D_La fine non appartiene ai morti/NonAiMorti2.odt` (v0.3, mar 2025)
