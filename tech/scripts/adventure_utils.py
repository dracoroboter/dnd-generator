"""
adventure_utils.py — Utility condivise per gli script del progetto D&D.

Fornisce la risoluzione dei path per avventure con varianti (parent/shared_from_parent).
"""

import json
from pathlib import Path

ADVENTURES_DIR = Path(__file__).parent.parent.parent / "adventures"


def load_manifest(adventure_dir):
    """Load manifest.json from adventure directory. Returns dict or empty dict."""
    manifest_path = Path(adventure_dir) / "manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text())
    return {}


def resolve_asset_dir(adventure_dir, subdir):
    """
    Resolve asset directory, falling back to parent if declared in shared_from_parent.

    Args:
        adventure_dir: Path to the adventure directory
        subdir: subdirectory to resolve (e.g. "maps", "characters/img", "img")

    Returns:
        Path to the resolved directory (in parent if shared, else in adventure itself)
    """
    adventure_dir = Path(adventure_dir)
    manifest = load_manifest(adventure_dir)
    shared = manifest.get("shared_from_parent", [])

    if subdir in shared:
        parent_name = manifest.get("parent")
        if parent_name:
            parent_dir = adventure_dir.parent / parent_name / subdir
            if parent_dir.exists():
                return parent_dir

    local = adventure_dir / subdir
    return local


def get_parent_dir(adventure_dir):
    """Get parent adventure directory if declared, else None."""
    adventure_dir = Path(adventure_dir)
    manifest = load_manifest(adventure_dir)
    parent_name = manifest.get("parent")
    if parent_name:
        return adventure_dir.parent / parent_name
    return None


def is_variant(adventure_dir):
    """Check if adventure is a variant (has parent field)."""
    manifest = load_manifest(Path(adventure_dir))
    return "parent" in manifest
