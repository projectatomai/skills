# Protomota skills

[skills.protomota.com](https://skills.protomota.com) is the public address for this collection. The seven skill folders below are maintained here. The reference catalog lists third-party tools separately and credits the original project for adaptations.

## Skills you can install from this repo

| Skill | What you can do with it |
|---|---|
| [Agent Council](skills/agent-council/SKILL.md) | Give Claude, Codex and Gemini the same decision, compare independent recommendations, then test what they agree on. Bring your own authorized model connections. |
| [Concise Reports](skills/concise-reports/SKILL.md) | Make agents report what they did, ending with what they did, with what they need from you as the last sentence. |
| [Glimmer MCP](skills/glimmer-mcp/SKILL.md) | Read daily coaching for a dashboard and save a practice. |
| [InkSpring MCP](skills/inkspring-mcp/SKILL.md) | Work with ideas, posts, newsletters and scheduled drafts. |
| [Jotley MCP](skills/jotley-mcp/SKILL.md) | Find, read and organize voice notes and transcripts. |
| [OpenTalon MCP](skills/opentalon-mcp/SKILL.md) | Manage tasks through a local agent connection. |
| [Textley MCP](skills/textley-mcp/SKILL.md) | Find, read, edit and save files in Textley vaults and tabs. |

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
- **Higgsfield** · `higgsfield`, `website-builder` · [Higgsfield](https://higgsfield.ai/).
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

`agent-team`, `ai-founder-outreach`, `ai-motion-design`, `animated-video-production`, `charsheet-soul`, `codex`, `comfyui-video-production`, `content-engine`, `design-direction`, `digital-product`, `figma-designer`, `grok-imagine`, `handoff-prompt`, `imagegen-2`, `jotley-instagram-slides`, `linkedin-agent`, `llm-wiki`, `market-scout`, `meanizer`, `motion-design-harness`, `n8n`, `nano-banana`, `newsletter`, `opentalon-ticket`, `proof`, `push-to-main`, `skill-maker`, `substack`, `suno-song`, `surreal-music-art-film`, `talking-head-recut`, `teardown`, `textley-mcp`, `ugc-influencer-video`, `upwork-proposals`, `viral-unhinged-video-research`, `voice-narration`, `x-post-hooks`, `youtube-channel-system`

Private client, infrastructure, publishing and account workflows stay in our private inventory. No private memory or operating configuration is distributed here.

## License

Protomota’s published files are available under the [MIT license](LICENSE). Each linked project retains its own license.
