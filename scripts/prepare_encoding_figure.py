"""Illustrate magnitude-prefix encoding; regenerate only the ch2-04 figure pair.

This analytic example is an illustration, not a saved experimental result.
Both panels use the same horizontal spatial grid and upright magnitude profile.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
font_manager.fontManager.addfont(ROOT / "public/fonts/NotoSerif-Regular.ttf")
plt.rcParams.update({"font.family": "Noto Serif", "font.size": 12,
                     "mathtext.fontset": "cm", "axes.linewidth": .7,
                     "axes.labelsize": 13, "xtick.labelsize": 11,
                     "ytick.labelsize": 11, "svg.fonttype": "path"})
OUT = ROOT / "public/figures/ch02"
K, ZMAX = 40, .2
x = np.linspace(0, 1, 51)
def field(x):
    return .15 * np.exp(-((x - .14) / .12)**2) + .18 * np.exp(-((x - .48) / .16)**2)
f = field(x)
n = np.floor(K * f / ZMAX).astype(int)
spikes = np.arange(1, K + 1)[:, None] <= n[None, :]
decoded = ZMAX * spikes.mean(axis=0)
assert np.all((f - decoded >= -1e-12) & (f - decoded < ZMAX / K))
assert np.array_equal(spikes.sum(axis=0), n)
BLUE, BROWN = "#315d79", "#8a4935"

def canvas(ylabel):
    fig = plt.figure(figsize=(6.1, 3.05), facecolor="white")
    ax = fig.add_axes([.15, .22, .81, .73])
    ax.set_xlim(-.01, 1.01)
    ax.set_xticks([0, .25, .5, .75, 1], ["0", "0.25", "0.5", "0.75", "1"])
    ax.set_xlabel(r"Spatial position $x$", labelpad=5)
    ax.set_ylabel(ylabel, labelpad=6)
    ax.tick_params(direction="out", length=3, pad=4)
    ax.spines[["top", "right"]].set_visible(False)
    return fig, ax

fig, ax = canvas(r"Field value $f(x)$")
xx = np.linspace(0, 1, 1001)
ax.plot(xx, field(xx), color=BLUE, lw=2.1, label=r"Continuous $f$")
ax.plot(x, decoded, color=BROWN, marker=".", markersize=3.5, lw=1,
        linestyle="--", label=r"Decoded $\hat f$")
ax.set_ylim(0, ZMAX)
ax.set_yticks([0, .05, .1, .15, .2], ["0", "0.05", "0.10", "0.15", "0.20"])
ax.legend(loc="upper right", frameon=False, fontsize=10, handlelength=1.8)
fig.savefig(OUT / "encoding_continuous.svg")
plt.close(fig)

fig, ax = canvas(r"Spike step $k$")
# Rows are spike steps, columns are spatial samples: no spatial transpose.
edges = np.linspace(-.01, 1.01, 52)
ax.pcolormesh(edges, np.arange(K + 1) + .5, spikes,
              cmap=ListedColormap(["#f0efed", BLUE]), vmin=0, vmax=1,
              edgecolors="white", linewidth=.35, shading="flat", rasterized=False)
ax.set_ylim(.5, K + .5)
ax.set_yticks([1, 10, 20, 30, 40])
fig.savefig(OUT / "encoding_discrete.svg")
plt.close(fig)
print("Generated matched continuous/discrete encoding figures (K=40, 51 spatial samples).")
