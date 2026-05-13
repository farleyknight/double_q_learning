"""
Diagram: conditional expectation as smoothing within partition cells.
"""

import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 4))

# Sample space [0, 1] partitioned into 4 cells by Z
boundaries = [0.0, 0.25, 0.5, 0.75, 1.0]
colors = ["#e8f0fe", "#fce8e6", "#e6f4ea", "#fef7e0"]
labels = ["$Z = z_1$", "$Z = z_2$", "$Z = z_3$", "$Z = z_4$"]

# X(omega): a wiggly function
omega = np.linspace(0, 1, 500)
X = 1.2 * np.sin(7 * omega) + 0.6 * np.cos(13 * omega) + 2.5 + 0.4 * np.sin(19 * omega)

# Shade cells and compute E[X | Z] on each
cell_means = []
for i in range(4):
    lo, hi = boundaries[i], boundaries[i + 1]
    ax.axvspan(lo, hi, color=colors[i], alpha=0.5)
    mask = (omega >= lo) & (omega < hi)
    mean = np.mean(X[mask])
    cell_means.append((lo, hi, mean))
    ax.text((lo + hi) / 2, 0.3, labels[i], ha="center", fontsize=11, color="#444")

# Plot X(omega)
ax.plot(omega, X, color="#1a73e8", linewidth=1.8, label="$X(\\omega)$", zorder=3)

# Plot E[X | Z] as a step function
for lo, hi, mean in cell_means:
    ax.plot([lo, hi], [mean, mean], color="#d93025", linewidth=2.5, zorder=4)
# Add a single legend entry for the step function
ax.plot([], [], color="#d93025", linewidth=2.5, label="$E[X \\mid Z]$")

# Vertical partition lines
for b in boundaries[1:-1]:
    ax.axvline(b, color="#888", linewidth=1, linestyle="--", zorder=2)

ax.set_xlim(0, 1)
ax.set_ylim(0, 4.2)
ax.set_xlabel("$\\omega \\in \\Omega$", fontsize=12)
ax.set_ylabel("value", fontsize=12)
ax.set_title("Conditioning on $Z$ = averaging $X$ within each cell of the partition $Z$ induces",
             fontsize=11, pad=10)
ax.legend(loc="upper right", fontsize=11, framealpha=0.9)
ax.set_xticks([])

fig.tight_layout()
fig.savefig("conditional_expectation.png", dpi=150, bbox_inches="tight")
print("Saved conditional_expectation.png")
