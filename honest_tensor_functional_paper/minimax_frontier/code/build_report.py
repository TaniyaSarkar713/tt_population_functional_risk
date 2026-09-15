"""Build evidence-based prose and continue the scientific issue registry."""
import csv
import json
from pathlib import Path
import numpy as np
from scipy.stats import binomtest

ROOT=Path(__file__).resolve().parents[1]


def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)+'\n\n'


def main():
    sim=json.loads((ROOT/'results/simulation_results.json').read_text());meta=json.loads((ROOT/'results/run_metadata.json').read_text())
    checks=json.loads((ROOT/'audit/theory_checks.json').read_text());timing=json.loads((ROOT/'results/timing.json').read_text())
    profiles=json.loads((ROOT/'results/analytic_profiles.json').read_text());caps=json.loads((ROOT/'results/analytic_caps.json').read_text())
    valid=[c for c in sim if c['signal']!='rank_two_violation']
    tests=sorted((binomtest(c['method']['covered'],c['B'],.95,alternative='less').pvalue,c['id']) for c in valid)
    rejected=[]
    for j,(p,k) in enumerate(tests):
        if p<=.05/(len(tests)-j):rejected.append(k)
        else:break
    screen=dict(tests=len(tests),holm_rejections=rejected,min_raw_p=tests[0][0],
                excluded='F159, deliberate rank-two violation of P5',
                evaluation='Four endpoint ULP steps; strict counts and all differences retained.',
                interpretation='Finite simulation discrepancy screen; not proof of uniform coverage.')
    (ROOT/'audit/coverage_screen.json').write_text(json.dumps(screen,indent=2)+'\n')
    slopes=[]
    for K in [3,4,5]:
        for d in range(2,K+1):
            rows=[c for c in sim if c['family']=='coordinate' and c['K']==K and c['distance']==d and c['signal']=='axis' and c['a'] in [100.,1000.]]
            x,y=rows
            slope=np.log(y['method']['mean_width']/x['method']['mean_width'])/np.log(10)
            se=np.sqrt((x['method']['width_mcse']/x['method']['mean_width'])**2+(y['method']['width_mcse']/y['method']['mean_width'])**2)/np.log(10)
            slopes.append(dict(K=K,d=d,observed_slope=float(slope),slope_mcse=float(se),limiting_exponent=1-d))
    (ROOT/'results/pointwise_slopes.json').write_text(json.dumps(slopes,indent=2)+'\n')
    text=r'''---
title: "Efficient one-cap minimax inference and new tensor rate frontiers"
subtitle: "Research progress, executed experiments, and unresolved generalizations"
date: "2026-09-15"
geometry: margin=0.85in
fontsize: 11pt
---

# Scientific advances and their scope

The new results resolve three substantial parts of the open program. A spectral
clipping interval is computationally efficient and minimax in rate for **every
loading, norm budget, and rank cap when one unfolding is constrained and all
other caps are unrestricted**. A multiscale rank-one mixture proves exact rates
up to constants for **every orthogonal loading profile in tensor order four and
higher**, under fixed positive Tucker or TT caps. A data-selected anchor gives
globally honest intervals with the **optimal coordinate-wise pointwise hierarchy
at unknown rank-one axis signals**. A fourth proposition explains why
deterministic affine intervals cannot attain the ideal fixed-cap diffuse rates.

Complete proofs and parameter-space definitions are in the accompanying
`technical_supplement.pdf` and `theory/results.md`. The new results are internally
labelled PROVED; they have not received independent peer review or formal
verification. Minimax claims are up to constants, not exact finite-sample constants.

The general efficient optimizer under several restrictive caps is still absent.
The preserved binary optimizer is an exponential benchmark. General cubic and
nonorthogonal loading rates, arbitrary simultaneous intermediate growing caps,
and a complete pointwise theory remain open. No experimental success below is
used to claim that those broader questions are closed.

'''
    text+=table(['Result','New conclusion','Boundary'],[
        ['M1','Loading SVD + scalar convex solve; full-model all-cap rates','Only one constrained unfolding'],
        ['M2','Affine constant-radius obstruction at flat loadings','No hardness claim for nonlinear algorithms'],
        ['L3','Exact Abel-profile rate for every orthogonal loading, all budgets','K at least 4; fixed caps; upper fits ideal'],
        ['P5','Optimal coordinate lengths at an unknown rank-one axis','Strong enough localization; other points/ranks unresolved']])
    text+=r'''# Efficient computation and intermediate caps

For the selected unfolding of the known loading, let $\sigma_i$ be its singular
values. At $M>\tau$, the minimax length scale is

$$T_r=\max_{b\ge0,\|b\|_1\le M\sqrt r,\|b\|_2\le\tau}\sigma^Tb
=\min_{t\ge0}\{M\sqrt r\,t+\tau\| (\sigma-t)_+\|_2\}.$$

For $M\le\tau$, use $T_r=M(\sum_{i\le r}\sigma_i^2)^{1/2}$. The squared-error
rate is $T_r^2$. Soft threshold the loading singular values, take the resulting
linear observation, and add the exact rank-constrained bias bound and a Gaussian
quantile. A loading-only comparison with the structural interval protects small
budgets. The scalar estimate has its own squared-bias-plus-variance selection
and structural clipping; it is not defined as an interval midpoint.

The lower bound is a mixture of rank-at-most-r matrices with dense off-diagonal
entries in their singular-vector blocks. It uses all tensor observations after
unfolding. A balanced partition controls the Frobenius norm, while independent
signs yield chi-square divergence at most $\exp(1/62)-1$. No exact-diagonal
restriction, known support, signal separation, or estimated-rank substitution
is used. For flat orthogonal loadings the rate simplifies to
$\min(M\sqrt{r/p},\tau)$ for every cap, including intermediate caps.

The method remains honest if more caps are supplied, but its lower bound does
not transfer to their intersection. At $M=\tau\sqrt p$, all fixed caps allow a
much smaller ideal rate than the noise-scale one-cap rate. M2 shows that merely
optimizing a deterministic affine center and constant radius cannot close this
gap. It does not rule out efficient nonlinear procedures.

The scalar optimizer exposes a feasible dual vector and objective gap. These
are floating-point residual checks, not formal interval-arithmetic certificates.
Preprocessing depends only on the loading and can be reused across observations.
The timings below use one numerical-library thread, medians of three calls,
and full dense input tensors. Input MiB is one array's storage, not peak memory.

'''
    text+=table(['Tensor shape','Entries','Input MiB','Preprocess (s)','Observation (s)'],[
        [' x '.join(map(str,c['shape'])),f"{c['entries']:,}",f"{c['input_mebibytes']:.2f}",f"{c['preprocessing_median_seconds']:.5f}",f"{c['observation_median_seconds']:.5f}"] for c in timing])
    text+='![Loading preprocessing is reusable. Timings include SVDs and the scalar solve; per-observation timing includes interval and scalar evaluation. Four shapes, three calls per shape, one library thread. These are measured runtimes, not timings of the unresolved multi-cap optimizer.](../figures/computation.pdf){width=80%}\n\n'
    text+=r'''# Exact higher-order loading profiles

For decreasing absolute orthogonal weights, define
$F_s=\min(M,\tau\sqrt{\log(es)})$, $F_0=0$. The exact rate proxy is

$$\mathcal A(w)=\sum_{s=1}^p w_s(F_s-F_{s-1}),\qquad K\ge4.$$

Previously, the lower bound used the largest compensated prefix and left a
possible doubly logarithmic gap. The new prior places one random coordinate in
each of several disjoint groups with entropy scales $1,4,16,\ldots$. Geometric
growth controls the rank-one norm and collision likelihood moments, while all
scales contribute to one common target. Its target is within fixed constants
of the entire Abel sum. This proves the lower bound matching the earlier ideal
prefix upper bound for every profile and every budget.

At the previously critical weights $w_i=c[\log(ei)]^{-1/2}$ the rate is $cM$ for
$M\le\tau$, and $c\tau[1+\log\min\{\log(ep),(M/\tau)^2\}]$ for $M>\tau$.
This includes dimension-dependent normalizations. General cubic profiles still
need a cross-scale harmonic-mixture argument that has not been established.
The easily evaluated proxy is not an implemented attaining interval.

'''
    text+=f'The saved analytic grid contains **{len(profiles)} loading-profile calculations** and **{len(caps)} cap/budget calculations**. They are separate from Monte Carlo observations. The largest old Abel/prefix ratio on this finite loading grid is {max(c["A_over_B"] for c in profiles):.3f}.\n\n'
    text+='![Analytic rate comparisons, not observed interval outputs. Left: normalized logarithmic profiles in order K at least 4 at M/tau = 1000; the new theorem matches the full Abel proxy rather than only its largest prefix. Right: at M/tau = sqrt(p), a single rank cap of one and several fixed caps define different full tensor parameter spaces. Constants are omitted in both rate curves.](../figures/statistical_frontiers.pdf){width=100%}\n\n'
    text+='# Newly executed simulations\n\n'
    text+=f'This stage generated **{meta["unique_mc_datasets"]:,} independent full-observation data sets in {meta["configurations"]} configurations**, with 2,000 draws per configuration. It includes 81 spectral configurations, 78 correctly specified coordinate configurations, and one deliberate rank-two violation. All seeds and configurations were saved before their draws. Every endpoint, scalar output where applicable, and selected-anchor outcome is retained. Methods use paired observations within a configuration. No earlier Monte Carlo data set or application result is counted as new.\n\n'
    text+='Coverage uses Wilson binomial intervals and the preserved four-endpoint-ULP comparison convention. Strict counts are also stored. One structural-boundary target (F037) is one representable step beyond an SVD-based bound: all 2,000 method counts and 1,890 direct counts differ from strict comparison. This is exposed in `audit/rounding_audit.json`; no target-scaled tolerance or statistical slack is used. These comparisons do not constitute rigorous numerical interval certification.\n\n'
    text+=f'Among the {len(valid)} configurations inside the stated models, observed method coverage ranges from {min(c["method"]["coverage"] for c in valid):.4f} to {max(c["method"]["coverage"] for c in valid):.4f}. A one-sided 95% coverage discrepancy screen with Holm correction has **{len(rejected)} rejections**. Such a finite screen is not proof of uniform coverage. Width and MSE uncertainty use empirical Monte Carlo standard errors.\n\n'
    text+='## Dense loadings and the full one-cap mean space\n\nThe tensor dimensions are 16 x 16 x 16, the selected mode cap is 1, 4, or 16, and M/tau is 0.3, 3, or 30. Three loading spectra (flat, spike plus tail, logarithmic decay) use dense random singular vectors. Means include zero, a rank-constrained worst-bias direction, and a dense random rank-constrained matrix reshaped as a tensor. Other caps are unrestricted. The direct Gaussian baseline uses the same known structural range and clipping.\n\n'
    spectral=sim[:81]
    text+=f'The smallest observed spectral/direct mean-width ratio is {min(c["method"]["mean_width"]/c["direct"]["mean_width"] for c in spectral):.3f}. The finite grid therefore shows modest width gains at best, despite the rate-optimal guarantee. The theory does not predict universal improvement in constants. The worst observed scalar MSE divided by its proved upper bound is {max(c["method"]["mse"]/c["mse_upper"] for c in spectral):.3f}; sampling variability can move an empirical ratio slightly above one.\n\n'
    text+='![Executed full one-unfolding cases at the worst-bias mean. Solid lines show the proposed interval, dashed lines the direct interval intersected with the same structural range. Colors indicate supplied rank caps. Each marker uses 2,000 paired observations; error bars are 1.96 Monte Carlo standard errors. The mean does not have exact diagonal support in observation coordinates.](../figures/spectral_performance.pdf){width=100%}\n\n'
    text+='## Pointwise coordinate hierarchy and adaptation\n\nFor the full rank-one ball, P5 selects an anchor using an independent artificial pilot. Validation intervals for that anchor and the changed coordinate fibers are combined through a rank-one product identity. A denominator interval crossing zero triggers the honest direct fallback. The original direct interval always bounds the final width. At an axis mean a E_J, coordinate Hamming distance d determines the optimal pointwise rate: tau for d = 0 or 1, and tau^d / |a|^(d-1) for d at least 2. The unknown axis location is never provided to the method.\n\n'
    text+='The sufficient localization condition is |a|/tau at least a constant times sqrt(log(eD)), where D is the number of tensor entries. Honesty does not need this condition. The finite runs use orders 3, 4 and 5, every distance d, and amplitudes 3, 10, 30, 100 and 1,000 with a fixed supplied budget M = 1,000. Additional zero, negative-axis, dense rank-one and rank-two-violation cases probe scope. Slope estimates below use only the two stated levels 100 and 1,000; they are finite-range descriptive contrasts, not estimates of an exact asymptotic exponent from an unlimited sequence.\n\n'
    text+=table(['Order K','Distance d','Observed slope','MCSE','Limit'],[[s['K'],s['d'],f"{s['observed_slope']:.3f}",f"{s['slope_mcse']:.3f}",s['limiting_exponent']] for s in slopes])
    text+='![Unknown-anchor coordinate intervals show the hierarchy across Hamming distances d. Each point has 2,000 independent data sets; error bars are 1.96 Monte Carlo standard errors. Dotted segments have the theoretical exponent 1-d, anchored at the last observed point for visual comparison. They are not additional Monte Carlo outcomes or exact predictions of finite-sample constants.](../figures/coordinate_hierarchy.pdf){width=100%}\n\n'
    text+=table(['Mean type','Amplitude','Coverage','Width','Anchor accuracy'],[[c['signal'],c['a'],f"{c['method']['coverage']:.4f}",f"{c['method']['mean_width']:.3g}",f"{c['correct_anchor_frequency']:.4f}"] for c in sim[-4:]])
    violation=sim[-1]
    text+=f'The rank-two negative control adds a target entry of 5 to a separated axis of amplitude 1,000. It has coverage {violation["method"]["coverage"]:.3f}, because the rank-one product identity is false. Its narrow or empty intersections are retained, including {violation["empty_count"]} empty replacements. This failure prevents extending P5 to a higher-rank honesty class without a new bias argument. No pointwise scalar-risk claim is made for this interval.\n\n'
    text+='# Verification, real data, and remaining work\n\n'
    text+=f'The newly executed mathematical and implementation suite passes **{checks["checks"]:,} finite checks**. These include an independent scalar convex optimizer, feasible dual constraints, exact small sign-mixture likelihoods, greedy norm partitions, compensated multiscale targets, full likelihood collision bounds, affine symmetry, rank-one ratio identities, and pointwise rotation alternatives. The largest relative scalar primal-dual gap is {checks["max_relative_optimizer_gap"]:.2g}. Source and artifact checks are separately recorded in `audit/validation.json`.\n\n'
    text+='The earlier 122-subject EEG analysis is preserved without rerunning it. Its primary cohort contrast is 2.222 microvolts, the finite-sample interval is [-77.920, 82.364], and the bias-calibrated projection interval is [-200, 200]. Those saved results demonstrate no tensor precision gain and do not establish the Gaussian or exact-rank assumptions of the new theorems. Subject independence and potential family dependence remain application limitations.\n\n'
    text+=r'''The expanded research program retains verdict **C: additional scientific work
required**. M1 and L3 have complete supplied upper/lower proofs on their stated
spaces, and P5 has a complete coordinate-axis theorem. The main remaining
requirements are a nonlinear efficient minimax procedure under simultaneous
fixed caps; full nonorthogonal and cubic profile rates; intermediate rates for
arbitrary simultaneous growing caps; and pointwise theory beyond the axis and
strong aligned families. The preserved focused review manuscript retains its
historical B assessment and is not silently presented as the new unified paper.

External novelty is not certified by these internal developments. Classical
convex geometry related to M1 is discussed by Argyriou, Foygel and Srebro,
*Sparse Prediction with the k-Support Norm* (2012),
<https://arxiv.org/abs/1204.5043>. Computational barriers require precisely
matched assumptions; see Luo and Zhang (2020),
<https://arxiv.org/abs/2005.10743>, and the bounded-degree setting of Fu and Sohn
(2026), <https://arxiv.org/abs/2605.30113>. A targeted priority check and eventual
integration of the new theorems into a coherent submission remain necessary.
'''
    (ROOT/'paper/report.md').write_text(text)
    previous=ROOT.parent/'scientific_extension/audit/issue_registry.csv'
    with previous.open() as f:reader=csv.DictReader(f);rows=list(reader);fields=reader.fieldnames
    fields=fields+['frontier_action','frontier_remaining','frontier_files']
    updates={
        'T01':('M1 supplies polynomial full-model minimax inference for one constrained unfolding; M2 proves a constant-radius affine obstruction.','General simultaneous-cap nonlinear optimizer remains open.'),
        'T02':('M1 proves and implements all intermediate caps for a full one-unfolding tensor class, every loading and budget.','General vectors of simultaneous growing Tucker/TT caps remain unmatched.'),
        'T03':('L3 matches the full Abel proxy for every orthogonal profile, every budget, K>=4; M1 handles every loading on its one-cap class.','General cubic/nonorthogonal multiple-cap profiles and efficient attaining prefix fits remain open.'),
        'T04':('P5 completes the unknown-axis coordinate hierarchy with global rank-one honesty and pointwise lower bounds.','Arbitrary points/loadings, higher/growing ranks, and optimal localization thresholds remain open.')}
    for row in rows:
        action,remaining=updates.get(row['id'],('Preserved prior scientific resolution and evidence; no new application analysis.',row.get('stage_remaining',row['remaining_issue'])))
        row.update(frontier_action=action,frontier_remaining=remaining,frontier_files='theory/results.md; code/methods.py; paper/report.md' if row['id'] in updates else '')
        if row['id'] in updates:row['status']='PARTIALLY RESOLVED'
    with (ROOT/'audit/issue_registry.csv').open('w',newline='') as f:writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    print('Report,',len(slopes),'pointwise slopes and',len(rows),'continued review issues built.')


if __name__=='__main__':main()
