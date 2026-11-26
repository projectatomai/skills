---
name: suno-song
description: Write songs for Suno the approval-first way. Offers five numbered options, each a different song with the exact style prompt, exclusions and full lyrics, and creates nothing until the person approves the exact text. Keeps a taste file of what they liked and rejected. Use for "write a song", "make a song", "song ideas", "write lyrics", "cover this song", "run it in Suno" or any mention of Suno.
metadata:
  version: "1.0.0"
---

# Suno songs, approved before they are made

The person approves the lyrics and the prompt before anything is created. "Make a song" means show options first. "Make three more songs" still starts with options.

## The flow

1. Read the taste file and work out what the song is for.
2. Write five options.
3. Show them and stop.
4. Apply the pick or the feedback, and save it.
5. Create in Suno, or hand over the exact text.
6. Check, save and report.

## 1. Read the taste file

Keep one file, `song-taste.md`, in the person's working folder. Start it from `references/taste-template.md` the first time. It holds the genres they like, genres they never want, how they phrase prompts, and every reaction so far in their own words.

Read it every time. The reactions section wins over anything in this skill, because it is what they actually said.

Then work out what the song is for: a standalone song, a soundtrack with a fixed length and tempo, a promo. A song for a video takes its length, tempo and whether it has vocals from the video.

Every song is a new song unless the person says "cover" or "remix" and names the source. A round of covers they liked does not make the next request a cover.

Decide anything else left open yourself and say so in one line above the options. The options are where they correct you.

## 2. Write five options

Always five, numbered 1 to 5, however many songs were asked for. They can pick one or several.

Make each a different song: its own subject, genre, prompt, lyric structure and vocal. Never offer one sound five times, or one section layout with new words. The exception is a round of covers, which keeps the source's sound and layout and differs in story and words.

If they name a genre, vary the subgenre, tempo and vocal inside it. If they name none, spread the five across the genres in the taste file. Never offer a genre the taste file rules out.

Use this format for each option:

    ## 1. Title, genre

    One plain sentence saying what the song is about.

    **Prompt:**
    The exact text for Suno's style box

    **Exclude:** the exact text for the exclusions box

    **Setup:** New song, one Create. For a cover: Cover of <song and link>, with the audio influence setting.

    **Lyrics:**
    ```
    [Verse]
    Full lyrics with section tags, ready to paste
    ```

Put all five in the message in full, because they are approving exact text. Also save them to a dated notes file in the working folder.

### Lyric rules

- Tell one clear story or situation. A listener should be able to say what the song is about after one play.
- Every line follows from the line before, and the verses move the story forward.
- Use everyday words, concrete details and real feeling. No riddles, running metaphors or non-human narrators unless they ask for them.
- Put the title in the chorus or refrain, and have it say what the song is about.
- Let the genre set the form. A blues takes AAB verses. A folk ballad can tell its story in verses with a refrain. A techno track can carry a short spoken story over long instrumental sections.
- Write full lines that move the story, not repeated filler chants.
- Keep one voice. No shout tags and no exclamation points. No punctuation at the end of a line except a question mark.
- Avoid worn-out song words in plain-spoken lyrics: shadow, ashes, echo, void, whisper, hollow, abyss, neon, static, chains, demons, scars.
- For a cover, match the source's section layout and line lengths so the new words sit on its melody, and end chorus lines on a strong word.
- Spell names the way they should be sung.
- No real people, brands or artists. Do not quote real songs or reuse a famous song title. Nothing hateful, and nothing that glorifies self-harm or violence.

### Prompt rules

- Write each prompt from scratch for its own song, with its own genre, tempo, key, instruments and vocal.
- Order: genre first, then drums and bass, texture, vocal, then structure or outro. Join with commas. Name the tempo, and the key when it is known.
- Describe the vocal plainly. Never name an artist.
- Start every Exclude with the genres the taste file rules out, so the model cannot drift there. Keep words that pull toward them out of the prompt as well.
- For a cover, keep the source's sound words and change only mood and delivery words.
- If they give a reference clip, plan to attach it as the audio reference, and say so in the Setup line.

### Check before showing

Read the five as a stranger would, or give them to a fresh reader with only the lyrics if your agent can start one. For each song, say in one sentence what it is about, and list any line that made you stop. Fix the real problems, then re-read any song you changed.

Then compare the five with each other. Outside a round of covers, no two should share a genre, tempo range, vocal or section layout.

## 3. Show them and stop

End with one question: which number, or what should change. Do not open Suno at this step.

## 4. Apply the pick or the feedback

- **They pick numbers with no changes:** that is approval for those exact options.
- **They pick a number and ask for changes:** make them, show the full changed option, and wait for a yes.
- **They give feedback on the whole set:** write five new options that apply it, keep what they liked, and number them 1 to 5 again.

Write every pick, rejection and comment into the taste file, dated and in their words, before moving on.

An approval covers only the exact text they saw, and only that song.

## 5. Create in Suno

There are two ways. Use the one that fits.

- **They create it.** Give them the title, prompt, exclusions and lyrics as separate blocks, in the order Suno's form asks for them. This always works.
- **You create it, when they ask and your agent can use their own signed-in browser.** Enter exactly what they approved. Before pressing Create, read every field back from the page and compare it with the approved text, and check the account, the model and the credit balance. Press Create once. If the site is signed out, stop and ask them to sign in. Check that the service's terms allow this kind of use before you start.

Each Create usually makes two takes and spends credits. Say what a run will cost before the first one. If Suno rejects the text, stop. Show the person what was rejected, suggest a reworded line, and wait for their yes before trying again.

## 6. Check, save and report

Confirm that each take finished and that its lyrics and style match the approved text. Add a results table to the notes file with each take's length and link. Report the links, the credits used and left, and anything odd, such as a take much longer than the rest. Say plainly that you have not listened to them.

When they react to a take, add that to the taste file too.

## Hard rules

- Never create anything before the person approves the exact option.
- Never offer or create a genre the taste file rules out. If they ask for one anyway, name the rule and ask once whether it has changed.
- Never buy credits, change the plan or accept new terms.
- Never publish, share, delete or rename anything in their Suno account. Download only when they ask.
- Never upload a song anywhere without a yes for that upload.

## Keep the taste file current

When the person corrects something or a step teaches you how the pages really behave, write it down in the same turn: reactions go in the taste file, and they stay there in the person's words. When a new rule replaces an old one, delete the old one.
