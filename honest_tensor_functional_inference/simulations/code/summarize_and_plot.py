"""Generate all draft tables and plots from the saved simulation output."""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import numpy as np
from scipy.stats import norm
from intervals import radii
from plot_utils import COLORS, configure, plt, save

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent


def fmt(x):
    return f"{float(x):.4f}"


def main():
    configure()
    rows = list(csv.DictReader((ROOT / "results/summary.csv").open()))
    alpha = 0.05
    z = norm.ppf(1-alpha/2)
    c = 1-2*alpha-0.5*np.sqrt(np.sqrt(8/7)-1)
    p = np.unique(np.geomspace(128, 10**12, 300).astype(np.int64))
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.05), layout="constrained")
    for K, color, style in zip((3,4,6), COLORS, ("-", "--", "-.")):
        y = 2*np.minimum(1, (8*np.log(2*p/alpha)/p)**((K-2)/(2*K)))
        axes[0].loglog(p, y, color=color, ls=style, label=f"Joint, K={K}")
    axes[0].axhline(2*z/(1+z), color="black", ls=":", label="Affine lower bound")
    axes[0].axhline(c/4, color="0.45", ls="--", label="One-unfolding lower bound")
    axes[0].set(xlabel="Mode dimension p (log scale)", ylabel=r"Interval length / $\tau$ (log scale)")
    axes[0].legend(loc="lower left", frameon=False)
    upper = 2*np.minimum(1, (8*np.log(2*p/alpha)/p)**(1/6))
    lower = (0.75-2*alpha)*np.sqrt(np.log(1+p/4)/p)
    axes[1].loglog(p, upper, color=COLORS[0], label="K=3: uniform upper bound")
    axes[1].loglog(p, lower, color=COLORS[1], ls="--", label="K=3: lower bound at zero")
    axes[1].fill_between(p, lower, upper, color="0.92")
    axes[1].set(xlabel="Mode dimension p (log scale)", ylabel=r"Length / $\tau$ (log scale)")
    axes[1].legend(loc="lower left", frameon=False)
    save(fig, ROOT / "figures", "theoretical_comparison")

    fig, axes = plt.subplots(2, 1, figsize=(6.6, 4.5), layout="constrained")
    eps = [0,0.001,0.01,0.1,0.5]
    x = np.arange(len(eps))
    for name, color, marker, offset in [("gaussian",COLORS[4],"s",-0.06),
                                         ("selected",COLORS[0],"o",0.06)]:
        selected = [next(r for r in rows if r["experiment"]=="weak_rank" and
                         r["p"]=="8192" and r["support"]=="1" and
                         float(r["epsilon"])==e and r["method"]==name) for e in eps]
        y = np.array([float(r["coverage"]) for r in selected])
        lo = np.array([float(r["coverage_ci_lower"]) for r in selected])
        hi = np.array([float(r["coverage_ci_upper"]) for r in selected])
        axes[0].errorbar(x+offset, y, yerr=[y-lo,hi-y], color=color, marker=marker,
                         capsize=3, ls="--" if name=="gaussian" else "-",
                         label="Direct Gaussian" if name=="gaussian" else "Selected, cap 2")
        widths = [float(r["mean_length"])/float(r["tau"]) for r in selected]
        axes[1].plot(x, widths, color=color, marker=marker,
                     ls="--" if name=="gaussian" else "-",
                     label="Direct Gaussian" if name=="gaussian" else "Selected, cap 2")
    axes[0].axhline(0.95, color="black", lw=1, ls=":", label="Nominal coverage")
    axes[0].set(ylabel="Coverage probability", ylim=(0.89,1.01), xticks=x,
                xticklabels=[str(e) for e in eps])
    axes[0].legend(loc="lower left", frameon=False, ncol=3)
    axes[1].set(ylabel=r"Interval length / $\tau$", xlabel=r"Second singular value $\epsilon$ (categorical spacing)",
                xticks=x, xticklabels=[str(e) for e in eps], ylim=(0,4.3))
    save(fig, ROOT / "figures", "weak_rank_coverage")

    for f in (ROOT/"figures").glob("*.pdf"):
        shutil.copy2(f, PROJECT/"paper/figures"/f.name)

    # Coverage ranges are descriptive across configurations, not simultaneous CIs.
    methods = ["gaussian","structural","nonlinear","selected","known_direction_oracle"]
    labels = {"gaussian":"Direct Gaussian", "structural":"Structural", "nonlinear":"Threshold",
              "selected":"Selected", "known_direction_oracle":"Known-direction oracle"}
    table = [r"\begin{tabular}{lrrr}",r"\toprule",r"Method & Configurations & Min. coverage & Max. coverage \\",r"\midrule"]
    report = ["# Simulation findings", "", "Fixed seed 20260909; 2,000 replications in each of 175 configurations. There are 172 configurations within the stated iid Gaussian model and three out-of-model stress configurations. Intervals share noise within a configuration; streams are independent across configurations.", "", "## In-model coverage", "", "| Method | Configurations | Minimum | Maximum |", "|---|---:|---:|---:|"]
    for method in methods:
        rr=[r for r in rows if r["in_model"]=="True" and r["method"]==method]
        values=[float(r["coverage"]) for r in rr]
        table.append(f"{labels[method]} & {len(rr)} & {min(values):.4f} & {max(values):.4f} " + r"\\")
        report.append(f"| {labels[method]} | {len(rr)} | {min(values):.4f} | {max(values):.4f} |")
    table += [r"\bottomrule",r"\end{tabular}"]
    (PROJECT/"paper/coverage_table.tex").write_text("\n".join(table)+"\n")
    report += ["", "The selected interval is conservative on this grid. Coverage ranges are descriptive extrema, not confidence bounds for uniform coverage. With 2,000 replications, the Monte Carlo standard error at coverage 0.95 is 0.00487. If all replications cover, the exact 95% binomial interval is approximately [0.99816,1], despite the plug-in Monte Carlo standard error being zero. Full configuration-level exact intervals, bias, bias standard errors and RMSE are in summary.csv.", "", "## Deterministic lengths at p=n=8192, cap one", "", "| Order K | Selected length / tau | Direct length / tau | Ratio to direct |", "|---|---:|---:|---:|"]
    for K in (2,3,4,6):
        rad=radii(K,8192,8192**-0.5)
        h=getattr(rad,rad.selected)
        report.append(f"| {K} | {2*h*np.sqrt(8192):.6f} | {2*z:.6f} | {h/rad.gaussian:.4f} |")
    report += ["", "These are exact evaluated formulas, not fitted empirical rates. At K=2 the selected length is 2 tau and no polynomial separation is obtained. The known-direction oracle may be far shorter for diffuse signals because it is given unavailable factor information; the proposed interval does not dominate that different experiment.", "", "## Assumption stress tests", "", "| Noise | Direct coverage | Threshold / selected coverage | Interpretation |", "|---|---:|---:|---|"]
    stress_table=[r"\begin{tabular}{lrr}",r"\toprule",r"Noise & Direct & Selected \\",r"\midrule"]
    for noise in ("gaussian","student_t3","variance_contamination","correlated"):
        rr={r["method"]:r for r in rows if r["experiment"]=="assumption_stress" and r["noise"]==noise}
        explanation={"gaussian":"In model", "student_t3":"Variance one, heavier tails; outside Gaussian proof", "variance_contamination":"5% noise SD multiplied by 10; stated variance calibration is false", "correlated":"Gaussian margins; direct variance wrong, nonlinear union bound still applies"}[noise]
        report.append(f"| {noise} | {fmt(rr['gaussian']['coverage'])} | {fmt(rr['selected']['coverage'])} | {explanation} |")
        stress_table.append(f"{noise.replace('_',' ')} & {fmt(rr['gaussian']['coverage'])} & {fmt(rr['selected']['coverage'])} "+r"\\")
    stress_table += [r"\bottomrule",r"\end{tabular}"]
    (PROJECT/"paper/stress_table.tex").write_text("\n".join(stress_table)+"\n")
    report += ["", "Stress-test results are not evidence of robustness. The heavy-tail result at zero does not establish coverage for other means. No data tuning or post hoc configuration removal was performed. The weak-rank radii remain constant as the second singular value vanishes, explicitly demonstrating the lack of actual-rank adaptation.", "", "## Figures and checks", "", "theoretical_comparison.pdf evaluates exact analytic bounds up to p=10^12; simulated dimensions stop at 8192. The shaded bracket is unresolved, not a confidence band. weak_rank_coverage.pdf uses exact binomial Monte Carlo intervals, with categorical spacing in epsilon. check_theory.py checks 101,101 scalar cases, 120 random tensors of each format, and exact finite-binomial mixture second moments. Numerical checks supplement the written proofs and cannot verify them logically."]
    (ROOT/"results/findings.md").write_text("\n".join(report)+"\n")
    artifacts=list((ROOT/"figures").glob("*"))+[ROOT/"results/findings.md", PROJECT/"paper/coverage_table.tex",PROJECT/"paper/stress_table.tex"]
    manifest={"input_sha256": hashlib.sha256((ROOT/"results/summary.csv").read_bytes()).hexdigest(),
              "code_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob("*.py")},
              "artifacts_sha256": {str(p.relative_to(PROJECT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in artifacts}}
    (ROOT/"results/analysis_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("Generated two vector figures, two manuscript tables and findings.md")


if __name__ == "__main__":
    main()
