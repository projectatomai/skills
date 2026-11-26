# Complete cut coverage for a reference video

Capture a frame from every cut in every new reference video, including fast montages, and the first shot too. Keep repeated appearances of a shot in the cut list even when the image was already captured.

1. **Probe and hash the source.** Identical copies share one audit. Note their other names.
2. **Decode the whole source.** Run `scripts/extract_cut_candidates.py SOURCE OUTPUT_DIRECTORY`. It saves candidate frames, numbered contact sheets in time order and an `audit.json`. The `--threshold` option changes sensitivity. The script finds candidates. It does not guarantee completeness.
3. **Review the full sequence in order.** Look at both sides of unclear edits and fast runs at full frame size. Add low-contrast cuts the detector missed. Rule out a camera move as a cut only after looking. Do not say the video was watched if only a sample was reviewed.
4. **Record each real cut:** timestamp, frame path and hash, a short description, review status, and whether it goes on a board. Save black or white flash frames locally and label them, then choose a clear frame from inside each shot for the board. Do not silently drop a brief new subject or angle.
5. **Compare the board with the cut list.** Add missing shots to the matching board and keep what the person added themselves. Avoid exact duplicates. Save before and after counts and proof that the changes are still there after reopening the board.

For an older board, run the same audit before claiming full coverage. If a board has no source video, keep it and say so.
