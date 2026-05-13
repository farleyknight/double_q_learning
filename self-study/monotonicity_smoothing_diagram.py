"""
Diagram: monotonicity of smoothing.
Coarser sigma-algebra => more smoothing => less variance in E[X|.], more within-cell variance.
Shows X, E[X|G] (fine), E[X|H] (coarse) on same plot.
"""

import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

omega = np.linspace(0, 1, 1000)
X = 1.2 * np.sin(7 * omega) + 0.6 * np.cos(13 * omega) + 2.5 + 0.4 * np.sin(19 * omega)

# Fine partition G: 6 cells
g_bounds = [0.0, 0.17, 0.33, 0.5, 0.67, 0.83, 1.0]
# Coarse partition H: 2 cells
h_bounds = [0.0, 0.5, 1.0]

g_colors = ["#dbe9ff", "#fce8e6"] * 3
h_colors = ["#e8f0fe", "#fce8e6"]


def cell_means(x_arr, omega_arr, bounds):
    means = []
    for i in range(len(bounds) - 1):
        mask = (omega_arr >= bounds[i]) & (omega_arr < bounds[i + 1])
        means.append(np.mean(x_arr[mask]))
    return means


g_means = cell_means(X, omega, g_bounds)
h_means = cell_means(X, omega, h_bounds)

# Compute variances for annotation
# Var(E[X|G]): variance of the step function E[X|G]
exg = np.zeros_like(omega)
for i in range(len(g_bounds) - 1):
    mask = (omega >= g_bounds[i]) & (omega < g_bounds[i + 1])
    exg[mask] = g_means[i]
var_exg = np.var(exg)

exh = np.zeros_like(omega)
for i in range(len(h_bounds) - 1):
    mask = (omega >= h_bounds[i]) & (omega < h_bounds[i + 1])
    exh[mask] = h_means[i]
var_exh = np.var(exh)

# E[Var(X|G)]: average within-cell variance
evar_g = 0
for i in range(len(g_bounds) - 1):
    mask = (omega >= g_bounds[i]) & (omega < g_bounds[i + 1])
    cell_weight = np.sum(mask) / len(omega)
    evar_g += cell_weight * np.var(X[mask])

evar_h = 0
for i in range(len(h_bounds) - 1):
    mask = (omega >= h_bounds[i]) & (omega < h_bounds[i + 1])
    cell_weight = np.sum(mask) / len(omega)
    evar_h += cell_weight * np.var(X[mask])

# --- Panel 1: X(omega) ---
ax = axes[0]
ax.plot(omega, X, color="#1a73e8", linewidth=1.8)
ax.set_ylabel("value", fontsize=11)
ax.set_title("$X(\\omega)$ — original, unsmoothed", fontsize=12)
ax.set_ylim(0, 4.5)
ax.text(0.98, 0.95, f"Var$(X)$ = {np.var(X):.3f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#f5f5f5", edgecolor="#ccc"))

# --- Panel 2: E[X|G] fine (6 cells) ---
ax = axes[1]
for i in range(len(g_bounds) - 1):
    ax.axvspan(g_bounds[i], g_bounds[i + 1], color=g_colors[i], alpha=0.3)
for b in g_bounds[1:-1]:
    ax.axvline(b, color="#aaa", linewidth=0.8, linestyle="--")
ax.plot(omega, X, color="#1a73e8", linewidth=0.8, alpha=0.25)
for i in range(len(g_bounds) - 1):
    ax.plot([g_bounds[i], g_bounds[i + 1]], [g_means[i], g_means[i]],
            color="#4caf50", linewidth=2.5)
ax.plot([], [], color="#4caf50", linewidth=2.5, label="$E[X \\mid \\mathcal{G}]$  (6 cells)")
ax.legend(loc="upper left", fontsize=10, framealpha=0.9)
ax.set_ylabel("value", fontsize=11)
ax.set_title("$\\mathcal{G}$ fine — mild smoothing", fontsize=12)
ax.set_ylim(0, 4.5)
ax.text(0.98, 0.95,
        f"Var$(E[X \\mid \\mathcal{{G}}])$ = {var_exg:.3f}\n"
        f"$E[$Var$(X \\mid \\mathcal{{G}})]$ = {evar_g:.3f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#e6f4ea", edgecolor="#4caf50"))

# --- Panel 3: E[X|H] coarse (2 cells) ---
ax = axes[2]
for i in range(len(h_bounds) - 1):
    ax.axvspan(h_bounds[i], h_bounds[i + 1], color=h_colors[i], alpha=0.3)
for b in h_bounds[1:-1]:
    ax.axvline(b, color="#333", linewidth=1.5, linestyle="-")
ax.plot(omega, X, color="#1a73e8", linewidth=0.8, alpha=0.25)
for i in range(len(h_bounds) - 1):
    ax.plot([h_bounds[i], h_bounds[i + 1]], [h_means[i], h_means[i]],
            color="#d93025", linewidth=3)
ax.plot([], [], color="#d93025", linewidth=3, label="$E[X \\mid \\mathcal{H}]$  (2 cells)")
ax.legend(loc="upper left", fontsize=10, framealpha=0.9)
ax.set_ylabel("value", fontsize=11)
ax.set_xlabel("$\\omega \\in \\Omega$", fontsize=12)
ax.set_title("$\\mathcal{H} \\subseteq \\mathcal{G}$ coarse — heavy smoothing", fontsize=12)
ax.set_ylim(0, 4.5)
ax.set_xticks([])
ax.text(0.98, 0.95,
        f"Var$(E[X \\mid \\mathcal{{H}}])$ = {var_exh:.3f}\n"
        f"$E[$Var$(X \\mid \\mathcal{{H}})]$ = {evar_h:.3f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#fce8e6", edgecolor="#d93025"))

fig.suptitle("Monotonicity of smoothing:  coarser $\\mathcal{H} \\subseteq \\mathcal{G}$"
             "  $\\Rightarrow$  more smoothing\n"
             "Var$(E[X \\mid \\mathcal{H}]) \\leq$ Var$(E[X \\mid \\mathcal{G}])$"
             "     and     "
             "$E[$Var$(X \\mid \\mathcal{H})] \\geq E[$Var$(X \\mid \\mathcal{G})]$",
             fontsize=12, y=1.04)
fig.tight_layout()
fig.savefig("/Users/farleyknight/Research/double_q_learning/self-study/monotonicity_smoothing.png",
            dpi=150, bbox_inches="tight")
print("Saved monotonicity_smoothing.png")
