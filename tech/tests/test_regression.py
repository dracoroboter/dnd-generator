#!/usr/bin/env python3
"""
test_regression.py — Test di non regressione per la pipeline D&D.

Verifica che gli script producano output corretto.
Supporta sia la struttura vecchia che la nuova (multilingua con it/en/).
Eseguire PRIMA e DOPO ogni milestone del refactoring multilingua.

Uso:
    python3 tech/tests/test_regression.py                    # tutti i test
    python3 tech/tests/test_regression.py -k test_md_to_xml  # singolo test
"""

import subprocess
import sys
import os
import re
import json
import tempfile
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ADVENTURES_DIR = PROJECT_ROOT / "adventures"
TECH_DIR = PROJECT_ROOT / "tech"

# Script paths
MD_TO_FC = TECH_DIR / "fightclub" / "md-to-fightclub.py"
GENERATE_SB = TECH_DIR / "fightclub" / "generate-statblocks.py"
CREATE_PDF = TECH_DIR / "create-pdf-adventure" / "create-pdf-adventure.py"
CHECK_ADV = TECH_DIR / "scripts" / "check-adventure.py"

ADVENTURES = ["FuoriDaHellfire", "LAnelloDelConte", "LoScettroDityr"]
PILOT = "FuoriDaHellfire"

# ── structure helpers ────────────────────────────────────────────────────

def is_multilingual(adventure):
    """Check if adventure uses new multilingual structure."""
    return (ADVENTURES_DIR / adventure / "manifest.json").exists()

def get_lang_dir(adventure, lang="it"):
    """Get the base directory for language-specific content."""
    if is_multilingual(adventure):
        return ADVENTURES_DIR / adventure / lang
    return ADVENTURES_DIR / adventure

def find_npc_md(adventure, lang="it"):
    """Find NPC/MON markdown files for an adventure."""
    base = get_lang_dir(adventure, lang)
    md_dir = base / "characters" / "markdown"
    if not md_dir.exists():
        return []
    return sorted(md_dir.glob("NPC_*.md")) + sorted(md_dir.glob("MON_*.md"))

def find_statblock_dir(adventure, lang="it"):
    """Find statblock directory."""
    return get_lang_dir(adventure, lang) / "characters" / "statblock"

def find_fightclub_dir(adventure, lang="it"):
    """Find fightclub directory."""
    return get_lang_dir(adventure, lang) / "characters" / "fightclub"

def find_main_md(adventure, lang="it"):
    """Find the main adventure .md file."""
    return get_lang_dir(adventure, lang) / f"{adventure}.md"

def find_modules(adventure, lang="it"):
    """Find module directories."""
    base = get_lang_dir(adventure, lang)
    return sorted([d for d in base.iterdir() if d.is_dir() and re.match(r'\d+_', d.name)])

# ── helpers ──────────────────────────────────────────────────────────────

def run(cmd, **kwargs):
    return subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(PROJECT_ROOT), **kwargs)

# ── test results tracking ────────────────────────────────────────────────

PASSED = []
FAILED = []

def test(name):
    def decorator(func):
        func._test_name = name
        return func
    return decorator

def run_test(func):
    name = getattr(func, '_test_name', func.__name__)
    try:
        func()
        PASSED.append(name)
        print(f"  ✓ {name}")
    except AssertionError as e:
        FAILED.append((name, str(e)))
        print(f"  ✗ {name}: {e}")
    except Exception as e:
        FAILED.append((name, f"EXCEPTION: {e}"))
        print(f"  ✗ {name}: EXCEPTION: {e}")

# ── tests: structure ─────────────────────────────────────────────────────

@test("Adventures directory exists")
def test_adventures_dir():
    assert ADVENTURES_DIR.exists()

@test("All adventures exist")
def test_adventures_exist():
    for adv in ADVENTURES:
        assert (ADVENTURES_DIR / adv).is_dir(), f"{adv} not found"

@test("Scripts exist")
def test_scripts_exist():
    for script in [MD_TO_FC, GENERATE_SB, CREATE_PDF, CHECK_ADV]:
        assert script.exists(), f"{script} not found"

@test("FuoriDaHellfire has expected structure")
def test_pilot_structure():
    adv_dir = ADVENTURES_DIR / PILOT
    assert (adv_dir / "README.md").exists()
    assert (adv_dir / "AdventureBook.md").exists()
    assert (adv_dir / "PlanBook.md").exists()
    assert find_main_md(PILOT).exists(), f"Main .md not found"
    md_dir = get_lang_dir(PILOT) / "characters" / "markdown"
    assert md_dir.is_dir(), f"characters/markdown not found at {md_dir}"
    fc_dir = find_fightclub_dir(PILOT)
    assert fc_dir.is_dir(), f"characters/fightclub not found at {fc_dir}"
    sb_dir = find_statblock_dir(PILOT)
    assert sb_dir.is_dir(), f"characters/statblock not found at {sb_dir}"

@test("FuoriDaHellfire has NPC/MON markdown files")
def test_pilot_npcs():
    npcs = find_npc_md(PILOT)
    assert len(npcs) >= 7, f"Expected >=7 NPC/MON, found {len(npcs)}"

@test("FuoriDaHellfire has modules")
def test_pilot_modules():
    modules = find_modules(PILOT)
    assert len(modules) == 2, f"Expected 2 modules, found {len(modules)}"

@test("Multilingual adventures have manifest.json")
def test_manifest():
    for adv in ADVENTURES:
        if is_multilingual(adv):
            manifest_path = ADVENTURES_DIR / adv / "manifest.json"
            data = json.loads(manifest_path.read_text())
            assert "default_lang" in data, f"{adv}: manifest missing default_lang"
            assert "languages" in data, f"{adv}: manifest missing languages"

# ── tests: md-to-fightclub ──────────────────────────────────────────────

@test("md-to-fightclub: Korex MD → XML")
def test_md_to_xml_korex():
    npcs = find_npc_md(PILOT)
    korex = [f for f in npcs if "Korex" in f.name]
    assert korex, "NPC_Korex.md not found"
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        r = run(["python3", str(MD_TO_FC), str(korex[0]), "-o", tmp_path])
        assert r.returncode == 0, f"Exit {r.returncode}: {r.stderr}"
        xml = Path(tmp_path).read_text()
        assert "<monster>" in xml
        assert "Korex" in xml
    finally:
        os.unlink(tmp_path)

@test("md-to-fightclub: all FuoriDaHellfire NPCs convert")
def test_md_to_xml_all_pilot():
    for md in find_npc_md(PILOT):
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            r = run(["python3", str(MD_TO_FC), str(md), "-o", tmp_path])
            assert r.returncode == 0, f"{md.name}: exit {r.returncode}: {r.stderr}"
            xml = Path(tmp_path).read_text()
            assert "<monster>" in xml, f"{md.name}: no <monster> tag"
        finally:
            os.unlink(tmp_path)

@test("md-to-fightclub: XML contains expected fields")
def test_md_to_xml_fields():
    korex = [f for f in find_npc_md(PILOT) if "Korex" in f.name][0]
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        run(["python3", str(MD_TO_FC), str(korex), "-o", tmp_path])
        xml = Path(tmp_path).read_text()
        for tag in ["name", "size", "type", "alignment", "ac", "hp", "speed",
                     "str", "dex", "con", "int", "wis", "cha", "cr"]:
            assert f"<{tag}>" in xml, f"Missing <{tag}>"
    finally:
        os.unlink(tmp_path)

# ── tests: generate-statblocks ──────────────────────────────────────────

@test("generate-statblocks: FuoriDaHellfire single NPC (no-image)")
def test_generate_sb_single():
    r = run(["python3", str(GENERATE_SB), PILOT, "NPC_Korex", "--no-image"])
    assert r.returncode == 0, f"Exit {r.returncode}: {r.stderr}\n{r.stdout}"
    fc = find_fightclub_dir(PILOT) / "NPC_Korex.xml"
    sb_pdf = find_statblock_dir(PILOT) / "NPC_Korex.pdf"
    sb_png = find_statblock_dir(PILOT) / "NPC_Korex.png"
    assert fc.exists(), f"NPC_Korex.xml not at {fc}"
    assert sb_pdf.exists(), f"NPC_Korex.pdf not at {sb_pdf}"
    assert sb_png.exists(), f"NPC_Korex.png not at {sb_png}"

@test("generate-statblocks: compendium XML generated")
def test_generate_sb_compendium():
    r = run(["python3", str(GENERATE_SB), PILOT, "--no-image"])
    assert r.returncode == 0, f"Exit {r.returncode}: {r.stderr}\n{r.stdout}"
    comp = find_fightclub_dir(PILOT) / f"{PILOT}_Compendium.xml"
    assert comp.exists(), f"Compendium not at {comp}"
    xml = comp.read_text()
    assert "<compendium" in xml
    assert xml.count("<monster>") >= 7, f"Expected >=7 monsters"

# ── tests: check-adventure ──────────────────────────────────────────────

@test("check-adventure: FuoriDaHellfire passes")
def test_check_adventure_pilot():
    r = run(["python3", str(CHECK_ADV), PILOT])
    assert r.returncode == 0, f"Exit {r.returncode}:\n{r.stdout}"

@test("check-adventure: all adventures run without crash")
def test_check_adventure_all():
    expected_failures = {"LAnelloDelConte"}
    for adv in ADVENTURES:
        r = run(["python3", str(CHECK_ADV), adv])
        if adv in expected_failures:
            assert r.returncode in (0, 1), f"{adv}: unexpected exit {r.returncode}:\n{r.stderr}"
        else:
            assert r.returncode == 0, f"{adv}: exit {r.returncode}:\n{r.stdout}"

# ── tests: create-pdf-adventure (HTML only) ─────────────────────────────

@test("create-pdf-adventure: FuoriDaHellfire HTML build")
def test_create_pdf_html():
    sys.path.insert(0, str(CREATE_PDF.parent))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("create_pdf", str(CREATE_PDF))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        adv_dir = ADVENTURES_DIR / PILOT
        html = mod.build_html(PILOT, adv_dir, raw_cover=True, use_lowres=False)
        assert "<html>" in html
        assert "Fuori Da Hellfire" in html or "Fuori da Hellfire" in html or PILOT in html
        assert "statblock-page" in html
    finally:
        sys.path.pop(0)

# ── main ─────────────────────────────────────────────────────────────────

def collect_tests():
    tests = []
    for name, obj in sorted(globals().items()):
        if callable(obj) and hasattr(obj, '_test_name'):
            tests.append(obj)
    return tests

def main():
    filter_pattern = None
    if "-k" in sys.argv:
        idx = sys.argv.index("-k")
        if idx + 1 < len(sys.argv):
            filter_pattern = sys.argv[idx + 1]

    tests = collect_tests()
    if filter_pattern:
        tests = [t for t in tests if filter_pattern in t.__name__ or filter_pattern in t._test_name]

    print(f"\n=== Test di non regressione — {len(tests)} test ===\n")
    for t in tests:
        run_test(t)

    print(f"\n{'='*50}")
    print(f"Passati: {len(PASSED)}/{len(PASSED)+len(FAILED)}")
    if FAILED:
        print(f"\nFALLITI ({len(FAILED)}):")
        for name, err in FAILED:
            print(f"  ✗ {name}: {err}")
        sys.exit(1)
    else:
        print("✓ Tutti i test passati.")

if __name__ == "__main__":
    main()
