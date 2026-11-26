# Guided planning and the production handoff

Lead the person through a new animated story, or pick up an unfinished one. Each stage has a concrete result. Skip stages that are already done. Match the scope: brainstorming stays a conversation, and a written plan does not quietly become an illustrated storyboard or a production run.

## 1. Orient

Read the latest brief, chosen assets, cast and voice records and the current state. Corrections made in conversation win over older files. Find out whether this is a new series, a pilot, a later episode or a revision, and whether they want ideas, artwork, auditions, a script or a finished film. Settle orientation and target length before locking the script.

Keep a short decision record in the film folder with these states: `selected`, `proposed`, `rejected`, `audition_only`, `superseded`. Keep a separate current-state summary, so old brainstorm notes do not make rejected ideas look current.

## 2. Story and tone

Offer a few premises that really differ, each with a concrete scene. Develop what the main character wants, what they fear, their contradiction and the choice that reveals them. For a series, name the conflict that repeats.

When the person rejects a direction, bring new options and remember the exclusion. When they ask for a stronger tone, change the stakes and consequences, not the adjectives. Once a direction is chosen, move to the next open question.

Result: a premise, a tone, a conflict and a proposed beginning, turn and ending. A pitch is not an approved script.

## 3. World and cast

Decide separately what the characters are (people, animals, objects, invented creatures) and how human they are. A natural animal body is different from an upright character with hands and clothes. Record exact name spellings. For each main character, set role, relationships, silhouette, palette, wardrobe, distinguishing anatomy and behavior. When species or body type changes, update every dependent description.

Result: a short character bible, a relationship map, world rules and a chosen visual treatment.

## 4. Character and prop references

Follow `preproduction.md`. For a full illustrated package, make clean identity references and prop sheets before any scene frame that depends on them. For a written package, write the specifications and prompts and mark them `not_rendered`. Record known flaws in a sheet. Do not silently declare a flawed sheet final.

## 5. Voices

Follow `voice-and-audio.md`. Discovery, audition and selection are three separate steps. "Try this voice" is an audition, not a recast.

## 6. The script

Write from selected decisions. Give each beat a visible action, a purpose, exact dialogue and a performance note kept apart from the spoken words. Make the key choice and the ending readable. Include pauses, reactions and inserts in the total. Do not pad shots to a provider's minimum or rush speech to fit. Add narration or music only when the brief includes them.

Result: one coherent, versioned script.

## 7. Storyboard and prompts

For every shot, record its id, scene and audio group, edited duration, composition, opening state, action, speaker and exact line, ending state, props and transition. Write the artwork prompt and a provider-neutral video direction. Leave model-specific fields empty until the model is chosen. Never invent upload ids, costs, measured timings or finished files.

Classify each join as a deliberate cut or a continuous blend. Group audio by dramatic continuity, independently of camera cuts.

List all media: existing references, concepts that need cleanup, new props and settings, scene frames, exact speech and optional music. Then build the storyboard video as `preproduction.md` describes.

## Planning exit and the pause

Keep `planning-state.json` in the film folder with one of:

- `planning_in_progress`: real story, cast or script work remains.
- `review_ready`: deliverables exist, but a choice that matters is still open.
- `planning_complete_waiting_to_start`: deliverables are complete and choices are settled.
- `production_preflight`: the person said start. Settle model and resolution, prepare exact assets and audio, check costs.
- `ready_to_submit`: chosen model, verified reference files, measured performance and a live estimate all support submission.
- `production`: jobs and accepted edits are being tracked.

Before marking planning complete, check:

- The requested scope is met. Requested media exists, and deferred media is listed.
- Premise, tone, cast, orientation, target length and ending are settled.
- No open audition is being treated as a final choice.
- Lines in the script and the shot list agree.
- Shot timings add up to the target, and estimates are not presented as measurements.
- Every shot has usable directions and correct join handling.
- For a storyboard, one playable video covers every shot in order with the scripted audio, and its file, duration and voice mapping are recorded.
- Someone new could find the assets, ids, prompts, open checks and the first production step from the handoff alone.

Open creative choices mean `review_ready`, not complete.

Write `PRODUCTION_HANDOFF.md` with: project, version and scope. The chosen brief. Paths to the script, prompts, storyboard video and timeline. The cast and voice map, marking temporary voices. Existing and pending assets and known flaws. Open choices. The join rules. The exact next actions. Finished jobs and receipts. What must not be re-rendered. How to resume.

**Then stop.** Say whether planning is complete or review-ready, and what remains. Do not start production, schedule it or wait in a running job.

## Resuming

When the person says start, read `planning-state.json`, the handoff, the script, the cast list and the references for the next stage. Do not brainstorm, redesign or re-audition. If the handoff is still review-ready, settle its open choices first. Ask for the video model and resolution only if they are still missing. Do the deferred cleanup, replace temporary speech with the chosen voices, measure, and update the storyboard video before any upload or estimate. Keep the handoff current as work completes.
