# Local copies and moodboard recovery

Keep local copies of the assets this workflow handles, organized by moodboard, so the project does not depend on one online account. This does not authorize new generation, animation, GPU work, schedules or downloading unrelated account content.

## Layout

Ask the person where media should live and record it in `direction.md`. A workable layout:

```
<media folder>/
  favorites/               originals of favorites and an identity ledger
  moodboards/
    <board name>/
      manifest.json        board name, link, id, ordered members
      references/          files needed to rebuild the board
      generated/           outputs made with this board
      favorites/
```

Keep earlier membership snapshots when a board is renamed, merged or changed. Do not delete local files because an online item disappeared.

## What to save

- The original supplied videos and stills.
- Every approved cut frame.
- Each board's reference images, including ones the person added.
- The original outputs of each approved image batch.

Copy an existing verified local original instead of downloading it again.

For each board, record: its name, link and id, the profile code when shown, the ordered member list, each item's address, the original job id and image index or local source, the local file, its SHA-256, dimensions, and when it was saved and verified. An image can belong to several boards. Never infer membership from resemblance. Each board folder must hold real files or a documented recovery package, not broken links.

When listing a board, allow for grids that load as you scroll. Record what is on the board now, apart from what was uploaded in the past. Never label a small web preview as a full-size original. If no original can be reached, keep the best copy, label its size honestly and report what is missing.

## Verify and restore

Check that every saved image opens, check dimensions and hashes, and match the manifest's count with the files. Keep an index and short restore steps: create a board, name it, and upload that board's `references/` files.

Reference images and membership can be rebuilt this way. A service's learned personalization may need retraining in another account, so do not promise it can be restored from the image files.
