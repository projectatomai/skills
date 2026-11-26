---
name: comfyui-video-production
description: Operate a local ComfyUI server to generate reference-guided dialogue videos, manage its queue, and assemble verified edits with local FFmpeg, audio mixing and reusable captions. Use for ComfyUI video production and for diagnosing audio and video sync problems.
metadata:
  version: "1.0.0"
---

# ComfyUI video production

Use the person's own ComfyUI installation and local editing tools. Start by identifying the active project, the latest accepted master, the requested change, the available references, and the state of the server and its queue. Keep generation and editorial changes separate: a trim does not need a new generation, but missing motion or a wrong performance does.

Read [references/comfy-api.md](references/comfy-api.md) when operating ComfyUI. Read [references/editing-and-sync.md](references/editing-and-sync.md) before assembly, audio processing, captions, or diagnosing drift.

If the project keeps its own notes (paths, accepted takes, character references, delivery preset), read them first. They are that project's preferences, not rules for other productions.

## Core workflow

- Inspect the existing API-format workflow JSON and the live node schema. JSON exported from the ComfyUI interface is not directly a `/prompt` payload. Custom nodes and node IDs differ between installations.
- Reuse verified image, wardrobe, scene and voice references. Assign each speaker explicitly to its reference audio. Use the exact dialogue, and stage silent listeners and natural reactions. Inspect the visual performance as well as the transcription.
- Choose clip length from the spoken duration plus the requested action and reaction beats. Respect the installed model's frame-count limits. If there is not enough natural motion for a pause, generate more footage. Do not hide the gap with slowed video or freezes unless the person asks for that effect.
- Query the queue before submitting. Submit one necessary job with a unique output prefix, and save the full payload and the returned prompt ID. If a submission times out, inspect the queue and history before retrying, because the first request may have succeeded. Do not clear or interrupt unrelated jobs.
- Read the specific job's history, tell completion from errors, inspect the produced file, and keep rejected versions separate. A successful API response does not mean the take is accepted.
- Do not splice voice audio unless the person asks for it. Cutting, joining, crossfading or patching pieces of voice recordings, or mixing takes from different sessions in one soundtrack, is audible. When a line changes, re-record the whole narration or connected scene in one pass and rebuild the mix from it. A review sample is one continuous stretch of the real render, not stitched excerpts.
- Assemble the latest accepted takes into an immutable, versioned master. Keep the clean dialogue, effects stems, cue timings, edit decisions and export settings, so a change can be reproduced.
- Validate decoded audio timestamps against cumulative samples, not only packet continuity or the nominal frame rate. Consistent timestamps alone do not prove lip sync. Compare the picture and audio positions of source shots near the start, the middle and the end.
- Return the complete requested final with its full local path. State any remaining limits on performance or verification. Do not post to a social platform just because the person asked for a render.

## Helpers

`scripts/comfy_status.py` reads the queue and, if asked, one job's history, without changing server state. `scripts/audit_audio_clock.py VIDEO` detects differences between decoded timestamps and the sample clock that packet-level checks can hide. Both use only the Python standard library. The audit also needs `ffprobe`. Their output is evidence to interpret, not an automatic lip-sync verdict.

## Keys and spending

Do not put API keys into this skill, a handoff, workflow JSON or command logs. If the person authorizes a paid audio or video provider, read only the named credential through their own secret mechanism and keep it out of all output. Local generation is not permission to spend cloud credits.
