#!/usr/bin/env python3
"""Read-only audit of a drive against its DRIVE.md. Prints a Markdown report.

Usage: drive_audit.py <drive-root> [--depth N]

Flags: items at the root that aren't zones, folders named after agents or tools,
URL-encoded names, temp/cache folders outside Scratch, and large video files
outside Video/Working, Video/Final Renders, Video/Final Cut, Video/Library, Archive and Backups.
Nothing is moved or deleted.
"""
import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drive_config import load_config  # noqa: E402

AGENT_NAME = re.compile(r"^(claude|codex|gemini|cursor|copilot|chatgpt|openai|anthropic)(\b|[ _-]|$)", re.I)
ENCODED = re.compile(r"%[0-9A-Fa-f]{2}")
RANDOM_SUFFIX = re.compile(r"\.(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[A-Z])(?=[A-Za-z0-9]*[a-z])[A-Za-z0-9]{8}$")
TEMP_NAME = re.compile(r"^(tmp|temp|render-tmp|.*-tmp|cache|.*-cache|node-compile-cache|npm-cache|playwright-artifacts.*|__pycache__)$", re.I)
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".mxf", ".prores"}
VIDEO_OK = ("Video/Working", "Video/Final Renders", "Video/Final Cut", "Video/Library", "Archive", "Backups", "Scratch")
LARGE = 200 * 1024 * 1024


def human(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024
    return f"{size:.0f} PB"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root")
    parser.add_argument("--depth", type=int, default=4)
    args = parser.parse_args()
    root = Path(args.root).expanduser()
    config = load_config(root)
    ignore = config["ignore"]
    zones = set(config["zones"])

    stray_root, agent_named, encoded, temp_outside, big_videos, random_suffix = [], [], [], [], [], []
    for entry in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if entry.name in ignore or entry.name in config["root_files_allowed"]:
            continue
        if entry.name not in zones:
            stray_root.append(entry)

    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        depth = len(rel.parts)
        dirnames[:] = [d for d in dirnames if d not in ignore and not d.startswith(".") and not d.endswith((".fcpbundle", ".photoslibrary", ".app"))]
        in_scratch = rel.parts[:1] == ("Scratch",)
        for name in list(dirnames):
            path = Path(dirpath) / name
            if AGENT_NAME.search(name):
                agent_named.append(path)
            if ENCODED.search(name):
                encoded.append(path)
            if RANDOM_SUFFIX.search(name):
                random_suffix.append(path)
            if TEMP_NAME.match(name) and not in_scratch:
                temp_outside.append(path)
                dirnames.remove(name)
        if depth >= args.depth:
            dirnames[:] = []
        rel_text = rel.as_posix()
        if not any(rel_text == ok or rel_text.startswith(ok + "/") for ok in VIDEO_OK):
            for name in filenames:
                path = Path(dirpath) / name
                if path.suffix.lower() in VIDEO_EXT:
                    try:
                        size = path.stat().st_size
                    except OSError:
                        continue
                    if size >= LARGE:
                        big_videos.append((size, path))

    def section(title: str, items: list, note: str) -> None:
        print(f"## {title} ({len(items)})\n")
        print(note + "\n")
        for item in items[:200]:
            if isinstance(item, tuple):
                print(f"- {human(item[0])}, `{item[1]}`")
            else:
                print(f"- `{item}`")
        if len(items) > 200:
            print(f"- … and {len(items) - 200} more")
        print()

    print(f"# Drive audit: {root}\n")
    section("Not a zone at the root", stray_root, "Move each into its zone or Inbox.")
    section("Named after an agent or tool", agent_named, "Re-file the contents by brand and project.")
    section("URL-encoded names", encoded, "Usually a duplicate of a properly named folder. Compare, then merge.")
    section("Random suffixes", random_suffix, "Temporary export or build folders. Rename or move to Scratch.")
    section("Temp or cache folders outside Scratch", temp_outside, "Move to Scratch/<tool-or-project>/ or delete with approval.")
    section("Large videos outside the video zones, Archive and Backups", sorted(big_videos, reverse=True), "Working renders belong in Video/Working/<Brand>/<project>/renders/; approved finals in Video/Final Renders/<Brand>/<project>/.")


if __name__ == "__main__":
    main()
