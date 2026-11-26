#!/usr/bin/env python3
"""Create a project folder in the right zone, with a PROJECT.md.

Usage: new_project.py <drive-root> <video|work> <Brand> <project-slug> "<one-line purpose>"

video -> Video/Working/<Brand>/<slug>/ (with renders/) and Video/Final Renders/<Brand>/<slug>/
work  -> Projects/<Brand>/<slug>/working/ and Projects/<Brand>/<slug>/final/
Refuses to run if a folder with the same slug already exists under Projects,
Video/Working, Video/Final Renders or Archive.
"""
import datetime
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drive_config import load_config, slugify  # noqa: E402


def existing_matches(root: Path, slug: str) -> list[str]:
    found = []
    for base in (root / "Projects", root / "Video" / "Working", root / "Video" / "Final Renders", root / "Archive"):
        if not base.is_dir():
            continue
        for dirpath, dirnames, _ in os.walk(base):
            if len(Path(dirpath).relative_to(base).parts) >= 3:
                dirnames[:] = []
            for name in dirnames:
                if slugify(name) == slug:
                    found.append(str(Path(dirpath) / name))
    return found


def main() -> None:
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    root, zone, brand, raw_slug, purpose = Path(sys.argv[1]).expanduser(), *sys.argv[2:]
    config = load_config(root)
    brand_root = brand.split("/")[0]
    if config["brands"] and brand_root not in config["brands"]:
        sys.exit(f"Unknown brand '{brand}'. Use one listed in DRIVE.md: {', '.join(config['brands'])}. "
                 "Add a new brand to DRIVE.md first if the person agrees.")
    slug = slugify(raw_slug)
    if slug != raw_slug:
        print(f"Using slug '{slug}'.")
    duplicates = existing_matches(root, slug)
    if duplicates:
        sys.exit("A project with this name already exists. Reuse it:\n  " + "\n  ".join(duplicates))

    if zone == "video":
        project = root / "Video" / "Working" / brand / slug
        working_renders = project / "renders"
        final = root / "Video" / "Final Renders" / brand / slug
        made = [project, working_renders, final]
    elif zone == "work":
        project = root / "Projects" / brand / slug
        working_renders = project / "working"
        final = project / "final"
        made = [project, working_renders, final]
    else:
        sys.exit("Zone must be 'video' or 'work'.")

    for folder in made:
        folder.mkdir(parents=True, exist_ok=folder is not project)
    today = datetime.date.today().isoformat()
    lines = [
        f"# {slug}",
        "",
        f"- **Brand:** {brand}",
        f"- **Purpose:** {purpose}",
        "- **Status:** active",
        f"- **Created:** {today}",
        f"- **Working files:** `{project}`",
        f"- **Working renders:** `{working_renders}`",
        f"- **Approved finals:** `{final}`",
    ]
    lines += [
        "- **Latest approved version:** none yet",
        "- **Source code:** none, or the path of the repository on the internal disk",
        "",
        "## Log",
        "",
        f"- {today}: project created.",
        "",
    ]
    (project / "PROJECT.md").write_text("\n".join(lines), encoding="utf-8")
    for folder in made:
        print(f"Created {folder}")


if __name__ == "__main__":
    main()
