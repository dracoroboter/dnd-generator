# Narrative Quality - Punteggio di coerenza e compattezza di un'avventura

Valuta la **qualità narrativa** di un'avventura o di un modulo scritto e ne ricava un **punteggio numerico** (0-100) di coerenza e compattezza tematica. Usa questa skill quando l'utente chiede "che voto ha questa avventura", "quanto è compatta questa storia", "valuta la sceneggiatura di X", o quando vuoi un controllo di qualità narrativa prima di dichiarare un modulo maturo.

Non misura l'originalità né il gusto: misura se la storia **regge insieme**. Un punteggio alto non garantisce una bella storia, ma un punteggio basso segnala quasi sempre una storia slegata, dispersiva o con promesse narrative tradite.

## Cosa misura: quattro tecniche

| Metrica | Cosa cattura | Domanda |
|---------|--------------|---------|
| **Logline** | compattezza tematica | L'opera si riassume in una frase-tema? Ogni modulo vi si aggancia? |
| **Perciò / ma** | compattezza causale | I legami tra scene sono causali ("perciò", "ma") o giustapposti ("e poi")? |
| **Setup / payoff** | coerenza di promessa | Ogni seme piantato viene raccolto? Ogni colpo di scena era stato seminato? |
| **Matrice tematica** | coerenza tematica | Ogni tema dichiarato è giocato da almeno una scena? Ogni scena tocca un tema? |

La **regola di Trey Parker** (South Park) sta dietro alla metrica perciò/ma: riassumendo la storia beat per beat, tra un beat e l'altro deve poterci stare "perciò" o "ma", mai "e poi". "E poi" è una lista di eventi; "perciò/ma" è una storia con causalità e conflitto.

Il **Cechov bidirezionale** sta dietro a setup/payoff: un fucile appeso alla parete deve sparare (seme senza raccolto = promessa tradita), e uno sparo deve avere un fucile appeso prima (raccolto senza seme = deus ex machina).

## Quando attivare quali metriche (contesti)

Non tutte le metriche vanno usate sempre. La skill le attiva secondo il contesto; nel file di input si compilano solo le sezioni pertinenti, e il punteggio si normalizza automaticamente sulle metriche presenti.

| Contesto | Logline | Perciò/ma | Setup/payoff | Matrice tematica |
|----------|:-------:|:---------:|:------------:|:----------------:|
| **Scena o singolo incontro** | no | sì | no | no |
| **Modulo singolo** (una sessione) | sì | sì | sì (interni al modulo) | no |
| **Avventura completa** (one-shot, saga breve) | sì | sì | sì | opzionale |
| **Campagna lunga** (molte sessioni) | sì | sì | sì | sì (essenziale) |

Ragione della tabella:
- La **logline** ha senso da un modulo in su: una singola scena non ha un tema proprio.
- Il **perciò/ma** si applica sempre che ci siano almeno due scene consecutive.
- Il **setup/payoff** dentro una scena non esiste; nel modulo riguarda i semi interni; nell'avventura e nella campagna riguarda i semi che attraversano i moduli.
- La **matrice tematica** è sovradimensionata per opere corte (poche scene, tema evidente) ed è invece decisiva per le campagne lunghe, dove il rischio di dispersione tematica è reale.

## Come usarla

1. **Genera il template** del file di input:
   ```bash
   python3 tech/scripts/score-narrative-quality.py --template > tech/reports/quality_<Nome>.yaml
   ```
2. **Compila** solo le sezioni pertinenti al contesto (vedi tabella). Cancella le sezioni non usate. Il giudizio semantico (quale transizione è "perciò" e quale "e poi", quale scena tocca quale tema) va fatto a mano leggendo l'avventura: lo script calcola il punteggio, non lo indovina.
3. **Calcola il punteggio**:
   ```bash
   python3 tech/scripts/score-narrative-quality.py tech/reports/quality_<Nome>.yaml
   ```
4. Leggi il punteggio complessivo, i punteggi per metrica e i **rilievi** (moduli fuori tema, transizioni "e poi", semi non raccolti, deus ex machina, temi non giocati). I rilievi sono la parte utile: dicono dove intervenire.

Il file di input compilato può restare in `tech/reports/` (non tracciato) oppure, se vuoi conservarlo come documentazione di design, spostarlo in `adventures/<Nome>/meta/`.

## Interpretare il punteggio

| Punteggio | Voto | Lettura |
|-----------|------|---------|
| 90-100 | eccellente | la storia regge, i legami sono causali, le promesse mantenute |
| 75-89 | buono | qualche punto debole isolato |
| 60-74 | sufficiente | tiene, ma con difetti da sistemare |
| 40-59 | debole | dispersione o legami deboli diffusi |
| < 40 | insufficiente | storia slegata, promesse tradite, temi dichiarati e non giocati |

Il punteggio è uno strumento diagnostico, non un verdetto. Guarda sempre i rilievi: un 70 con un solo modulo fuori tema si corregge facilmente; un 70 diffuso è un problema strutturale.

## Misura complementare: validate-narrative.py

Per una valutazione più completa, affianca a questa skill lo script `validate-narrative.py`, che opera su un piano diverso e complementare. Il narratore può usarlo come ulteriore misura di bontà della scrittura.

- `score-narrative-quality.py` (questa skill) valuta la **sceneggiatura scritta**: coerenza e compattezza della storia come viene raccontata.
- `validate-narrative.py` valuta un'**analisi in stereotipi** dell'opera (un file in `tech/data/references/analyses/`) contro il vocabolario e la grammatica narrativa: copertura del vocabolario, prerequisiti tra stereotipi soddisfatti, regole di sequenza rispettate, densità e varietà, ripetizioni eccessive.

```bash
python3 tech/scripts/validate-narrative.py tech/data/references/analyses/<opera>.yaml
```

Usarli insieme dà due angolazioni: `validate-narrative` verifica che la struttura narrativa rispetti la grammatica degli stereotipi (l'ossatura è ben formata); `score-narrative-quality` verifica che la storia raccontata sia coerente e compatta (la carne regge). Un'opera può passare l'uno e non l'altro: una struttura grammaticalmente corretta può comunque essere una lista di "e poi", e una storia compatta può usare pochi stereotipi catalogati.

## Note

- La directory di lavoro è `~/dungeonandragon`.
- Le metriche assenti dal file di input sono escluse dalla media pesata: il punteggio è sempre normalizzato sulle metriche attivate.
- Il giudizio semantico resta umano (dell'utente o del narratore che ragiona sull'avventura). Lo script non legge la prosa: legge la tua classificazione delle transizioni, dei semi e dei temi. Serve a rendere esplicito e numerico un giudizio che altrimenti resta implicito.
- Questa valutazione è ortogonale a `measure-prose.py` (stile e formato) e a `check-encounter-difficulty.py` (bilanciamento): coprono dimensioni diverse della qualità.
