# PlanBook — Lo Scettro di Tyr (VerT)

## Stato del progetto

- [x] Scaffolding struttura directory
- [x] Normalizzazione Modulo A da variante G 2.2
- [x] Copia Moduli B/C/D da LoScettroDityr
- [ ] Uniformare Moduli B/C/D alle differenze del Modulo A VerT
- [ ] Traduzione inglese
- [ ] Verifica con check-adventure.py (zero errori)

## Prossimo passo — Condivisione asset

Dopo il porting dei contenuti, trattare LoScettroDiTyr-VerT come **variante** di LoScettroDityr: le immagini (mappe, characters/img, cover) e altri file pesanti non devono essere duplicati ma condivisi (symlink o directory comune). Obiettivo: ridurre l'occupazione complessiva del progetto.

Opzioni da valutare:
- Symlink delle directory `maps/`, `characters/img/`, `img/` verso LoScettroDityr
- Directory condivisa esterna (es. `adventures/_shared/LoScettroDityr-assets/`)
- Convenzione nel manifest.json (`"shares_assets_with": "LoScettroDityr"`)
- Aggiornare check-adventure.py per accettare il pattern `PascalCase-VerX` senza errore di naming

## Problemi aperti

- Il Modulo A VerT usa **Dispater** nella Torre di Torth, mentre la versione Draco usa **Vecna**. I moduli B/C/D fanno riferimento a Vecna. Serve decidere se uniformare tutto a Dispater o mantenere Vecna nei moduli successivi.
- Il palazzo di Malebranche è nel Modulo A (VerT) ma anche nel Modulo D (Draco). Serve decidere se rimuoverlo dal D o se il D ha un secondo confronto con Malebranche.
- Il livello di partenza è 7 (VerT) vs 8 (Draco). I moduli B/C/D sono calibrati per lv9-10. Serve una milestone nel Modulo A per portare i PG a lv8-9 prima del Modulo B.

## Note sulla variante G 2.2

- Fonte: PDF 21 pagine, datato 10 febbraio 2025
- Avventura per 5-6 PG di livello 7
- Include il palazzo di Malebranche come finale (non presente nella versione Draco del modulo A)
- Personaggi: Frankie Partenope, Lord Cedric Malebranche, Malachias Ombrascura, Axel Ruby, Miranda Emerald, Kreig Wildforge, Mesusu Merconè, Dispater, Zikzle l'Illuminato
