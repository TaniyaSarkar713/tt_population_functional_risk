"""Shared publication-figure settings; output uses vector PDF."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#555555"]


def configure():
    plt.rcParams.update({"font.family": "serif", "font.size": 9,
                         "axes.labelsize": 9, "legend.fontsize": 9,
                         "xtick.labelsize": 9, "ytick.labelsize": 9,
                         "pdf.fonttype": 42, "ps.fonttype": 42,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "lines.linewidth": 1.5, "savefig.bbox": "tight"})


def save(fig, directory, name):
    directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(directory / (name + ".pdf"))
    fig.savefig(directory / (name + ".png"), dpi=180)
    plt.close(fig)
