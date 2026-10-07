"""Render saved WSG predictions with the historical Darcy panel palette.

Lightweight figure preparation only; no model execution. The historical color
bar supplies its palette; WSG panels share the first test target's value range.
"""
from pathlib import Path
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/darcy-wsg-matplotlib")
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.font_manager import FontProperties

ROOT = Path(__file__).resolve().parents[1]
original = np.asarray(Image.open(ROOT / "public/figures/ch04/darcy_global.png").convert("RGB"))
h, w = original.shape[:2]
# Sample inside the original MATLAB color bar, away from its outline/ticks.
palette = original[np.linspace(round(.885*h), round(.078*h), 256).astype(int), round(.81*w)] / 255
cmap = ListedColormap(palette)
plt.rcParams["mathtext.fontset"] = "cm"
font = FontProperties(fname=str(ROOT / "public/fonts/NotoSerif-Regular.ttf"), size=18)
for method, job in [("global", 7076193), ("layerwise", 7076196)]:
    run = ROOT / f"data/raw/ch04/darcy_wsg/runs/{method}_nosc/20261006-wsg-wide-{method}-{job}"
    with np.load(run / "payload.npz") as data:
        field, target = data["prediction"][0], data["reference"][0]
        error = float(data["relative_l2"][0])
    fig = plt.figure(figsize=(3.5, 2.625))
    ax = fig.add_axes([.23, .25, .48, .64])
    image = ax.imshow(field, origin="lower", extent=[0, 1, 0, 1], interpolation="nearest", cmap=cmap,
                      vmin=float(target.min()), vmax=float(target.max()))
    ax.set_xticks([0, .5, 1], ["0", "0.5", "1"])
    ax.set_yticks([0, .5, 1], ["0", "0.5", "1"])
    ax.set_xlabel("x", fontproperties=font, labelpad=-5)
    ax.set_ylabel("y", fontproperties=font, labelpad=-5)
    ax.tick_params(direction="in", top=True, right=True, pad=2, length=2)
    for label in ax.get_xticklabels() + ax.get_yticklabels(): label.set_fontproperties(font)
    ax.set_title(r"$L_2=" + f"{error:.3f}" + "$", fontsize=18, pad=3)
    cax = fig.add_axes([.75, .25, .035, .64])
    colorbar = fig.colorbar(image, cax=cax, ticks=[0, .2, .4])
    colorbar.ax.tick_params(direction="in", length=2, pad=2)
    for label in colorbar.ax.get_yticklabels(): label.set_fontproperties(font)
    fig.savefig(ROOT / f"public/figures/ch04/darcy_wsg_{method}_styled.png", dpi=200)
    plt.close(fig)
