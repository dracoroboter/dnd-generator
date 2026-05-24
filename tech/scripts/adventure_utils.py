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

    If the variant has its own local directory for a shared subdir, both are valid:
    scripts should check the local dir first, then fall back to parent.
    Use resolve_asset_dirs() to get both paths in priority order.

    Args:
        adventure_dir: Path to the adventure directory
        subdir: subdirectory to resolve (e.g. "maps", "characters/img", "img")

    Returns:
        Path to the resolved directory (parent if shared and no local override, else local)
    """
    adventure_dir = Path(adventure_dir)
    manifest = load_manifest(adventure_dir)
    shared = manifest.get("shared_from_parent", [])

    # If subdir is shared, check if local override exists
    if subdir in shared:
        local = adventure_dir / subdir
        parent_name = manifest.get("parent")
        if parent_name:
            parent_dir = adventure_dir.parent / parent_name / subdir
            # If local exists (override), return local; scripts needing both use resolve_asset_dirs()
            if local.exists():
                return local
            if parent_dir.exists():
                return parent_dir

    return adventure_dir / subdir


def resolve_asset_dirs(adventure_dir, subdir):
    """
    Resolve asset directories with fallback: returns list of paths to check in priority order.
    For variants with partial override: [local, parent]. For normal adventures: [local].

    Args:
        adventure_dir: Path to the adventure directory
        subdir: subdirectory to resolve

    Returns:
        List of Paths in priority order (first found wins for individual files)
    """
    adventure_dir = Path(adventure_dir)
    manifest = load_manifest(adventure_dir)
    shared = manifest.get("shared_from_parent", [])
    dirs = []

    local = adventure_dir / subdir
    if local.exists():
        dirs.append(local)

    if subdir in shared:
        parent_name = manifest.get("parent")
        if parent_name:
            parent_dir = adventure_dir.parent / parent_name / subdir
            if parent_dir.exists():
                dirs.append(parent_dir)

    if not dirs:
        dirs.append(local)  # fallback to local even if doesn't exist

    return dirs


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
