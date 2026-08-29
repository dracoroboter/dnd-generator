# Refine Adventure - Loop iterativo di miglioramento di un'avventura

Ciclo di raffinamento di un'avventura (o di un modulo) attraverso giri successivi di validazione, correzione e giudizio umano. Usa questa skill quando l'utente dice "miglioriamo X", "raffiniamo il modulo Y", "facciamo un giro di revisione su Z", o quando dopo aver scritto contenuto vuoi portarlo a maturità in modo controllato.

Il loop è **semi-manuale a controllo umano**: l'orchestratore esegue validazione e correzione, ma il giro non si chiude né riparte senza il giudizio dell'utente. Il valore vero emerge dalla lettura umana, non dagli script: gli script trovano errori, l'utente giudica la qualità.

## Il ciclo (un giro)

```
[1. VALIDAZIONE/GIUDIZIO]  (orchestratore)
     ↓
[2. CORREZIONE]            (narratore scrive, orchestratore ri-valida)
     ↓
[3. GIUDIZIO UMANO]        (l'utente legge e critica) ← punto interattivo
     ↓
[4. CHIUSURA DEL GIRO]     STOP se approvato o giri esauriti, altrimenti nuovo giro
```

### 1. Validazione / giudizio (orchestratore)

Raccogli gli esiti oggettivi e il tuo giudizio qualitativo. Usa **tutti** gli strumenti di verifica pertinenti al tipo di modifica del giro; non saltarne nessuno per fretta.

- **Formale**: `check-adventure.py <Avventura>` — struttura, file obbligatori, sezioni, immagini NPC, path.
- **Stile e prolissità**: `measure-prose.py <Avventura>` — rapporto prosa/dati, densità, boxed text, dialogo, HR, righe per heading. `find-long-boxed.py <Avventura>` — zoom sui boxed text troppo lunghi (dettaglio della stessa dimensione che measure-prose aggrega).
- **Bilanciamento**: `check-encounter-difficulty.py <Avventura>` — confronta la difficoltà dichiarata nei moduli con il calcolo XP su tutta l'avventura. Per validare un **singolo** incontro nuovo o ritoccato, `encounter-difficulty.py` (calcolo puntuale di soglie/CR per un party).
- **Coerenza e compattezza narrativa**: `score-narrative-quality.py` (skill `narrative-quality`, punteggio 0-100 su logline/perciò-ma/setup-payoff/matrice tematica) e `validate-narrative.py <analisi.yaml>` (ossatura in stereotipi contro grammatica e vocabolario; con `--check-all` valida tutti gli YAML narrativi del sistema).
- **Sintassi** (solo se il giro tocca file YAML/JSON, es. agenti o grammatica narrativa): `validate-syntax.py <file...>` oppure i preset `--agents` / `--narrative`.
- **Giudizio qualitativo tuo** (ciò che nessuno script coglie): rileggi cercando buchi di sceneggiatura, moventi ingiustificati (test "chi sa cosa" e "perché lo vuole"), contraddizioni, prolissità, anglicismi, meta-linguaggio da autore, tono incoerente.

Nota: `test_regression.py` verifica gli **script** della toolchain, non le avventure; entra in gioco solo se il giro modifica uno script (compito dell'orchestratore), non nel raffinamento del contenuto. Gli strumenti di generazione/pipeline (create-pdf, generate-statblocks, encounter-builder, ecc.) non sono verificatori e non fanno parte di questo passo.

Quali strumenti attivare dipende dal contesto del giro:
- **Modulo di prosa** ritoccato: check-adventure, measure-prose, find-long-boxed, score-narrative-quality (contesto modulo), giudizio qualitativo.
- **Incontri** ritoccati: aggiungi check-encounter-difficulty (e encounter-difficulty sul singolo incontro cambiato).
- **Lore / arco / struttura di campagna**: aggiungi score-narrative-quality (contesto campagna) e, se esiste un'analisi in stereotipi, validate-narrative.
- **File di configurazione YAML/JSON** toccati: aggiungi validate-syntax.

### 2. Correzione (narratore + orchestratore)

- La scrittura delle correzioni va **delegata al narratore** (vedi skill `dungeonmaster`, divisione dei ruoli).
- L'orchestratore **ri-valida** dopo la correzione: le correzioni non devono introdurre nuovi problemi.

### 3. Giudizio umano (l'utente) — punto interattivo

Presenta all'utente il risultato del giro (cosa è stato validato, cosa corretto) e **chiedi il suo giudizio**. In questa fase il giudizio è **libero**: l'utente scrive critiche in prosa, come preferisce. Non forzare una struttura.

Le critiche dell'utente sono l'input più prezioso: vanno raccolte con cura e trattate come il to-do del giro successivo.

### 4. Chiusura del giro

- Se l'utente **approva**: STOP, il loop termina.
- Se l'utente **critica**: le sue critiche diventano il to-do del giro successivo. Si riparte dal punto 1.
- **Cap: massimo 3 giri.** Se al terzo giro non c'è approvazione, ferma comunque il loop e riepiloga all'utente cosa resta aperto, senza avviare un quarto giro. L'utente decide se rilanciare esplicitamente.

## Tracciamento (breve)

Ogni giro va tracciato **in modo sintetico**, per permettere una meta-analisi sul processo. Per ora, tieni la traccia inline nella conversazione e, a fine loop, scrivi un riepilogo breve nel PlanBook dell'avventura (sezione dedicata o log di sessione). Formato minimo per giro:

```
Giro N: [validazione: esiti chiave] → [correzioni applicate] → [giudizio utente] → [decisione: STOP | nuovo giro]
```

Non serve un documento elaborato: bastano poche righe per giro. Servono a capire, a posteriori, come è evoluto il lavoro e quali critiche ricorrono.

## Note

- La directory di lavoro è `~/dungeonandragon`.
- Questa skill orchestra strumenti che esistono già (`narrative-quality`, `dungeonmaster`, gli script di verifica): non li sostituisce, li mette in sequenza con l'utente come cancello.
- Il cap a 3 giri è una scelta iniziale, rivedibile. Serve a evitare loop infiniti e a forzare una decisione.
- Stato sperimentale: questa è la prima forma del loop (descrizione + giudizio libero + tracciamento breve). Estensioni pianificate (log di raffinamento dedicato, giudizio misto voti+note, pipeline automatica coi sub-agent) sono nel `plan-meta-dnd.md`.
