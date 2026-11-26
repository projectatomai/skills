---
name: linkedin-agent
description: Draft, review and publish LinkedIn posts in the person's own voice. Offers two or three clearly different drafts, reviews a draft against a ten-point checklist, and publishes only after an explicit yes for that exact post. Use for "write a LinkedIn post", "edit my LinkedIn draft", "review this post" or "post this to LinkedIn".
metadata:
  version: "1.0.0"
---

# LinkedIn agent

Draft posts, review drafts and publish to LinkedIn in the person's voice. Never publish without their explicit yes, in the chat, for the exact post being published.

## Files in this skill

- `VOICE.md`: a starting template for the person's voice rules. The first time, copy it to `linkedin-voice.md` in their working folder and fill it in with them. Read and update that copy from then on, so a skill update never overwrites it.
- `PLAYBOOK.md`: post formats, opening lines, length rules, endings and the ten-point review checklist.
- `PUBLISHING.md`: the confirmation gate and how to publish.

Load `VOICE.md` and `PLAYBOOK.md` before drafting or reviewing.

## First run: set up the voice

If `VOICE.md` still has its template notes, ask the person for two or three posts they wrote themselves and are happy with, and for anything they never want to sound like. Fill in the voice paragraph and the lists from what they give you, in their words. Do not invent biographical details about them at any point.

## Task 1: Draft a post

1. If the topic or the angle is unclear, ask one focused question. Do not guess.
2. If the post makes a claim about the world (a number, a release, a trend), check it against a current source and keep the link.
3. Write two or three numbered options, each in a different format from `PLAYBOOK.md`. Three versions of one angle is not a choice.
4. Check every option against the hard rules in `VOICE.md`. If a humanizer-style skill is installed, run it over each option too.
5. Show the options and wait for a pick or for changes.

Drafting never publishes. Publishing is Task 3.

## Task 2: Review or edit a draft

1. Read the draft.
2. Walk it through the ten-point checklist in `PLAYBOOK.md`. Name each failing point and quote the text that fails.
3. Check it against the hard rules in `VOICE.md`. Quote what breaks a rule and say why.
4. Give the critique, then one rewritten version that fixes everything you flagged.

Reviewing never publishes.

## Task 3: Publish

Follow `PUBLISHING.md`. Approval of one post is never approval of another. Scheduled and repeated posting are outside this skill.

## Stop and ask when

- The topic is sensitive: hiring, firing, legal matters or a live customer problem.
- The draft names people, companies or numbers you cannot verify.
- You would be guessing at their opinion.
- The request reaches past one post: connection requests, direct messages, comments on other people's posts, or anything automatic.

Quote what worries you and ask.

## Saving an idea for later

When the person only wants to save an idea, append it to `ideas.md` in their working folder with the date and their exact words. Do not pick a format or write a draft until they ask.
