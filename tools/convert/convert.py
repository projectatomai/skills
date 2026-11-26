#!/usr/bin/env python3
"""Convert skills written for one agent into copies that read the same in Claude Code, Codex CLI and Gemini CLI.

    python3 tools/convert/convert.py --source-root <folder holding the cloned source repos> [--check]

What a conversion does, and nothing more:
  1. Rewrites the SKILL.md front matter to the open Agent Skills format (agentskills.io) and records where the
     skill came from.
  2. Puts a short note above the original text that tells any agent how to read Claude-only wording, and lists
     what the skill needs installed. The original text below the note is kept byte for byte.
  3. Replaces sandbox-only output paths in example files with paths that exist on any machine.
  4. Writes NOTICE.md with the source, the licence and every change made.

Every rule is mechanical, so the same source always gives the same output. `--check` converts into a temporary
folder and fails when the result differs from what is committed.
"""
from __future__ import annotations

import argparse
import filecmp
import hashlib
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

VERSION = '1'
HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT = REPO / 'converted'

TEXT_SUFFIXES = {'.md', '.py', '.js', '.mjs', '.cjs', '.ts', '.sh', '.txt', '.json', '.html', '.css', '.yaml', '.yml'}
NAME_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
FRONT_RE = re.compile(r'^---\r?\n(.*?)\r?\n---\r?\n', re.S)

# Front matter keys only Claude Code reads. They are dropped and listed in NOTICE.md.
CLAUDE_ONLY_KEYS = ['model', 'argument-hint', 'disable-model-invocation', 'user-invocable', 'context', 'agent', 'hooks', 'when_to_use', 'version']

# Python import name -> package to install. Imports not listed here install under their own name.
PIP_NAMES = {'PIL': 'pillow', 'pptx': 'python-pptx', 'yaml': 'pyyaml', 'cv2': 'opencv-python', 'docx': 'python-docx', 'bs4': 'beautifulsoup4', 'fitz': 'pymupdf', 'sklearn': 'scikit-learn'}
NODE_BUILTINS = {'fs', 'path', 'os', 'util', 'child_process', 'crypto', 'http', 'https', 'url', 'stream', 'zlib', 'events', 'assert', 'buffer', 'readline', 'process', 'module', 'worker_threads', 'perf_hooks'}

# Programs a skill calls: (label shown to the reader, pattern that shows the skill uses it).
PROGRAMS = [
    ('LibreOffice (`soffice`)', re.compile(r'\b(soffice|libreoffice)\b', re.I)),
    ('Poppler (`pdftoppm`)', re.compile(r'\b(pdftoppm|pdftotext|pdfimages|poppler)\b', re.I)),
    ('Pandoc', re.compile(r'\bpandoc\b')),
    ('FFmpeg', re.compile(r'\bffmpeg\b', re.I)),
    ('qpdf', re.compile(r'\bqpdf\b')),
    ('Tesseract', re.compile(r'\b(tesseract|pytesseract)\b', re.I)),
]

# Wording that only makes sense inside Claude: (key, pattern). Each one found adds a line to the note.
SIGNALS = [
    ('subagents', re.compile(r'\bsub-?agents?\b', re.I)),
    ('artifacts', re.compile(r'\bclaude\.ai\b|\b(HTML|interactive|single) artifacts?\b', re.I)),
    ('tools', re.compile(r'\b(str_replace|create_file|present_files|bash_tool|AskUserQuestion|TodoWrite)\b|\bview tool\b')),
    ('preinstalled', re.compile(r'\bpre-?installed\b', re.I)),
    ('claude', re.compile(r'\bClaude (should|will|can|must|may|is|has|reads|needs|does|interprets|uses|loads)\b|\b(next|another|future) Claude\b')),
]

# Sandbox paths that do not exist outside Claude's own sandbox -> a path that works anywhere.
PATH_RULES = [('/mnt/user-data/outputs/', './'), ('/mnt/user-data/uploads/', './')]
LEFTOVER_RE = re.compile(r'/mnt/user-data|/mnt/skills|/home/claude')

# Description wording that names one agent -> neutral wording.
DESCRIPTION_RULES = [
    (re.compile(r'\bClaude should use this skill\b'), 'Use this skill'),
    (re.compile(r'\bClaude (should|will|can|needs to)\b'), r'the agent \1'),
]


class ConvertError(Exception):
    pass


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_text(path: Path) -> str | None:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return None
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return None


def split_front(text: str, where: str) -> tuple[dict, str]:
    m = FRONT_RE.match(text)
    if not m:
        raise ConvertError(f'{where}: SKILL.md has no front matter')
    front = yaml.safe_load(m.group(1))
    if not isinstance(front, dict):
        raise ConvertError(f'{where}: front matter is not a mapping')
    return front, text[m.end():]


def python_imports(code: str) -> set[str]:
    found = set()
    for m in re.finditer(r'^[ \t]*(?:import|from)[ \t]+([A-Za-z_][A-Za-z0-9_]*)', code, re.M):
        found.add(m.group(1))
    return found


def node_imports(code: str) -> set[str]:
    found = set()
    for m in re.finditer(r'''(?:require\(|from[ \t]+|import[ \t]+)['"]([^'"\n]+)['"]''', code):
        name = m.group(1)
        if name.startswith(('.', '/', 'node:')):
            continue
        parts = name.split('/')
        found.add('/'.join(parts[:2]) if name.startswith('@') else parts[0])
    return found


def fenced(text: str, langs: tuple[str, ...]) -> str:
    return '\n'.join(m.group(2) for m in re.finditer(r'```([A-Za-z0-9_+-]*)[^\n]*\n(.*?)```', text, re.S) if m.group(1).lower() in langs)


NPM_NAME_RE = re.compile(r'^(@[a-z0-9~-][a-z0-9._~-]*/)?[a-z0-9~-][a-z0-9._~-]*$')
PIP_NAME_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]*$')


def installs(text: str, tool: str) -> set[str]:
    """Package names that follow `pip install` or `npm install` anywhere in a document."""
    found = set()
    for m in re.finditer(tool + r' install((?:[ \t]+[@A-Za-z0-9][A-Za-z0-9@/._~-]*)+)', text):
        found |= {w.rstrip('.') for w in m.group(1).split() if not w.startswith('-')}
    return found


def requirements(src: Path) -> dict:
    """What the skill needs on the machine: what its own scripts import, and what its written examples use."""
    script_py: set[str] = set()
    script_node: set[str] = set()
    doc_py: set[str] = set()
    doc_node: set[str] = set()
    runs_node = False
    everything = []
    for path in sorted(src.rglob('*')):
        if not path.is_file():
            continue
        text = read_text(path)
        if text is None:
            continue
        everything.append(text)
        suffix = path.suffix.lower()
        if suffix == '.py':
            # A name is the skill's own module when a file or folder of that name sits beside the script or above it.
            above = [d for d in path.parents if d == src or src in d.parents]
            script_py |= {n for n in python_imports(text) if not any((d / f'{n}.py').exists() or (d / n).is_dir() for d in above)}
        elif suffix in {'.js', '.mjs', '.cjs', '.ts'}:
            script_node |= node_imports(text)
            runs_node = runs_node or 'require(' in text or text.startswith('#!/usr/bin/env node')
        elif suffix == '.md':
            doc_py |= python_imports(fenced(text, ('python', 'py'))) | installs(text, 'pip')
            doc_node |= node_imports(text) | installs(text, 'npm')
    blob = '\n'.join(everything)
    stdlib = set(sys.stdlib_module_names)

    def py_names(found: set[str]) -> set[str]:
        return {PIP_NAMES.get(n, n) for n in found if n not in stdlib and not n.startswith('_') and PIP_NAME_RE.match(n)}

    def node_names(found: set[str]) -> set[str]:
        return {n for n in found if n not in NODE_BUILTINS and NPM_NAME_RE.match(n)}

    lower = lambda names: sorted(names, key=str.lower)  # noqa: E731
    spy, snode = py_names(script_py), node_names(script_node)
    own = {p.stem for p in src.rglob('*.py')} | {p.name for p in src.rglob('*') if p.is_dir()}
    dpy = {n for n in py_names(doc_py - own) if n.lower() not in {x.lower() for x in spy}}
    dnode = node_names(doc_node) - snode
    return {
        'script_py': lower(spy), 'script_node': lower(snode), 'doc_py': lower(dpy), 'doc_node': lower(dnode),
        'programs': [label for label, pattern in PROGRAMS if pattern.search(blob)],
        'python': bool(spy) or any(src.rglob('*.py')), 'node': bool(snode) or runs_node,
    }


def ticks(names: list[str]) -> str:
    return ', '.join(f'`{n}`' for n in names)


def needs_lines(req: dict) -> list[str]:
    """One line per kind of need, for the note. Empty when the skill is text only."""
    lines = []
    scripts = []
    if req['python']:
        scripts.append('Python 3' + (f" with {ticks(req['script_py'])}" if req['script_py'] else ''))
    if req['node']:
        scripts.append('Node.js' + (f" with {ticks(req['script_node'])}" if req['script_node'] else ''))
    if scripts:
        lines.append('**Its scripts need:** ' + '; '.join(scripts) + '.')
    examples = []
    if req['doc_py']:
        examples.append(f"Python packages {ticks(req['doc_py'])}")
    if req['doc_node']:
        examples.append(f"Node.js packages {ticks(req['doc_node'])}")
    if examples:
        lines.append('**Its written examples also use:** ' + '; '.join(examples) + '. Install only the ones a task calls for.')
    if req['programs']:
        lines.append('**Programs it calls:** ' + ', '.join(req['programs']) + '.')
    return lines


def needs_short(req: dict) -> str:
    """The same needs as one plain phrase, for the front matter and the index."""
    parts = []
    if req['python']:
        parts.append('Python 3' + (f" with {', '.join(req['script_py'])}" if req['script_py'] else ''))
    if req['node']:
        parts.append('Node.js' + (f" with {', '.join(req['script_node'])}" if req['script_node'] else ''))
    parts += [re.sub(r'[`]', '', p) for p in req['programs']]
    if req['doc_py'] or req['doc_node']:
        parts.append('more packages for some tasks (see the note in SKILL.md)')
    return '; '.join(parts)


def signals(src: Path) -> set[str]:
    found = set()
    for path in sorted(src.rglob('*.md')):
        text = read_text(path) or ''
        for key, pattern in SIGNALS:
            if pattern.search(text):
                found.add(key)
    return found


def note(source: dict, name: str, sig: set[str], needs: list[str], bundled: bool) -> str:
    url = f"https://github.com/{source['repo']}/tree/{source['commit']}/{source['path']}/{name}"
    lines = [
        f"> **Skillfarm multi-agent version.** Converted from [{source['repo']}]({url}) by {source['maker']} so it reads the same in Claude Code, Codex CLI and Gemini CLI. "
        'The original text follows this note unchanged. NOTICE.md lists every change.',
        '>',
        '> How to read it, whichever agent you are:',
    ]
    if 'claude' in sig:
        lines.append('> - Where it says "Claude", it means you, the agent running this skill.')
    if 'subagents' in sig:
        lines.append('> - Where it asks for subagents and you cannot start any, do those steps yourself, one at a time.')
    if 'artifacts' in sig:
        lines.append('> - Where it says "artifact" or claude.ai, write the result to a file in the working folder and tell the person its path.')
    if 'tools' in sig:
        lines.append('> - Tool names in the text are Claude\'s. Use your own tool for the same job, and ask questions in plain chat.')
    if 'preinstalled' in sig or needs:
        lines.append('> - It was written for a sandbox with its tools already installed. Here, check that what it needs is present before you start, and ask the person before you install anything.')
    if bundled:
        lines.append("> - File paths in the text are relative to this skill's folder.")
    if len(lines) == 3:
        lines[2] = '> It needs nothing changed to run in any of the three.'
    for line in needs:
        lines += ['>', f'> {line}']
    return '\n'.join(lines) + '\n'


def dump_front(front: dict) -> str:
    return yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=100, default_flow_style=False)


def convert_skill(source: dict, src: Path, dst: Path) -> dict:
    name = src.name
    where = f"{source['repo']}/{name}"
    if not NAME_RE.match(name) or len(name) > 64:
        raise ConvertError(f'{where}: folder name is not a valid skill name')
    licence_file = next((p for p in sorted(src.iterdir()) if p.is_file() and p.name.lower().startswith('license')), None)
    if licence_file is None:
        raise ConvertError(f'{where}: no licence file in the skill folder')
    original = (src / 'SKILL.md').read_text(encoding='utf-8')
    front, body = split_front(original, where)
    changes: list[str] = []

    if front.get('name') != name:
        raise ConvertError(f"{where}: front matter name {front.get('name')!r} does not match its folder")
    description = ' '.join(str(front.get('description') or '').split())
    if not description:
        raise ConvertError(f'{where}: no description')
    new_description = description
    for pattern, repl in DESCRIPTION_RULES:
        new_description = pattern.sub(repl, new_description)
    if new_description != description:
        changes.append('SKILL.md: description reworded so it names no single agent. It read: "' + description + '"')
    if len(new_description) > 1024:
        raise ConvertError(f'{where}: description is {len(new_description)} characters, over the 1,024 limit')

    bundled = any(p.is_file() and p.name != 'SKILL.md' and p != licence_file for p in src.rglob('*'))
    req = requirements(src)
    needs = needs_lines(req)
    short = needs_short(req)
    sig = signals(src)

    shutil.copytree(src, dst)
    changed_files: set[str] = {'SKILL.md'}
    for path in sorted(dst.rglob('*')):
        if not path.is_file() or path.name == 'SKILL.md':
            continue
        text = read_text(path)
        if text is None:
            continue
        new = text
        count = 0
        for old, repl in PATH_RULES:
            count += new.count(old)
            new = new.replace(old, repl)
        if count:
            rel = path.relative_to(dst).as_posix()
            if path.suffix in {'.py', '.sh'}:
                marker = '# Changed by Skillfarm: sandbox output paths now point at the working folder. See NOTICE.md.\n'
                new = (new.split('\n', 1)[0] + '\n' + marker + new.split('\n', 1)[1]) if new.startswith('#!') else marker + new
            path.write_text(new, encoding='utf-8')
            changed_files.add(rel)
            changes.append(f'{rel}: sandbox path `/mnt/user-data/...` replaced with `./` in {count} place{"s" if count != 1 else ""}, and a comment added saying so.')

    out_front: dict = {'name': name, 'description': new_description}
    out_front['license'] = f"{source['license']}. Complete terms in {licence_file.name}"
    compat = 'Converted by Skillfarm to read the same in Claude Code, Codex CLI and Gemini CLI.'
    if short:
        compat += ' Needs ' + short + '.'
    if front.get('compatibility'):
        compat = str(front['compatibility']).strip() + ' ' + compat
    if len(compat) > 500:
        compat = compat[:497].rsplit(' ', 1)[0] + '...'
    out_front['compatibility'] = compat
    if 'allowed-tools' in front:
        out_front['allowed-tools'] = front['allowed-tools']
    metadata = {str(k): str(v) for k, v in (front.get('metadata') or {}).items()} if isinstance(front.get('metadata'), dict) else {}
    metadata.update({
        'source': f"https://github.com/{source['repo']}/tree/{source['commit']}/{source['path']}/{name}",
        'source-commit': source['commit'],
        'original-author': source['maker'],
        'converted-by': 'Skillfarm (https://skillfarm.ai)',
        'converter-version': VERSION,
    })
    out_front['metadata'] = metadata
    dropped = [k for k in front if k in CLAUDE_ONLY_KEYS]
    unknown = [k for k in front if k not in {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'} and k not in CLAUDE_ONLY_KEYS]
    if unknown:
        raise ConvertError(f'{where}: front matter has keys the converter does not know: {", ".join(unknown)}')

    changes.insert(0, 'SKILL.md: front matter rewritten to the open Agent Skills format. The licence line now names the licence, and `compatibility` and `metadata` (source, commit, author, converter) were added.'
                   + (f' Dropped keys only Claude Code reads: {", ".join(dropped)}.' if dropped else ''))
    changes.insert(1, 'SKILL.md: a note was added above the original text. It says this is a modified copy, tells any agent how to read Claude-only wording' + (', and lists what the skill needs installed.' if needs else '.'))
    (dst / 'SKILL.md').write_text('---\n' + dump_front(out_front) + '---\n\n' + note(source, name, sig, needs, bundled) + body, encoding='utf-8')

    same = sum(1 for p in src.rglob('*') if p.is_file() and p.relative_to(src).as_posix() not in changed_files)
    notice = [
        '# Notice',
        '',
        f'This folder is a modified copy of the skill `{name}` by {source["maker"]}.',
        '',
        f"- Original: https://github.com/{source['repo']}/tree/{source['commit']}/{source['path']}/{name}",
        f"- Licence: {source['license_name']}. The full text is in {licence_file.name}, unchanged.",
        f'- Copyright stays with the original authors. Protomota and Skillfarm claim no ownership of the original work, and {source["maker"]} has not reviewed or endorsed this copy.',
        f'- Converted by Skillfarm (https://skillfarm.ai) with `tools/convert` version {VERSION}, so the skill reads the same in Claude Code, Codex CLI and Gemini CLI.',
    ]
    if source.get('third_party_notices'):
        notice.append(f"- The original repo's third-party notices are kept beside this folder, in `converted/{third_party_name(source)}`.")
    notice += ['', '## Changes from the original', ''] + [f'- {c}' for c in changes] + ['- NOTICE.md: added.', '', f'The text of SKILL.md below the note, and the other {same} file{"s" if same != 1 else ""}, are byte for byte the same as the original.', '']
    (dst / 'NOTICE.md').write_text('\n'.join(notice), encoding='utf-8')
    return {'name': name, 'description': new_description, 'needs': short, 'changed': sorted(changed_files), 'files': same + len(changed_files) + 1}


def third_party_name(source: dict) -> str:
    return 'THIRD_PARTY_NOTICES-' + source['repo'].replace('/', '-') + '.md'


def validate(source: dict, src: Path, dst: Path) -> list[str]:
    """Checks on one converted skill. Returns a list of problems, empty when it is sound."""
    problems = []
    name = dst.name
    text = (dst / 'SKILL.md').read_text(encoding='utf-8')
    try:
        front, body = split_front(text, name)
    except ConvertError as e:
        return [str(e)]
    if front.get('name') != name or not NAME_RE.match(name):
        problems.append('name does not match the folder')
    if not (1 <= len(front.get('description', '')) <= 1024):
        problems.append('description is empty or over 1,024 characters')
    if len(front.get('compatibility', '')) > 500:
        problems.append('compatibility is over 500 characters')
    if not all(isinstance(v, str) for v in front.get('metadata', {}).values()):
        problems.append('metadata values must be text')
    _, original_body = split_front((src / 'SKILL.md').read_text(encoding='utf-8'), name)
    if not body.endswith(original_body):
        problems.append('the original SKILL.md text is not intact below the note')
    for path in src.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(src)
        twin = dst / rel
        if not twin.is_file():
            problems.append(f'missing file {rel.as_posix()}')
        elif rel.as_posix() != 'SKILL.md' and sha(path) != sha(twin):
            new = read_text(twin) or ''
            if 'Changed by Skillfarm' not in new:
                problems.append(f'{rel.as_posix()} differs from the original without a change notice')
    for path in dst.rglob('*'):
        if path.is_file() and path.name != 'NOTICE.md':
            t = read_text(path)
            if t and LEFTOVER_RE.search(t):
                problems.append(f'{path.relative_to(dst).as_posix()} still has a sandbox-only path')
    for m in re.finditer(r'\]\(([^)#\s]+)(?:#[^)]*)?\)', body):
        target = m.group(1)
        if re.match(r'^[a-z][a-z0-9+.-]*:', target) or target.startswith('/'):
            continue
        if not (dst / target).exists():
            problems.append(f'SKILL.md links to {target}, which is not in the folder')
    if not (dst / 'NOTICE.md').is_file():
        problems.append('NOTICE.md is missing')
    return problems


def index(results: list[dict], skipped: list[dict]) -> str:
    lines = [
        '# Converted skills',
        '',
        'Skills written for one agent, converted by [Skillfarm](https://skillfarm.ai) so they read the same in Claude Code, Codex CLI and Gemini CLI.',
        'Each folder is a modified copy of someone else\'s work, used under its licence. The original author keeps the credit and the copyright, and each folder\'s NOTICE.md links to the original and lists every change.',
        '',
        'The conversion is mechanical and small on purpose: the front matter moves to the open [Agent Skills](https://agentskills.io/specification) format, a short note tells any agent how to read Claude-only wording and what the skill needs installed, and sandbox-only paths are replaced. The author\'s own text is kept as it was. The converter is in [`tools/convert`](../tools/convert).',
        '',
        '## Install one',
        '',
        '```sh',
        'npx skills add https://github.com/protomota/skills/tree/main/converted/<name> -a claude-code -g -y',
        '```',
        '',
        'Use `-a codex` or `-a gemini-cli` for the other agents.',
        '',
        '## What is here',
        '',
        '| Skill | Original | Licence | Needs |',
        '|---|---|---|---|',
    ]
    for r in results:
        s = r['source']
        lines.append(f"| [{r['name']}]({r['name']}/SKILL.md) | [{s['repo']}](https://github.com/{s['repo']}/tree/{s['commit']}/{s['path']}/{r['name']}) by {s['maker']} | {s['license']} | {r['needs'] or 'Nothing extra'} |")
    if skipped:
        lines += ['', '## Not converted', '', 'These stay as links to the original, with the reason.', '', '| Skill | Original | Why |', '|---|---|---|']
        for k in skipped:
            s = k['source']
            lines.append(f"| {k['name']} | [{s['repo']}](https://github.com/{s['repo']}/tree/{s['commit']}/{s['path']}/{k['name']}) | {k['why']} |")
    return '\n'.join(lines) + '\n'


def run(source_root: Path, out: Path) -> tuple[list[dict], list[dict], list[str]]:
    sources = yaml.safe_load((HERE / 'sources.yaml').read_text(encoding='utf-8'))
    results, skipped, problems = [], [], []
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for source in sources:
        root = source_root / source['checkout'] / source['path']
        if not root.is_dir():
            raise ConvertError(f"{source['repo']}: {root} not found. Clone the repo at commit {source['commit']} first.")
        skip = source.get('skip') or {}
        for src in sorted(p for p in root.iterdir() if (p / 'SKILL.md').is_file()):
            if src.name in skip:
                skipped.append({'name': src.name, 'why': skip[src.name], 'source': source})
                continue
            dst = out / src.name
            if dst.exists():
                raise ConvertError(f'{src.name}: two sources convert to the same name')
            r = convert_skill(source, src, dst)
            r['source'] = source
            results.append(r)
            problems += [f"{src.name}: {p}" for p in validate(source, src, dst)]
        if source.get('third_party_notices'):
            shutil.copyfile(source_root / source['checkout'] / source['third_party_notices'], out / third_party_name(source))
    (out / 'README.md').write_text(index(results, skipped), encoding='utf-8')
    return results, skipped, problems


def same_tree(a: Path, b: Path) -> bool:
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    _, mismatch, errors = filecmp.cmpfiles(a, b, cmp.common_files, shallow=False)
    return not mismatch and not errors and all(same_tree(a / d, b / d) for d in cmp.common_dirs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--source-root', required=True, type=Path, help='folder that holds the cloned source repos named in sources.yaml')
    ap.add_argument('--check', action='store_true', help='convert into a temporary folder and fail if it differs from converted/')
    args = ap.parse_args()
    try:
        if args.check:
            with tempfile.TemporaryDirectory() as tmp:
                results, skipped, problems = run(args.source_root, Path(tmp) / 'converted')
                if not same_tree(Path(tmp) / 'converted', OUT):
                    problems.append('converted/ is out of date: run the converter again and commit the result')
        else:
            results, skipped, problems = run(args.source_root, OUT)
    except ConvertError as e:
        print(f'error: {e}', file=sys.stderr)
        return 2
    for r in results:
        print(f"converted  {r['name']:<24} {r['files']:>3} files  needs: {r['needs'] or '-'}")
    for k in skipped:
        print(f"skipped    {k['name']:<24} {k['why']}")
    for p in problems:
        print(f'PROBLEM    {p}', file=sys.stderr)
    print(f'{len(results)} converted, {len(skipped)} skipped, {len(problems)} problems')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
