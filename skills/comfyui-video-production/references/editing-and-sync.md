# Assembly and synchronization

## A failure worth knowing

Several nested concatenations of compressed AAC clips can produce overlapping decoded audio timestamps at the joins. The file can report normal H.264 and AAC and continuous packet timestamps, while the decoded sample count drifts further from the timestamps at every join. The drift can reach several tenths of a second by the middle of a short video and more by the end. Different players and transcoders exposed it differently.

**Do not repair this by applying `asetpts=N/SR/TB` first.** That throws away the timestamps needed to find the overlaps, and turns the extra decoded samples into a growing delay. A clean clock does not mean the audio matches the picture. Do not blame a platform without comparing the actual files. If the downloaded file matches the local original byte for byte, the platform changed nothing.

## Diagnose

Use `scripts/audit_audio_clock.py` to compare each decoded audio frame's `best_effort_timestamp_time` with cumulative `nb_samples / sample_rate`. Growing negative offsets often mean overlaps. A fixed offset at the start can be normal encoder priming or deliberate placement, so inspect it instead of shifting everything.

Check the audio and video starts and ends, the actual frame intervals, the packet DTS and PTS, and the decoded-frame clocks. For a suspected platform change, compare SHA-256 first. If the hashes match, the file was not converted. For lip sync, compare a standalone source shot against the final by picture matching and waveform correlation, or inspect the mouth performance itself. Speech recognition measures the timing of speech, not of lips.

## Correct overlap while keeping the timeline

One repair is to decode the clean master, with its original timestamps, like this:

```bash
ffmpeg -i SOURCE_WITH_ORIGINAL_TIMESTAMPS.mp4 -vn \
  -af 'aresample=48000:async=1:first_pts=0:min_hard_comp=0.001' \
  -ac 2 -c:a pcm_s24le repaired-dialogue.wav
```

This reconciles overlaps and gaps from the original timestamps. It is not a preset for every sync failure. Keep the original. Inspect the effect of hard compensation near the joins, and compare source clips from the start, the middle and the end. A lip mismatch that came from generation may need a new generation instead.

For new assemblies, use decoded PCM audio and explicit, matching picture and audio trims. Normalize each accepted clip's clock once, reconcile timestamp gaps before concatenating, and encode to AAC once at the end. Avoid nested `-c copy` concatenations of AAC. Rebuild stems on the final timeline.

## Captions and effects

A transcription made from the raw concatenated samples of a damaged file can carry the same growing offset. Transcribe the repaired clean audio again, or map the old sample-clock timestamps back to true timestamps and verify them. Do not reuse captions from one master on a later master unchanged.

Keep sound effects and crowd reactions on their own stem, apart from the dialogue. Speech transcribers can invent words in non-speech audio, so check those sections by listening. Do not layer new effects over a master that already contains them.

Keep captions editable (SRT or ASS) and built from reviewed, timed words and the matching clean audio. Caption wording and timing still need a person's review. Keep an uncaptioned master.

## Delivery

A safe upload preset for vertical video is 1080×1920 H.264, yuv420p, constant 30 fps, a keyframe every 2 seconds, AAC-LC stereo at 48 kHz, with faststart. Keep the duration of motion as generated. An upscale adds no original detail. Match the stream ends without cutting dialogue or closing sounds. A tiny black pad at the very end is different from freezing a reaction inside the story.

Verify that the final decodes, that frame intervals are a true 30 fps, that decoded audio agrees with the sample clock, and that source shots line up. Report the evidence precisely: waveform and picture placement relative to a source verifies the edit alignment, not the model's original lip performance.
