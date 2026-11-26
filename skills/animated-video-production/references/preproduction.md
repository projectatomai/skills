# Character sheets, shot lists and the storyboard

## Character bible

Give each recurring character a stable id and name. Record:

- Species or type, apparent age, silhouette, height relative to the cast, proportions, face, eyes, hair or fur, and any asymmetry.
- Exact wardrobe and palette, materials, footwear, and how many accessories and where.
- Personality shown through posture and movement, and how hands, wings or paws work.
- Voice identity, and whether they speak, narrate or only make sounds.
- What never changes, and what changes by script (a sleeve torn in scene 3).

For each main character, make a neutral full-body reference with front, three-quarter, side and back views, a small range of expressions and one or two story poses. Add a cast lineup for scale when characters share scenes. Keep clean individual references apart from the labeled review sheet: neutral background, even light, no story props.

### Recurring props get their own sheets

A cake carried through several shots needs a sheet as much as a character does. For each key item, set an id, its owner, silhouette, relative size, materials, palette, exact counts and arrangement of parts, grip points and allowed changes. Show useful views and close-ups, plus labeled states where relevant (closed and open, intact and broken). Save a labeled sheet and a separate clean reference. Use the clean reference for video conditioning. A collage of views must never become a shot's opening frame.

### Character art prompt shape

```text
Production character reference for [NAME] for [FILM].
Style and materials: [approved style].
Identity: [species, silhouette, proportions, face, colors, exact clothing].
Details that never change: [accessory counts, which side, distinctive features].
Views: [full-body views], at consistent scale.
Expressions and poses: [story-relevant set].
Neutral background, even light, whole silhouette visible, generous spacing.
No story setting, extra props or extra characters.
```

Keep the original output and the exact prompt.

### Accepting a sheet

Open the real image. Check silhouette, species, scale, costume, accessory count, asymmetries, expressions, anatomy and agreement between views. Fix the reference before its errors multiply into scenes. Mark the accepted version, and keep replaced candidates with a clear status.

## A development scene for each named character

Write a brief scene that shows who each named character is through behavior: they want something, meet a small obstacle, and make a revealing choice. A description or an expression grid does not replace it.

Record: character, title, setting, rough duration, what they want, the trait it reveals, three beats (setup, choice, reaction), a line or two if useful, framing and the key pose, and which storyboard shots it belongs to, or the label "standalone character study".

Prefer a moment that already belongs in the story. A standalone study stays out of the film's runtime. Illustrate one clear key pose per scene once the model sheet is accepted.

Example: a careful repair robot wants to straighten a crooked handmade sign. It starts measuring, notices the owner admiring the uneven letters, and lowers its ruler. It asks, "Would you like it changed?" The moment shows precision, an assumption about what "better" means, and the ability to listen.

## The shot list

Each shot has: an id, its scene, its purpose, intended edited duration, requested generation duration, framing and camera, opening state, visible action, dialogue with speaker, audio cues, ending state, props, references and transition. The ending state is a written note, not a reason to generate an end frame.

### Pacing

- Do not turn every panel into a ten-second clip or divide the runtime into equal blocks.
- Cut where attention, action or understanding changes.
- Use two or three second shots for a glance, a detail or a simple action, and group several when the story is brisk.
- Give dialogue, difficult actions and emotional reactions room.

For example: 2 seconds of paws pulling string, 3 seconds as the kite tips, 2 seconds on a surprised face, 6 seconds for the reply and a decision. That is one 13 second scene in four shots.

Check the chosen model's minimum clip length. If it is longer than the shot, request the shortest clip that holds the beat and plan which part you will use. Record both durations.

### Scene image prompt shape

```text
Single clean [aspect ratio] animation frame for shot [ID], [story beat].
Style: [the approved materials, rendering and light].
Cast references: [which attached image is which character].
Location and time: [setting and point in the story].
Composition: [shot size, camera position, where everyone is, eye lines].
Acting: [clear action and readable emotion].
Continuity: [wardrobe, prop owners, counts and condition, light].
This frame shows the shot's [opening / key beat] state.
No captions, speech bubbles, panel borders, watermarks or stray lettering.
```

Never upload a multi-panel review sheet as a video's opening frame.

## The storyboard video

Every storyboard delivery includes **one continuous playable video of all scenes and shots in their current order, with synchronized audio.** Timed stills are enough. Assemble it locally, before the pause. Paid animation and final lip sync are not needed for it.

- Use the current script and the latest chosen frames. Include the opening, every beat, transitions and the full ending.
- Leave out rejected shots, alternate auditions and standalone character studies.
- Put the real scripted lines and sound cues in the audio track. If casting is open, use clearly labeled temporary voices. Do not replace dialogue with an invented narrator.
- Keep the chosen aspect ratio and the planned shot lengths. Do not speed up speech to match an estimate.
- Export a versioned file such as `storyboard-preview-v1.mp4` with video and audio. H.264 with AAC plays almost anywhere.
- Save the editable timeline: ordered shot ids, frame paths, audio sources, cue positions and durations.
- Rebuild the video whenever artwork, dialogue, order or timing changes.

Check it against the shot list: every scene present, current frames, current dialogue audible, speech endings intact, cues right, sound in sync, runtime, and a full decode. Play it and listen when you can, and say what you could not do. If the video is missing, the storyboard is not complete.

## Panels and records

Arrange frames in reading order, grouped by scene, with the shot id, edited duration, a short action and the dialogue outside each image. An HTML gallery with one video player at the top, plus contact sheets and the shot data as Markdown or JSON, makes review and later edits easy.

Before handing over, check story sense, coverage from beginning to end, cast identity, prop order of events, time of day, entrances and exits, eye lines, variety of framing and timing. Mark unresolved panels as drafts.
