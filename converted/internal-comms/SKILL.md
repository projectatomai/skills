---
name: internal-comms
description: A set of resources to help me write all kinds of internal communications, using the formats
  that my company likes to use. Use this skill whenever asked to write some sort of internal communications
  (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project
  updates, etc.).
license: Apache-2.0. Complete terms in LICENSE.txt
compatibility: Converted by Skillfarm to read the same in Claude Code, Codex CLI and Gemini CLI.
metadata:
  source: https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/internal-comms
  source-commit: e4bb5d960d87126ff3b3a8af1a104b7db67560ba
  original-author: Anthropic
  converted-by: Skillfarm (https://skillfarm.ai)
  converter-version: '1'
---

> **Skillfarm multi-agent version.** Converted from [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/internal-comms) by Anthropic so it reads the same in Claude Code, Codex CLI and Gemini CLI. The original text follows this note unchanged. NOTICE.md lists every change.
>
> How to read it, whichever agent you are:
> - Where it says "Claude", it means you, the agent running this skill.
> - File paths in the text are relative to this skill's folder.

## When to use this skill
To write internal communications, use this skill for:
- 3P updates (Progress, Plans, Problems)
- Company newsletters
- FAQ responses
- Status reports
- Leadership updates
- Project updates
- Incident reports

## How to use this skill

To write any internal communication:

1. **Identify the communication type** from the request
2. **Load the appropriate guideline file** from the `examples/` directory:
    - `examples/3p-updates.md` - For Progress/Plans/Problems team updates
    - `examples/company-newsletter.md` - For company-wide newsletters
    - `examples/faq-answers.md` - For answering frequently asked questions
    - `examples/general-comms.md` - For anything else that doesn't explicitly match one of the above
3. **Follow the specific instructions** in that file for formatting, tone, and content gathering

If the communication type doesn't match any existing guideline, ask for clarification or more context about the desired format.

## Keywords
3P updates, company newsletter, company comms, weekly update, faqs, common questions, updates, internal comms
