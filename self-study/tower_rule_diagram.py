"""
Diagram: tower rule / smoothing property of conditional expectation.
E[E[X | G] | H] = E[X | H] when H ⊆ G.

Shows X as a wiggly function, E[X|G] as a fine step function,
and E[X|H] as a coarser step function that equals E[E[X|G]|H].
"""

import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

# Sample space [0, 1]
omega = np.linspace(0, 1, 1000)

# X(omega): wiggly function
X = 1.2 * np.sin(7 * omega) + 0.6 * np.cos(13 * omega) + 2.5 + 0.4 * np.sin(19 * omega)

# Fine partition G: 6 cells
g_bounds = [0.0, 0.17, 0.33, 0.5, 0.67, 0.83, 1.0]
# Coarse partition H: 3 cells (each H-cell is a union of 2 G-cells)
h_bounds = [0.0, 0.33, 0.67, 1.0]

g_colors_light = ["#dbe9ff", "#fce8e6", "#dbe9ff", "#fce8e6", "#dbe9ff", "#fce8e6"]
h_colors_light = ["#e8f0fe", "#fce8e6", "#e6f4ea"]

def cell_mean(x_arr, omega_arr, lo, hi):
    mask = (omega_arr >= lo) & (omega_arr < hi)
    return np.mean(x_arr[mask])

# Compute E[X | G]
g_means = []
for i in range(len(g_bounds) - 1):
    g_means.append(cell_mean(X, omega, g_bounds[i], g_bounds[i + 1]))

# Compute E[X | H] directly
h_means = []
for i in range(len(h_bounds) - 1):
    h_means.append(cell_mean(X, omega, h_bounds[i], h_bounds[i + 1]))

# --- Panel 1: X(omega) with G partition ---
ax = axes[0]
for i in range(len(g_bounds) - 1):
    ax.axvspan(g_bounds[i], g_bounds[i + 1], color=g_colors_light[i], alpha=0.4)
for b in g_bounds[1:-1]:
    ax.axvline(b, color="#aaa", linewidth=0.8, linestyle="--")
ax.plot(omega, X, color="#1a73e8", linewidth=1.8)
ax.set_ylabel("value", fontsize=11)
ax.set_title("$X(\\omega)$ with fine partition $\\mathcal{G}$ (6 cells)", fontsize=12)
ax.set_ylim(0, 4.2)

# --- Panel 2: E[X | G] step function, then averaged over H ---
ax = axes[1]
# Shade H cells
for i in range(len(h_bounds) - 1):
    ax.axvspan(h_bounds[i], h_bounds[i + 1], color=h_colors_light[i], alpha=0.3)
# G partition lines
for b in g_bounds[1:-1]:
    ax.axvline(b, color="#aaa", linewidth=0.8, linestyle="--")
# H partition lines (thicker)
for b in h_bounds[1:-1]:
    ax.axvline(b, color="#333", linewidth=1.5, linestyle="-")
# E[X|G] step function
for i in range(len(g_bounds) - 1):
    ax.plot([g_bounds[i], g_bounds[i + 1]], [g_means[i], g_means[i]],
            color="#1a73e8", linewidth=2.5)
# E[E[X|G] | H] = E[X|H]
for i in range(len(h_bounds) - 1):
    ax.plot([h_bounds[i], h_bounds[i + 1]], [h_means[i], h_means[i]],
            color="#d93025", linewidth=3, linestyle="--")
ax.plot([], [], color="#1a73e8", linewidth=2.5, label="$E[X \\mid \\mathcal{G}]$")
ax.plot([], [], color="#d93025", linewidth=3, linestyle="--",
        label="$E[E[X \\mid \\mathcal{G}] \\mid \\mathcal{H}]$")
ax.set_ylabel("value", fontsize=11)
ax.set_title("Average fine cells within each coarse $\\mathcal{H}$-cell (3 cells, bold lines)",
             fontsize=12)
ax.legend(loc="upper right", fontsize=10, framealpha=0.9)
ax.set_ylim(0, 4.2)

# --- Panel 3: E[X | H] directly ---
ax = axes[2]
for i in range(len(h_bounds) - 1):
    ax.axvspan(h_bounds[i], h_bounds[i + 1], color=h_colors_light[i], alpha=0.3)
for b in h_bounds[1:-1]:
    ax.axvline(b, color="#333", linewidth=1.5, linestyle="-")
ax.plot(omega, X, color="#1a73e8", linewidth=1, alpha=0.3)
for i in range(len(h_bounds) - 1):
    ax.plot([h_bounds[i], h_bounds[i + 1]], [h_means[i], h_means[i]],
            color="#d93025", linewidth=3)
ax.plot([], [], color="#d93025", linewidth=3, label="$E[X \\mid \\mathcal{H}]$ directly")
ax.plot([], [], color="#1a73e8", linewidth=1, alpha=0.3, label="$X(\\omega)$ (faded)")
ax.set_ylabel("value", fontsize=11)
ax.set_xlabel("$\\omega \\in \\Omega$", fontsize=12)
ax.set_title("$E[X \\mid \\mathcal{H}]$ computed directly — same result", fontsize=12)
ax.legend(loc="upper right", fontsize=10, framealpha=0.9)
ax.set_ylim(0, 4.2)
ax.set_xticks([])

fig.suptitle("Tower rule: $E[E[X \\mid \\mathcal{G}] \\mid \\mathcal{H}] = E[X \\mid \\mathcal{H}]$"
             "  when  $\\mathcal{H} \\subseteq \\mathcal{G}$",
             fontsize=14, y=1.02)
fig.tight_layout()
fig.savefig("tower_rule.png", dpi=150, bbox_inches="tight")
print("Saved tower_rule.png")
