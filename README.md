# Protomota skills

[skills.protomota.com](https://skills.protomota.com) is the public address for this collection. The skill folders below are maintained here. The reference catalog lists third-party tools separately and credits the original project for adaptations.

## Skills you can install from this repo

| Skill | What you can do with it |
|---|---|
| [Agent Council](skills/agent-council/SKILL.md) | Give Claude, Codex and Gemini the same decision, compare independent recommendations, then test what they agree on. Bring your own authorized model connections. |
| [Agent Team](skills/agent-team/SKILL.md) | Say which agent leads which kind of work, and when to bring in a second opinion. |
| [AI Founder Outreach](skills/ai-founder-outreach/SKILL.md) | Shortlist AI-first startups worth contacting, with evidence and screenshots, and draft only for the ones you pick. |
| [AI Motion Design](skills/ai-motion-design/SKILL.md) | Turn a reference video and a message into an editable Remotion or HyperFrames video. |
| [Animated Video Production](skills/animated-video-production/SKILL.md) | Plan and produce an animated short: characters, voices, script, a playable storyboard, then the edit. |
| [Bitwarden Secrets](skills/bitwarden-secrets/SKILL.md) | Fetch a key from Bitwarden Secrets Manager for one command without ever showing it. |
| [Bucksley MCP](skills/bucksley-mcp/SKILL.md) | Read balances, spending and budgets, and tidy transactions in Bucksley. |
| [ComfyUI Video Production](skills/comfyui-video-production/SKILL.md) | Run ComfyUI video jobs, check every clip and fix audio sync. |
| [Concise Reports](skills/concise-reports/SKILL.md) | Make agents say only what they did, ending with exactly what they need from you. |
| [Design Direction First](skills/design-direction-first/SKILL.md) | Get a style direction and real references before designing anything. |
| [Design Reference Review](skills/design-reference-review/SKILL.md) | Ground a UI in real references and check the rendered result against them. |
| [Dev Tunnels](skills/dev-tunnels/SKILL.md) | Keep dev servers and reserved ngrok tunnels matched, one port per project. |
| [Drive Organizer](skills/drive-organizer/SKILL.md) | Keep a shared media drive in order with a map, naming rules and helper scripts. |
| [Figma Designer](skills/figma-designer/SKILL.md) | Design in Figma through the Figma MCP server. |
| [Glimmer MCP](skills/glimmer-mcp/SKILL.md) | Read daily coaching for a dashboard and save a practice. |
| [Grok Imagine](skills/grok-imagine/SKILL.md) | Make and edit images with xAI's Grok Imagine API. |
| [Handoff Prompt](skills/handoff-prompt/SKILL.md) | Write a handoff for the next agent and deliver it as a file. |
| [Imagegen 2](skills/imagegen-2/SKILL.md) | Make images with OpenAI's gpt-image-2, from text or from a reference photo. |
| [InkSpring MCP](skills/inkspring-mcp/SKILL.md) | Work with ideas, posts, newsletters and scheduled drafts. |
| [Jotley MCP](skills/jotley-mcp/SKILL.md) | Find, read and organize voice notes and transcripts. |
| [LinkedIn Agent](skills/linkedin-agent/SKILL.md) | Draft, review and publish LinkedIn posts in your own voice, never without a yes. |
| [LLM Wiki](skills/llm-wiki/SKILL.md) | Keep a wiki of linked Markdown pages that your agent builds from the sources you give it. |
| [Market Scout](skills/market-scout/SKILL.md) | Find one product people already pay for and write a one-page sheet on the gap. |
| [Nano Banana](skills/nano-banana/SKILL.md) | Make images with Google's Gemini image model. |
| [OpenTalon MCP](skills/opentalon-mcp/SKILL.md) | Manage tasks through a local agent connection. |
| [Proof](skills/proof/SKILL.md) | End a task with a screenshot or recording of the real result. |
| [Suno Song](skills/suno-song/SKILL.md) | Write songs for Suno: five options with prompt and lyrics, nothing made until you approve. |
| [Surreal Music Art Film](skills/surreal-music-art-film/SKILL.md) | Build a music-led art film from your own references, with moodboards, image batches and motion checks. |
| [Textley MCP](skills/textley-mcp/SKILL.md) | Find, read, edit and save files in Textley vaults and tabs. |
| [Upwork Proposals](skills/upwork-proposals/SKILL.md) | Screen Upwork jobs, talk through the concerns, and write only the proposals you approve. |
| [Voice Narration](skills/voice-narration/SKILL.md) | Never splice voice audio. Re-record the whole pass. |
| [X Post Hooks](skills/x-post-hooks/SKILL.md) | Write the opening line of an X post. |
| [YouTube Channel System](skills/youtube-channel-system/SKILL.md) | Build and improve a YouTube channel as a system. |

The Mac apps host their own MCP servers. [App connection guides](https://protomota.com/mcp).

## Install once and keep your agents in sync

Clone this repository once. From the checkout, link the skill into each local client that should discover it. For example, on macOS:

```sh
git clone https://github.com/protomota/skills.git
cd skills
mkdir -p ~/.claude/skills ~/.agents/skills
ln -s "$PWD/skills/agent-council" ~/.claude/skills/agent-council
ln -s "$PWD/skills/agent-council" ~/.agents/skills/agent-council
```

Use the skill discovery directory supported by your client. If a destination already exists, inspect it before replacing it. Run `git pull --ff-only` in the checkout to update every link, then start a fresh agent session.

Each skill records its version as `metadata.version` in the `SKILL.md` front matter. Raise it whenever the skill changes. The Protomota Mac apps bundle their skill and compare this version with the copy in each agent's skill folder: **Settings** offers **Update** when the installed copy is older, and shows **Installed** when it is the same or newer.

## Converted skills

[`converted/`](converted) holds skills written for one agent that [Skillfarm](https://skillfarm.ai) has converted to read the same in Claude Code, Codex CLI and Gemini CLI. Each is a modified copy of someone else's work, used under its licence, with a NOTICE.md that links to the original and lists every change. The converter is in [`tools/convert`](tools/convert).

## Third-party skills we use

Install and update these collections from their maintainers. A listing identifies a workflow available in our setup. Versions and client bundles change over time.

- [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) — `embedded-captions`, `faceless-explainer`, `figma`, `general-video`, `hyperframes`, `hyperframes-animation`, `hyperframes-audio`, `hyperframes-cli`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-registry`, `hyperframes-studio`, `media-use`, `motion-graphics`, `music-to-video`, `pr-to-video`, `product-launch-video`, `remotion-to-hyperframes`, `slideshow`, `talking-head-recut`.
- [remotion-dev/skills](https://github.com/remotion-dev/skills) — `remotion-best-practices`, `remotion-captions`, `remotion-create`, `remotion-docs`, `remotion-interactivity`, `remotion-maps`, `remotion-markup`, `remotion-multimedia`, `remotion-render`, `remotion-saas`, `remotion-studio`, `remotion-upgrade`.
- [runpod/runpod-plugins-official](https://github.com/runpod/runpod-plugins-official) — `companion-clis`, `flash`, `runpod`, `runpod-mcp`, `runpod-migrate`, `runpod-templates`, `runpod-usage`, `runpodctl`.
- [openai/skills](https://github.com/openai/skills) — `gh-fix-ci`, `playwright`, `vercel-deploy`.
- [blader/humanizer](https://github.com/blader/humanizer) — `humanizer`.
- [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) — `last30days`.
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable) — `impeccable`.
- [chaseai-yt/claudex-loop](https://github.com/chaseai-yt/claudex-loop) — `claudex-loop`.

## Adaptations and related originals

| Workflow | Original or related project | What changed here |
|---|---|---|
| LLM Wiki | [LLM Wiki idea file](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) by Andrej Karpathy | The pattern is his. Our skill is an independent way to run it, with a schema, an inbox and two roles. |
| Design Reference Review | A thread by Prajwal Tomar, credited in the skill | Independent write-up of a reference-first way to design and check a UI. |
| Figma Designer | [Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) by Anthropic (Apache-2.0) | Related design guidance. Our skill is about working in Figma through its MCP server and points to theirs for visual direction. |
| AI Motion Design | Posts by [Rexan Wong](https://x.com/rexan_wong/status/2103707054108299437) and [Codila](https://x.com/0xCodila/status/2107119130239185232) | Independent write-up of a reference-led motion workflow for Remotion and HyperFrames. |
| Agent Council | [ClaudeX Loop](https://github.com/chaseai-yt/claudex-loop) | Related predecessor. Our independently written skill adds a Gemini vote, a host-neutral review, a challenge round, and evidence checks. |
| Motion Design Harness | [Mortiflix OSS](https://github.com/GTKottman/mortiflix-oss) | Local adaptation adds staged approval of briefs, style frames, transitions and animatics, plus delivery checks. |
| HyperFrames | [HyperFrames](https://github.com/heygen-com/hyperframes) | Local install has additional intake, brief, production and review references compared with its recorded upstream revision. |
| Media Use | [HyperFrames](https://github.com/heygen-com/hyperframes) | The local tree adds a host-audio helper and tests. |
| Remotion to HyperFrames | [HyperFrames](https://github.com/heygen-com/hyperframes) | The local tree adds frame-strip and render-comparison scripts. |
| Remotion Render | [Remotion skills](https://github.com/remotion-dev/skills) | Local instructions send renders and caches to a designated media volume. |
| Runpod workflows | [Runpod plugins](https://github.com/runpod/runpod-plugins-official) | Local operations include queue continuity and ComfyUI model-repair guidance. |
| Meanizer | [Humanizer](https://github.com/blader/humanizer) | Related writing approach. The custom skill adds audience-specific voice, dictated corrections and safeguards against invented anecdotes. |

## Skills supplied with connected clients and plugins

- **Claude official plugins** · `frontend-design`, `playwright`, `ralph-loop`, `supabase`, `swift-lsp` · [Anthropic](https://github.com/anthropics/claude-plugins-official).
- **OpenAI system skills** · `create-statusline`, `imagegen`, `openai-docs`, `review-agent`, `skill-creator`, `skill-installer` · [OpenAI distribution](https://openai.com/codex/).
- **documents** · `documents` · [OpenAI distribution](https://openai.com/codex/).
- **frontend-design** · `frontend-design` · [Anthropic](https://github.com/anthropics/claude-plugins-official).
- **google-drive** · `google-docs`, `google-drive`, `google-drive-comments`, `google-sheets`, `google-slides` · [OpenAI distribution](https://openai.com/codex/).
- **openai-templates** · `artifact-template-analytics-dashboard`, `artifact-template-business-review`, `artifact-template-design-report`, `artifact-template-experiment-analysis`, `artifact-template-financial-budget`, `artifact-template-investment-committee-memo`, `artifact-template-legal-memorandum`, `artifact-template-market-trends-report`, `artifact-template-minimal-letterhead`, `artifact-template-operating-calendar`, `artifact-template-operating-review`, `artifact-template-project-kickoff`, `artifact-template-project-tracker`, `artifact-template-sales-pipeline`, `artifact-template-simple-dark-mode`, `artifact-template-simple-light-mode`, `artifact-template-strategy-memorandum`, `artifact-template-system-design`, `artifact-template-team-alignment`, `artifact-template-three-statement-forecast` · [OpenAI distribution](https://openai.com/codex/).
- **pages** · `maintain-space`, `manage-schedules`, `organize-space`, `write-page` · [OpenAI distribution](https://openai.com/codex/).
- **pdf** · `pdf` · [OpenAI distribution](https://openai.com/codex/).
- **plugin-management** · `plugin-management` · [OpenAI distribution](https://openai.com/codex/).
- **presentations** · `presentations` · [OpenAI distribution](https://openai.com/codex/).
- **sites** · `sites`, `sites-remix` · [OpenAI distribution](https://openai.com/codex/).
- **spreadsheets** · `excel-live-control`, `spreadsheets` · [OpenAI distribution](https://openai.com/codex/).
- **supabase** · `supabase`, `supabase-postgres-best-practices` · [Supabase](https://github.com/supabase/agent-skills).
- **template-creator** · `template-creator` · [OpenAI distribution](https://openai.com/codex/).
- **vercel** · `access-protected-vercel-deployment`, `ai-gateway`, `ai-sdk`, `auth`, `bootstrap`, `build-agents`, `cdn-caching`, `chat-sdk`, `create-a-backend`, `custom-metrics`, `deployments-cicd`, `domains`, `env-vars`, `eve`, `flags-sdk`, `is-agentic`, `knowledge-update`, `marketplace`, `microfrontends`, `queues`, `react-best-practices`, `routing-middleware`, `runtime-cache`, `vercel-agent`, `vercel-cli`, `vercel-connect`, `vercel-firewall`, `vercel-functions`, `vercel-sandbox`, `vercel-services`, `vercel-storage`, `verification`, `workflow` · [Vercel](https://github.com/vercel/vercel-plugin).
- **visualize** · `visualize` · [OpenAI distribution](https://openai.com/codex/).
- **work-pets** · `create-pet`, `pets`, `update-pet` · [OpenAI distribution](https://openai.com/codex/).

## Additional workflows in our toolkit

These are catalog entries only. Source, rights and public release are reviewed separately.

`charsheet-soul`, `content-engine`, `digital-product`, `meanizer`, `motion-design-harness`, `talking-head-recut`, `teardown`, `ugc-influencer-video`

Private client, infrastructure, publishing and account workflows stay in our private inventory. No private memory or operating configuration is distributed here.

## License

The published files here are public domain under [The Unlicense](LICENSE). Each linked project retains its own license.
