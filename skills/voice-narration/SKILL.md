---
name: voice-narration
description: One rule for AI voice work - never splice voice audio, re-record the whole pass. Use whenever recording, fixing, mixing or previewing narration or dialogue for a video with ElevenLabs or another text-to-speech tool.
metadata:
  version: "1.0.0"
---

# Voice narration

Spliced voices never sound right, so voice audio is never spliced. This applies to every video: a narrated explainer, a reel, a short or a sample, whatever tool makes the picture.

## The rule

- Never build or repair a voice track by cutting, joining, crossfading or patching pieces of recordings. Never cut inside a take.
- Never mix takes recorded in different sessions in one soundtrack. A line recorded later sounds different from the lines around it, even with the same voice, model, settings and seed.
- When any line changes (its wording, a mispronounced word, the pacing, a bad take), record the whole narration again, or the whole connected scene, in one pass from start to finish. Then rebuild the full mix, and any picture timing fitted to the audio, from that pass.
- A review sample is one continuous stretch of the real render with its full mix. Never stitch excerpts together, never fade to black in the middle, and say which time range the sample covers.

## How to record a pass

1. Lock the script first. Keep respellings for hard words in a separate spoken field, so the text on screen keeps the real spelling.
2. Test every hard word before the pass. Record one short sentence with several candidate spellings as separate auditions, label them, and let the person pick by ear. A plain respelling can still come out wrong, so always test.
3. Check how much of the account's allowance is left before a full pass, and say how much the pass will use.
4. Record every line in script order in one session. One request per line is fine when each line is a complete take. If the tool can be told what was said before and what comes next, tell it, so the lines read as one performance. With ElevenLabs, that means passing `previous_request_ids` and `next_text`. Check its current documentation for how long request ids stay usable and which models support this.
5. Where the tool offers word or character timings, save them next to each line's audio, so picture cues can be matched to words.
6. Keep the previous pass whole in its own folder until the new one is checked. Do not overwrite it or mix the two.
7. Place each take whole on the timeline, and set the pauses between lines (about 1.5 to 2 seconds between narration lines, unless a beat needs more). Adjust only the silence between takes, never the takes.

## Keys and voices

- Read the API key from an environment variable or a secrets manager, and use it only inside the one command that calls the API. Never print it, log it, save it to a file or ask the person to paste it into the chat.
- Never imitate or clone a real person's voice. Use premade or designed voices.
