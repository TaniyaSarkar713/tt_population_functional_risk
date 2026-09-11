"""Generate manuscript figures and concise result summaries from saved outputs."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / 'results' / (name + '.json')).read_text())


def main():
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'savefig.bbox': 'tight'})
    adaptive = load('adaptive_intervals')
    loading = load('general_loadings')
    robust = load('robust_full_scan')
    approximation = load('approximate_ranks')
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.4), constrained_layout=True)
    for rank, color, marker in [(1, '#176b9b', 'o'), (2, '#b45309', 's')]:
        rows = [x for x in adaptive if x['noise'] == 'gaussian' and x['loading'] == 'diagonal' and x['rank'] == rank]
        x = [r['strength_over_eta'] for r in rows]
        axes[0].plot(x, [r['length_to_direct'] for r in rows], marker=marker, color=color, label=f'Actual rank {rank}')
        y = np.array([r['coverage']['rate'] for r in rows])
        intervals = np.array([r['coverage']['ci95'] for r in rows])
        axes[1].errorbar(x, y, yerr=np.maximum(0, np.stack([y - intervals[:, 0], intervals[:, 1] - y])),
                         marker=marker, color=color, capsize=3, label=f'Actual rank {rank}')
    for ax in axes:
        ax.set_xscale('log')
        ax.axvspan(.2, 2, color='#fce7e7')
        ax.axvline(2, color='#9f1239', linestyle=':', linewidth=1)
        ax.set_xlabel('Smallest signal singular value / pilot bound')
        ax.grid(alpha=.15)
    axes[0].axhline(1, color='gray', linestyle='--', linewidth=1)
    axes[0].set_ylabel('Mean interval length / direct length')
    axes[0].legend(frameon=False)
    axes[0].set_title('A. Bias correction limits the gain')
    axes[1].axhline(.95, color='gray', linestyle='--', linewidth=1)
    axes[1].set_ylabel('Coverage with exact 95% binomial intervals')
    axes[1].set_ylim(-.03, 1.05)
    axes[1].set_title('B. Shaded region violates separation')
    fig.savefig(ROOT / 'figures/adaptive_intervals.pdf')
    fig.savefig(ROOT / 'figures/adaptive_intervals.png', dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.4), constrained_layout=True)
    positions = np.arange(len(robust))
    for key, offset, color, label in [('robust_envelope', -.08, '#176b9b', 'Directional medians'),
                                     ('sample_mean_gaussian_envelope', .08, '#b45309', 'Gaussian calibration of means')]:
        y = np.array([r[key]['rate'] for r in robust])
        ci = np.array([r[key]['ci95'] for r in robust])
        axes[0].errorbar(positions + offset, y, yerr=np.maximum(0, np.stack([y - ci[:, 0], ci[:, 1] - y])),
                         color=color, marker='o', linestyle='none', capsize=3, label=label)
    axes[0].set_xticks(positions, ['Gaussian', 'Signs', 'Student t(3)', 'Rare outliers'], rotation=20)
    axes[0].axhline(.95, color='gray', linestyle='--', linewidth=1)
    axes[0].set_ylabel('Simultaneous noise-envelope coverage')
    axes[0].set_ylim(.8, 1.035)
    axes[0].legend(frameon=False, fontsize=8, loc='lower left')
    axes[0].set_title('A. Full p=2 scan; 400 repetitions')
    for p, color in [(256, '#176b9b'), (4096, '#b45309')]:
        rows = [r for r in loading if r['p'] == p and r['noise'] == 'gaussian' and r['signal'] == 'off_diagonal']
        axes[1].plot([r['epsilon'] for r in rows], [r['length'] for r in rows], marker='o', color=color, label=f'p={p}')
    axes[1].axhline(2 * 1.95996398454, color='gray', linestyle='--', linewidth=1, label='Direct Gaussian interval')
    axes[1].set_xlabel('Known loading remainder norm')
    axes[1].set_ylabel('Interval length (noise scale = 1)')
    axes[1].set_title('B. Efficient loading correction; K=4')
    axes[1].legend(frameon=False, fontsize=8)
    fig.savefig(ROOT / 'figures/robustness_and_loadings.pdf')
    fig.savefig(ROOT / 'figures/robustness_and_loadings.png', dpi=150)
    plt.close(fig)

    valid = [r for r in adaptive if r['theorem_assumptions']]
    minimum = min(valid, key=lambda r: r['coverage']['rate'])
    summary = dict(adaptive_configurations=len(adaptive), adaptive_valid_configurations=len(valid),
                   adaptive_invalid_configurations=len(adaptive) - len(valid), adaptive_repetitions=500,
                   adaptive_min_valid_coverage=minimum['coverage'],
                   adaptive_min_valid_coverage_setting={k: minimum[k] for k in ['noise', 'loading', 'rank', 'strength_over_eta']},
                   loading_configurations=len(loading), loading_repetitions=1000,
                   loading_min_coverage=min(r['coverage']['rate'] for r in loading),
                   robust_configurations=len(robust), robust_repetitions=400,
                   approximation_configurations=len(approximation), approximation_repetitions=1000,
                   approximation_min_coverage=min(r['coverage']['rate'] for r in approximation),
                   total_monte_carlo_repetitions=500 * len(adaptive) + 1000 * len(loading) + 400 * len(robust) + 1000 * len(approximation))
    (ROOT / 'results/experiment_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
