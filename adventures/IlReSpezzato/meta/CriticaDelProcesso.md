# Critica del processo — orchestrazione con agenti e limiti della shell

Documento di critica del processo. A differenza di `ProcessoDiCreazione.md` (che descrive COME è stata costruita la campagna), questo documento analizza il PROCESSO DI LAVORO con gli agenti: cosa ha funzionato, cosa no, dove ho sbagliato la diagnosi, e quali sono i limiti architetturali emersi.

Data: 2026-08-29.

---

## 1. Il flusso di lavoro adottato

```
Utente (requisiti)
   │
   ▼
Orchestratore (Kiro) ──► Meta-narratore (analisi/diagnosi)
   │                          │
   │                          ▼
   │                     analyses/*.yaml
   │
   ├──────────────────► Narratore (scrittura moduli/schede)
   │                          │
   │                          ▼
   │                     adventures/**
   │
   ▼
Orchestratore (verifica con toolchain) ──► check-adventure, encounter-difficulty, measure-prose
   │
   ▼
Introspezione (migliora gli agenti) ──► narratore-prompt.md, narrative-grammar.yaml
```

Il pattern centrale: **l'orchestratore delega la creazione ai sub-agent (meta-narratore per l'analisi, narratore per la scrittura) e tiene per sé la verifica e l'introspezione.**

---

## 2. Cosa ha funzionato

- **Separazione dei ruoli.** Meta-narratore analizza, narratore scrive, orchestratore verifica. Chi scrive non è chi giudica: la validazione è più onesta.
- **Diagnosi prima della scrittura.** Far dire al meta-narratore "è una Tragedia, non sconfiggi-il-mostro" ha riorientato tutto il design a monte, evitando un arco costruito sul plot sbagliato.
- **Toolchain come rete di sicurezza.** Gli script hanno trovato problemi reali che la lettura non aveva colto: sezioni obbligatorie mancanti, discrepanze di difficoltà (Porte EASY vs TRIVIAL), boxed text lunghi, HR di troppo.
- **Introspezione iterativa.** Tre giri, ognuno su un livello di problema più profondo (cosa produce → come lo presenta → quanto è robusto/overfitting). Il terzo giro ha saputo riconoscere il proprio confine invece di inventare miglioramenti marginali.

---

## 3. Cosa NON ha funzionato: la shell dei sub-agent

### Il sintomo
Ogni volta che il narratore (come sub-agent) doveva eseguire uno script di verifica (`check-encounter-difficulty.py`, `measure-prose.py`, ecc.), il comando veniva bloccato. Il sub-agent riportava "Command not in allowed list". Ho dovuto eseguire io le verifiche dall'orchestratore, raddoppiando i passaggi.

### La mia diagnosi sbagliata
Ho attribuito il blocco ai **pattern rigidi** nel `narratore.json`: gli `allowedCommands` richiedevano il prefisso `wsl bash -c.*script`, e ho supposto che il sub-agent invocasse `python3 ...` diretto, non combaciando col regex. Ho quindi "corretto" i pattern rendendoli flessibili (`.*script\.py`).

### La verità (emersa dalla riprova)
Facendo eseguire al narratore un test diagnostico, è emerso che **anche `echo test` viene bloccato**. Il blocco è totale, non dipende né dalla forma di invocazione né dallo specifico script. La shell dell'orchestratore invece funziona perfettamente (stessi comandi, stessa macchina).

Conclusione: **i sub-agent spawnati non hanno accesso alla shell.** È una restrizione dell'ambiente di esecuzione dei sub-agent, non della configurazione dell'agente. La whitelist nel `narratore.json` è irrilevante quando l'agente gira come sub-agent, perché la shell è disabilitata a monte.

### La lezione
Ho commesso l'errore classico: ho ipotizzato una causa plausibile (pattern rigidi) e ho applicato un fix senza prima verificare l'ipotesi con un test isolante. Il test giusto (`echo test` in un sub-agent) avrebbe smascherato la causa reale in un colpo. L'ho fatto solo dopo, nella riprova. La regola che ne traggo: **prima isolare la causa con il test più semplice possibile, poi fixare** — non fixare sull'ipotesi.

Nota: il fix ai pattern NON è inutile. Quando il narratore viene usato **direttamente** (comando `@narratore` o scorciatoia da tastiera), la sua shell funziona e i pattern flessibili gli permettono di lanciare gli script in qualsiasi forma. Il fix è corretto per l'uso diretto, inefficace per l'uso come sub-agent.

---

## 4. Conseguenze pratiche per il workflow

Dato che i sub-agent non possono eseguire script:

| Compito | Chi lo fa |
|---------|-----------|
| Analisi narrativa (meta-narratore) | Sub-agent — non serve shell, usa solo lettura/conoscenza |
| Scrittura moduli/schede (narratore) | Sub-agent — non serve shell, usa solo write |
| Verifica con toolchain (check, encounter, prose) | **Orchestratore** — la delega al sub-agent fallisce |
| Uso diretto del narratore con verifiche | Narratore attivato direttamente (non come sub-agent) |

Regola operativa: **non delegare ai sub-agent compiti che richiedono la shell.** Delegare loro scrittura e analisi (dove eccellono), tenere all'orchestratore l'esecuzione degli script. Oppure, per un flusso in cui il narratore verifica da sé, usarlo come agente attivo diretto invece che come sub-agent.

---

## 5. Altri limiti del processo

- **I sub-agent dichiarano metriche stimate come se fossero calcolate.** Il narratore, non potendo eseguire measure-prose, ha "calcolato a mano" le metriche replicando la logica dello script. Le stime erano vicine ma non identiche ai valori reali (es. rapporto prosa/dati 0.47 stimato vs 0.48-0.85 reale su file diversi). Rischio: prendere per verificato ciò che è solo stimato. Mitigazione: l'orchestratore ri-esegue sempre gli script veri.
- **Overfitting su un solo caso di prova.** Vedi `ProcessoDiCreazione.md` § 4. Tre giri di introspezione sullo stesso tipo di storia (tragedia seria) rischiano di specializzare gli strumenti su quel registro.
- **Il costo dei round di delega.** Ogni delega a un sub-agent è un round completo (prompt, esecuzione, lettura output, verifica). Per compiti piccoli, l'orchestratore che fa direttamente è più veloce. La delega conviene per lavori corposi e ben isolati (scrivere un modulo intero, analizzare un'opera).

---

## 6. Suggerimenti di miglioramento del processo

1. **Documentare il limite shell dei sub-agent** dove serve (fatto qui). Evita di ripetere la diagnosi sbagliata in futuro.
2. **Protocollo di debug**: davanti a un blocco, prima il test isolante minimo (`echo test`), poi la diagnosi, poi il fix. Mai fixare sull'ipotesi non verificata.
3. **Divisione del lavoro esplicita**: nei prompt ai sub-agent, dire chiaramente "non eseguire script, li eseguo io" quando li si usa come sub-agent, per non fargli perdere tempo e non fargli dichiarare stime come verifiche.
4. **Valutare se serve davvero il sub-agent**: per verifiche pure (solo script), l'orchestratore è più diretto. Il sub-agent conviene per scrittura/analisi lunghe.
5. **Test anti-overfitting**: la prossima validazione degli agenti su un'avventura di tipo opposto (one-shot leggera, dungeon crawl), come già indicato in ProcessoDiCreazione.md § 5.

---

## 7. Verifiche finali dell'avventura (eseguite dall'orchestratore)

Stato de Il Re Spezzato al termine della sessione, verificato con gli script reali:

- `check-adventure.py`: 0 errori critici, 9 warning (immagini NPC mancanti, attese).
- `check-encounter-difficulty.py`: modulo Drakenhold tutti gli incontri ✓ (Porte EASY, Fiamma MEDIUM, Ponte HARD, dichiarato = calcolato). Modulo Nerrok: 1 discrepanza nota e già marcata da ribilanciare (lv4-5 → lv7).
- `measure-prose.py`: modulo Drakenhold in target (prosa/dati 0.48, densità 0.57, dialogo 12.5%, 0 boxed lunghi).
- Battle map presenti nei 3 incontri di Drakenhold.
