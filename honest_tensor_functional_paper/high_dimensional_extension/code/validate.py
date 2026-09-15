"""Validate existing saved results, source hashes, and preservation."""
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
            assert digest(ROOT / 'code' / source) == expected, f'Stale source: {source}'
    baseline = json.loads((ROOT / 'baseline_manifest.json').read_text())
    for source, expected in baseline['sha256'].items():
        assert digest(REPO / source) == expected, f'Previous stage changed: {source}'
    growing = json.loads((ROOT / 'results/growing_caps.json').read_text())['cases']
    pointwise = json.loads((ROOT / 'results/pointwise.json').read_text())['cases']
    loading = json.loads((ROOT / 'results/loading_rates.json').read_text())
    assert len(growing) == 36 and sum(x['repetitions'] for x in growing) == 7200
    assert len(pointwise) == 12 and sum(x['repetitions'] for x in pointwise) == 1900
    assert len(loading['loading_cases']) == 96 and len(loading['adaptation_obstructions']) == 8
    for row in pointwise:
        assert row['max_right_svd_entries'] <= row['input_entries']
        assert sum(row['choices'].values()) == row['repetitions']
        assert row['pilot_failure_budget'] == .05 * row['cap'] / (8 * row['p'])
        assert 0 <= row['covered'] <= row['repetitions']
    for pdf in ['paper/main.pdf', 'progress_report.pdf']:
        assert (ROOT / pdf).read_bytes().startswith(b'%PDF')
    log = (ROOT / 'results/theory_build.log').read_text()
    assert 'Undefined control sequence' not in log and 'undefined references' not in log
    report = (ROOT / 'progress_report.md').read_text()
    assert '7,200' in report and '1,900' in report
    result = dict(passed=True, preserved_files=len(baseline['sha256']), growing_trials=7200,
                  pointwise_trials=1900, loading_calculations=96, adaptation_comparisons=8,
                  largest_full_tensor_entries=max(x['input_entries'] for x in pointwise))
    (ROOT / 'results/validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
