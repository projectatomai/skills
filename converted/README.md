# Converted skills

Skills written for one agent, converted by [Skillfarm](https://skillfarm.ai) so they read the same in Claude Code, Codex CLI and Gemini CLI.
Each folder is a modified copy of someone else's work, used under its licence. The original author keeps the credit and the copyright, and each folder's NOTICE.md links to the original and lists every change.

The conversion is mechanical and small on purpose: the front matter moves to the open [Agent Skills](https://agentskills.io/specification) format, a short note tells any agent how to read Claude-only wording and what the skill needs installed, and sandbox-only paths are replaced. The author's own text is kept as it was. The converter is in [`tools/convert`](../tools/convert).

## Install one

```sh
npx skills add https://github.com/protomota/skills/tree/main/converted/<name> -a claude-code -g -y
```

Use `-a codex` or `-a gemini-cli` for the other agents.

## What is here

| Skill | Original | Licence | Needs |
|---|---|---|---|
| [algorithmic-art](algorithmic-art/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/algorithmic-art) by Anthropic | Apache-2.0 | Nothing extra |
| [brand-guidelines](brand-guidelines/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/brand-guidelines) by Anthropic | Apache-2.0 | Nothing extra |
| [canvas-design](canvas-design/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/canvas-design) by Anthropic | Apache-2.0 | Nothing extra |
| [discernment-nudge](discernment-nudge/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/discernment-nudge) by Anthropic | Apache-2.0 | Nothing extra |
| [docx](docx/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/docx) by Anthropic | Apache-2.0 | Python 3 with defusedxml, lxml; LibreOffice (soffice); Poppler (pdftoppm); Pandoc; more packages for some tasks (see the note in SKILL.md) |
| [frontend-design](frontend-design/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/frontend-design) by Anthropic | Apache-2.0 | Nothing extra |
| [internal-comms](internal-comms/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/internal-comms) by Anthropic | Apache-2.0 | Nothing extra |
| [mcp-builder](mcp-builder/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/mcp-builder) by Anthropic | Apache-2.0 | Python 3 with anthropic, mcp; more packages for some tasks (see the note in SKILL.md) |
| [pdf](pdf/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/pdf) by Anthropic | Apache-2.0 | Python 3 with pdf2image, pdfplumber, pillow, pypdf; Poppler (pdftoppm); qpdf; Tesseract; more packages for some tasks (see the note in SKILL.md) |
| [pptx](pptx/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/pptx) by Anthropic | Apache-2.0 | Python 3 with defusedxml, lxml, pillow, python-pptx; Node.js with jszip; LibreOffice (soffice); Poppler (pdftoppm); more packages for some tasks (see the note in SKILL.md) |
| [slack-gif-creator](slack-gif-creator/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/slack-gif-creator) by Anthropic | Apache-2.0 | Python 3 with imageio, numpy, pillow; FFmpeg |
| [theme-factory](theme-factory/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/theme-factory) by Anthropic | Apache-2.0 | Nothing extra |
| [webapp-testing](webapp-testing/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/webapp-testing) by Anthropic | Apache-2.0 | Python 3 with playwright |
| [xlsx](xlsx/SKILL.md) | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/xlsx) by Anthropic | Apache-2.0 | Python 3 with defusedxml, lxml, openpyxl; LibreOffice (soffice) |

## Not converted

These stay as links to the original, with the reason.

| Skill | Original | Why |
|---|---|---|
| academy-guide | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/academy-guide) | It recommends Anthropic's own courses for learning Claude, so it only makes sense inside Claude. |
| claude-api | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/claude-api) | It is a guide to Claude's own API and Claude Code's settings, where Claude-only names are the subject and must stay as written. |
| doc-coauthoring | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/doc-coauthoring) | Its folder has no licence file, so there is no clear permission to share a changed copy. |
| skill-creator | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/skill-creator) | Its test and benchmark loop is built on Claude's subagents and the `claude` command, which needs a rewrite by hand and not a mechanical conversion. |
| web-artifacts-builder | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/web-artifacts-builder) | It builds artifacts for claude.ai, a Claude-only feature. |
