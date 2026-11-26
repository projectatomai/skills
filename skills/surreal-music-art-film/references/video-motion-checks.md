# Motion and corruption checks for every generated video

Run these on every generated clip, including retries, before it goes on a timeline or into a delivery. A container that plays, a clean exit code, frames that differ slightly or a good thumbnail do not prove animation.

## Before generating

- Look at the real source image and write the subject's action, the motion in the setting and the camera direction for that image. Name visible actions: a wing flexing, a head turning, cloth moving, a creature changing posture. Mist, light changes and zooms do not stand in for subject animation.
- Keep the source's full composition unless the person asks for a crop. Check its aspect ratio before choosing video settings.
- In image-to-video models, using the same still as a strong middle or end guide can freeze the clip or keep snapping it back to the still. Start with first-frame conditioning and the model's current official guidance. Add end conditioning only when stillness or a fixed endpoint is wanted.
- Prove one representative clip before queuing a large batch, and again after changing the workflow, the model, the aspect ratio or after a server restart.

## Checks on each clip

1. **Decode it fully.** Check frame count, duration, dimensions and frame rate, and record its SHA-256. Decode errors, truncated files and wrong settings fail.
2. **Scan every frame** for near-identical runs, very low change and abrupt jumps:

   ```bash
   python3 scripts/check_video_motion.py /absolute/clip.mp4 --expected-frames 97 --expected-fps 24 --output /absolute/clip-motion-check.json
   ```

   Give the real planned frame count and rate. The example numbers are not defaults. Exit code 2 is a flag to investigate. When you move to another resolution or style, calibrate with one clip you know moves and one you know is frozen. The script needs `ffmpeg`, `ffprobe` and Pillow.
3. **Look at it.** Compare the source with five frames: the start, one quarter, the middle, three quarters and the end. Then watch at normal speed. Check for real subject movement, natural anatomy and contact, motion direction, flicker, block corruption, melting, invented subjects, resets to the still, and unwanted crop or zoom.
4. **Write a receipt** tied to the file's hash: the frames viewed, the comparison with the source, the movement you saw, and your decision on motion, framing and glitches. Never pass a clip on numbers alone, and never record a review you did not do. Moving fog, water, grain or camera can raise the numbers while the subject stays frozen.
5. **Hold back** flagged and unreviewed clips from imports, timelines and exports. A real false alarm needs a note saying what motion you saw and where.

## When clips keep failing

If frozen or glitched output repeats, stop accepting it and find the cause before continuing the batch. Pause only your own pending jobs, and only with permission, after matching their ids against your saved submissions. Never clear or interrupt other work. Check logs and the workflow. Restart only the service involved, within what the person allowed, then prove a fresh clip.

Repair within the approved scope and attempt limit. Keep originals, hashes and history. Move rejected media to the trash only when the person has allowed deletion, and never empty the trash.

These checks do not authorize new generation, extra batches, infrastructure changes or deletion.
