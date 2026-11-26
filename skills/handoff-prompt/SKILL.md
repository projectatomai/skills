---
name: handoff-prompt
description: Write a handoff for the next agent or person and deliver it as a Markdown file, never pasted into the chat. Use for "handoff prompt", "give me a handoff", "hand this off", "write a prompt for the next agent", or any request to pass work to another agent, another session or a person.
metadata:
  version: "1.0.0"
---

# Handoff prompt

## The rule

A handoff always goes to the person as a **Markdown file**. Never paste its text into the chat reply.

The reason: they pass the handoff to someone else, so they need one file they can hand over whole.

## Steps

1. Read the live state again before you write. A handoff with stale facts is worse than none. Check the things the next reader will act on: ids, revisions, file paths, what is published and what is scheduled.
2. Write the handoff to a `.md` file in the project's working folder, named for its topic, for example `HANDOFF-checkout-bug.md`. If the project has a rule for where such files go, follow it.
3. Deliver the file. If you can attach files to your reply, attach it. If you cannot, give its full path.
4. Keep the reply to one or two lines: what the file covers and where it is. Do not repeat its contents.

## What the file must contain

Write for a reader who starts cold and has seen none of this conversation.

- **The goal**, in the person's own words where possible.
- **What is done**, with the date each fact was checked.
- **What is not done**, stated plainly. Do not let "attempted" read as "finished".
- **What is unknown.** Label anything you did not verify as UNKNOWN. Do not guess.
- **Exact references:** ids, URLs, file paths, revision numbers.
- **Decisions already made** by the person, quoted, and the ones still theirs to make.
- **Changes and side effects** this session caused, so nobody has to rediscover them.
- **Traps** that cost time, and the route that worked.
- **Other people or agents** working in the same files or accounts.

## What a handoff must not do

- It must not pass on permission. Approval to post, publish, send, spend, delete or push comes only from the person, given to the agent that will do it. Say so in the file. One session's approval does not carry over to the next.
- It must not include secrets, tokens or personal details the next reader does not need.
- It must not decide open questions for the person. List them as open.
