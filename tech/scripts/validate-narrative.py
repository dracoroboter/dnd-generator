#!/usr/bin/env python3
"""
validate-narrative.py — Validazione automatica di un'analisi narrativa
contro il vocabolario e la grammatica.

Uso:
  python3 tech/scripts/validate-narrative.py tech/data/references/analyses/nome-opera.yaml

Produce un report con metriche oggettive e warning.
"""
import yaml
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
STEREO_FILE = os.path.join(PROJECT_ROOT, "tech/data/references/narrative-stereotypes.yaml")
GRAMMAR_FILE = os.path.join(PROJECT_ROOT, "tech/data/references/narrative-grammar.yaml")


def load_vocabolario(filepath):
    """Load stereotypes and build lookup structures."""
    with open(filepath, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    names = set()
    by_type = {}
    prereqs = {}  # nome -> [prerequisiti]
    
    for s in data["stereotipi"]:
        nome = s["nome"]
        names.add(nome)
        # Also add short name (before parenthesis)
        short = nome.split(" (")[0]
        names.add(short)
        
        tipo = s["tipo"]
        by_type.setdefault(tipo, []).append(nome)
        
        if "puo_aver_bisogno_di" in s:
            prereqs[nome] = s["puo_aver_bisogno_di"]
            prereqs[short] = s["puo_aver_bisogno_di"]
    
    return names, by_type, prereqs


def load_grammatica(filepath):
    """Load grammar rules."""
    with open(filepath, encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_name(name, known_names):
    """Try to match a name from the analysis to a known stereotype."""
    if not isinstance(name, str):
        return None
    if name in known_names:
        return name
    # Try short match
    short = name.split(" (")[0]
    if short in known_names:
        return short
    # Try partial match
    for known in known_names:
        if name in known or known.startswith(name):
            return known
    return None


def validate_analysis(analysis_file, known_names, by_type, prereqs, grammar):
    """Validate an analysis file and produce metrics."""
    with open(analysis_file, encoding="utf-8") as f:
        analysis = yaml.safe_load(f)
    
    report = {
        "file": analysis_file,
        "opera": analysis.get("opera", {}).get("titolo", "???"),
        "metriche": {},
        "errori": [],
        "warning": [],
        "info": [],
    }
    
    # --- Collect all stereotypes used in the analysis ---
    all_used = []  # in order of appearance
    archi = analysis.get("struttura", {}).get("archi", [])
    
    for arco in archi:
        for field in ["situazioni", "personaggi", "tecniche", "relazioni"]:
            for nome in arco.get(field, []):
                if isinstance(nome, str):
                    all_used.append(nome)
    
    # --- METRICA 1: Copertura del vocabolario ---
    resolved = 0
    unresolved = []
    for nome in all_used:
        if resolve_name(nome, known_names):
            resolved += 1
        else:
            unresolved.append(nome)
    
    total = len(all_used) if all_used else 1
    copertura = resolved / total * 100
    report["metriche"]["copertura_vocabolario"] = f"{copertura:.0f}% ({resolved}/{total})"
    
    if unresolved:
        report["errori"].append(f"Stereotipi non trovati nel vocabolario: {unresolved}")
    
    if copertura >= 80:
        report["info"].append(f"✅ Copertura OK ({copertura:.0f}%)")
    else:
        report["errori"].append(f"❌ Copertura insufficiente ({copertura:.0f}% < 80%)")
    
    # --- METRICA 2: Prerequisiti soddisfatti ---
    seen_so_far = set()
    prereq_ok = 0
    prereq_fail = 0
    prereq_details = []
    
    for nome in all_used:
        resolved_name = resolve_name(nome, known_names)
        if resolved_name and resolved_name in prereqs:
            for req in prereqs[resolved_name]:
                # Check if prerequisite appeared earlier
                req_resolved = resolve_name(req, known_names)
                if req_resolved and req_resolved in seen_so_far:
                    prereq_ok += 1
                elif req in seen_so_far or any(req in s for s in seen_so_far):
                    prereq_ok += 1
                else:
                    prereq_fail += 1
                    prereq_details.append(f"{nome} richiede '{req}' ma non appare prima")
        seen_so_far.add(nome)
        if resolved_name:
            seen_so_far.add(resolved_name)
    
    total_prereqs = prereq_ok + prereq_fail
    if total_prereqs > 0:
        prereq_pct = prereq_ok / total_prereqs * 100
        report["metriche"]["prerequisiti_soddisfatti"] = f"{prereq_pct:.0f}% ({prereq_ok}/{total_prereqs})"
        if prereq_fail > 0:
            report["warning"].extend(prereq_details)
    else:
        report["metriche"]["prerequisiti_soddisfatti"] = "N/A (nessun prerequisito verificabile)"
    
    # --- METRICA 3: Regole di sequenza ---
    seq_rules = grammar.get("regole_sequenza", [])
    seq_ok = 0
    seq_fail = 0
    seq_details = []
    
    # Build position map
    positions = {}
    for i, nome in enumerate(all_used):
        if nome not in positions:
            positions[nome] = i
        resolved_name = resolve_name(nome, known_names)
        if resolved_name and resolved_name not in positions:
            positions[resolved_name] = i
    
    for rule in seq_rules:
        prima = rule["prima"]
        dopo_list = rule["dopo"]
        prima_pos = None
        
        # Find position of "prima"
        for key, pos in positions.items():
            if prima in key or key.startswith(prima):
                prima_pos = pos
                break
        
        if prima_pos is None:
            continue  # Rule not applicable (element not in this analysis)
        
        for dopo in dopo_list:
            dopo_pos = None
            for key, pos in positions.items():
                if dopo in key or key.startswith(dopo):
                    dopo_pos = pos
                    break
            
            if dopo_pos is None:
                continue  # Element not in this analysis
            
            if prima_pos <= dopo_pos:
                seq_ok += 1
            else:
                seq_fail += 1
                seq_details.append(f"'{dopo}' appare PRIMA di '{prima}' (viola regola)")
    
    total_seq = seq_ok + seq_fail
    if total_seq > 0:
        seq_pct = seq_ok / total_seq * 100
        report["metriche"]["regole_sequenza"] = f"{seq_pct:.0f}% ({seq_ok}/{total_seq})"
        if seq_fail > 0:
            report["warning"].extend(seq_details)
    else:
        report["metriche"]["regole_sequenza"] = "N/A (nessuna regola applicabile)"
    
    # --- METRICA 4: Densità (stereotipi per arco) ---
    if archi:
        densities = []
        for arco in archi:
            count = sum(len(arco.get(f, [])) for f in ["situazioni", "personaggi", "tecniche", "relazioni"])
            densities.append(count)
        avg_density = sum(densities) / len(densities)
        report["metriche"]["densita_media_per_arco"] = f"{avg_density:.1f} stereotipi/arco"
        
        if avg_density < 3:
            report["warning"].append(f"Densità bassa ({avg_density:.1f}) — archi poco dettagliati")
    
    # --- METRICA 5: Varietà dei tipi ---
    types_used = {"situazione": 0, "personaggio": 0, "tecnica": 0, "relazione": 0, "plot": 0}
    for arco in archi:
        types_used["situazione"] += len(arco.get("situazioni", []))
        types_used["personaggio"] += len(arco.get("personaggi", []))
        types_used["tecnica"] += len(arco.get("tecniche", []))
    
    report["metriche"]["varieta_tipi"] = types_used
    if types_used["personaggio"] == 0:
        report["warning"].append("Nessun personaggio-archetipo identificato")
    if types_used["tecnica"] == 0:
        report["warning"].append("Nessuna tecnica narrativa identificata")
    
    # --- METRICA 6: Ripetizioni eccessive ---
    from collections import Counter
    counts = Counter(all_used)
    repeated = {k: v for k, v in counts.items() if v >= 3}
    if repeated:
        report["warning"].append(f"Stereotipi usati 3+ volte (possibile monotonia): {repeated}")
    report["metriche"]["stereotipi_unici"] = f"{len(counts)} unici su {len(all_used)} totali"
    
    # --- METRICA 7: Sovversioni documentate ---
    sovversioni = analysis.get("sovversioni", [])
    report["metriche"]["sovversioni_documentate"] = len(sovversioni)
    
    return report


def print_report(report):
    """Pretty-print the validation report."""
    print(f"\n{'='*60}")
    print(f"VALIDAZIONE: {report['opera']}")
    print(f"File: {report['file']}")
    print(f"{'='*60}")
    
    print(f"\n📊 METRICHE:")
    for k, v in report["metriche"].items():
        print(f"  {k}: {v}")
    
    if report["errori"]:
        print(f"\n❌ ERRORI ({len(report['errori'])}):")
        for e in report["errori"]:
            print(f"  • {e}")
    
    if report["warning"]:
        print(f"\n⚠️  WARNING ({len(report['warning'])}):")
        for w in report["warning"]:
            print(f"  • {w}")
    
    if report["info"]:
        print(f"\n✅ INFO:")
        for i in report["info"]:
            print(f"  • {i}")
    
    # Overall score
    has_errors = len(report["errori"]) > 0
    print(f"\n{'='*60}")
    if has_errors:
        print("❌ VALIDAZIONE FALLITA — servono correzioni")
    else:
        print("✅ VALIDAZIONE OK — l'analisi è coerente con vocabolario e grammatica")
    print(f"{'='*60}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 validate-narrative.py <file-analisi.yaml>")
        print("     python3 validate-narrative.py --self-test")
        sys.exit(1)
    
    # Load vocabulary and grammar
    known_names, by_type, prereqs = load_vocabolario(STEREO_FILE)
    grammar = load_grammatica(GRAMMAR_FILE)
    
    if sys.argv[1] == "--self-test":
        print(f"Vocabolario caricato: {len(known_names)} nomi noti")
        print(f"Prerequisiti definiti: {len(prereqs)} stereotipi con prereq")
        print(f"Regole sequenza: {len(grammar.get('regole_sequenza', []))}")
        print(f"Regole casting: {len(grammar.get('regole_casting', []))}")
        print("Self-test OK")
        sys.exit(0)
    
    if sys.argv[1] == "--check-all":
        # Validate all YAML files in the narrative system
        files_to_check = [
            STEREO_FILE,
            GRAMMAR_FILE,
            os.path.join(PROJECT_ROOT, "tech/data/references/dm-conduct-principles.yaml"),
        ]
        # Also check all analysis files
        analyses_dir = os.path.join(PROJECT_ROOT, "tech/data/references/analyses")
        if os.path.isdir(analyses_dir):
            for fname in sorted(os.listdir(analyses_dir)):
                if fname.endswith(".yaml"):
                    files_to_check.append(os.path.join(analyses_dir, fname))
        
        all_ok = True
        for fpath in files_to_check:
            if not os.path.exists(fpath):
                continue
            try:
                with open(fpath, encoding="utf-8") as f:
                    yaml.safe_load(f)
                print(f"  ✅ {os.path.basename(fpath)}")
            except yaml.YAMLError as e:
                print(f"  ❌ {os.path.basename(fpath)}: {e}")
                all_ok = False
        
        if all_ok:
            print(f"\n✅ Tutti i {len(files_to_check)} file YAML sono formalmente corretti")
        else:
            print(f"\n❌ Alcuni file hanno errori YAML")
            sys.exit(1)
        sys.exit(0)
    
    analysis_file = sys.argv[1]
    if not os.path.exists(analysis_file):
        print(f"File non trovato: {analysis_file}")
        sys.exit(1)
    
    # Step 0: Validate YAML syntax
    try:
        with open(analysis_file, encoding="utf-8") as f:
            yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"\n❌ ERRORE YAML FORMALE nel file {analysis_file}:")
        print(f"   {e}")
        print(f"\n   Il file non è YAML valido. Correggi la sintassi prima di validare il contenuto.")
        sys.exit(1)
    
    report = validate_analysis(analysis_file, known_names, by_type, prereqs, grammar)
    print_report(report)
