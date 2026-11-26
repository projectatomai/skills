# References, moodboards and image batches

The examples use Midjourney's words (moodboard, style reference, personalization). The method works with any image generator that takes reference images.

Use the tools and documentation the person's agent actually has. Do not call undocumented endpoints or rely on remembered page internals. Check the service's terms before driving its site with a browser tool. If automated use is not allowed, prepare everything and let the person press the buttons.

## Reference coverage

Find the supplied videos and stills and any existing frame lists. For videos, follow `cut-coverage.md`. For each reference frame, note scale, composition, palette, light, materials, texture, subject and mood. Track which frames guided which concept, and pick unused ones when the person asks for variety. Text inspired by a frame is not an attached image reference, so do not describe it as one.

## Moodboards

- Update the board the person named. If they want one board per source video, make separate boards and confirm each one saved before removing anything from an old combined board.
- Keep items the person added. Record which source went to which board, with before and after counts.
- If two boards are equally likely and they did not say which, prepare the frames and ask, while doing other work.
- Upload in small groups, wait for each to finish, and record the source file against the saved item.
- An upload that was started is not a saved item. Confirm by leaving the board and opening it again.
- Changing a board never authorizes generation.

## Attaching a reference to a prompt

Choose the role on purpose:

- **Style reference:** the visual treatment. The usual choice here.
- **Image prompt:** composition, subject and layout, when that is intended.
- Other roles only when needed and supported by the current model.

Wait for an uploaded image to finish processing before selecting it, and check that you selected the new one. Clear old attachments before changing the combination. Reuse an already uploaded reference address only when you have recorded which source it came from. Never invent an address.

## Settings

Write the agreed preset in `direction.md`: model version, quality, aspect ratio, speed mode, personalization and board. Before each batch, confirm each setting is available and selected in the live interface. If something agreed is unavailable, report the conflict. Do not substitute a faster paid mode, a draft mode, a different model or a lower quality.

After a job is accepted, read the settings back from the job itself. Flags typed into a prompt are not evidence of what was accepted. If the service ignores a parameter with the current setup, stop sending it and vary the subjects and other settings.

A prompt shape, to be filled with new subjects each time:

```text
[subject and action], [one impossible relationship], [setting and tactile materials], [controlled light]. [The project's style words]. [aspect ratio, model, quality and speed flags] [verified reference addresses] [current profile and board ids] [things to leave out: text, logos, watermarks]
```

Shorten style wording when the attached references already carry it.

## Queue and receipts

- Read the live queue before each small group and stay inside its free slots.
- Save "submitted" for each prompt straight after its one attempt, before the next.
- A "submitting" card is not acceptance. Confirm a queued or rendering state, or a returned job id.
- Keep the evidence of any "queue full" or "creation failed" message before retrying. Failed attempts do not count as output.
- Fix a validation error only when it clearly happened before a job was created. If the job may exist, resolve it by reading history. Never resubmit blindly.
- Long lists hide off-screen cards. Merge what you see into existing receipts. Do not mark unseen jobs as failed.
- A stuck percentage may be a stale page. Refresh after submissions are recorded. Never create a job as a status check.
- After an interruption, continue only with prompts that were planned and never submitted.

## Finishing a batch

Require the agreed number of distinct finished jobs, the real outputs, the accepted settings and reference roles, and a look at every set. Record missing or failed jobs honestly. Save a `delivery.json` with ids, links, counts and settings, and one screenshot of the finished state. Save local copies as `local-backups.md` describes.
