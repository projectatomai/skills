# Local editing and checks

Use the FFmpeg already on the machine. Check with `command -v ffmpeg ffprobe`.

## Keep sources and an editable timeline

Never overwrite a provider's original download. Version every export. A workable layout:

```text
film/
  production.md
  characters/     clean references, labeled sheets, notes
  props/          prop sheets and clean references
  storyboard/     frames, gallery, prompts, the storyboard video
  shots/001/      original.mp4, generation.json, start.png
  audio/          voice plan, manifest, masters, music
  edit/           timeline.json and the commands or editor project
  output/         versioned movies
  review/         probes, extracted frames, notes
```

A `timeline.json` records the edit decisions:

```json
{
  "fps": 24,
  "width": 1920,
  "height": 1080,
  "segments": [
    {"shot_id": "001", "source": "../shots/001/original.mp4", "in_seconds": 0, "out_seconds": 6},
    {"shot_id": "002", "source": "../shots/002/original.mp4", "in_seconds": 0.5, "out_seconds": 4}
  ],
  "transition": "hard_cut"
}
```

It is a record, not an editor's import format. Save the commands that implement it.

## Inspect every download

```bash
ffprobe -v error -count_frames -show_entries 'stream=index,codec_type,codec_name,width,height,pix_fmt,avg_frame_rate,start_time,duration,nb_read_frames,sample_rate,channels:format=duration' -of json shots/001/original.mp4
ffmpeg -nostdin -v error -xerror -i shots/001/original.mp4 -f null -
```

Stream duration, container duration and decoded frame count are three different numbers. A nominal ten-second clip can hold one frame more or less than you expect.

Before joining clips, confirm they share dimensions, frame rate and color type, and that sound and picture start together. If not, decide how to normalize them and write it down. Do not silently crop or drop an offset.

## Extract the last included frame

Only for a continuous blend. For a constant-rate clip trimmed to end at 6 seconds at 24 frames a second, the last included frame is number 143:

```bash
ffmpeg -nostdin -n -v error -i shots/001/original.mp4 -vf 'select=eq(n\,143)' -frames:v 1 review/shot-001-actual-end.png
```

Decide the trim first, then extract. Open the image and compare it with the plan.

## Trim and join with hard cuts

This joins two compatible clips, keeping each clip's own sound in step with its picture. Change the paths and intervals to match the timeline. `-n` refuses to overwrite.

```bash
ffmpeg -nostdin -n -v error \
  -i shots/001/original.mp4 -i shots/002/original.mp4 \
  -filter_complex '[0:v:0]trim=start=0:end=6,setpts=PTS-STARTPTS,fps=24,setsar=1,format=yuv420p[v0];[0:a:0]atrim=start=0:end=6,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a0];[1:v:0]trim=start=0.5:end=4,setpts=PTS-STARTPTS,fps=24,setsar=1,format=yuv420p[v1];[1:a:0]atrim=start=0.5:end=4,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]' \
  -map '[v]' -map '[a]' \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  output/film-v001.mp4
```

Frame-accurate cuts need re-encoding. For a longer film, build the same pair of trim branches for every segment and join them in timeline order, always from the original clips, never from an earlier export.

Use the storyboard's varied shot lengths. A provider's minimum clip length does not set the length of a shot in the film.

## Music and the final mix

1. Plan cues from the story's emotional beats. Silence is a valid choice.
2. Generate music only after the picture timing is known, as an instrumental unless vocals are in the brief. Keep the originals, prompts and receipts.
3. Add music as its own track after picture and dialogue are assembled. Keep an export with dialogue and scene sound only.
4. Lower the music under speech. Let a cue run across related shots, not restart at every cut. Fades belong on the music track, not on speech.
5. If a generated clip arrives with music in it, deal with that before adding a score. Do not stack two music beds, and do not mute the whole track and lose the dialogue.
6. Listen to the full mix and every cue boundary for clarity, abrupt starts, pumping and clipping.

## Other edits

- **Pacing:** change the interval of picture and sound together, update the timeline, export a new version.
- **Reordering:** update the timeline, then recheck the order of events and props.
- **Captions:** only when asked. Time them from the delivered speech, not the script's draft timings. Check they are readable and do not cover faces.
- **Voice replacement:** only when asked, and recheck mouth sync for every line.

A crossfade or a crop can hide a cut without fixing a wrong identity, anatomy or action. Fix the source, then rebuild.

## Check the export

```bash
ffprobe -v error -count_frames -show_entries 'stream=codec_type,codec_name,width,height,avg_frame_rate,nb_read_frames,sample_rate,channels,duration:format=duration' -of json output/film-v001.mp4
ffmpeg -nostdin -v error -xerror -i output/film-v001.mp4 -f null -
```

Check the frame count, duration, dimensions and that there is an audio stream. Extract the frames on both sides of each cut and compare them with the sources.

Then watch and listen. Review the start, middle and end of every shot and every cut. Listen for missing or repeated words, mouth sync, clipped breaths and abrupt music changes. Scan a contact sheet of the whole film for drift in cast and props and for stray text.

Record the file, its intervals, duration and frame count, stream details, the decode result, what you looked at, what you listened to, and known issues. Deliver the movie with its originals, plan, prompts, receipts and rebuild commands. A movie file alone is not an editable package.
