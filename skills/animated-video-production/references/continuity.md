# Visual continuity

Repeatedly feeding generated frames back into a video model tends to darken faces, raise contrast, simplify eyes and hair and change props, even when every clip is full resolution and its dialogue is complete. These checks exist to stop that.

## Prefer deliberate cuts

Design self-contained shots with intended cuts at complete lines or actions. Camera movement inside one shot is fine. Do not split a walk-and-talk at a provider's length limit and assume the motion will match.

For every shot, record its opening composition, its intended ending, its dialogue interval and its outgoing join type before generating.

When flowing action really is needed, prepare for it: a start and an end reference frame for each clip, matching identity, clothing, location, light, camera geometry, gaze, hands, pose and direction of motion. Render dependent clips one after another. If the model cannot take the endpoint controls you need, redesign as cuts or say so first. Do not promise a seamless result.

## Four separate authorities

Keep these in the production folder with real file names and versions:

- **Blocking:** the planned boundary frame defines camera, pose, who holds what and the action state. The real clip endpoints decide whether the plan was met.
- **Identity and materials:** the original accepted character artwork governs faces, eyes, hair, wardrobe, proportions and material detail.
- **Props:** each recurring object has an id and one canonical piece of source art, with shape, size, color, markings, owner and allowed changes. Similar objects get different ids. Intact and broken versions of one object share an id.
- **Lighting:** one original reference per lighting phase, with time of day, exposure, shadow softness, contrast and palette. Light changes with a story beat, not by drift.

Attach the prop's artwork when building any frame it appears in. Naming it in the prompt is not enough.

## Chaining frames in a continuous blend

Use this only inside a stretch meant to flow as one action. For clips A, B, C: make A's opening and ending frames, then reuse each accepted ending as the next opening and generate only the new ending.

For a clip that already exists, its accepted edit is the authority:

1. Lock the trim that fits the performance.
2. Extract the last included frame losslessly. At a constant frame rate F with an out-point of T seconds, that is frame T times F, minus 1.
3. Look at it. Then use that exact image as the next opening frame.

Never use a player screenshot, a thumbnail, a nearby timestamp or the untrimmed clip's last frame. Never lengthen a dialogue clip just to reach the provider's final frame. Record the source clip and its hash, the interval, the frame index and the image's hash.

Generate the next ending with the original character, prop and lighting artwork as the appearance authorities, so the chain cannot slowly redefine the cast.

Render, inspect and trim one clip before generating the next. Then compare the real last frame with the next real first frame, and watch the join at normal speed.

## When the endpoint has drifted

Compare the extracted frame with the original artwork: faces, materials, wardrobe, counts, ownership, exposure and background. If it has drifted, do not quietly repaint the next opening, because that breaks the exact match. Record the conflict. For a shot not yet accepted, a corrected source may fix it, within the retry limit. For an accepted clip, report the limit and carry on only as the person chooses.

Upscaling does not fix wrong identity, tone or props.

## Deliberate cuts

A new angle, a new scene, a new place or a time jump gets an opening frame only. Do not generate or attach an end frame, even when the model supports one. Describe the action and its ending in words, and let the measured performance set the cut. Keep the action axis, eye lines, cast, prop state and order of events consistent across the cut.

## Checks before submitting

- Inputs match the join type. No leftover end frame is attached to a deliberate-cut request.
- Use original artwork with the full background to restore a still. Attaching whole earlier scenes as loose references can reset the camera or cause a cut inside the clip.
- Describe stable exposure across the whole shot: soft fill on faces, readable shadows, a consistent palette, no vignette and no pumping.
- Remove old prompt wording after a correction. Contradictory phrases bring the defect back.

## Accepting a clip

Look at the beginning, several frames of the action and the last included frame, with close checks of faces and key props. Compare with the original references, and watch the whole sequence for slow darkening or loss of detail.

Record separate results for: tone and exposure, identity and anatomy, props, the opening, action, ending and cut, and speech and technical integrity. A resolution probe, a decode or a transcript cannot stand in for looking.

If a defect appears, hold every generation that depends on that frame. Fix and verify one replacement before applying the fix across the sequence.

## Darkening

Compare the same frames from the source clip and the assembled export, and check color range, transfer, HDR or SDR and pixel format. If the source is already dark, changing export tags or brightening the film will not bring detail back: restore the references and regenerate. If assembly introduced the change, fix the conversion.
