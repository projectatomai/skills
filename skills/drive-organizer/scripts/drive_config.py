"""Shared helpers: read the drive-config block from a drive's DRIVE.md."""
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_IGNORE = {
    ".DS_Store", ".Spotlight-V100", ".Trashes", ".fseventsd", ".TemporaryItems",
    ".DocumentRevisions-V100", ".localized", ".VolumeIcon.icns",
}


def find_manifest(root: Path) -> Path:
    """The map is DRIVE.md at the drive root.

    To keep maps in version control instead, set DRIVE_MAP_DIR to a folder that
    holds <drive-name>/DRIVE.md (the drive name in lowercase). That copy wins.
    """
    candidates = []
    map_dir = os.environ.get("DRIVE_MAP_DIR")
    if map_dir:
        candidates.append(Path(map_dir).expanduser() / root.name.lower() / "DRIVE.md")
    candidates.append(root / "DRIVE.md")
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    sys.exit(f"No map for {root}. Expected {candidates[-1]}. "
             "Propose one from references/default-layout.md first.")


def load_config(root: Path) -> dict:
    manifest = find_manifest(root)
    text = manifest.read_text(encoding="utf-8")
    match = re.search(r"```drive-config\s*\n(.*?)\n```", text, re.S)
    if not match:
        sys.exit(f"{manifest} has no ```drive-config block.")
    try:
        config = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        sys.exit(f"The drive-config block in {manifest} isn't valid JSON: {error}")
    config.setdefault("zones", {})
    config.setdefault("video_subzones", ["Working", "Final Renders", "Library", "Final Cut"])
    config.setdefault("brands", [])
    config.setdefault("root_files_allowed", [])
    config["ignore"] = set(config.get("ignore", [])) | DEFAULT_IGNORE
    return config


def slugify(text: str) -> str:
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")
