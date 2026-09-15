"""Generate a concise results report and the standalone theory supplement."""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    optimizer = json.loads((ROOT / 'results/optimizer_experiments.json').read_text())['cases']
    adaptation = json.loads((ROOT / 'results/adaptation_experiments.json').read_text())['cases']
    checks = json.loads((ROOT / 'results/checks.json').read_text())
    n_opt = sum(x['repetitions'] for x in optimizer)
    n_adapt = sum(x['repetitions'] for x in adaptation)
    n_cert = sum(x['certified_to_tolerance'] for x in optimizer)
    report = '''# Progress on the remaining weak-signal problems

Status: 2026-09-11. The work supplies a global computational benchmark and
narrows the loading/adaptation questions. It does **not** solve all three
general open problems. Earlier manuscripts and numerical results are preserved.

## What is established

1. The ideal finite-net residual criterion is implemented on the complete
   continuous binary rank-one tensor ball. A global lower/upper objective
   bracket distinguishes an approximately optimal fit from a local solution.
   Confidence-set projection returns safe outer endpoints and feasible inner
   witnesses, with an explicit gap and budget status. This is an exponential
   benchmark, not a high-dimensional efficient optimizer.
2. For every loading tensor, fixed positive caps, and $M\\le\\tau$, minimax
   interval length is of order $M\\rho(L)$ and squared risk is of order
   $M^2\\rho(L)^2$, where $\\rho(L)$ is the best unit product overlap.
   Computing that overlap need not be efficient. Unequal orthogonal weights
   additionally have an implemented optimized-prior mixture lower bound.
3. The existing ideal outer interval already adapts in minimax **rate** to
   every smaller positive fixed-cap class, without separation. This follows
   because all those classes share the rank-one lower bound. It does not
   resolve rank-dependent constants, growing caps, or pointwise oracle lengths.
4. A new supplied-cap tangent interval stays honest at zero and arbitrarily
   weak signals. Unresolved singular values receive a worst-case angle bound.
   Correctly calibrated artificial splitting and a simultaneous direct
   interval implement it in the original single-observation experiment.
   Strong signals can shorten it; weak-signal minimax optimality is unproved.

Complete statements and proofs are in [theory/results.md](theory/results.md)
and [the technical supplement](paper/main.pdf). The [audit](theory/audit.md)
separates proved regimes, numerical certificates, and remaining requirements.

## Newly run optimizer experiments

All supports and 1,002 calibrated scan constraints were used for
order three and mode size two. The optimization parameter space is continuous.
The stopping tolerance is $0.2\\tau$, with 600 branch expansions per trial.
Intervals reported below always use the outer bounds, including budget stops.

| Signal | Loading | Covered / trials | Coverage 95% Wilson interval | Endpoint gap certified to tolerance | Mean outer length | Mean nodes |
|---|---|---:|---|---:|---:|---:|
'''
    for x in optimizer:
        ci = x['coverage_wilson_95']
        report += f"| {x['case']} | {x['loading']} | {x['covered']}/{x['repetitions']} | [{ci[0]:.3f}, {ci[1]:.3f}] | {x['certified_to_tolerance']}/{x['repetitions']} | {x['mean_width']:.3f} | {x['mean_nodes']:.1f} |\n"
    report += f'''
There are {n_opt} new optimizer trials, with {n_cert} meeting the endpoint
tolerance. The strong-signal cases hit the short node budget; their wider
outer intervals remain the reported result. Full coverage in these finite
trials is not a proof of uniform coverage. The small dimensions and conservative
union thresholds do not establish a useful high-dimensional minimax gain.

Independent analytic checks include a one-atom residual minimum with known
exact value, the exact structural support of a flat binary loading, a
certified empty confidence set, and a positive non-rank-one residual optimum.
The latter has global bracket
[{checks['optimizer_examples']['incompatible_fit']['lower']:.6f},
{checks['optimizer_examples']['incompatible_fit']['upper']:.6f}].
An intentional one-node stop verifies that incomplete endpoint optimization
is not silently presented as a completed optimizer.

## Newly run original-model adaptation experiments

Each trial starts with one $4\\times4\\times4$ Gaussian tensor at $\\tau=1$.
Artificial splitting uses noise scale $\\sqrt2$ in each half. The reported
interval intersects the cap-valid interval at error $\\alpha/2$ with the
original-data direct interval at error $\\alpha/2$, for $\\alpha=0.05$.
The extra component, when present, lies on an orthogonal product atom.

| Main amplitude | Weak extra | Supplied mode cap | Covered / 1000 | Coverage 95% Wilson interval | Mean length | Tangent chosen | Previous separated method covered / 1000 |
|---:|---:|---:|---:|---|---:|---:|---:|
'''
    for x in adaptation:
        ci = x['coverage_wilson_95']
        report += f"| {x['amplitude']:g} | {x['weak_extra']:g} | {x['supplied_mode_cap']} | {x['covered']} | [{ci[0]:.3f}, {ci[1]:.3f}] | {x['mean_width']:.3f} | {x['pilot_choices'].get('tangent', 0)} | {x['old_covered']} |\n"
    report += f'''
There are {n_adapt:,} new trials here. The old method is deliberately used
outside its separation assumption in the weak-signal rows; those failures
show why removing the assumption from the statement alone is invalid.
The new interval retains coverage through conservative fallback. At a very
large amplitude and a tight cap it uses the tangent option. A loose cap can
prevent that gain even when the actual signal has rank one: the procedure
does not pretend to have solved actual-rank adaptation. The very large
amplitude also shows how conservative its finite-sample bias bound is.

## Loading calculations and verification

The saved loading calculation has 27 combinations of support size, weight
profile and budget. It evaluates a valid full-data lower bound, not a
simulation or a proof of a matching general rate.

Fresh finite checks passed: {checks['checks']['cosine_ranges']:,} cosine ranges,
{checks['checks']['box_containment_points']:,} parameter-box containment points,
{checks['checks']['optimizer_contract_cases']} optimizer contract cases,
{checks['checks']['weighted_mixture_identities']} independent mixture identities,
{checks['checks']['unseparated_bias_certificates']} first-order bias certificates,
and {checks['checks']['cap_safe_tangent_certificates']} cap-valid tangent
certificates including weak, zero, lower-rank, and strong cases.

The bounds are proved in real arithmetic. Implementations use double
precision and conservative guards, not formal directed-rounding arithmetic.
Run manifests record seeds, software versions and source hashes. The
previous stage's tracked files are checked against its baseline hashes.

## What remains open

- Efficient minimax weak-signal intervals at general dimensions and caps.
- Sharp larger-budget geometry for every loading and unequal weight sequence.
- Optimal growing-cap factors and pointwise adaptation where it is possible.
- General-dimensional certified optimization and formal numerical enclosures.

The code, proofs, and new experiments are a concrete advance, with those
general problems still open. Reproduction commands are in [README.md](README.md).
'''
    (ROOT / 'progress_report.md').write_text(report)
    with tempfile.TemporaryDirectory(prefix='tt-certified-build-') as temporary:
        theory = Path(temporary) / 'supplement.md'
        theory.write_text((ROOT / 'theory/results.md').read_text().split('\n', 1)[1])
        subprocess.run(['pandoc', str(theory), '-s', '-f', 'markdown+tex_math_dollars',
                        '-t', 'latex', '-o', str(ROOT / 'paper/main.tex'),
                        '-M', 'title=Certified optimization and weak-signal tensor inference',
                        '-M', 'date=September 11, 2026', '-V', 'geometry:margin=0.85in',
                        '-V', 'fontsize=10pt', '-V', 'colorlinks=true'], check=True)
    with (ROOT / 'results/theory_build.log').open('w') as log:
        subprocess.run(['latexmk', '-xelatex', '-interaction=nonstopmode', '-halt-on-error', 'main.tex'],
                       cwd=ROOT / 'paper', stdout=log, stderr=subprocess.STDOUT, check=True)
    (ROOT / 'paper/main.xdv').unlink(missing_ok=True)
    with (ROOT / 'results/report_build.log').open('w') as log:
        subprocess.run(['pandoc', 'progress_report.md', '-o', 'progress_report.pdf',
                        '-f', 'markdown+tex_math_dollars', '--pdf-engine=xelatex',
                        '-V', 'geometry:margin=0.85in', '-V', 'fontsize=10pt'],
                       cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True)
    print('Built report and technical supplement.')


if __name__ == '__main__':
    main()
