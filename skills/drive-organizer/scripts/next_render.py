#!/usr/bin/env python3
"""Print the next unused versioned render path.

Usage: next_render.py <renders-folder> <project>-<cut> <resolution><fps> <ext>
Example: next_render.py "/Volumes/Media/Video/Working/Example-Brand/product-tour/renders" product-tour-full 2160p60 mp4
-> /Volumes/Media/Video/Working/Example-Brand/product-tour/renders/product-tour-full-v05-2160p60.mp4
Versions are shared across resolutions, so v05 means the same cut everywhere.
It also checks the matching Final Renders folder so a version number is never reused.
"""
import re
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    folder, base, spec, ext = Path(sys.argv[1]).expanduser(), sys.argv[2], sys.argv[3], sys.argv[4].lstrip(".")
    pattern = re.compile(rf"^{re.escape(base)}-v(\d+)(?:-|\.)")
    highest = 0
    folders = [folder]
    parts = folder.parts
    if "Working" in parts:
        index = parts.index("Working")
        tail = [p for p in parts[index + 1:] if p != "renders"]
        final = Path(*parts[:index], "Final Renders", *tail)
        folders += [final, final / "superseded"]
    for candidate in folders:
        if not candidate.is_dir():
            continue
        for entry in candidate.iterdir():
            match = pattern.match(entry.name)
            if match:
                highest = max(highest, int(match.group(1)))
    print(folder / f"{base}-v{highest + 1:02d}-{spec}.{ext}")


if __name__ == "__main__":
    main()
