"""
Diagram: injective Y on finite Omega generates the full power set.
Contrast injective vs non-injective mappings and their sigma-algebras.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))


def draw_mapping(ax, title, omega_els, y_vals, arrows, atoms, atom_colors, sigma_text):
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-1.8, 3.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=12, pad=10)

    # Omega ellipse (left)
    omega_ellipse = mpatches.Ellipse((1, 1.2), 1.6, 2.8, edgecolor="black",
                                      facecolor="#f0f0f0", linewidth=2)
    ax.add_patch(omega_ellipse)
    ax.text(1, 2.8, "$\\Omega$", ha="center", fontsize=13, fontweight="bold")

    # Y-values ellipse (right)
    y_ellipse = mpatches.Ellipse((3.5, 1.2), 1.6, 2.8, edgecolor="black",
                                  facecolor="#f0f0f0", linewidth=2)
    ax.add_patch(y_ellipse)
    ax.text(3.5, 2.8, "range of $Y$", ha="center", fontsize=11)

    # Omega elements
    n = len(omega_els)
    omega_positions = []
    for i, el in enumerate(omega_els):
        y_pos = 2.0 - i * (2.0 / (n - 1)) if n > 1 else 1.2
        omega_positions.append((1, y_pos))
        ax.text(1, y_pos, el, ha="center", va="center", fontsize=13,
                fontweight="bold", color="#1a73e8")

    # Y-value elements
    y_positions = {}
    ny = len(y_vals)
    for i, v in enumerate(y_vals):
        y_pos = 2.0 - i * (2.0 / (ny - 1)) if ny > 1 else 1.2
        y_positions[v] = (3.5, y_pos)
        ax.text(3.5, y_pos, v, ha="center", va="center", fontsize=13,
                fontweight="bold", color="#d93025")

    # Arrows
    for src_idx, tgt_val in arrows:
        sx, sy = omega_positions[src_idx]
        tx, ty = y_positions[tgt_val]
        ax.annotate("", xy=(tx - 0.35, ty), xytext=(sx + 0.35, sy),
                     arrowprops=dict(arrowstyle="->", color="#666", lw=1.5))

    # Atoms display below
    ax.text(2.25, -0.6, "Atoms of $\\sigma(Y)$:", ha="center", fontsize=10,
            fontweight="bold")
    x_start = 0.2
    for i, (atom, color) in enumerate(zip(atoms, atom_colors)):
        rect = mpatches.FancyBboxPatch((x_start, -1.3), len(atom) * 0.45 + 0.15, 0.45,
                                        boxstyle="round,pad=0.05", edgecolor="#555",
                                        facecolor=color, alpha=0.5, linewidth=1.2)
        ax.add_patch(rect)
        for j, el in enumerate(atom):
            ax.text(x_start + 0.2 + j * 0.45, -1.08, el, ha="center", va="center",
                    fontsize=11, fontweight="bold")
        x_start += len(atom) * 0.45 + 0.35

    # Sigma algebra summary
    ax.text(2.25, -1.65, sigma_text, ha="center", fontsize=10, style="italic",
            color="#333")


# --- Left panel: injective Y ---
draw_mapping(axes[0],
             "Injective $Y$: each $\\omega$ gets a unique value",
             ["$\\omega_1$", "$\\omega_2$", "$\\omega_3$"],
             ["$y_1$", "$y_2$", "$y_3$"],
             [(0, "$y_1$"), (1, "$y_2$"), (2, "$y_3$")],
             [["$\\omega_1$"], ["$\\omega_2$"], ["$\\omega_3$"]],
             ["#e8f0fe", "#fce8e6", "#e6f4ea"],
             "$\\sigma(Y) = 2^\\Omega$ (power set, 8 sets)")

# --- Right panel: non-injective Y ---
draw_mapping(axes[1],
             "Non-injective $Y$: two outcomes collide",
             ["$\\omega_1$", "$\\omega_2$", "$\\omega_3$"],
             ["$y_1$", "$y_2$"],
             [(0, "$y_1$"), (1, "$y_1$"), (2, "$y_2$")],
             [["$\\omega_1$", "$\\omega_2$"], ["$\\omega_3$"]],
             ["#e8f0fe", "#e6f4ea"],
             "$\\sigma(Y) = \\{\\emptyset, \\{\\omega_1,\\omega_2\\}, \\{\\omega_3\\}, \\Omega\\}$ (4 sets)")

fig.suptitle("Injective $Y$ $\\Rightarrow$ $\\sigma(Y)$ is maximal; non-injective $\\Rightarrow$ coarser",
             fontsize=13, y=1.0)
fig.tight_layout()
fig.savefig("injective_sigma.png", dpi=150, bbox_inches="tight")
print("Saved injective_sigma.png")
