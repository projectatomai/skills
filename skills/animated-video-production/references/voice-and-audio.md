# Voices, recording and timing

The examples name ElevenLabs endpoints because many people use it. Any voice provider works. Check the provider's current documentation before the first call, because models, limits and parameter names change.

## Keys

Read the key from an environment variable such as `ELEVENLABS_API_KEY`. Check that it is set without printing it:

```bash
[ -n "$ELEVENLABS_API_KEY" ] && echo "key is set" || echo "ELEVENLABS_API_KEY is not set"
```

If it is not set, stop and ask the person to set it. Never print a key or store one in a script, a prompt, a receipt or a gallery page.

## Discovery, audition and selection are separate

1. **Discovery.** Search the provider's current voices and the project's saved voices. Offer a short shortlist of contrasting options with exact names, ids and links, and say why each might fit. If you are judging from descriptions and have not listened, say so. A request for recommendations allows looking, not generating.
2. **Selection.** Record the exact id the person gives. Verify it resolves to that voice. A new selection overrides an earlier idea about accent. Never silently substitute a voice you could not reach.
3. **Audition.** Generate only the samples asked for: about 8 to 20 seconds of representative dialogue per role, with a change of emotion in it. Reuse the same text and settings when comparing voices.
4. **Review.** Show playable samples, the exact role to voice mapping, and which checks you really did. Keep the source files.
5. **Iteration.** "Try this voice" makes an `audition_only` take. The earlier selection stands until the person changes it. If they keep searching, mark the role open.

Never relabel an old recording as a new voice.

## Cast identities

Make one role record per speaking character: register, texture, accent, pace, phrasing, emotional range and pronunciation notes.

**A narrator always has a different voice id and a different underlying voice from every character.** Renaming a voice or changing its speed, pitch or settings does not make a new identity. Before any batch, check that the narrator's id is not among the character ids. A request for character voices alone does not add a narrator.

## Directing a performance

Keep the chosen voice and direct the delivery for each scene. Before generating, write a short delivery map outside the spoken text: who the character is talking to, the intention of each thought, words worth stressing, and where the energy changes. An authoritative voice should still sound engaged. Avoid announcer rhythm, forced chuckles and the same emphasis on every sentence.

Use only the performance controls the current model supports. Never put acting notes into the spoken text unless the model supports that syntax.

When the person says a take is monotone, revise the performance, not the casting: same voice, same approved words, a new versioned take that changes phrasing, emphasis, tempo and pauses. Do not speed up or pitch-shift the recording as a substitute for acting.

## Recording

- **Designing a new voice** (ElevenLabs: `POST /v1/text-to-voice/design`, then `POST /v1/text-to-voice` to save the chosen preview). Save each candidate's audio and id at once, so resuming does not design again.
- **A single voice** (`POST /v1/text-to-speech/{voice_id}/with-timestamps`). Keep the original audio and the timing data, and make a WAV working copy.
- **A connected conversation** (`POST /v1/text-to-dialogue/with-timestamps`, with ordered lines and each speaker's voice id). Use this when speakers respond to each other. Split long groups at natural dramatic boundaries.
- **A long narration** recorded line by line: generate the lines in order in one session, passing each request the ids of the lines before it and the text that follows, so they read as one performance.

Cache by voice id plus exact text, model, settings and seed. Version a changed request. Never overwrite a selected take.

## Never splice voices

Build a soundtrack only from complete takes of one recording pass. When any line changes (wording, pronunciation, pacing, a bad take), record the whole narration or the whole connected scene again in one pass and rebuild the mix and the picture timing that depends on it.

- Separate requests are fine within one pass when each line is a complete take, generated in script order and placed whole on the timeline with silence around it. Never cut inside a take.
- To fix a hard word, make short test recordings of several spellings, let the person pick by ear, then record the full pass with the chosen spelling.
- A review sample is one continuous stretch of the real mix. Say which time range it covers.

## Build the performance before choosing clip lengths

1. Write lines that are natural to say. Give each speaker an exact line once, with delivery notes outside the quoted words.
2. Group audio by dramatic continuity. Record a connected conversation together. Separate unrelated scenes and time jumps. Audio grouping is independent of picture cuts: one conversation can run across several deliberate cuts.
3. Record the exact current lines in the chosen voices. An audition proves identity, not the duration of different lines.
4. Edit each group into a sequence master. Keep natural breaths and pauses, and add silence where a discovery, a hesitation, a joke or a reaction needs room. Do not join every line with one fixed gap.
5. Listen to the whole sequence against the timed storyboard before any video. Transcription and decoding do not measure acting or rhythm.
6. Measure the edited performance, including pauses. Save the master, its timings and each shot's interval on it. Export shot slices from that timeline so each pause appears exactly once when the slices are put back together.

## Pauses

Plan breathing room as part of the performance. A short thought pause and a long reveal pause do different jobs. Do not add a pause after every word or make every gap the same.

State a pause as the total time from the end of one spoken phrase to the start of the next. Measure the gap that already exists and add only the difference. At a scene join, count the outgoing tail and the incoming lead together, so the break is not doubled.

If the paced performance runs past a hard length limit, change the plan or tell the person. Never squeeze the voice to fit.

## Cutting safely

- Speaker boundaries and timestamps from a provider are hints. A boundary can fall inside a word. Check against the waveform and an independent transcript.
- Cut only in a verified quiet interval between complete phrases. Check both sides of every seam for cut syllables, clicks and repeated fragments.
- A small fade can smooth a quiet seam. It must never fade a spoken sound.
- Check the files you will actually upload, after all trimming and encoding. A correct whole transcript cannot prove each slice is correct: a word split across two files still reads fine when they are joined.

Do not submit video with a known cut word, an exaggerated pause or an unresolved timing problem.

## Keeping billed seconds down

For each shot, record measured audio length, intended edit length, the shortest supported generation that fits, the unavoidable extra, and the estimate. If the performance is 5.2 seconds and whole seconds are supported, request 6, not 10. The performance is fixed in this sum: do not trim consonants, pauses or breaths to drop into a cheaper bracket.

For several short lines, compare the cost of one combined clip with several minimum-length clips. Run the estimate on the complete request, with references. Prove one representative shot before committing a batch.

## After generation

Reference timing does not guarantee delivered timing. Check the generated speech for missing, extra or repeated words and measure where it really ends. Remove only unused lead and tail. Keep the planned beats, and never pad the cut to the provider's duration. Prefer a local edit when it fixes the problem acceptably. Once the person accepts an edit or says not to re-render, stop generating for that issue.

## Records

Save a voice plan and a voice manifest in the film's `audio/` folder: role, description, provider, model, voice id, exact sample text and settings, file paths, duration, checksum, selection status and the checks performed.
