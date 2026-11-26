---
name: drive-organizer
description: Use before reading, saving, rendering, downloading, moving or cleaning up anything on a shared storage drive. Puts every file in the right zone, brand and project, keeps working renders apart from approved finals and temp files in Scratch, and stops agents from leaving files in random folders.
metadata:
  version: "1.0.0"
---

# Drive Organizer

Several agents (Claude, Codex, Gemini and others) share one storage drive. Without a common map, each one invents folders: `Claude Media`, `Codex Media`, `Codex%20Media`, `render-tmp` at the root, finals mixed in with drafts, loose files at the top level. This skill gives every agent the same map and the same habits, so anyone can find anything later.

The core rule: **work happens in Working, approved output goes to Final Renders, and both are organized by brand and project.**

Use it any time a task touches the drive, not only for video. That includes app release media, QA evidence, screenshots, design files, downloads, backups, renders, caches and cleanup.

## The drive's map

Every drive has one map, a file named `DRIVE.md` at the drive root. It lists the zones, the brand names and the naming rules for that drive, and it wins over anything in this file.

If the drive has no `DRIVE.md`, write a proposal from [references/default-layout.md](references/default-layout.md), show it to the person, and wait for their approval before creating folders.

Some people keep their maps in a version-controlled folder instead of on the drive. If the environment variable `DRIVE_MAP_DIR` is set, the scripts read `$DRIVE_MAP_DIR/<drive-name>/DRIVE.md` (the drive's name in lowercase) before the copy on the drive. Change the map where the person keeps it.

Code checkouts do not go on a media drive. They stay on the internal disk.

## Before you write anything

1. **Read the map.** Open the drive's `DRIVE.md`. It lists the zones, the brand names and the naming rules. Follow it over anything in this file.
2. **Find the existing home.** Search the right zone for the brand and project before creating anything. Run `python3 scripts/find_project.py <drive-root> <words>` from this skill's folder. Reuse the folder you find. Never create a second folder for the same project with a different name.
3. **Pick the zone by what the file is, not by which agent made it or when.**

| The file is… | It goes in… |
|---|---|
| Anything in progress for a video: compositions, project files, source captures, audio, scripts, checks | `Video/Working/<Brand>/<project>/` |
| A working, draft or review render | `Video/Working/<Brand>/<project>/renders/` |
| An approved final: the master, its delivery copies, poster, thumbnail and captions | `Video/Final Renders/<Brand>/<project>/` |
| Reusable footage, music, voices, logos, fonts, LUTs used across projects | `Video/Library/<kind>/` |
| Final Cut libraries and their media | `Video/Final Cut/` |
| Work that isn't a video edit (release media, QA evidence, screenshots, design files, plans, research) while it's in progress | `Projects/<Brand>/<project>/working/` |
| The approved output of that work (the screenshot set that ships, the final deck) | `Projects/<Brand>/<project>/final/` |
| Photo libraries, AI image sets, product photos | `Images/<collection>/` |
| Music projects, stems, sound libraries | `Audio/<collection>/` |
| 3D scenes and engine projects | `3D/<tool>/<project>/` |
| Builds, simulator downloads, app data a tool keeps on the drive | `Apps/<tool>/` |
| Snapshots, migrations, offloads, git bundles | `Backups/<what>-<YYYY-MM-DD>/` |
| Finished or retired work kept as it is | `Archive/<Brand>/<project>/` |
| Caches, render temp, intermediate segments and frames, browser test artifacts | `Scratch/<tool-or-project>/` |
| Something you can't place | `Inbox/`, and tell the person what it is and where you think it belongs |

## Naming

- **Brands** use the exact spelling in `DRIVE.md` (for example `Example-Brand`, `Side-Project`). Client work goes under `Clients/<Name>`.
- **Project folders** are lowercase kebab-case slugs that stay the same for the life of the project: `product-tour`, `mac-tutorial`, `app-store-screenshots-2-4`. Put dates inside `PROJECT.md`, not in the folder name, unless the project really is a one-day event.
- **Renders** are `<project>-<cut>-v<NN>-<resolution><fps>.<ext>`, for example `product-tour-full-v04-2160p60.mp4`. Bump the version for every new export. Never overwrite an export someone may have reviewed. Get the next name with `python3 scripts/next_render.py <project-renders-folder> <project>-<cut> <resolution><fps> <ext>`.
- Never name a folder after an agent or tool (`Claude Media`, `Codex`, `Gemini output`). Never use URL-encoded names (`%20`), random suffixes (`.x7Qk2mPa`) or vague names (`new`, `final2`, `stuff`, `tmp` outside `Scratch`).
- Never put files at the drive root. Only the zone folders live there.

## Starting a project

Create it with `python3 scripts/new_project.py <drive-root> <zone> <Brand> <project-slug> "<one-line purpose>"`. Zones are `video` or `work`. For video it creates `Video/Working/<Brand>/<slug>/` (with a `renders/` folder inside) and `Video/Final Renders/<Brand>/<slug>/`. For other work it creates `Projects/<Brand>/<slug>/working/` and `final/`. It writes a `PROJECT.md` and refuses to create a duplicate of an existing project.

Keep `PROJECT.md` current. It records what the project is, its status, where the source and renders are, the latest approved version, and the agent and date of each major change. It's how the next agent picks up the work.

## While you work

- Point tools at the right place from the start. Send renders to the project's `Video/Working/<Brand>/<project>/renders/` folder and caches to `Scratch/<project>/` (for example `TMPDIR`, `--cache-dir`, a framework's output flag). Don't let a tool default to the root, your home folder or a folder named after you.
- Intermediate files (segments, frames, proxies, logs) go in `Scratch/<project>/`. Delete your own Scratch files when the task is verified. Never delete someone else's.
- **Promote a final only when the person approves it.** Move the approved render (and its delivery copies, poster and captions) from `Working/.../renders/` to `Final Renders/<Brand>/<project>/`, keeping the same file name, and record it in `PROJECT.md`. Final Renders only ever holds approved versions. If a newer version is approved, move the old final into `Final Renders/<Brand>/<project>/superseded/`.

## Moving or cleaning up existing files

Reorganizing is allowed. Breaking things isn't.

1. Run `python3 scripts/drive_audit.py <drive-root>` first. It's read-only and lists files at the root, agent-named and URL-encoded folders, temp folders outside `Scratch`, and large videos outside the working, final, library, archive and backup areas.
2. Write a move plan (old path → new path) and show it to the person before moving anything they didn't ask you to move.
3. Before moving a folder, check for things that point into it: repo scripts, website media paths, app build scripts, review pages, notes. Search the person's code folders and notes for the old path. Update those references in the same change, or leave a `MOVED.md` in the old location with the new path.
4. Move with `mv` on the same drive, which keeps files intact. Don't copy-then-delete, and never delete originals unless the person asked for that and approved the exact list.
5. Merge duplicates only when they're byte-identical (compare hashes). Otherwise keep both and note it in `PROJECT.md`.
6. Log what moved in the map's **Move log** section: the date, the agent, and old → new. For a large reorganization, keep a TSV move log (time, old path, new path) next to the map, so an old path in a note or script can be looked up later.

## Finish

Report every file you created or moved with its **full absolute path** (for example `/Volumes/Media/Video/Final Renders/Example-Brand/product-tour/product-tour-full-v04-2160p60.mp4`), never a relative path or a description. Say what's waiting for approval and which Scratch files you cleaned up.
