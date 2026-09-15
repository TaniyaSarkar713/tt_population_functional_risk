"""Read-only inventory of the submission package and preservation baseline."""
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parent.parent
PACKAGE=ROOT.parent

def dump(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def active_sources():
    main=PACKAGE/'robust_adaptive_extension/paper/main.tex'
    sources=[main]
    for name in re.findall(r'\\input\{([^}]+)\}',main.read_text()):
        sources.append(main.parent/name)
    for stage in ['certified_weak_signal','high_dimensional_extension']:
        sources.extend([PACKAGE/stage/'paper/main.tex',PACKAGE/stage/'theory/results.md'])
    sources.extend([PACKAGE/'empirical_study/report.md',PACKAGE/'empirical_study/manuscript/empirical_sections.md'])
    return list(dict.fromkeys(sources))

def main():
    sources=active_sources()
    baseline={}
    for p in PROJECT.rglob('*'):
        if not p.is_file() or ROOT in p.parents or any(part in ['.git','__pycache__','.DS_Store'] for part in p.parts):continue
        baseline[str(p.relative_to(PROJECT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    dest=ROOT/'logs/input_hashes.json'
    if dest.exists():
        if json.loads(dest.read_text())!=baseline:raise RuntimeError('Inputs changed; preserve the initial baseline.')
    else:dump(dest,baseline)
    dump(ROOT/'logs/active_sources.json',[str(p.relative_to(PROJECT)) for p in sources])
    inventory=[]
    for p in sources:
        text=p.read_text()
        if p.suffix=='.tex':
            pattern=r'\\begin\{(theorem|proposition|lemma|corollary)\}(?:\[([^\]]*)\])?(.*?)(?=\\end\{\1\})'
            for m in re.finditer(pattern,text,re.S):
                label=re.search(r'\\label\{([^}]+)\}',m.group(3))
                inventory.append(dict(source=str(p.relative_to(PROJECT)),line=text[:m.start()].count('\n')+1,
                    kind=m.group(1),title=m.group(2),label=label.group(1) if label else None,statement=m.group(3).strip()))
        elif p.name=='results.md':
            for m in re.finditer(r'^## ([A-Z]\d+)\. ([^\n]*)\n(.*?)(?=^## |\Z)',text,re.M|re.S):
                inventory.append(dict(source=str(p.relative_to(PROJECT)),line=text[:m.start()].count('\n')+1,
                    kind='supplement result',title=m.group(2),label=m.group(1),statement=m.group(3).strip()))
    dump(ROOT/'tables/theorem_inventory.json',inventory)
    terms=['innovative','pioneering','revolutionary paradigm','transformative framework','superior','surpass',
           'excel','remarkable','unprecedented','breakthrough performance','general-purpose','is capable of',
           'notably','yet','yielding','at its essence','encompass','differentiate','reveal','underscore',
           'pave the way for','highlight the potential of','profound challenges','stems from','rigid','impede']
    scan=[]
    for p in sources:
        for n,line in enumerate(p.read_text().splitlines(),1):
            hits=[t for t in terms if t in line.lower()]
            if '—' in line or (p.suffix=='.tex' and '---' in line):hits.append('em dash')
            if hits:scan.append(dict(source=str(p.relative_to(PROJECT)),line=n,terms=hits,text=line))
    dump(ROOT/'tables/style_scan.json',scan)
    print('Preserved baseline:',len(baseline),'files. Active sources:',len(sources),
          'result statements:',len(inventory),'style hits:',len(scan))

if __name__=='__main__':main()
