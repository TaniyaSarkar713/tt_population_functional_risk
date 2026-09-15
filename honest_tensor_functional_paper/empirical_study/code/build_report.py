"""Write observed-result prose only after the analysis and plots exist."""
import json
import subprocess
from pathlib import Path
from common import ROOT


def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)


def main():
    audit=json.loads((ROOT/'results/analysis_audit.json').read_text())
    records=json.loads((ROOT/'tables/summary.json').read_text());rows=[r for r in records if r['alpha']==.05]
    slopes=json.loads((ROOT/'tables/slopes.json').read_text())
    geometry=json.loads((ROOT/'tables/pointwise_geometry.json').read_text())
    solver=json.loads((ROOT/'tables/solver.json').read_text())
    captions=json.loads((ROOT/'figures/captions.json').read_text())
    check=json.loads((ROOT/'logs/implementation_checks.json').read_text())
    def select(**kw):return [r for r in rows if all(r.get(k)==v for k,v in kw.items())]
    def one(**kw):return select(**kw)[0]
    def cov(r):return f"{r['coverage']:.3f} [{r['coverage_wilson_95'][0]:.3f}, {r['coverage_wilson_95'][1]:.3f}]"
    def length(r):return f"{r['length']:.3g} ± {r['length_se']:.2g}"
    suite_table=table(['Suite','Registered cases','MC data sets','Summary rows'],[(s,d['configurations'],f"{d['data_sets']:,}",d['interval_or_event_rows']) for s,d in audit['counts'].items()])
    slope_table=table(['Curve','Observed slope','MC slope SE','Reference'],[(s['label'],f"{s['slope']:.4f}",f"{s['slope_se']:.4f}" if s['slope_se'] is not None else 'deterministic',f"{s['reference_exponent']:.4g}") for s in slopes])
    geometry_table=table(['p','Cap','Observed length / rate','Frozen-subspace length / rate','Difference in MCSE'],[
        [r['p'],r['rank'],f"{r['observed_over_rate']:.3f}",f"{r['prediction_over_rate']:.3f}",f"{r['discrepancy_in_mcse']:.2f}"] for r in geometry])
    summaries=[]
    for suite,method in [('S01','growing'),('S02','threshold_selected'),('S03','pointwise'),('S04','pointwise'),('S05','calibrated'),('S06','directional_mom')]:
        data=[r for r in select(suite=suite,method=method) if r['guarantee']=='finite_sample']
        summaries.append([suite,method,len(data),f"{min(r['coverage'] for r in data):.3f}–{max(r['coverage'] for r in data):.3f}",
                          f"{min(r['repetitions'] for r in data)}–{max(r['repetitions'] for r in data)}"])
    coverage_table=table(['Suite','Method','In-scope cases','95% coverage range','B per case'],summaries)
    pointwise_table=table(['p','Cap','Method','95% coverage [Wilson CI]','Mean length ± MCSE'],[
        [r['p'],r['rank'],r['method'],cov(r),length(r)] for r in select(suite='S03')
        if r['p'] in [16,64] and r['method'] in ['direct','pointwise','xch_known','oracle']])
    solver_table=[]
    for case in sorted({r['case'] for r in solver}):
        data=[r for r in solver if r['case']==case and r['alpha']==.05 and r['budget']==3000]
        finite=[r['endpoint_gap'] for r in data if r['endpoint_gap'] is not None]
        mean=sum(finite)/len(finite) if finite else None
        solver_table.append([data[0]['signal'],data[0]['loading'],f"{sum(r['certified_to_tolerance'] for r in data)}/{len(data)}",
                             f'{mean:.4g}' if mean is not None else 'no feasible witness',sum(r['endpoint_gap'] is None for r in data)])
    solver_table=table(['Signal','Loading','Certified at budget 3000','Mean finite gap','No witness'],solver_table)
    confirmation=one(suite='S13');original=one(case='S03_007',method='direct')
    corr=one(suite='S05',law='gaussian',rho=.8,method='iid_gaussian');cal=one(suite='S05',law='gaussian',rho=.8,method='calibrated')
    shift=one(suite='S05',law='mean_shift',method='iid_gaussian')
    sentinel=audit['pointwise_midpoint_sentinel_cases']
    example=one(case='S03_002',method='pointwise')
    miss_rank=[r for r in select(suite='S04',method='pointwise') if r['guarantee']=='outside_supplied_rank']
    loading_omission=one(suite='S09',kind='loading',epsilon=.5,method='omitted_correction')
    approx_omission=one(suite='S09',kind='approximation',eta=1.,method='omitted_correction')
    gap_cases=[]
    for rank in [1,16,64,256,1024]:
        r=one(suite='S12',p=65536,rank=rank,M=256.,method='cap_upper')
        meta=json.loads((ROOT/'results'/(r['case']+'.json')).read_text())
        gap_cases.append([rank,f"{r['length']:.4g}",f"{meta['extra']['length_lower']:.4g}",f"{r['length']/meta['extra']['length_lower']:.3g}"])
    gap_table=table(['Cap at p=65536','Executable length','Diagonal-mixture lower','Upper / lower'],gap_cases)
    power_table=table(['Local shift','Method','Rejection probability [Wilson CI]'],[
        [r['shift'],r['method'],f"{r['rejection']:.3f} [{r['rejection_wilson_95'][0]:.3f}, {r['rejection_wilson_95'][1]:.3f}]"]
        for r in select(suite='S10') if r['method'] in ['direct','pointwise','xch_known','oracle']])
    comparison=[
        ['G1 large caps','S01','min(M sqrt(r/p),tau); n slope -1/2','Structural and noise slopes recorded above; rate-normalized risk/length saved','Consistent on registered configurations'],
        ['Fixed-cap diagonal method','S02','Threshold rate and honest coverage','Shortening with p; raw versus selected curves and conservative coverage','Executable diagonal method only; full-data attainment untested'],
        ['P1 pointwise rate','S03','tau sqrt(r/p) at strong saturated means','Normalized widths reported; finite-grid slopes -.474 and -.179 differ from limiting -.5 and -.25','No exact exponent confirmation; frozen-subspace intersection diagnostic explains finite-dimension trend'],
        ['Unseparated validity / adaptation limits','S04','Honesty under valid caps; no promise of weak-signal efficiency','Correction delays shortening; understated caps and gap-based rank selection can fail','Expected domain boundaries'],
        ['Joint noise calibration','S05','Known covariance/proxy matters',f'At rho=.8 naive/calibrated coverage {corr["coverage"]:.4f}/{cal["coverage"]:.4f}','Consistent; contaminated-mean rows violate assumptions'],
        ['Finite-variance directional medians','S06','Simultaneous feasibility under iid replicates and known covariance','All recorded median events covered; threshold ratios and Gaussian failures retained','Feasibility component only, conservative'],
        ['Loading profiles','S07','Small-budget geometry; all-budget ideal power-decay envelope','Direct/structural MC and separately labeled analytic envelopes','High-p block-fit attainment not tested'],
        ['Certified binary computation','S08/S11','Budget stops preserve outer endpoints; gaps need reporting','2,160 solves retain gaps, status, nodes, and independent cost checks','Exponential binary benchmark; general computation remains open'],
        ['Loading / approximate-rank transfer','S09','Supplied residuals require correction',f'Omitted correction coverage {loading_omission["coverage"]:.3f} at loading eps=.5 and {approx_omission["coverage"]:.3f} at eta=1','Corrected methods checked; sharp full-data optimizer absent'],
        ['CI inversion / regular pivots','S10','Null calibration, Gaussian reference power','Full rejection and standardized-statistic tables retained','No optimal-testing or nonlinear-CLT claim'],
        ['Intermediate caps','S12 follow-up','Valid upper versus existing lower, generally unmatched','Upper/lower gap remains at intermediate caps','Diagnostic; no rate resolution'],
        ['Unusual Gaussian realization','S13 follow-up','Independent exact marginal calibration',f'Original {original["coverage"]:.4f}; independent confirmation {confirmation["coverage"]:.4f}','Original result preserved; see numerical regeneration audit'],
        ['Real-data applicability','R01','Scientifically justified target and sampling/noise model','No suitable data/model supplied in current workspace','PENDING; no application claim']]
    comparison_md='# Theory–experiment comparison\n\n'+table(['Theory','Experiment','EXPECTED','OBSERVED','INTERPRETED'],comparison)
    (ROOT/'theory_comparison.md').write_text(comparison_md)
    report=f'''# Simulation study of honest tensor-functional intervals

Status: {audit['status']}; completed simulation results, 2026-09-13. Real-data execution remains pending a dataset and justified sampling model. The open theoretical problems are unchanged.

The study executed **{audit['monte_carlo_data_sets']:,} Monte Carlo data sets** in **{audit['monte_carlo_cases']} stochastic configurations**, plus **{audit['analytic_only_cases']} analytic-only configurations** ({audit['registered_cases']} statistical/envelope configurations total). A separate 18-setting runtime study is excluded from these coverage counts. The initial registry had 351 configurations and 824,640 data sets; a separately registered requirements/calibration follow-up added 51 configurations and 260,000 data sets. There are {audit['solver_solves']:,} binary optimizer solves on 240 shared data sets, not that many independent coverage observations. All summaries, raw per-trial endpoints/errors, seeds and numerical statuses are retained.

The main findings are rate-scale shortening in the regimes with executable guarantees, a substantial precision cost for conservative pointwise correction, severe failures under incorrectly supplied assumptions, and remaining computational gaps. Simulations do not prove minimax optimality, uniform honesty, or impossibility.

## Design and checks

The design, theorem map and initial registry were written before implementation/execution. Gaussian sample-mean experiments use tau=1/sqrt(n). Scalar/diagonal sufficient observations are generated exactly for methods that use only those contractions; full tensors are generated for projection and optimization. Procedures share observations, and split ablations share the same valid artificial Gaussian split. Supplied bounds are not selected using truth after seeing a realization. Signal construction uses truth only to define the prescribed parameter class and explicitly labeled oracles.

The study uses {check['checks']} known-answer checks, including 36 equivalence checks against the preserved cap-valid implementation, exact Tucker tangent-Jacobian variance checks, noiseless reconstruction, net calibration and model membership. Final analysis independently recomputes all interval coverages and mean widths, verifies all configuration/source hashes and preserves {audit['preserved_files']} earlier files unchanged. Python/NumPy/SciPy versions and single-thread settings are in the run manifests.

{suite_table}

Cheap cases use B=5,000, giving nominal 95% coverage MCSE .00308. Full-tensor B is 500, 300 or 150, with nominal MCSE .00975, .01258 or .01780. Solver B=30 gives .03979. Wilson intervals are retained even at 0/100% coverage. Mean lengths, losses and paired differences have uncertainty summaries. Squared-loss Monte Carlo standard errors are not claimed for t3 noise, whose fourth moment is infinite. Aggregate timing from the prolonged host session includes scheduling/inactive periods; separate S11 calls provide the computational comparison.

## Coverage and rate validation

The table gives descriptive ranges over tested parameters, not confidence bounds for worst-case coverage over a continuum. All 90%, 95% and 99% levels are in the full tables. The predeclared family-wise lower-coverage screen includes {audit['finite_sample_screen_rows']} in-scope rows and flagged {audit['finite_sample_undercoverage_flags']} at Bonferroni cutoff {audit['bonferroni_threshold']:.3g}. Lack of a flag is not proof of uniform coverage and does not hide the individual low-coverage case discussed below.

{coverage_table}

{slope_table}

Log-regression slopes are descriptive finite-grid diagnostics. Mean-length error bars vanish for deterministic-radius procedures, so their fitted slopes partly check formulas, not stochastic attainment. The noise-branch RMSE and full-tensor expected-length slopes use observed losses/lengths with Monte Carlo uncertainty. Threshold reference exponents exclude the displayed logarithmic correction. See `tables/summary.csv` for length/rate, squared-loss/rate-squared and paired differences.

The P1 slopes do not equal their limiting references over p=8–64: the fixed-cap slope is about -0.474 and the growing-cap slope about -0.179. These departures exceed the reported Monte Carlo slope errors, which do not account for finite-dimension curvature. We do not label this exact exponent validation. A post-hoc diagnostic freezes the fitted subspaces at their true values and the singular values at the prescribed amplitude. If the resulting tangent and direct radii are h and d, their center difference is N(0,tau^2), and the intersection length is max(0,min(2min(h,d),h+d-abs(W))). Integrating this expression predicts the finite-dimension clipping effect. All eight approximate mean-length predictions are within two observed Monte Carlo standard errors; the integral formula is independently checked by quadrature. This is an explanatory approximation using unavailable true geometry, not a new theorem for estimated subspaces.

{geometry_table}

## Pointwise precision and an estimator failure

{pointwise_table}

At p=16, cap one, the P1 test amplitude is about 310,930 noise standard deviations. Such signals deliberately satisfy a conservative sufficient condition; practical signal sweeps extend from zero upward and show that this condition is far from a useful empirical cutoff. The Xu–Chen–Han comparator uses its two simultaneous iterations and exact fitted-core tangent variance. It is an asymptotic regular-signal procedure, not an honest weak-signal competitor, and often gives materially shorter intervals in the strong regime. The support oracle has unavailable structure. There is no claim of leading-constant or universal practical dominance.

The cap-valid implementation replaces empty interval intersections by {{0}}. At large nonzero means its **interval midpoint can have enormous MSE**: in S03_002, the observed midpoint MSE is {example['mse']:.6g} (MCSE {example['mse_se']:.3g}), despite coverage {example['coverage']:.3f} and mean length {example['length']:.4g}. The large squared-loss uncertainty reflects rare sentinel events. There are {len(sentinel)} tested 95% pointwise cases with at least one such nonzero-target sentinel. This is retained in raw records and the audit. The P1 theorem concerns honesty and expected length; it does not promise midpoint MSE control. A useful estimation repair needs a separate analysis, rather than silently reinterpreting this midpoint as the ideal residual-fit estimator.

## Assumption failures and calibration investigation

Under equicorrelated Gaussian coordinates with rho=.8, naive iid calibration covers {corr['coverage']:.4f}, while the known-covariance interval covers {cal['coverage']:.4f}. Mean-shift contamination gives naive coverage {shift['coverage']:.4f}; a variance correction does not remove its bias. The finite-variance median scan tests the full binary net and a known covariance upper bound. Its simultaneous feasibility is conservative in these draws; the study does not implement the general robust minimax projection and does not claim dependence or Huber-contamination robustness.

Understated rank caps produce minimum pointwise coverage {min(r['coverage'] for r in miss_rank):.3f} in the deliberate violations. The previous rank selector can return a zero interval at weak nonzero signals, outside its separation assumption. Loading residual and approximation-allowance omissions also cause severe failures. Corrected intervals retain their explicitly supplied assumptions; general arbitrary-loading and approximate-rank sharp computation is not established by these examples.

The original S03_007 direct Gaussian interval covers {cov(original)} with B=150. This unusually low realization is displayed, including its interval excluding .95; it is not discarded because the broad family-wise screen did not flag it. Regeneration of its full Gaussian tensors checks the direct statistic independently. The separately registered S13 confirmation covers {cov(confirmation)} with B=10,000, using a new fixed stream of exact diagonal observations. It is a diagnostic addition, not a replacement or a pooled result. See `results/gaussian_diagnostic.json` for the original one-sided test and regeneration discrepancy.

## Computation and intermediate caps

{solver_table}

Only continuous rank-one binary tensors are optimized. All support levels in the implemented projective net are included. For every tolerance/budget the outer interval is retained, along with feasible witnesses and endpoint gaps; unmet tolerances are explicit. Float64 guard bounds are numerical evidence, not formal interval arithmetic. The ideal general-dimensional minimax residual/block optimizer remains absent. S11 reports actual diagonal access through p=1,048,576, full tensors through 64^3, and binary order-three/four costs; traced allocations exclude untraced native workspace.

{gap_table}

The follow-up uses sparse common-target diagonal signals. Its diagonal-mixture lower bound need not be the strongest available fixed-cap bound, especially for K=3. The remaining upper/lower gap is a diagnostic of these constructions, not a new minimax theorem. Matching intermediate growing-cap factors, arbitrary loading profiles and a complete pointwise characterization remain open.

## Local power and distribution diagnostics

Intervals are inverted for the zero functional at strong signed rank-two means. Alternatives shift the target by c tau sqrt(r/p), with c in {{0,1,2,4,8}}. The exact direct-Gaussian power curve and empirical paired rejection probabilities are reported. Direct and oracle statistics are exact Gaussian pivots; XCH diagnostics are interpreted under regular-signal assumptions. No CLT is asserted for nonlinear interval midpoints or global-solver endpoints.

{power_table}

## Real-data status and outstanding empirical requirements

No scientifically justified repeated-tensor dataset, independent target loading or known directional noise calibration was supplied. `real_data/README.md` records the missing sampling units, calibration, rank/approximation bounds, missingness and split/preprocessing requirements. R01 remains pending. Simulated observations, synthetic tensors and noise-injected images are not represented as real-data validation.

The main empirical limitations are the small solver replication count, conservative P1 signal floor, largest-p coverage uncertainty, unavailable general residual/block fits, unmatched intermediate-cap bounds, and lack of a justified application. Lower bounds and impossibility results are analytic statements, not experimentally proved. The full reviewer audit and theory/experiment comparison separate those gaps from completed simulation execution.
'''
    (ROOT/'report.md').write_text(report)
    # A self-contained manuscript section, generated from actual observed results.
    section='''# Simulation study

We evaluated honest confidence intervals for fixed scalar loadings in the additive tensor model Z=A+tau G, with known noise and supplied Frobenius and rank bounds. The primary design was fixed before execution and separates implementable theory validation from paired comparisons and assumption violations. Exact sufficient observations are used for diagonal procedures; full tensors are generated for projection and the binary global benchmark. All methods share observations, with correctly scaled independent artificial splitting when needed.

The direct Gaussian and structural intervals are compared with calibrated sequence-style thresholding, the cap-valid pointwise method, the Xu–Chen–Han tensor PCA procedure, and explicitly labeled known-support/direction oracles. The PCA comparator is reimplemented from Section 4.2 and Algorithm 3 of the primary preprint (https://arxiv.org/abs/2501.16223v1), including its exact tangent variance. Its regular-signal guarantee is kept distinct from finite-sample cap-uniform honesty. The diagonal comparison is connected to the Gaussian functional literature of Collier, Comminges and Tsybakov (https://arxiv.org/abs/1502.00665).

'''+f'''The completed study contains {audit['monte_carlo_data_sets']:,} data sets and {audit['registered_cases']} configurations, including 51 explicitly registered follow-ups and {audit['analytic_only_cases']} analytic-only envelope configurations. Confidence levels 90%, 95% and 99% are evaluated with Wilson intervals, mean-length standard errors, scalar losses and paired differences. Expensive full tensors and solver cases have fewer replications; their uncertainty is retained.

The large-cap interval follows its structural and noise rate branches. Strong saturated pointwise signals permit shortening, while regular-signal and oracle intervals can be substantially shorter. The observed pointwise p slopes are about -0.474 and -0.179, compared with limiting references -0.5 and -0.25; these finite-grid discrepancies exceed Monte Carlo slope errors. An explicitly post-hoc frozen-subspace calculation predicts the effect of intersection with the direct interval and matches all eight mean lengths within two Monte Carlo standard errors. It is an explanatory approximation, not exact exponent validation or a new estimated-subspace theorem. At moderate signals, the cap-valid method may remain near or above the direct interval's width. The ideal general-dimensional residual optimizer is not replaced by diagonal thresholding or analytic loading envelopes.

{slope_table}

At 95% confidence, correlated Gaussian noise with rho=.8 yields coverage {corr['coverage']:.4f} under naive iid calibration and {cal['coverage']:.4f} under known covariance calibration. Understated rank bounds, omitted loading/approximation contributions and rank selection outside separation produce failures in the deliberately misspecified settings. The finite-variance full-net event is conservative in the tested laws; this does not establish contamination or dependent-replicate robustness.

An unusual direct-Gaussian realization in the largest-dimensional primary case is retained: coverage {cov(original)}, B=150. Independent, separately registered confirmation gives {cov(confirmation)}, B=10,000; the confirmation is not substituted for the original result. A further negative finding concerns the {{0}} fallback for empty cap-valid interval intersections: its midpoint can have large squared error at strong nonzero signals, even when the interval's coverage and expected length behave as predicted. The pointwise theorem does not provide a midpoint risk bound.

The binary rank-one optimizer performs {audit['solver_solves']:,} finite-budget solves on 240 independent observations, with all gaps and unresolved certificates retained. This is an exponential numerical benchmark. Intermediate-cap upper/lower comparisons and general loading envelopes remain diagnostic rather than claims of sharp computational attainment. Complete configuration-level results, uncertainty, numerical statuses, source hashes and code accompany the study.

# Real-data analysis: current limitation

No real-data inference result is asserted. The available workspace does not supply a defensible repeated-tensor sampling model with calibrated directional noise, an independently fixed scientific loading, and justified norm/rank or approximation bounds. An application would require those choices before preprocessing, split construction or interval evaluation. The accompanying application audit records the missing inputs; simulated data are not presented as observational validation.
'''
    (ROOT/'manuscript/empirical_sections.md').write_text(section)
    figures='\n\n# Figures\n\n'+ '\n\n'.join(f'![{caption}](figures/{name}.pdf)' for name,caption in captions.items())
    (ROOT/'report_with_figures.md').write_text(report+figures)
    for source,dest in [('report_with_figures.md','report.pdf'),('manuscript/empirical_sections.md','manuscript/empirical_sections.pdf')]:
        subprocess.run(['pandoc',source,'-o',dest,'--pdf-engine=xelatex','-V','geometry:margin=0.7in',
                        '-V','fontsize=10pt','-V','colorlinks=true'],cwd=ROOT,check=True)
    print('Built observed report and manuscript sections, with PDFs.')


if __name__=='__main__':main()
