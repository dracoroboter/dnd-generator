#!/usr/bin/env python3
"""
score-narrative-quality.py — Punteggio di coerenza e compattezza tematica
di un'avventura (o di un singolo modulo) SCRITTA.

A differenza di validate-narrative.py (che valida un'ANALISI di stereotipi
contro grammatica e vocabolario), questo script valuta la QUALITA' NARRATIVA
di una sceneggiatura, combinando quattro tecniche:

  1. Logline           — l'opera si riassume in una frase-tema, e ogni modulo
                         vi si aggancia? (compattezza tematica)
  2. Perciò / ma        — i legami tra scene sono causali ("perciò", "ma")
                         o giustapposti ("e poi")? (compattezza causale)
                         [regola di Trey Parker / South Park]
  3. Setup / payoff     — ogni seme (setup) ha un raccolto (payoff) e viceversa?
                         (coerenza di promessa narrativa, Cechov bidirezionale)
  4. Matrice tematica   — ogni asse tematico dichiarato è toccato da almeno una
                         scena, e ogni scena tocca almeno un asse? (coerenza
                         tematica su opere lunghe)

Non tutte le metriche vanno usate sempre: vedi la skill
`.kiro/skills/narrative-quality/SKILL.md` per i contesti di attivazione.
Le metriche non presenti nel file di input vengono semplicemente escluse dalla
media pesata: il punteggio finale è sempre normalizzato sulle sole metriche
attivate.

Il giudizio semantico (quale transizione è "perciò" e quale è "e poi", quale
scena tocca quale tema) NON è automatizzabile: va compilato a mano dal
narratore/orchestratore in un file YAML di input. Lo script calcola il
punteggio, non lo indovina.

Uso:
  python3 tech/scripts/score-narrative-quality.py <file-input.yaml>
  python3 tech/scripts/score-narrative-quality.py --template   # stampa un template vuoto
  python3 tech/scripts/score-narrative-quality.py --self-test

Formato file di input: vedi --template.
"""
import sys
import os

try:
    import yaml
except ImportError:
    print("Serve pyyaml: pip install pyyaml")
    sys.exit(1)


# Pesi di default delle quattro metriche nel punteggio complessivo.
# Vengono rinormalizzati sulle sole metriche effettivamente presenti nel file.
PESI_DEFAULT = {
    "logline": 0.20,
    "perciò_ma": 0.30,
    "setup_payoff": 0.30,
    "matrice_tematica": 0.20,
}

TEMPLATE = """\
# Input per score-narrative-quality.py
# Compila SOLO le sezioni pertinenti al contesto (vedi la skill).
# Le sezioni assenti vengono escluse dalla media: il punteggio si normalizza
# sulle metriche presenti. Cancella le sezioni che non usi.

opera: "Nome avventura o modulo"
contesto: "modulo singolo | avventura completa | campagna lunga"

# --- 1. LOGLINE (compattezza tematica) ---
# La frase-tema che riassume tutta l'opera. Poi, per ogni modulo/blocco,
# dichiara se si aggancia alla logline (true/false) e come.
logline:
  frase: "In una frase: di cosa parla davvero questa storia?"
  moduli:
    - nome: "Modulo 1"
      aggancio: true
      come: "come questo modulo serve il tema"
    - nome: "Modulo 2"
      aggancio: true
      come: "..."

# --- 2. PERCIO' / MA (compattezza causale, regola di Trey Parker) ---
# Elenca le transizioni tra scene/beat consecutivi. Per ognuna, la congiunzione
# che descrive il legame: "perciò" o "ma" = causale (buono);
# "e_poi" = giustapposto (debole).
percio_ma:
  transizioni:
    - da: "Scena A"
      a: "Scena B"
      legame: "perciò"      # perciò | ma | e_poi
    - da: "Scena B"
      a: "Scena C"
      legame: "e_poi"

# --- 3. SETUP / PAYOFF (Cechov bidirezionale) ---
# Ogni seme piantato e dove viene raccolto. Se un seme non ha raccolto o un
# raccolto non ha seme, è un difetto. Usa payoff: null per un seme non raccolto.
setup_payoff:
  semi:
    - setup: "Cosa viene piantato (es. i simulacri dei figli a Nerrok)"
      payoff: "Dove viene raccolto (es. il ritorno dei figli in M3)"
    - setup: "Un dettaglio seminato ma mai ripreso"
      payoff: null
  # Raccolti che compaiono SENZA essere stati seminati prima (deus ex machina):
  payoff_orfani:
    - "Un colpo di scena introdotto senza semina"

# --- 4. MATRICE TEMATICA (coerenza tematica, opere lunghe) ---
# Definisci gli assi tematici, poi per ogni scena quali assi tocca.
matrice_tematica:
  assi:
    - "Asse tematico 1"
    - "Asse tematico 2"
    - "Asse tematico 3"
  scene:
    - nome: "Scena/Modulo 1"
      assi: ["Asse tematico 1"]
    - nome: "Scena/Modulo 2"
      assi: ["Asse tematico 1", "Asse tematico 2"]
"""


def score_logline(data):
    """Punteggio compattezza tematica: quota di moduli agganciati alla logline.
    Penalità se la frase-tema manca."""
    frase = (data.get("frase") or "").strip()
    moduli = data.get("moduli", []) or []
    dettagli = []
    if not frase:
        dettagli.append("Manca la frase-tema (logline): -30%")
    if not moduli:
        return (0.0 if not frase else 60.0), ["Nessun modulo dichiarato"]
    agganciati = sum(1 for m in moduli if m.get("aggancio"))
    quota = agganciati / len(moduli)
    non_agg = [m.get("nome", "?") for m in moduli if not m.get("aggancio")]
    if non_agg:
        dettagli.append(f"Moduli fuori tema (non agganciati alla logline): {non_agg}")
    base = quota * 100
    if not frase:
        base *= 0.7  # penalità per logline mancante
    return base, dettagli


def score_percio_ma(data):
    """Punteggio compattezza causale: quota di transizioni causali (perciò/ma)
    sul totale. Gli 'e_poi' sono i punti deboli."""
    trans = data.get("transizioni", []) or []
    if not trans:
        return None, ["Nessuna transizione dichiarata"]
    causali = 0
    e_poi = []
    for t in trans:
        legame = (t.get("legame") or "").strip().lower()
        if legame in ("perciò", "percio", "ma", "but", "therefore"):
            causali += 1
        else:
            e_poi.append(f"{t.get('da','?')} -> {t.get('a','?')} ({legame or 'non classificato'})")
    quota = causali / len(trans)
    dettagli = []
    if e_poi:
        dettagli.append(f"Transizioni 'e poi' (giustapposte, non causali): {e_poi}")
    return quota * 100, dettagli


def score_setup_payoff(data):
    """Punteggio coerenza di promessa: penalizza semi orfani (setup senza payoff)
    e payoff orfani (raccolti senza semina)."""
    semi = data.get("semi", []) or []
    payoff_orfani = data.get("payoff_orfani", []) or []
    if not semi and not payoff_orfani:
        return None, ["Nessun setup/payoff dichiarato"]
    semi_orfani = [s.get("setup", "?") for s in semi if not s.get("payoff")]
    totale_promesse = len(semi) + len(payoff_orfani)
    difetti = len(semi_orfani) + len(payoff_orfani)
    quota_ok = 1 - (difetti / totale_promesse) if totale_promesse else 1.0
    dettagli = []
    if semi_orfani:
        dettagli.append(f"Semi non raccolti (fucili di Cechov che non sparano): {semi_orfani}")
    if payoff_orfani:
        dettagli.append(f"Raccolti senza semina (deus ex machina): {payoff_orfani}")
    return quota_ok * 100, dettagli


def score_matrice_tematica(data):
    """Punteggio coerenza tematica: penalizza assi non toccati da alcuna scena
    (colonne vuote) e scene che non toccano alcun asse (righe vuote)."""
    assi = data.get("assi", []) or []
    scene = data.get("scene", []) or []
    if not assi or not scene:
        return None, ["Assi o scene mancanti"]
    assi_toccati = set()
    scene_vuote = []
    for s in scene:
        s_assi = s.get("assi", []) or []
        if not s_assi:
            scene_vuote.append(s.get("nome", "?"))
        for a in s_assi:
            assi_toccati.add(a)
    assi_vuoti = [a for a in assi if a not in assi_toccati]
    problemi = len(assi_vuoti) + len(scene_vuote)
    totale = len(assi) + len(scene)
    quota_ok = 1 - (problemi / totale) if totale else 1.0
    dettagli = []
    if assi_vuoti:
        dettagli.append(f"Assi tematici mai toccati da alcuna scena (temi dichiarati ma non giocati): {assi_vuoti}")
    if scene_vuote:
        dettagli.append(f"Scene fuori tema (non toccano alcun asse): {scene_vuote}")
    return quota_ok * 100, dettagli


SCORERS = {
    "logline": score_logline,
    "perciò_ma": score_percio_ma,
    "setup_payoff": score_setup_payoff,
    "matrice_tematica": score_matrice_tematica,
}

# Le chiavi YAML usano l'underscore ASCII per robustezza
CHIAVI_YAML = {
    "logline": "logline",
    "perciò_ma": "percio_ma",
    "setup_payoff": "setup_payoff",
    "matrice_tematica": "matrice_tematica",
}


def voto_da_punteggio(p):
    if p >= 90:
        return "eccellente"
    if p >= 75:
        return "buono"
    if p >= 60:
        return "sufficiente"
    if p >= 40:
        return "debole"
    return "insufficiente"


def run(input_file):
    with open(input_file, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    opera = data.get("opera", "???")
    contesto = data.get("contesto", "non dichiarato")

    print(f"\n{'='*64}")
    print(f"QUALITA' NARRATIVA: {opera}")
    print(f"Contesto: {contesto}")
    print(f"{'='*64}")

    punteggi = {}   # metrica -> punteggio 0-100
    tutti_dettagli = {}

    for metrica, scorer in SCORERS.items():
        chiave = CHIAVI_YAML[metrica]
        sezione = data.get(chiave)
        if sezione is None:
            continue  # metrica non attivata: esclusa dalla media
        punteggio, dettagli = scorer(sezione)
        if punteggio is None:
            continue
        punteggi[metrica] = punteggio
        tutti_dettagli[metrica] = dettagli

    if not punteggi:
        print("\nNessuna metrica attivata nel file di input. Niente da valutare.")
        print("Usa --template per vedere il formato.")
        return 1

    # Rinormalizza i pesi sulle sole metriche presenti
    peso_totale = sum(PESI_DEFAULT[m] for m in punteggi)
    complessivo = sum(punteggi[m] * PESI_DEFAULT[m] for m in punteggi) / peso_totale

    print("\nMETRICHE ATTIVATE:")
    for metrica in SCORERS:
        if metrica not in punteggi:
            print(f"  {metrica:<18} —  (non attivata)")
            continue
        peso_eff = PESI_DEFAULT[metrica] / peso_totale
        print(f"  {metrica:<18} {punteggi[metrica]:5.1f}/100   (peso {peso_eff*100:.0f}%)")

    # Dettagli / problemi
    problemi = {m: d for m, d in tutti_dettagli.items() if d}
    if problemi:
        print("\nRILIEVI:")
        for metrica, dettagli in problemi.items():
            for d in dettagli:
                print(f"  [{metrica}] {d}")

    print(f"\n{'='*64}")
    print(f"PUNTEGGIO COMPLESSIVO: {complessivo:.1f}/100  ({voto_da_punteggio(complessivo)})")
    print(f"{'='*64}")
    print("Nota: il punteggio misura coerenza e compattezza, non l'originalità")
    print("o il gusto. Un 90 non garantisce una bella storia, ma un 40 segnala")
    print("quasi sempre una storia slegata o dispersiva.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--template":
        print(TEMPLATE)
        sys.exit(0)

    if sys.argv[1] == "--self-test":
        test = yaml.safe_load(TEMPLATE)
        assert "logline" in test and "percio_ma" in test
        # Verifica che gli scorer girino senza errori sul template
        for metrica, scorer in SCORERS.items():
            chiave = CHIAVI_YAML[metrica]
            scorer(test.get(chiave, {}))
        print("Self-test OK: template valido, tutti gli scorer eseguibili.")
        sys.exit(0)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"File non trovato: {input_file}")
        sys.exit(1)
    try:
        with open(input_file, encoding="utf-8") as f:
            yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Errore YAML nel file di input:\n  {e}")
        sys.exit(1)
    sys.exit(run(input_file))
