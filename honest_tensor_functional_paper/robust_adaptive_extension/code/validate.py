"""Check provenance, source/result consistency, links, and PDF builds."""
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


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    baseline = json.loads((ROOT / 'baseline_manifest.json').read_text())
    prior = (ROOT / baseline['source']).resolve()
    for name, expected in baseline['sha256'].items():
        require(digest(prior / name) == expected, 'Previous stage changed: ' + name)
    source = '\n'.join(p.read_text() for p in sorted((ROOT / 'paper').glob('*.tex')))
    labels = re.findall(r'\\label\{([^}]+)\}', source)
    refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', source)
    require(len(labels) == len(set(labels)), 'Duplicate labels')
    require(set(refs) <= set(labels), 'Missing references: ' + str(set(refs) - set(labels)))
    counts = {k: len(re.findall(r'\\begin\{' + k + r'\}', source)) for k in ['theorem', 'proposition', 'lemma', 'proof']}
    require(counts == dict(theorem=21, proposition=15, lemma=9, proof=45), 'Unexpected result/proof count: ' + str(counts))
    require(source.count('Roadmap.') == 45, 'Missing proof roadmaps')
    log = (ROOT / 'paper/main.log').read_text()
    diagnostics = [line for line in log.splitlines() if re.search(r'undefined|Overfull|LaTeX Warning|Package natbib Warning|^!', line)]
    require(not diagnostics, 'LaTeX diagnostics: ' + str(diagnostics))
    pages = {}
    for name in ['paper/main.pdf', 'progress_report.pdf']:
        reader = pypdf.PdfReader(ROOT / name)
        require(all((page.extract_text() or '').strip() for page in reader.pages), 'Empty PDF page: ' + name)
        pages[name] = len(reader.pages)
    experiments = json.loads((ROOT / 'results/experiment_run.json').read_text())
    for name, expected in experiments['sources'].items():
        require(digest(ROOT / 'code' / name) == expected, 'Stale experiment code: ' + name)
    checks = json.loads((ROOT / 'results/theory_checks.json').read_text())
    require(checks['status'] == 'PASS', 'Finite checks failed')
    require(checks['source_sha256'] == digest(ROOT / 'code/check_extensions.py'), 'Stale finite-check source')
    sizes = dict(adaptive_intervals=54, general_loadings=36, robust_full_scan=4, approximate_ranks=12)
    for name, size in sizes.items():
        rows = json.loads((ROOT / 'results' / (name + '.json')).read_text())
        require(len(rows) == size, 'Missing experiment configurations: ' + name)
        for row in rows:
            for value in row.values():
                if isinstance(value, dict) and 'successes' in value:
                    require(value['successes'] / value['repetitions'] == value['rate'], 'Inconsistent proportion')
                    require(value['ci95'][0] <= value['rate'] <= value['ci95'][1], 'Invalid binomial interval')
    summary = json.loads((ROOT / 'results/experiment_summary.json').read_text())
    require(summary['total_monte_carlo_repetitions'] == 76600, 'Incorrect experiment total')
    links = 0
    generated = {ROOT / 'results/validation.json', ROOT / 'deliverable_manifest.json'}
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
            if target.startswith(('https:', 'http:', '#')):
                continue
            dest = (path.parent / target.split('#')[0]).resolve()
            require(dest in generated or dest.exists(), 'Broken link: ' + str(path) + ' -> ' + target)
            links += 1
    result = dict(status='PASS', scope='Artifact/provenance validation, not independent mathematical review',
                  baseline_files_preserved=len(baseline['sha256']), result_counts=counts,
                  labels=len(labels), local_links=links, pdf_pages=pages, latex_diagnostics=diagnostics,
                  experiment_configurations=sum(sizes.values()), monte_carlo_repetitions=76600,
                  environment=dict(python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__, pypdf=pypdf.__version__))
    (ROOT / 'results/validation.json').write_text(json.dumps(result, indent=2) + '\n')
    manifest = {str(p.relative_to(ROOT)): digest(p) for p in sorted(ROOT.rglob('*'))
                if p.is_file() and p.suffix in {'.md', '.tex', '.bib', '.pdf', '.png', '.py', '.json'}
                and p.name != 'deliverable_manifest.json'}
    (ROOT / 'deliverable_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
