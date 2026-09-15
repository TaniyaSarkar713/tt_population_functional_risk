"""Build all numerical prose and tables from saved outputs; no MC reruns."""
import csv,json,platform,sys
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import binomtest
ROOT=Path(__file__).resolve().parents[1]

def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)+'\n'

def main():
    sim=json.loads((ROOT/'results/simulation_results.json').read_text());follow=json.loads((ROOT/'results/followup_results.json').read_text());minor=json.loads((ROOT/'results/minor_results.json').read_text());grid=json.loads((ROOT/'results/loading_grid.json').read_text());real=json.loads((ROOT/'real_data/analysis_results.json').read_text());prov=json.loads((ROOT/'real_data/provenance.json').read_text());checks=json.loads((ROOT/'audit/theory_checks.json').read_text());primary=real['analyses'][1]
    evidence=[]
    for c in sim:evidence.append((c['id'],c['methods']['safe' if c['family']=='tensor' else 'sparse']))
    for j,c in enumerate(follow):
        if c['family']!='diagonal_assumption_violation':evidence.append((f'followup_{j}',c.get('method',c.get('corrected'))))
    for c in minor:evidence.append((f"minor_{c['a']}",c))
    pv=sorted([(binomtest(round(v['coverage']*v['replications']),v['replications'],.95,alternative='less').pvalue,k) for k,v in evidence]);reject=0
    for i,(p,k) in enumerate(pv):
        if p<=.05/(len(pv)-i):reject+=1
        else:break
    screen={'tests':len(pv),'holm_rejections':reject,'min_raw_p':pv[0][0],'excluded':'deliberately misspecified diagonal model and uncorrected projection diagnostic','interpretation':'A screen for discrepancies, not verification of uniform coverage.'}
    (ROOT/'audit/coverage_screen.json').write_text(json.dumps(screen,indent=2)+'\n')
    nmc=sum(c['B'] for c in sim)+len(follow)*2000+len(minor)*4000
    report='''---
title: "Scientific extensions and an executed subject-level application"
author: "Tensor functional inference: research supplement"
date: "14 September 2026"
geometry: margin=0.8in
fontsize: 11pt
---

# Scientific progress and scope

The new work develops all-budget orthogonal-loading envelopes, sharp rates for new slow-decay profiles, a scalar safeguard with strong-pointwise squared-risk guarantees, general Tucker and TT implementations, and a sharp off-tangent rank-one interval. It also implements the exact diagonal sparse submodel across intermediate caps and executes a public EEG analysis with measured projection bias. Full proofs are in `theory/results.md` and `paper/technical_supplement.pdf`.

The general polynomial fixed-cap weak-signal minimax optimizer remains open. So do exact rates for every loading and every intermediate Tucker/TT cap, and a complete pointwise theory. These results are substantive restricted advances, not a claim that the full research program is complete. The reviewed submission in `review_revision/` and all earlier experimental results are preserved.

'''
    report+=table(['Result','Before this stage','Scientific advance','Remaining boundary'],[
        ['AB1','General orthogonal profiles unmatched','All-budget upper/lower proxies within 1 + nu log log(ep)','Ideal prefix optimizers; nonorthogonal tensors remain general'],
        ['AB2','Fixed power-decay weights only','Sharp logarithmic-decay profiles, all budgets','Critical exponents and varying-exponent constants'],
        ['P2','R1 protects only noise-scale MSE','Pre-intersection scalar with uniform and strong-pointwise risk','No weak-signal minimax estimator'],
        ['P3','Strong diagonal Tucker length','Arbitrary-core Tucker and single-cut TT length; local risk lower bounds','Strong signal, saturation/alignment, nonoptimal thresholds'],
        ['P4','Off-tangent points excluded by alignment','Four-entry rank-one interval, sharp tau^2/a expected length','Prespecified minor and axis base point'],
        ['D2','General intermediate caps unmatched','O(p) interval/estimator on exact sparse diagonal model','Additional model restriction; classical sparse rate'],
        ['B1/B1a','No executed defensible application','Bounded subject target; fixed-stratum bias calibration','Subject independence; no Gaussian low-rank validation']])
    report+='''# Computation and rate interpretation

For decreasing absolute orthogonal weights $w_i$, let $F_s=\\sqrt{s}r_K(s,M,\\tau)$. The new Abel upper proxy is $A(w)=\\sum_s(w_s-w_{s+1})F_s$ and the compensated-prefix lower proxy is $B(w)=\\max_s w_sF_s$. The exact proxy inequality is $B\\le A\\le B[1+\\log(F_p/F_1)]$. Statistical comparison constants also depend on the fixed caps, tensor order, and confidence. These proxies can be evaluated quickly; their attaining confidence-set projection and residual fit are still ideal constructions. No plotted envelope is an observed output of a high-dimensional minimax optimizer.

For weights $w_i=c[\\log(ei)]^{-\\beta}$, the complete proof supplies all-budget phase formulas. In the large-budget cubic regime $M\\ge\\tau\\sqrt p$ the rate is $c\\tau\\ell_p^{3/2-\\beta}$ for fixed $0<\\beta<3/2$ away from critical cases, and $c\\tau$ for $\\beta>3/2$. In higher order the transition is at $\\beta=1/2$. The full budget dependence and excluded boundaries must be retained when applying these formulas.

The general Gaussian implementation accepts unequal dimensions, arbitrary loadings, and supplied Tucker or TT caps. Its SVD candidates have explicit unresolved-subspace bias bounds; a pilot chooses a radius before independent artificial-split validation. This gives uniform honesty, including zero and undersaturation, but can fall back to the noise-scale direct candidate. The new scalar protects the candidate center before narrow-interval intersection. It avoids turning rare empty intersections into enormous scalar errors. A distinct four-entry ratio interval exploits a rank-one minor identity at off-tangent points, with honest denominator fallback at weak signals.

'''
    report+=f'The analytic grid contains **{len(grid)} calculations**. Its largest observed Abel/prefix proxy ratio is **{max(x["proxy_ratio"] for x in grid):.3f}**. This finite grid does not establish sharpness or rule out worse profiles.\n\n'
    report+='![All orthogonal profiles have a controlled rate bracket. Shading shows the Abel upper and prefix lower proxies for normalized logarithmic weights in order three, not simulated confidence intervals. The right panel varies the norm budget at 65,536 loading terms; critical beta=1.5 is displayed as an unmatched bracket.](../figures/loading_envelopes.pdf){width=100%}\n\n'
    timing_path=ROOT/'results/runtime_results.json'
    if timing_path.exists():
        timing=json.loads(timing_path.read_text())
        report+='The full public API was also timed on fixed observations, separately from Monte Carlo coverage runs. Each row reports the median of three calls with one library thread, including loading SVDs and artificial splitting. Tensor storage is input-array storage only, not a peak-memory measurement. These timings demonstrate tractability of the cap-valid procedure, not attainment of the ideal weak-signal rate.\n\n'
        report+=table(['Geometry','p','Cap','Input entries','Input MiB','Median seconds'],[[r['geometry'],r['p'],r['rank'],f"{r['entries']:,}",f"{r['input_tensor_mebibytes']:.2f}",f"{r['median_seconds']:.4f}"] for r in timing['results'] if r['rank']==1])
    report+='''# New simulations

All configurations and seeds were saved before their own Monte Carlo draws. Methods are paired on each observation where appropriate. New results are separate from earlier saved experiments. Coverage intervals use Wilson binomial limits; MSE and width Monte Carlo errors use the empirical standard deviation across independent data sets. MSE error bars can be unreliable for very rare losses, so maximum losses and individual outcomes are retained. Runs use one numerical-library thread.

'''
    report+=f'This stage generated **{nmc:,} independent Monte Carlo data sets in {len(sim)+len(follow)+len(minor)} configurations**, plus {len(grid)} analytic calculations. The main grid contains {len(sim)} configurations and {sum(c["B"] for c in sim):,} data sets. Five follow-ups add 10,000, and seven minor configurations add 28,000. These counts do not include the earlier 87,200 revision data sets or 1,084,640 preserved pre-review data sets.\n\n'
    report+='## Strong and weak tensor means\n\nStrong cases use caps one and two, known rotated flat loadings, Tucker order three and TT order four. The Tucker rank-two core has nonzero off-diagonal entries. Signal levels deliberately satisfy the conservative sufficient theorem inequalities; these runs do not establish optimal SNR thresholds. Zero, weak and strong-undersaturated cases test the same public API. A separate dense TT-core experiment uses unequal dimensions (4,5,4,3), caps (2,3,2), and an arbitrary loading aligned with one cut.\n\n'
    strong=[c for c in sim if c['family']=='tensor' and c['signal']=='strong'];rows=[]
    for c in strong:
        m=c['methods']['safe'];rows.append([c['geometry'],c['p'],c['rank'],c['B'],f"{m['coverage']:.3f}",f"{m['mean_width']:.3f}",f"{m['mse']:.4f} ({m['mse_mcse']:.4f})",f"{c['methods']['direct']['mse']:.3f}"])
    report+=table(['Geometry','p','Cap','Draws','Coverage','Width','Safe MSE (MCSE)','Direct MSE'],rows)
    report+='![The protected scalar follows the strong-pointwise rank-to-dimension scale in these favorable cases. Error bars are 1.96 Monte Carlo standard errors for root MSE by the delta method, with 500 or 1,000 paired draws per configuration. Dotted sqrt(2r/p) curves are limiting split-noise references, not exact finite-sample predictions or fitted slopes.](../figures/pointwise_risk.pdf){width=100%}\n\n'
    rows=[]
    for c in strong:
        if c['empty_count']:
            rows.append([c['id'],c['geometry'],c['p'],c['empty_count'],f"{c['methods']['same_interval_midpoint']['mse']:.1f}",f"{c['methods']['legacy_direct_fallback']['mse']:.4f}",f"{c['methods']['safe']['mse']:.4f}"])
    report+='The same-interval midpoint and direct-fallback ablations use the **new pilot calibration**. They are not claimed to be exact reproductions of the preceding R1 algorithm. Empty intervals remain in coverage and loss accounting.\n\n'
    report+=table(['Case','Geometry','p','Empty','Midpoint MSE','Fallback MSE','P2 MSE'],rows)
    tt=next(c for c in follow if c['family']=='dense_TT_core_loading' and c['signal']=='strong')
    report+=f"The dense-core TT follow-up has core loading norm 0.2, safe MSE **{tt['method']['mse']:.5f}**, direct MSE **{tt['direct']['mse']:.5f}**, mean width **{tt['method']['mean_width']:.3f}**, and coverage **{tt['method']['coverage']:.4f}** over 2,000 draws. At strong undersaturated means the general procedure selects split-direct throughout; its scalar MSE is about two rather than the original direct estimator's one. This is the real cost of artificial splitting when the geometry cannot be certified.\n\n"
    report+='## Intermediate caps: a restricted positive result and a negative control\n\nThe exact sparse diagonal experiments use dimensions 256, 4,096 and 65,536, caps on both sides of square-root dimension, and three norm-budget multipliers. Equal positive active entries near the hard threshold stress truncation bias. D2 selects structural, direct or threshold intervals from deterministic radius bounds. It is sharp only under the exact diagonal-mean restriction; tensor rank one by itself does not imply this restriction.\n\n'
    report+='![The implemented sparse-diagonal procedure retains bounded rate-normalized loss and width across the tested caps. These are exact-diagonal means at the largest budget multiplier, with 1,000 draws per case; MSE error bars are 1.96 Monte Carlo standard errors transformed by the delta method. This figure does not match the unresolved intermediate-cap rates of the full Tucker or TT model.](../figures/diagonal_caps.pdf){width=100%}\n\n'
    negative=next(c for c in follow if c['family']=='diagonal_assumption_violation')
    report+=f"A deliberately invalid use on the diagonal of a **dense rank-one full tensor** gives coverage **{negative['method']['coverage']:.3f}** and MSE **{negative['method']['mse']:.1f}** over 2,000 draws. The threshold interval's mean width is {negative['method']['mean_width']:.3f}. This is a counterexample to extending D2 to the full tensor class, not a failure of its stated theorem. The off-diagonal means exist mathematically; no enormous full tensor is allocated because this procedure accesses only the diagonal.\n\n"
    report+='## Off-tangent rank-one points\n\nThe P4 target is diagonally opposite a prespecified anchor in a two-by-two rank-one minor. A corresponding supplied unfolding cap of one suffices for honesty, even with larger caps elsewhere. At the axis mean its first derivative vanishes; two small factor rotations produce the target only at second order. The interval handles a denominator whose confidence interval crosses zero by returning to a globally valid range/direct intersection.\n\n'
    report+=table(['a/tau','Draws','Coverage','Mean width/tau','Width x a/tau^2'],[[r['a'],r['replications'],f"{r['coverage']:.4f}",f"{r['mean_width']:.5f}",f"{r['scaled_length']:.3f}"] for r in minor])
    report+='![The minor interval exhibits inverse-anchor expected length at strong axis means. Each point uses 4,000 draws; error bars are 1.96 Monte Carlo standard errors. The slope-minus-one guide is anchored to the first plotted measured width, and the scaled panel shows the approach to a constant. The sufficient theorem condition is a/tau at least 4 z_(1-alpha/12), so the smallest plotted point is a transition diagnostic.](../figures/minor_pointwise.pdf){width=100%}\n\n'
    report+='## Projection-bias calibration and coverage screen\n\nA bounded Bernoulli-subject experiment chooses a shrinkage map on an independent pilot, then compares signed residual calibration with the uncorrected projected interval. Both target the same original bounded mean when assessing coverage. The latter is deliberately labeled a diagnostic: its interval is valid for the projected mean, not automatically for the original mean.\n\n'
    report+=table(['Calibration n','Validation n','Corrected coverage','Corrected width','Uncorrected target coverage'],[[c['n_calibration'],c['n_validation'],f"{c['corrected']['coverage']:.4f}",f"{c['corrected']['mean_width']:.3f}",f"{c['uncorrected_DIAGNOSTIC']['coverage']:.4f}"] for c in follow if c['family']=='bounded_projection_bias'])
    report+=f"Among {screen['tests']} in-model proposed-procedure coverage checks, {reject} one-sided binomial tests reject nominal 95% coverage after Holm correction at family error 0.05. The smallest unadjusted p-value is {screen['min_raw_p']:.4g}. This is a finite diagnostic, not proof of uniform coverage. The deliberate diagonal violation and uncorrected projection diagnostic are excluded from this in-model screen and reported separately.\n\n"
    report+='''# Real-data analysis: EEG subject responses

## Source, units and estimand

The full [UCI EEG Database](https://archive.ics.uci.edu/dataset/121/eeg%2Bdatabase), credited to Begleiter (1995), DOI 10.24432/C5TS3D, is distributed under CC BY 4.0. Its training and test versions reuse subjects, so they were not treated as independent samples. We downloaded the full archive and processed the subject files directly. The source, archive/subject/trial checksums, preserved metadata and parser are included in `real_data/`. Raw data remain in the documented temporary download cache and can be downloaded again.

The protocol was hashed before raw download. It fixes the nonmatching-minus-matching S2 response at CZ and PZ, averaged over recorded sample indices 64--127, after clipping each voltage to +/-100 microvolts. We do not equate those indices to a verified post-stimulus physiological window. A subject is one sampling unit: all valid trials are averaged within condition before averaging across subjects. The resulting tensor has condition, recorded-channel and time-bin axes. Auxiliary channels remain in the tensor demonstration; they do not enter the primary contrast. This is an observed-response estimand after clipping and trial-quality filtering, not a causal stimulus effect or diagnostic claim.

Before calculating contrasts, the sampling plan was refined because the source describes separately recruited groups. The primary target is the fixed study-mixture of two within-group means, with archive weights 77/122 and 45/122. Independent subjects with a common distribution **within each group** are assumed. Disease prevalence is not estimated. Family identifiers and sampling probabilities are unavailable, so independence and population representativeness cannot be verified from this archive. Familial dependence would invalidate the independent-subject intervals; the cohort descriptive mean remains descriptive without that assumption. The amendment, its timing and its design-based reason are recorded separately from the immutable initial protocol.

'''
    totalvalues=sum(s['voltage_values'] for s in prov['subjects']);clipped=sum(s['clipped_counts'][1] for s in prov['subjects'])
    report+=f"The actual archive contains **{prov['trial_file_count']:,} trial files**, of which **{prov['trial_status_counts']['included']:,}** pass the recorded checks. Exclusions are {prov['trial_status_counts']['error_flag']} error-flagged trials and {prov['trial_status_counts']['unknown_condition']} files without a recognized condition. All **{prov['eligible_subjects']} subjects** retain all three conditions. Valid trial counts range from {min(s['valid_trials'] for s in prov['subjects'])} to {max(s['valid_trials'] for s in prov['subjects'])}; trials are never counted as independent inferential replications. At the primary clipping level, {100*clipped/totalvalues:.4f}% of retained voltage values are clipped. Missing/error trials may be informative: the target explicitly concerns the retained recorded-response process, and no missing-at-random recovery of unobserved responses is asserted.\n\n"
    report+='## Results and uncertainty\n\nThe primary finite-sample interval uses the two-sided empirical Bernstein bound separately by group and combines them at the fixed mixture weights. Its variance and range terms are given in B1/B1a. We additionally report a stratified approximate t interval using a Welch-Satterthwaite degrees-of-freedom calculation. It relies on an approximation and is not promoted to a finite-sample result. Clipping sensitivities change the estimand and are exploratory, without a simultaneous confidence claim.\n\n'
    rows=[]
    for a in real['analyses']:
        eb=a['primary_stratified_EB'];ap=a['approximate_stratified_t'];corr=a['corrected_projection'];rows.append([int(a['clip_microvolts']),f"{a['cohort_descriptive_mean']:.3f}",f"[{eb['lo']:.3f}, {eb['hi']:.3f}]",f"[{ap['lo']:.3f}, {ap['hi']:.3f}]",f"[{corr['lo']:.1f}, {corr['hi']:.1f}]"])
    report+=table(['Clip (+/- microvolts)','Cohort mean','Stratified 95% EB','Approximate 95% t','Calibrated projection'],rows)
    report+=f"At the primary threshold the sample standard deviation of subject contrasts is {primary['subject_sd']:.3f} microvolts. The descriptive mean is {primary['cohort_descriptive_mean']:.3f}; its conservative finite-sample interval includes zero. The approximate interval excludes zero, but that stronger empirical conclusion rests on its approximation and subject sampling assumptions. We make no claim of clinical utility, causality, or population-generalizable disease differences.\n\n"
    report+='![Finite-sample uncertainty is much wider than the approximate t interval. Left: the 122 subject contrasts at the prespecified 100-microvolt clipping threshold, grouped by recorded recruitment code; black segments mark group means. Right: the fixed-mixture direct empirical Bernstein (EB), approximate t, and independently bias-calibrated projection intervals, with the full certified ranges retained. Real-data coverage is not observable; these intervals refer to different uncertainty assumptions, with sample allocation stated in the text.](../figures/eeg_intervals.pdf){width=100%}\n\n'
    report+='## What the tensor demonstration does and does not show\n\n'
    report+=f"The stratified split allocates **{primary['n_pilot']} pilot, {primary['n_calibration']} calibration and {primary['n_validation']} validation subjects**. Selection using only the pilot chooses Tucker caps **{tuple(primary['projection_caps'])}** from the prespecified list. The pilot reconstruction residual is **{100*primary['pilot_reconstruction_relative_error']:.2f}%** of its Frobenius norm. This is a fitted pilot property, not a certificate of exact low population rank.\n\n"
    report+='The projected scalar is clipped to the same known response range. A held-out calibration sample estimates its signed bias relative to the original contrast; the validation sample estimates its projected mean. Four group-by-component bounds share the confidence budget. The resulting certified interval spans the entire feasible target range at every clipping sensitivity. Thus this application supplies **no demonstrated precision advantage** for the tensor procedure. The correction is honest under the stated subject model but costly with this sample size. Direct all-subject and direct nonpilot comparisons, all split memberships and uncorrected bias diagnostics are retained in machine-readable outputs. The protocol\'s nested projection choices favor the largest cap under its residual-loading criterion; the procedure should not be described as recovering the true rank.\n\n'
    report+='The real-data analysis addresses the absence of an executed application with an explicit target, sampling units and uncertainty. It does not validate iid entrywise Gaussian noise, known norm/noise bounds, exact population rank, the ideal minimax optimizer, or the strong-pointwise sufficient conditions. A scientific application demonstrating those original assumptions and an efficiency gain remains a separate task.\n\n'
    report+='''# Scientific audit and readiness

The supplied arguments distinguish rate proxies from computable intervals; fixed from growing cap constants; pointwise length from local minimax risk; and known Gaussian noise from bounded subject data. The negative diagonal example makes the new submodel restriction operational. Projection-bias calibration is tested against an uncorrected counterexample, and the application retains the uninformative certified result.

The central remaining concerns are still substantive. General efficient weak-signal minimax computation is unresolved. AB1 leaves a doubly logarithmic gap in general orthogonal profiles, and critical exponents and general nonorthogonal profiles remain unmatched. D2 does not close the full-model intermediate-cap problem. P3's separation/alignment conditions are sufficient and conservative; P4 covers one prespecified second-order geometry. General weak, undersaturated and higher-order pointwise transitions remain open. Family-level dependence and representative sampling remain unverified in the public application.

The expanded research program receives internal verdict **C: additional theoretical or empirical work required** for the original broad goals. The preserved focused paper's earlier B verdict is not retroactively changed. The supplement can support a focused theory submission after independent proof and priority checks, but a claim to have solved the general program would be premature. Bernoulli or a focused statistics-methodology venue is a more defensible starting discussion than claiming immediate readiness for a broad Annals/JASA minimax-and-application paper; a final venue decision needs external assessment of novelty and significance.

'''
    report+=f"Fresh verification includes **{checks['checks']:,} finite mathematical/implementation checks**, all passing. These are grouped into independent inequality, projector, TT-rank, clipping, sparse-integral and minor checks, not {checks['checks']:,} independent theorem proofs. Numerical library versions are Python {platform.python_version()}, NumPy {np.__version__}, SciPy {scipy.__version__}. Rebuild commands and allocation scope appear in README.md; the validation artifact records the final file hashes and preservation check.\n"
    (ROOT/'paper/report.md').write_text(report)
    # Complete inherited registry with stage-local continuation fields.
    previous=list(csv.DictReader((ROOT.parent/'review_revision/tables/issue_registry.csv').open()))
    actions={
      'F04':('RESOLVED','P2 globally protects scalar risk and adds strong-pointwise upper bounds.','Local two-point, not degenerate single-point, minimax lower criterion.'),
      'T01':('PARTIALLY RESOLVED','General Tucker/TT SVD implementation plus P4 constant-entry pointwise interval.','No general polynomial diffuse weak-signal minimax optimizer; exponential benchmark preserved.'),
      'T02':('PARTIALLY RESOLVED','D2 implements a sharp all-cap exact diagonal submodel with negative full-model control.','Full Tucker/TT intermediate-cap rates remain unmatched.'),
      'T03':('PARTIALLY RESOLVED','AB1 all-budget O(log log p) orthogonal-profile bracket; AB2 sharp slow-decay families.','Critical exponents, exact general profiles, nonorthogonal loading, efficient attaining fits.'),
      'T04':('PARTIALLY RESOLVED','P2/P3 strong arbitrary-core Tucker and TT length/risk; P4 sharp off-tangent minor length.','Full weak/undersaturated/unknown geometry, optimal thresholds and general growing-cap adaptation.'),
      'D01':('PARTIALLY RESOLVED','Executed full-archive subject-level EEG analysis with locked estimand and calibrated bias.','Subject/family sampling assumptions unverified; no original Gaussian-model efficiency validation.'),
      'T05':('PARTIALLY RESOLVED','B1/B1a removes exact low-rank and Gaussian scale assumptions for a bounded subject estimand.','Arbitrary dependence, selected target loadings and original unknown-directional-scale theory remain open.')}
    for row in previous:
        st,action,remaining=actions.get(row['id'],(row['status'],'Preserved resolution; no new change in this stage.',row['remaining_issue']))
        row['previous_status']=row['status'];row['status']=st;row['stage_action']=action;row['stage_remaining']=remaining
        row['stage_files']=json.dumps(['theory/results.md','code/methods.py','paper/report.md']+(['real_data/protocol.md','real_data/sampling_amendment.md','real_data/analysis_results.json','code/analyze_eeg.py'] if row['id'] in ['D01','T05'] else ['results/simulation_results.json','results/followup_results.json','results/minor_results.json']) if row['id'] in actions else [])
    with (ROOT/'audit/issue_registry.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(previous[0]));w.writeheader();w.writerows(previous)
    ledger=[{'id':id,'status':'PROVED','statement_scope':scope,'proof':'theory/results.md','implementation':impl,'novelty_scope':novel} for id,scope,impl,novel in [
        ('AB1','Fixed caps, all budgets, every prescribed orthogonal profile','code/methods.py::loading_envelope (proxy only)','New derivation within project; independent priority review outstanding'),
        ('AB2','Fixed noncritical logarithmic decay exponent, all budgets','code/methods.py::log_profile_rate (proxy only)','New matched families within project; independent priority review outstanding'),
        ('P2','Uniform noise-scale scalar risk plus conditional strong-pointwise upper risk','code/methods.py::cap_interval, safe_scalar','New safeguard and supplied risk argument'),
        ('P3','Strong aligned saturated Tucker or one saturated TT cut','code/methods.py::cap_interval','New geometry/risk extension; ordinary SVD subspace perturbation'),
        ('P4','Rank-one prescribed minor at a strong axis mean','code/methods.py::rank_one_minor_interval','Rank-one geometric specialization of elementary ratio confidence sets'),
        ('D2','Exact diagonal sparse mean, all caps and budgets','code/methods.py::diagonal_sparse','Classical sparse-functional rate; explicit finite-sample interval specialization'),
        ('B1','Independent bounded subjects, independently selected projection and calibrated bias','code/methods.py::corrected_projection_interval','Application of Maurer-Pontil, not a new concentration inequality'),
        ('B1a','Fixed strata, fixed mixture target, independent held-out subjects','code/analyze_eeg.py','Union-bound corollary of B1')]]
    (ROOT/'theory/theorem_status.json').write_text(json.dumps(ledger,indent=2)+'\n')
    print(f'Built report, inherited 19-issue registry and theorem ledger: {nmc:,} MC datasets.')
if __name__=='__main__':main()
