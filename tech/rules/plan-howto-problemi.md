# Problemi riscontrati — Scaffolding FuoriDaHellfire

Data: 2026-04-18
Contesto: primo uso reale di `new-adventure.sh` + how-to per creare un'avventura nuova.

---

## Problemi nello script `new-adventure.sh`

### P1 — Il modulo placeholder ha un nome scomodo
Lo script rinomina il file del modulo in `FuoriDaHellfire_Modulo01.md`. Questo nome non segue la naming convention: dovrebbe essere il nome del modulo (es. `DiscesaNelleFogne.md`), non `NomeAvventura_ModuloNN.md`. Il DM deve comunque rinominarlo subito.

**Suggerimento**: lasciare il file come `NomeModulo.md` (placeholder generico) oppure non rinominarlo affatto — tanto va rinominato al 100%.

### P2 — Il commento saga nel README.md ha placeholder sbagliati
Lo script fa sed di `NomeAvventura` → `FuoriDaHellfire` ovunque, incluso dentro il commento HTML della saga. Risultato:
```
**Segue**: — (o FuoriDaHellfirePrecedente)
**Precede**: — (o FuoriDaHellfireSuccessiva)
```
Dovrebbe restare generico (`NomeAvventuraPrecedente`) perché è un commento-guida, non un valore da compilare.

**Suggerimento**: nel template usare un placeholder diverso che non venga catturato dal sed, es. `<AVVENTURA_PRECEDENTE>`.

### P3 — Il placeholder NPC viene rinominato in `.placeholder` ma non è documentato chiaramente
Il file diventa `NPC_NomePersonaggio.md.placeholder`. L'how-to dice di eliminarlo, ma un nuovo utente potrebbe non capire che è un file da cancellare e non da rinominare.

**Suggerimento**: o lo script lo elimina direttamente (lasciando la directory `personaggi/` vuota), oppure il file mantiene estensione `.md` con un commento interno che dice "questo è un placeholder, rinominami o cancellami".

### P4 — Lo script non crea moduli aggiuntivi
Se il concept prevede 3 moduli, il DM deve creare manualmente `02_*` e `03_*` copiando dal primo. L'how-to documenta il processo, ma lo script potrebbe accettare un parametro opzionale per il numero di moduli.

**Suggerimento futuro**: `new-adventure.sh NomeAvventura --modules 3`

---

## Problemi nell'how-to

### H1 — Fase 1 documenta il risultato dello scaffolding ma il nome del file modulo è sbagliato
L'how-to dice che lo script crea `NomeMiaAvventura_Modulo01.md`, che è corretto rispetto allo script attuale, ma è un nome che nessuno userà mai. La guida dovrebbe enfatizzare che il primo passo dopo lo scaffolding è rinominare il modulo.

### H2 — Manca la Fase 0 come file separato
Il concept (Fase 0) viene scritto a mente o in chat, ma non ha un posto nel repository. Potrebbe stare nel `PlanBook.md` come prima sezione, o in un file dedicato. Attualmente il PlanBook template è troppo scarno per ospitarlo.

---

## Azioni

- [x] P1: script corretto — il file modulo resta `NomeModulo.md`
- [x] P2: template corretto — placeholder saga ora `<avventura-precedente>`
- [x] P3: script corretto — placeholder NPC eliminato, directory `personaggi/` vuota
- [x] P4: script corretto — aggiunto `--modules N`
- [x] H1: how-to aggiornato per riflettere tutte le correzioni
- [x] H2: concept va nel PlanBook — aggiunta sezione `## Concept` al template


---

## Problemi emersi nella sessione 2026-04-18/19

### P5 — check-adventure.py non conosce la nuova struttura personaggi/
Lo script cerca `NPC_*.md` direttamente in `personaggi/`, ma ora i file sono in `personaggi/markdown/`. Va aggiornato per cercare in entrambe le posizioni (retrocompatibilità).

### P6 — Corridoi nel renderer v2 hanno bordi che non arrivano ai muri
I bordi laterali dei corridoi si estendono di `ext` pixel ma il fix è parziale (solo orizzontali). Serve un approccio più robusto — possibilmente spline o calcolo geometrico dei punti di intersezione corridoio/muro.
