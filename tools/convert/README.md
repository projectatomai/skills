# The converter

Turns skills written for one agent into copies that read the same in Claude Code, Codex CLI and Gemini CLI. The copies live in [`converted/`](../../converted).

## What it changes

1. **Front matter.** Rewritten to the open [Agent Skills](https://agentskills.io/specification) format: the licence by name, a `compatibility` line, and `metadata` that records the source repo, the exact commit and the original author. Keys only Claude Code reads are dropped.
2. **A note above the original text.** It says the folder is a modified copy, tells any agent how to read Claude-only wording (subagents, artifacts, Claude's tool names), and lists what the skill needs installed. The needs are read from the skill itself: what its scripts import, what its written examples use, and which programs it calls.
3. **Sandbox paths.** Output paths that only exist in Claude's own sandbox are replaced with the working folder, and the changed file says so in a comment.
4. **NOTICE.md.** The source link, the licence and a list of every change.

The author's own text is kept byte for byte, and the converter checks that after every run. A skill is skipped, and stays a link to the original, when it has no licence file, when its subject is a Claude-only product, or when making it work elsewhere would need a rewrite by hand.

## Run it

```sh
# clone each source repo named in sources.yaml into one folder, at the pinned commit
git clone https://github.com/anthropics/skills.git sources/anthropics_skills
git -C sources/anthropics_skills checkout e4bb5d960d87126ff3b3a8af1a104b7db67560ba

python3 tools/convert/convert.py --source-root sources          # rebuild converted/
python3 tools/convert/convert.py --source-root sources --check  # fail if converted/ is out of date or unsound
```

It needs Python 3.10 or later with `pyyaml`. The same sources always give the same output.

## Add a source

Add an entry to `sources.yaml` with the repo, the commit, the folder that holds the skills, the maker and the licence. Only add work whose licence allows sharing changed copies, and list anything that should stay a link under `skip` with the reason.
