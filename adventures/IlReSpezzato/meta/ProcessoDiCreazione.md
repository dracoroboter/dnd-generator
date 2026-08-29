# Processo di creazione — Il Re Spezzato (documentazione)

Documento di processo. Registra COME è stata costruita la campagna Il Re Spezzato usando gli agenti (narratore, meta-narratore) e la toolchain, quali limiti sono emersi e quali miglioramenti sono stati adottati o restano da adottare.

Data: 2026-08-29. Autore assistito: Kiro (narratore + meta-narratore).

---

## 1. Il processo, passo per passo

La campagna esisteva come draft (documento principale, meccanica del Medaglione, un modulo — Nerrok). Il lavoro di questa sessione ha trasformato il draft in un arco di campagna strutturato con un modulo portato a livello giocabile. Il processo effettivo è stato:

### Fase 0 — Raccolta requisiti (dialogo con l'autore)
Prima di generare, sono state fissate con l'autore le decisioni che vincolano la struttura:
- Campagna autoconclusiva, lv7 → lv12, ~20 sessioni, moduli densi.
- 2-3 finali parzialmente pilotati (convergenza sugli snodi, divergenza sulle conseguenze).
- Il Re resta un mistero che si svela lentamente. I tre figli tornano.
- Vincolo primario: semplicità. I PG non sono dell'autore.

Lezione: le domande giuste PRIMA della generazione hanno evitato di produrre materiale poi da buttare. Le decisioni su livello, numero moduli e tipo di finale determinano tutto il resto.

### Fase 1 — Valutazione con il meta-narratore
Il meta-narratore ha analizzato il draft contro la grammatica narrativa, producendo `analyses/ilrespezzato.yaml`. Output chiave:
- Identificazione del plot dominante (Tragedia, con Dorian villain-vittima), non "sconfiggi il mostro".
- Regole di grammatica rilevanti e anti-pattern da evitare (railroading morale, vie astratte, nemesi scollegata).
- Raccomandazioni concrete per un arco lungo (spina dorsale a 5 moduli, costruzione del legame con Dorian, fazioni leggibili).

Lezione: far analizzare la struttura PRIMA di scriverla ha dato una bussola. La diagnosi "è una tragedia" ha riorientato tutte le scelte successive.

### Fase 2 — Costruzione dell'arco con il narratore
Il narratore ha scritto la struttura dei 5 moduli nel documento principale, più le sezioni lore/fazioni/figli/finali/legame, e ha semplificato la meccanica del Medaglione. Prodotto a livello SCALETTA (dichiarato).

### Fase 3 — Schede NPC
8 schede NPC scritte (Dorian, Gorim, i 3 volti-fazione, i 3 figli). Gorim riusato dalla scheda de L'Anello del Conte (stesso personaggio, tono aggiornato).

### Fase 4 — Un modulo portato a draft giocabile
Il Modulo 2 (Drakenhold), il più critico, è stato portato da scaletta a draft giocabile: scene concrete, incontri con CR validati, battle map, boxed text, transizioni.

### Fase 5 — Cicli di introspezione e miglioramento degli strumenti
Tre giri di introspezione sugli agenti stessi, ciascuno seguito dall'applicazione dei miglioramenti e da una riprova. Vedi sezione 3.

### Fase 6 — Verifica con la toolchain
A ogni passo: `check-adventure.py` (struttura), `encounter-difficulty.py` + `check-encounter-difficulty.py` (bilanciamento), `measure-prose.py` (stile). Le verifiche hanno trovato problemi reali (sezioni mancanti, discrepanze di difficoltà, boxed lunghi) che sono stati corretti.

---

## 2. Ruoli degli agenti

| Agente | Ruolo nel processo | Quando |
|--------|--------------------|--------|
| Meta-narratore | Analizza, diagnostica il plot, verifica contro la grammatica, raccomanda | Prima di scrivere (Fase 1) |
| Narratore | Costruisce l'arco, scrive moduli e schede, valida col toolchain | Dopo la diagnosi (Fasi 2-4, 6) |
| Kiro (orchestratore) | Raccoglie requisiti, delega, verifica gli output, introspezione | Trasversale |

Pattern efficace: meta-narratore diagnostica → narratore costruisce → toolchain verifica → introspezione migliora gli agenti. Il meta-narratore e il narratore sono separati apposta: chi analizza non è chi scrive, e questo dà una validazione più onesta.

---

## 3. Limiti emersi e miglioramenti (tre giri di introspezione)

### Giro 1 — Limiti su COSA produce il narratore
| Limite | Miglioramento adottato |
|--------|------------------------|
| Produceva scaffold dove serviva contenuto giocabile | Regola "Livelli di maturità" (scaletta / draft giocabile / rifinito) |
| Inventava CR "a occhio" | Regola "Validazione obbligatoria dei CR" con encounter-difficulty |
| Non applicava le metriche di stile spontaneamente | measure-prose come step automatico a fine scrittura |
| Grammatica forte in analisi, debole in generazione | Sezione `ricette_di_scena` (6 pattern generativi) |
| Nessuna nozione di ritmo su scala campagna | Sezione `pacing_campagna` |
| Meccaniche custom fuori dal dominio della grammatica | Sezione `meccanica_al_servizio_della_narrazione` |

### Giro 2 — Limiti su COME presenta
| Limite | Miglioramento adottato |
|--------|------------------------|
| Lasciava i "ponteggi" (nomi delle ricette) nel prodotto finale | Regola "I ponteggi non vanno nel prodotto finale" + note di design vs note al master |
| Anglicismi ed emoji che le metriche non colgono | Controllo qualitativo dello stile oltre measure-prose |
| Le ricette non dicevano di sparire dal prodotto | Nota "impalcatura, non etichette" nelle ricette |
| Rischio di scambiare documento ottimo per sessione garantita | Meta-limite in testa alla grammatica: gli strumenti misurano il testo, non l'esperienza |

### Giro 3 — Limiti su ROBUSTEZZA e overfitting (parzialmente adottati)
| Limite | Stato |
|--------|-------|
| Le scene assumono che i PG "sentano" ciò che l'autore vuole; pochi piani B per le deviazioni | Da adottare: regola "progettare per il caso in cui i PG rompono lo script" |
| Le tabelle "Se i PG..." elencano azioni chiuse, non categorie di approccio | Da adottare: progettare per categorie (forza/astuzia/parola/magia/fuga) |
| Nessuna verifica sistematica di continuità tra moduli in fase di scrittura | Da adottare: verifica checkpoint ingresso/uscita e elementi ricorrenti |
| Le ricette di scena sono tutte drammatiche (overfitting sul tragico) | Da adottare: ricette di registri diversi (comico, meraviglia, tensione, mistero) |
| **Meta-limite: gli strumenti sono migliorati su UN SOLO caso (una tragedia seria)** | Riconosciuto, non risolvibile con una regola |

### Aggiunta post-introspezione (richiesta dall'autore)
| Gap | Miglioramento adottato |
|-----|------------------------|
| I combattimenti non fornivano info per disegnare le battle map | Regola "Informazioni per la battle map" nel narratore + applicata al M2 |

---

## 4. Il limite più profondo: overfitting su un solo tipo di storia

Tutti e tre i giri di introspezione hanno usato lo stesso materiale: Il Re Spezzato, una campagna tragica, drammatica, con villain-vittima. Ogni miglioramento è, in parte, un adattamento a questo tipo di storia.

Rischio: gli strumenti diventano eccellenti per le tragedie serie e potenzialmente peggiori per one-shot leggere, dungeon crawl, commedie. Le sei ricette di scena aggiunte servono tutte il dramma; il pacing è tarato su archi emotivi lunghi.

Questo non si corregge con un'altra regola. Si corregge cambiando il caso di prova.

---

## 5. Suggerimenti di miglioramento (prossimi passi)

Ordinati per impatto.

1. **Validare gli strumenti su un'avventura tonalmente opposta.** Prendere una one-shot leggera o un dungeon crawl esistente (es. FuoriDaHellfire) e far girare narratore + meta-narratore. Verificare se le regole aggiunte (ricette drammatiche, pacing di campagna, legame emotivo) aiutano o ostacolano. È il test anti-overfitting. Priorità: ALTA.

2. **Adottare i miglioramenti del giro 3** (robustezza alle deviazioni, categorie di approccio, verifica continuità tra moduli). Sono generali, valgono per qualsiasi avventura. Priorità: MEDIA.

3. **Aggiungere ricette di scena di registri non drammatici** (comico, meraviglia, tensione esplorativa, mistero) per bilanciare l'overfitting sul tragico. Priorità: MEDIA.

4. **Scrivere i moduli M1, M3, M4, M5 di Drakenhold a livello draft giocabile** applicando lo stesso processo del M2. M1 (Nerrok) va anche ribilanciato da lv4-5 a lv7 (già segnato). Priorità: dipende dall'uso.

5. **Il test vero resta il tavolo.** Nessuna metrica dice se il legame con Dorian scatta davvero. La prossima validazione forte è una sessione giocata, non un altro giro di strumenti. Priorità: quando possibile.

---

## 6. Cosa ha funzionato bene (da mantenere)

- La sequenza requisiti → diagnosi (meta) → costruzione (narratore) → verifica (toolchain) → introspezione.
- La separazione meta-narratore / narratore: analizzare e scrivere sono ruoli distinti.
- La toolchain di verifica (check-adventure, encounter-difficulty, measure-prose) ha trovato problemi reali che l'occhio non aveva colto.
- I cicli di introspezione: ogni giro ha corretto un livello di problema più profondo del precedente, e il terzo ha saputo riconoscere il proprio confine (overfitting) invece di inventare miglioramenti marginali.
