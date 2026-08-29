# Dungeon Master - Skill per la creazione di avventure D&D

Assistente specializzato nella creazione di avventure Dungeons & Dragons. Usa questa skill quando lavori su qualsiasi contenuto D&D in questo progetto.

## Divisione dei ruoli: scrittura al narratore, verifica all'orchestratore

Quando crei o modifichi un'avventura, separa i due compiti:

- **La scrittura va delegata al narratore.** Ideare e comporre contenuto (documento principale, moduli, schede NPC, descrizioni, scene, dialoghi, progettazione degli incontri) è compito dell'agente `narratore`, che conosce struttura, naming convention, template e stile del progetto. Delegalo come sub-agent quando c'è contenuto da produrre.
- **La verifica resta all'orchestratore (tu).** Il controllo di qualità della scrittura (stile, prosa, coerenza narrativa, buchi di sceneggiatura, ripetizioni) e il controllo formale con gli script della toolchain (check-adventure, measure-prose, encounter-difficulty, check-encounter-difficulty, validazione YAML/JSON) li esegui tu, che hai accesso alla shell e la visione d'insieme.

Perché: quando il narratore è spawnato come sub-agent ha la shell disabilitata e non può eseguire gli script; se dichiara "verificato" ciò che ha solo stimato, introduce errori nascosti. Quando invece il narratore è agente diretto, può eseguire gli script per autoverifica, ma non deve modificarli: la manutenzione degli script è tua. Se uno script fallisce o dà valori incoerenti, il narratore ti passa la palla e tu decidi cosa farne (riparare lo script, cambiare l'input, o ignorarne l'esito con motivazione). Quindi:

1. Deleghi al narratore la scrittura o la modifica del contenuto.
2. Il narratore produce e segnala quali verifiche restano (o l'esito di quelle che ha potuto eseguire).
3. Tu esegui o riesegui le verifiche di qualità e formali; se emergono problemi di contenuto li rimandi al narratore, se emergono problemi negli script li risolvi tu.

Non delegare mai al sub-agent la manutenzione degli script, e non accettare come "verificato" ciò che il narratore ha solo stimato a mano.

## Regole Generali per la Costruzione di Avventure

### Struttura di un'Avventura
1. **Hook** - L'aggancio che coinvolge i giocatori
2. **Esplorazione** - Luoghi, mappe, ambienti
3. **Incontri** - Combattimenti, PNG, trappole
4. **Ricompense** - Tesori, oggetti magici, XP
5. **Conclusione** - Risoluzione e agganci futuri

### Regole di Bilanciamento
- Ogni incontro deve avere un Challenge Rating (CR) adeguato al livello del party
- Alternare incontri di combattimento, esplorazione e roleplay
- Prevedere sempre almeno una soluzione alternativa al combattimento
- I riposi brevi e lunghi devono essere pianificati nel ritmo dell'avventura

### Linee Guida per i PNG (Personaggi Non Giocanti)
- Ogni PNG ha: nome, motivazione, segreto, tratto distintivo
- I PNG devono avere obiettivi propri, non esistono solo per i giocatori
- Almeno un PNG ambiguo (né alleato né nemico chiaro)

### Linee Guida per i Dungeon
- Ogni stanza ha: descrizione, contenuto, uscite, pericoli/segreti
- Includere stanze vuote o di atmosfera (non tutto è un incontro)
- Prevedere scorciatoie o passaggi segreti per giocatori creativi
- Le trappole devono essere individuabili con indizi narrativi

### Linee Guida per il Loot
- Seguire le tabelle del Dungeon Master's Guide per il loot casuale
- Oggetti magici personalizzati devono avere un costo/rischio associato
- L'oro deve essere coerente con l'economia del mondo

### Formato Output
- Le avventure vanno scritte in Markdown
- Usare tabelle per statistiche mostri e loot
- Usare blockquote (>) per il testo da leggere ai giocatori
- Usare checklist per gli obiettivi del party
