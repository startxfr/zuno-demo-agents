#!/usr/bin/env python3
"""Build the agent-bundle report: one self-contained HTML page.

    generate.py [REPO_ROOT] OUT.html     build the page and print the drift report
    generate.py [REPO_ROOT] --rehash     record the current prompt hashes in assets/rules.py

Everything is parsed from agents/<name>/ (agent.okf.md, tasks/, prompts/, tools/,
rag/) except the rules in assets/rules.py, which are hand-written paraphrases of
the prompts. Documentation is never read.
"""
import hashlib, json, pathlib, re, sys

sys.dont_write_bytecode = True  # rules.py is rewritten by --rehash; a stale .pyc would hide it

import yaml

SKILL = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / 'assets'))
import rules as RU  # noqa: E402


def split(path):
    parts = path.read_text(encoding='utf-8').split('---', 2)
    return (yaml.safe_load(parts[1]) or {}), (parts[2].strip() if len(parts) > 2 else '')


def prompt_hash(agent_dir, task):
    h = hashlib.sha256()
    for p in sorted((agent_dir / 'prompts').glob(task + '*.md')):
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def parse_tool(name, fm):
    z = fm.get('zuno', {})
    lim = ' | '.join(z.get('known_limitations', []))
    access = 'write' if re.search(r'Write access|Access: write', lim) else 'read'
    mm = (re.search(r'min_classification[ (]*(C\d)', lim) or re.search(r'Data classification (C\d)', lim)
          or re.search(r'treated as (C\d)', lim))
    g = re.search(r'allowed_groups: ([^.|]*)', lim) or re.search(r'Allowed groups: ([^.|(]*)', lim)
    groups = [x.strip() for x in g.group(1).split(',')] if g else []
    if 'ocp-ai-ops only' in lim:
        groups = ['ocp-ai-ops']
    return {'name': name, 'canon': RU.CANON.get(name, name), 'access': access,
            'cls': mm.group(1) if mm else None, 'groups': groups,
            'local': bool(re.search(r'allow_context false|local models only|stay on local models', lim)),
            'live': bool(z.get('live_read')), 'usage': z.get('usage_notes', ''),
            'limits': z.get('known_limitations', [])}


def build(root):
    agents, warnings = [], []
    dirs = sorted(p for p in (root / 'agents').iterdir() if (p / 'agent.okf.md').exists())
    names = [p.name for p in dirs]
    # active agents first, then in a stable order
    def key(p):
        fm, _ = split(p / 'agent.okf.md')
        return (fm['zuno']['status'] != 'active', p.name)
    for p in sorted(dirs, key=key):
        a = p.name
        fm, _ = split(p / 'agent.okf.md')
        z = fm['zuno']
        tools = {}
        for f in sorted((p / 'tools').glob('*.md')) if (p / 'tools').is_dir() else []:
            tools[f.stem] = parse_tool(f.stem, split(f)[0])
        tasks = []
        for t in z['tasks']:
            tf = split(p / 'tasks' / f'{t}.md')[0]
            tz = tf['zuno']
            rules = RU.R.get(f'{a}/{t}', [])
            if not rules:
                warnings.append(f'no rules written for {a}/{t}')
            want, have = prompt_hash(p, t), RU.PROMPT_SHA.get(f'{a}/{t}')
            if have is None:
                warnings.append(f'{a}/{t}: no recorded prompt hash (new task?)')
            elif have != want:
                warnings.append(f'{a}/{t}: prompt changed since its rules were written, re-read it')
            tl = []
            for n in tz.get('allowed_tools', []):
                if n not in tools:
                    warnings.append(f'{a}/{t}: tool {n} has no note in the bundle (shown hollow)')
                tl.append({'name': n, 'canon': RU.CANON.get(n, n), 'noted': n in tools})
            tasks.append({
                'id': t, 'title': tf['title'], 'desc': tf['description'], 'primary': t == z.get('primary_task'),
                'tools': tl, 'knowledge': tz.get('allowed_knowledge', []), 'live': tz.get('live_read_tool'),
                'maxTokens': tz.get('max_tokens'), 'models': (tz.get('models') or {}).get('preferred', []),
                'projectRequired': bool(tz.get('project_required')),
                'reflect': ((tz.get('prompts') or {}).get('reflect') or {}).get('classification_ceiling'),
                'examples': tz.get('prompt_examples', []), 'rules': rules})
            for k in tz.get('allowed_knowledge', []):
                if k not in RU.DOMAIN:
                    warnings.append(f'knowledge domain {k} has no description in assets/rules.py')
        if a not in RU.AGENT_RULES:
            warnings.append(f'no agent-level rules written for {a}')
        mem = z.get('memory', {}).get('history') or z.get('limits', {}).get('memory', {}).get('history')
        agents.append({
            'id': a, 'name': fm['title'], 'desc': fm['description'], 'status': z['status'],
            'shape': z.get('graph_shape'), 'cls': z['model']['preferred_classification'],
            'localOnly': bool(z['model'].get('local_only')), 'modelNote': z['model'].get('notes', ''),
            'groups': z['access']['groups'], 'color': z['ui']['color'], 'icon': z['ui']['icon'],
            'tile': z['ui']['tileDescription'], 'version': (p / 'VERSION').read_text().strip(),
            'memory': mem, 'delegation': (z.get('delegation', {}).get('targets') or []),
            'guardrails': (z.get('guardrails') or {}).get('mode'), 'topK': (z.get('rag') or {}).get('top_k'),
            'tools': tools, 'tasks': tasks, 'rules': RU.AGENT_RULES.get(a, [])})
    for a in RU.AGENT_RULES:
        if a not in names:
            warnings.append(f'rules for {a} but no such bundle (removed?)')
    release = 'v' + (root / 'VERSION').read_text().strip()
    return {'agents': agents, 'domains': RU.DOMAIN, 'release': release}, warnings


def rehash(root):
    path = SKILL / 'assets' / 'rules.py'
    src = path.read_text()
    sha = {}
    for p in sorted((root / 'agents').iterdir()):
        for t in sorted((p / 'tasks').glob('*.md')) if (p / 'tasks').is_dir() else []:
            if t.name != 'README.md':
                sha[f'{p.name}/{t.stem}'] = prompt_hash(p, t.stem)
    src = src[:src.index('PROMPT_SHA = ')] + 'PROMPT_SHA = ' + json.dumps(sha, indent=1) + '\n'
    path.write_text(src)
    print(f'recorded {len(sha)} prompt hashes in {path}')


def main():
    args = [x for x in sys.argv[1:] if x != '--rehash']
    root = pathlib.Path(args[0]) if len(args) == 2 or (len(args) == 1 and '--rehash' in sys.argv) else pathlib.Path.cwd()
    if '--rehash' in sys.argv:
        return rehash(root)
    out = pathlib.Path(args[-1])
    data, warnings = build(root)
    tpl = (SKILL / 'assets' / 'template.html').read_text()
    assert tpl.count('/*DATA*/null') == 1, 'template placeholder missing'
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    out.write_text(tpl.replace('/*DATA*/null', blob), encoding='utf-8')
    print(f'wrote {out} ({out.stat().st_size // 1024} KB), release {data["release"]}')
    for a in data['agents']:
        print(f'  {a["id"]:<10} {a["status"]:<11} {a["cls"]}  {len(a["tasks"])} tasks  {len(a["tools"])} tool notes')
    print('DRIFT REPORT' if warnings else 'No drift: every task has rules and an unchanged prompt.')
    for w in warnings:
        print('  -', w)


if __name__ == '__main__':
    main()
