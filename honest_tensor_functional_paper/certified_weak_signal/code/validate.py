"""Read saved artifacts, check source provenance and preserved-stage integrity."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for name in ['checks.json', 'run_manifest.json']:
        saved = json.loads((ROOT / 'results' / name).read_text())
        for source, expected in saved['source_hashes'].items():
            assert digest(ROOT / 'code' / source) == expected, f'Stale result: {name}: {source}'
    baseline = json.loads((ROOT / 'baseline_manifest.json').read_text())
    for path, expected in baseline['sha256'].items():
        assert digest(REPO / path) == expected, f'Preserved stage changed: {path}'
    optimizer = json.loads((ROOT / 'results/optimizer_experiments.json').read_text())['cases']
    adaptation = json.loads((ROOT / 'results/adaptation_experiments.json').read_text())['cases']
    assert len(optimizer) == 8 and len(adaptation) == 8
    for row in optimizer:
        assert row['covered'] == sum(x['covered'] for x in row['trials'])
        assert row['certified_to_tolerance'] == sum(x['certified_to_tolerance'] for x in row['trials'])
        for trial in row['trials']:
            assert trial['lo'] <= trial['hi']
            if trial.get('inner_lo') is not None:
                assert trial['lo'] <= trial['inner_lo'] <= trial['inner_hi'] <= trial['hi']
            if trial['certified_to_tolerance']:
                assert trial['endpoint_gap'] <= .2 * row['tau'] + 1e-12
    for pdf in ['paper/main.pdf', 'progress_report.pdf']:
        assert (ROOT / pdf).read_bytes().startswith(b'%PDF')
    log = (ROOT / 'results/theory_build.log').read_text()
    assert 'Undefined control sequence' not in log and 'undefined references' not in log
    report = (ROOT / 'progress_report.md').read_text()
    assert '8,000' in report and '320' in report
    result = dict(passed=True, baseline_files=len(baseline['sha256']), optimizer_trials=320,
                  adaptation_trials=8000, optimizer_tolerance_met=sum(x['certified_to_tolerance'] for x in optimizer),
                  pdf_bytes={name: (ROOT / name).stat().st_size for name in ['paper/main.pdf', 'progress_report.pdf']})
    (ROOT / 'results/validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
