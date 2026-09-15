"""Build the new standalone supplement and a source-grounded progress report."""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    growing = json.loads((ROOT / 'results/growing_caps.json').read_text())['cases']
    pointwise = json.loads((ROOT / 'results/pointwise.json').read_text())['cases']
    checks = json.loads((ROOT / 'results/checks.json').read_text())
    loading = json.loads((ROOT / 'results/loading_rates.json').read_text())
    n_growing = sum(x['repetitions'] for x in growing)
    n_pointwise = sum(x['repetitions'] for x in pointwise)
    report = r'''# Progress beyond the exponential benchmark

Status: 2026-09-12. This stage gives matching theory and polynomial
procedures in additional regimes, rather than extending the small
exponential optimizer. The general fixed-cap weak-signal computation
problem remains open. All previous-stage files are preserved.

## Main results

| Requested direction | New conclusion | Remaining limit |
|---|---|---|
| Efficient high-dimensional minimax computation | If the smallest cap $r\gtrsim\sqrt p$, a structural/direct interval attains sharp length $\min(M\sqrt{r/p},\tau)$ for every budget | Fixed and intermediate caps with diffuse weak signals remain open |
| Loading rates beyond small budgets | For fixed polynomial decay $\lvert w_i\rvert\le C\lvert w_1\rvert i^{-\beta}$, sharp length is $\lvert w_1\rvert\min(M,\tau)$ at every budget; a class of nonorthogonal perturbations is included | General profiles remain open; the matching block-fit construction is not an efficient optimizer |
| Growing-rank adaptation | Simultaneous minimax adaptation from growing outer caps to positive fixed inner caps is impossible | This is an impossibility for that objective, not a characterization of every adaptation opportunity |
| Pointwise inference | A polynomial cap-valid interval has optimal expected-length rate $\tau\sqrt{r/p}$ at strong diagonal Tucker means saturating their caps | Requires a conservative sufficient amplitude and norm slack; not optimal signal thresholds or leading constants |
| Computational limits | For power exponents $0<\beta<1/K$, a loading-compatible low-degree prior gives a polynomial gap from the new sharp estimation rate | Restricted polynomial-estimator result; no blanket hardness claim for efficient confidence intervals |

The growing-cap conclusion uses a previously proved sparse-diagonal
mixture and supplies its matching upper bound. The pointwise proof uses
the same outer honesty class for both bounds and controls the pilot
failure contribution with a budget shrinking as $r/p$. The loading proof
uses dyadic blocks with explicit error allocations and a summable decay
envelope. Complete supplied derivations are in
[theory/results.md](theory/results.md) and [the supplement](paper/main.pdf).
These results have not undergone independent mathematical review.

## Newly run growing-cap experiments

The interval reads only diagonal observations, so the experiment generates
exactly those independent Gaussian coordinates. It does not materialize the
unused off-diagonal noise. Coverage is proved for the full tensor class;
simulation uses zero and rank-cap boundary means. The largest loading
dimension is 16,384. The table shows its boundary cases; all dimensions and
zero cases are retained in `results/growing_caps.json`.

| $p$ | Cap $r$ | Structural radius / $\tau$ | Covered / trials | Coverage 95% Wilson interval | Mean length |
|---:|---:|---:|---:|---|---:|
'''
    for x in growing:
        if x['p'] == 16384 and x['signal'] == 'boundary':
            ci = x['coverage_wilson_95']
            h = x['M'] * (x['cap'] / x['p']) ** .5
            report += f"| {x['p']} | {x['cap']} | {h:.2f} | {x['covered']}/{x['repetitions']} | [{ci[0]:.3f}, {ci[1]:.3f}] | {x['mean_length']:.3f} |\n"
    report += f'''
There are {len(growing)} configurations and {n_growing:,} newly run trials.
The structural/direct choice is deterministic and the theoretical
worst-case squared-risk bound is saved alongside empirical squared error.
Finite Monte Carlo deviations are not used as proof of a uniform guarantee.

## Newly run pointwise experiments

These experiments generate the complete tensor observation, then make a
correctly scaled artificial split. No additional observed replicate is
assumed. The supplied cap is retained. In the strong rows, the signal
amplitude is eight times the theorem's conservative sufficient bound;
it ranges from approximately 60,000 at $p=8$ to 9.4 million at $p=64$,
with $\\tau=1$. These are deliberately very strong signals.

| $p$ | Cap $r$ | Covered / trials | Coverage 95% Wilson interval | Mean length | Mean time (ms) |
|---:|---:|---:|---|---:|---:|
'''
    for x in pointwise:
        if x['case'] == 'strong_saturated':
            ci = x['coverage_wilson_95']
            report += f"| {x['p']} | {x['cap']} | {x['covered']}/{x['repetitions']} | [{ci[0]:.3f}, {ci[1]:.3f}] | {x['mean_length']:.3f} | {1000*x['mean_seconds']:.2f} |\n"
    report += r'''
At rank one, the mean length decreases with dimension consistently with
the proved $p^{-1/2}$ scale. All strong saturated trials choose the
tangent option. Small sample counts at the largest dimensions produce
wide coverage uncertainty; those rows are runtime/behavior checks, not
high-precision coverage estimates.

The remaining cases test honesty outside the pointwise-optimality family:

| Case | $p$ | Cap | Covered / trials | Mean length | Chosen option |
|---|---:|---:|---:|---:|---|
'''
    for x in pointwise:
        if x['case'] != 'strong_saturated':
            choices = ', '.join(f'{key}: {value}' for key, value in x['choices'].items())
            report += f"| {x['case']} | {x['p']} | {x['cap']} | {x['covered']}/{x['repetitions']} | {x['mean_length']:.3f} | {choices} |\n"
    report += f'''
The pointwise suite has {len(pointwise)} configurations and {n_pointwise:,}
new trials. Conservative fallback is retained when actual rank is below
the supplied cap or weak additional components are present. This is
consistent with the limitation in the theorem, not a claim of full
actual-rank adaptation.

Economy SVDs remove an avoidable allocation from the preceding prototype.
For $64^3$ input, the largest returned right singular matrix has 262,144
entries, compared with 16,777,216 for a full right singular matrix: a
factor of 64 reduction in that array. This is an array-size comparison,
not a measured factor-of-64 reduction in total memory or runtime.

## Loading and adaptation calculations

There are {len(loading['loading_cases'])} new loading-envelope calculations
covering dimensions 64, 1,024 and 16,384, power exponents 0.1, 0.25, 0.5
and 1, orders three/four, and norm budgets from 0.1 to one million.
They evaluate the deterministic diameter of ideal block fits. They do
not numerically solve those fits or claim measured interval coverage.
The fixed-decay proof is uniform over budgets and dimensions; its
constants deteriorate as the decay exponent tends to zero.

Eight saved comparisons evaluate the growing-outer-cap lower bound
against the positive fixed-cap oracle rate. The proved divergence rules
out general simultaneous rate adaptation even for unlimited computation.
The weighted low-degree proof separately explains why a sharp statistical
loading rate need not yield a polynomial estimator.

## Verification and remaining work

Fresh checks passed: {checks['checks']['exact_hypergeometric_moments']} exact
hypergeometric likelihood moments, {checks['checks']['attained_structural_bounds']}
attained structural bounds, {checks['checks']['dyadic_profiles_and_tail_bounds']}
dyadic/tail bounds, {checks['checks']['pointwise_bias_and_allocation_cases']}
pointwise bias/allocation cases, {checks['checks']['economy_projection_equivalences']}
independent projection comparisons, {checks['checks']['weighted_low_degree_moments']}
weighted low-degree moment comparisons, and
{checks['checks']['strong_pointwise_geometry']} signed unknown-support
strong-signal checks. Seeds, actual software versions, source hashes,
coverage intervals, timing, and the previous-stage manifest are saved.

Still open are efficient minimax intervals for the original fixed-cap
diffuse weak-signal class, arbitrary loading geometry, intermediate
growing-cap rates, a full pointwise characterization, and optimal signal
thresholds for computation. The precise audit is in
[theory/audit.md](theory/audit.md); reproduction is in [README.md](README.md).
'''
    (ROOT / 'progress_report.md').write_text(report)
    with tempfile.TemporaryDirectory(prefix='tt-high-dimensional-') as temporary:
        source = Path(temporary) / 'theory.md'
        source.write_text((ROOT / 'theory/results.md').read_text().split('\n', 1)[1])
        subprocess.run(['pandoc', str(source), '-s', '-f', 'markdown+tex_math_dollars', '-t', 'latex',
                        '-o', str(ROOT / 'paper/main.tex'), '-M',
                        'title=Larger budgets, growing ranks, and pointwise tensor inference',
                        '-M', 'date=September 12, 2026', '-V', 'geometry:margin=0.85in', '-V', 'fontsize=10pt'], check=True)
    with (ROOT / 'results/theory_build.log').open('w') as log:
        subprocess.run(['latexmk', '-xelatex', '-interaction=nonstopmode', '-halt-on-error', 'main.tex'],
                       cwd=ROOT / 'paper', stdout=log, stderr=subprocess.STDOUT, check=True)
    (ROOT / 'paper/main.xdv').unlink(missing_ok=True)
    with (ROOT / 'results/report_build.log').open('w') as log:
        subprocess.run(['pandoc', 'progress_report.md', '-f', 'markdown+tex_math_dollars',
                        '-o', 'progress_report.pdf', '--pdf-engine=xelatex',
                        '-V', 'geometry:margin=0.85in', '-V', 'fontsize=10pt'],
                       cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True)
    print('Built theory supplement and progress report.')


if __name__ == '__main__':
    main()
