#!/usr/bin/env python3
"""Find existing project folders that match some words, so agents reuse them.

Usage: find_project.py <drive-root> <word> [<word> ...]
Searches folder names up to four levels deep and prints matches, best first.
Read-only.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drive_config import DEFAULT_IGNORE, slugify  # noqa: E402

SKIP = DEFAULT_IGNORE | {"Scratch", "node_modules", ".git"}


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    root = Path(sys.argv[1]).expanduser()
    words = [slugify(word) for word in sys.argv[2:] if slugify(word)]
    hits = []
    for dirpath, dirnames, _ in os.walk(root):
        depth = len(Path(dirpath).relative_to(root).parts)
        dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith(".")]
        if depth >= 4:
            dirnames[:] = []
        for name in dirnames:
            slug = slugify(name)
            score = sum(1 for word in words if word in slug)
            if score:
                hits.append((score, depth, str(Path(dirpath) / name)))
    if not hits:
        print("No existing folder matches. It's safe to create a new project.")
        return
    for score, _, path in sorted(hits, key=lambda hit: (-hit[0], hit[1], hit[2]))[:40]:
        print(f"{score}/{len(words)}  {path}")


if __name__ == "__main__":
    main()
