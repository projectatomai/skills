---
name: animated-video-production
description: Plan and produce a short animated video with generated images, voices and video clips. Guides brainstorming, character and prop sheets, voice auditions, the script and shot list, and a storyboard delivered as one playable video with audio. Pauses before paid production, then covers video generation, continuity checks, local editing with FFmpeg and optional YouTube packaging. Use for "make an animated short", "character sheet", "voice auditions", "storyboard this", "animate the storyboard", "edit the clips together" or "prepare the YouTube upload".
metadata:
  version: "1.0.0"
---

# Animated video production

Build an editable production package whose characters, props, shots and audio stay consistent from the first idea to the final movie. Start from the person's existing story, accepted artwork and latest direction before inventing anything.

This skill is provider-neutral. It works with whatever image, voice, video and music tools the person has. Read the chosen tool's current documentation before each stage, because models, limits and prices change.

## Do the scope that was asked for

| The request | Deliver | Do not |
|---|---|---|
| Brainstorm, or recommend voices | Ideas and options, with decisions recorded | Generate images, audio or video |
| One character sheet, or named voice samples | Exactly those, with reusable records | Expand into a full storyboard or add a narrator |
| Script, prompts or a written plan | Script, character and prop specifications, shot list, per-shot directions, asset list, handoff | Render media. Label it "not rendered" |
| Storyboard | Reviewed panels plus **one playable video of every scene in order, with audio** | Call it done without that video |
| Animate or produce | The requested shots, inspected and assembled | Treat one sample as the whole film |
| Edit existing video | A new versioned export from the original clips | Regenerate clips unless asked or clearly needed |
| YouTube packaging or upload | Title, description, thumbnail, upload when asked | Publish publicly without being told to |

Read only the reference each stage needs:

- `references/planning.md`: the guided walk from idea to handoff, and the pause before production.
- `references/preproduction.md`: character and prop sheets, development scenes, the shot list and the storyboard video.
- `references/voice-and-audio.md`: casting, auditions, recording, timing and pauses.
- `references/continuity.md`: joins between shots, drift, and visual acceptance.
- `references/editing.md`: local assembly with FFmpeg, music, and checking the export.
- `references/publishing.md`: YouTube title, description, thumbnail and upload.

Copy `assets/production-template.md` into the film's own folder and keep it current. Never store production files inside the skill folder.

## Costs and keys

- Image, voice, video and music generation cost money. Say what a step will cost before the first paid call, and ask which video model and resolution to use. A recommendation is not a choice.
- Keys come from environment variables the person has set, such as `ELEVENLABS_API_KEY`. Check that a variable is set without printing it. Never ask for a key in the chat, and never write one into a prompt, a script or a receipt.
- Save a "pending" record before every paid call and mark it complete only after saving the result. After an unclear failure, read the job history before retrying. Never resubmit blindly.
- Allow one corrected retry for a quality failure. If it fails again, report the problem and stop.

## Rules that hold through every stage

### 1. Plan first, then pause before paid production

Finish the planning package, including the storyboard video, then stop and hand over. The person reviews it, settles open choices and tells you to start. Do not start production yourself, schedule it, or change any settings while paused. Their instruction to start releases the pause, and they can waive it in advance.

### 2. The storyboard is one playable video

Every storyboard includes one locally assembled video of all scenes in order with their dialogue and sound. Timed stills are enough. Contact sheets, separate clips and audio players are extras, not substitutes. Temporary voices are fine when casting is still open, as long as they are labeled.

### 3. Record the whole scene's dialogue before generating video

Record all spoken lines for a scene with the chosen voices before any video. That recording is the authority for wording, pacing and edit timing. Design the picture cuts around it. If a video tool needs shorter audio, cut exact continuous intervals from the master at quiet points, keeping whole words and breaths.

### 4. Never splice voices

Never build or repair a voice track by joining, crossfading or patching pieces of different recordings, and never mix takes from different sessions in one soundtrack. When any line changes, record the whole narration or the whole connected scene again in one pass, then rebuild the mix and the picture timing from it.

### 5. Protect the pacing

Natural spacing between words, breaths and dramatic pauses is part of the performance. Never shorten pauses, speed up speech or run lines together to hit a runtime or a cheaper clip length. If the story is too long, change the plan or tell the person.

### 6. Prefer deliberate cuts

Design self-contained shots that cut at complete lines or actions. Do not rely on separately generated clips looking like one unbroken take. Classify every join before making images:

- **Deliberate cut:** the shot gets its own opening frame only. Do not make or attach an end frame.
- **Continuous blend:** only when flowing action is truly needed. The previous clip's actual last included frame becomes the next clip's opening frame.

Never hide a failed join with a dissolve, a morph or a zoom, and never call a join seamless without watching it.

### 7. Original artwork is the authority

Accepted character, prop and lighting artwork governs identity throughout the film. A later generated frame does not replace it because it is newer. Give recurring props their own reference sheets. Keep exact details: species, proportions, clothing, how many accessories, who owns a prop and what state it is in.

### 8. Fit clip length to measured audio

Measure the edited performance, then request the shortest supported generation that holds it. Record intended seconds, billed seconds and the estimate. Trimming later does not refund anything.

### 9. Music is separate and comes last

Generate background music as its own asset, keep it out of dialogue recordings and video prompts, and mix it under the dialogue after the picture is assembled. Add music only when it is in the brief.

### 10. Report what you actually checked

Say which files you watched, which you listened to, and what you only probed or decoded. A file that decodes says nothing about acting, lip sync or visual quality. Do not describe a contact-sheet review as a lip-sync review.

## The working order

1. Read the project's brief, accepted references, storyboard, receipts and edit scripts. Old work logs describe the past. They do not authorize repeating it.
2. Settle story, length, aspect ratio, style, cast, speech and delivery from what you have. Ask only for what is missing, and keep preparing meanwhile. Decide the target length before locking the script.
3. Build the character bible, clean cast references and sheets for recurring props. Give each named character a short scene that shows who they are through a choice.
4. Generate and inspect character and prop sheets before any scene frame that depends on them. Fix identity problems first. Cast voices. A narrator always has a different voice from every character.
5. Write the script and the shot list. Label each join. Prepare the frames each shot needs.
6. Assemble the storyboard video, write the handoff, and pause.
7. After the person says start: confirm model and resolution, record the scene dialogue, measure it, check live estimates, submit, save job ids at once, wait, and inspect real results.
8. Assemble locally. Keep original downloads untouched, save edit decisions and commands with versioned exports, and check the movie and its sound, not only the plan.

## Delivery

- **Storyboard:** lead with the one playable video, then the panels and the editable plan.
- **Finished film:** the playable movie, its editable sources, the original clips and the verification record.
- **Smaller scopes:** only what was asked for and actually made.

Give full local paths. If a manual step is unavoidable, give numbered steps with exact addresses and file names. At the planning boundary, carry open choices and unrendered media into the handoff in plain words.
