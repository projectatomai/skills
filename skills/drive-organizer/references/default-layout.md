# Default drive layout

Use this as the starting point for a drive that has no `DRIVE.md`. Save it as `DRIVE.md` at the drive root (or where the person keeps their drive maps), replace the brand list with the person's own brands, and get their approval before creating folders.

The `drive-config` block at the end is read by the scripts in this skill. Keep it valid JSON.

---

# DRIVE.md: map of this drive

Every agent and person who saves files here follows this map. Organize by **what the file is**, then **brand**, then **project**. Never by agent, tool or date. Work happens in Working; only approved output goes to Final Renders (or a project's `final/`).

```
<drive>/
├── DRIVE.md                       this map
├── Inbox/                         unsorted arrivals; triage them, don't work in here
├── Projects/<Brand>/<project>/    non-video work: release media, QA, screenshots, design, plans, research
│   ├── working/                     in progress
│   └── final/                       approved output only
├── Video/
│   ├── Working/<Brand>/<project>/        everything in progress, plus renders/ for working and review renders
│   ├── Final Renders/<Brand>/<project>/  approved finals only: masters, delivery copies, posters, captions
│   ├── Library/<kind>/                   reusable footage, music, voices, logos, fonts, LUTs
│   └── Final Cut/                        Final Cut libraries and media
├── Images/<collection>/           photo libraries, AI image sets, product photos
├── Audio/<collection>/            music projects, stems, sound libraries
├── 3D/<tool>/<project>/           3D scenes, engine projects
├── Apps/<tool>/                   builds, simulator downloads, app data kept on the drive
├── Backups/<what>-<YYYY-MM-DD>/   snapshots, migrations, offloads, git bundles
├── Archive/<Brand>/<project>/     finished or retired work, kept as is
└── Scratch/<tool-or-project>/     caches and temp; safe to delete when no task is running
```

## Brands

`Example-Brand`, `Personal`, `Clients/<Name>`. Use these spellings exactly.

## Rules

- No files at the root. No folders named after an agent or tool. No `%20` or random suffixes.
- Project folders are stable kebab-case slugs with a `PROJECT.md` inside.
- Renders: `<project>-<cut>-v<NN>-<resolution><fps>.<ext>`. Never overwrite a reviewed export.
- Temp and intermediate files go in `Scratch/`. Clean up your own when done.
- Code checkouts don't live on this drive.

## Move log

| Date | Agent | Old path | New path |
|---|---|---|---|

```drive-config
{
  "zones": {
    "Inbox": "Unsorted arrivals",
    "Projects": "Non-video work by brand and project",
    "Video": "Video projects, renders, library, Final Cut",
    "Images": "Image collections",
    "Audio": "Audio collections",
    "3D": "3D and engine projects",
    "Apps": "Builds and app data",
    "Backups": "Dated snapshots",
    "Archive": "Finished work",
    "Scratch": "Caches and temp"
  },
  "video_subzones": ["Working", "Final Renders", "Library", "Final Cut"],
  "brands": ["Example-Brand", "Personal", "Clients"],
  "root_files_allowed": ["DRIVE.md"],
  "ignore": [".DS_Store", ".Spotlight-V100", ".Trashes", ".fseventsd", ".TemporaryItems", ".DocumentRevisions-V100", ".localized", ".VolumeIcon.icns"]
}
```
