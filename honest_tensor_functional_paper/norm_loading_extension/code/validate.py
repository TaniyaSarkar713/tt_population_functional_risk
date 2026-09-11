"""Validate provenance, source links, builds, and saved finite checks; not proofs."""
import hashlib
import json
import platform
import re
from pathlib import Path

import numpy
import pypdf
import scipy

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    baseline = json.loads((ROOT / 'baseline_manifest.json').read_text())
    prior = (ROOT / baseline['source']).resolve()
    for name, expected in baseline['sha256'].items():
        require(digest(prior / name) == expected, 'Preserved baseline changed: ' + name)
    source = '\n'.join(p.read_text() for p in sorted((ROOT / 'paper').glob('*.tex')))
    labels = re.findall(r'\\label\{([^}]+)\}', source)
    refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', source)
    require(len(labels) == len(set(labels)), 'Duplicate labels')
    require(set(refs) <= set(labels), 'Undefined references: ' + str(set(refs) - set(labels)))
    counts = {kind: len(re.findall(r'\\begin\{' + kind + r'\}', source))
              for kind in ('theorem', 'proposition', 'lemma', 'proof')}
    require(counts == dict(theorem=15, proposition=11, lemma=9, proof=35), 'Unexpected result/proof counts: ' + str(counts))
    require(source.count('Roadmap.') == counts['proof'], 'A proof is missing its roadmap')
    log = (ROOT / 'paper/main.log').read_text()
    diagnostics = [line for line in log.splitlines() if re.search(r'undefined|Overfull|LaTeX Warning|Package natbib Warning|^!', line)]
    require(not diagnostics, 'LaTeX diagnostics: ' + str(diagnostics))
    pdf_pages = {}
    for name in ('paper/main.pdf', 'progress_report.pdf'):
        reader = pypdf.PdfReader(ROOT / name)
        require(len(reader.pages) > 0, 'Empty PDF: ' + name)
        require(all((page.extract_text() or '').strip() for page in reader.pages), 'Page has no text: ' + name)
        pdf_pages[name] = len(reader.pages)
    checks = json.loads((ROOT / 'results/theory_checks.json').read_text())
    require(checks['status'] == 'PASS', 'Finite checks did not pass')
    require(checks['source_sha256'] == digest(ROOT / 'code/check_theory.py'), 'Saved checks have stale source hash')
    links = 0
    generated = {ROOT / 'results/validation.json', ROOT / 'deliverable_manifest.json'}
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
            if target.startswith(('http:', 'https:', '#')):
                continue
            dest = (path.parent / target.split('#')[0]).resolve()
            require(dest in generated or dest.exists(), f'Broken link: {path.name} -> {target}')
            links += 1
    result = dict(status='PASS', scope='Artifact and provenance validation, not formal mathematical proof verification',
                  baseline_files_preserved=len(baseline['sha256']), result_counts=counts,
                  labels=len(labels), local_links=links, pdf_pages=pdf_pages, latex_diagnostics=diagnostics,
                  environment=dict(python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__, pypdf=pypdf.__version__))
    (ROOT / 'results/validation.json').write_text(json.dumps(result, indent=2) + '\n')
    manifest = {str(p.relative_to(ROOT)): digest(p) for p in sorted(ROOT.rglob('*'))
                if p.is_file() and p.suffix in {'.md', '.tex', '.bib', '.pdf', '.py', '.json'}
                and p.name != 'deliverable_manifest.json'}
    (ROOT / 'deliverable_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
