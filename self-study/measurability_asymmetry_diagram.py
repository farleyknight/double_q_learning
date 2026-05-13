"""
Diagram: asymmetry of measurability.
Constant Y is measurable w.r.t. any G.
Injective Y requires G = power set.
More informative Y => stricter requirement on G.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(11, 7))
ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-0.5, 7.5)
ax.axis("off")

# Title
ax.text(5.25, 7.2,
        "Asymmetry of measurability: more information in $Y$"
        " $\\Rightarrow$ stricter requirement on $\\mathcal{G}$",
        ha="center", fontsize=13, fontweight="bold")

# --- Y axis (vertical): information in Y, low to high ---
ax.annotate("", xy=(0.3, 6.8), xytext=(0.3, 0.5),
            arrowprops=dict(arrowstyle="->", color="#333", lw=2))
ax.text(0.1, 3.7, "information\nin $Y$", ha="center", va="center",
        fontsize=10, rotation=90, color="#333")

# --- Three rows: constant, moderate, injective ---
rows = [
    {
        "y": 1.2, "y_label": "$Y \\equiv c$\n(constant)",
        "info": "zero",
        "sigma_y": "$\\sigma(Y) = \\{\\emptyset, \\Omega\\}$",
        "g_needed": "any $\\mathcal{G}$",
        "bar_width": 1.0, "bar_color": "#4caf50",
        "examples": ["$\\{\\emptyset,\\Omega\\}$", "any coarse", "$2^\\Omega$"],
        "check": [True, True, True],
    },
    {
        "y": 3.5, "y_label": "$Y = \\omega$ mod $2$\n(2-to-1)",
        "info": "partial",
        "sigma_y": "$\\sigma(Y)$ = 4 sets",
        "g_needed": "$\\mathcal{G} \\supseteq \\sigma(Y)$",
        "bar_width": 2.2, "bar_color": "#ff9800",
        "examples": ["$\\{\\emptyset,\\Omega\\}$", "$\\sigma(Y)$", "$2^\\Omega$"],
        "check": [False, True, True],
    },
    {
        "y": 5.8, "y_label": "$Y = \\omega$\n(injective)",
        "info": "maximum",
        "sigma_y": "$\\sigma(Y) = 2^\\Omega$",
        "g_needed": "$\\mathcal{G} = 2^\\Omega$ only",
        "bar_width": 3.8, "bar_color": "#d93025",
        "examples": ["$\\{\\emptyset,\\Omega\\}$", "any coarse", "$2^\\Omega$"],
        "check": [False, False, True],
    },
]

for row in rows:
    y = row["y"]

    # Y label on left
    ax.text(1.6, y, row["y_label"], ha="center", va="center", fontsize=11,
            fontweight="bold", color="#1a73e8")

    # sigma(Y) box
    rect = mpatches.FancyBboxPatch((3.0, y - 0.35), 2.2, 0.7,
                                    boxstyle="round,pad=0.08",
                                    edgecolor="#888", facecolor="#f5f5f5",
                                    linewidth=1.2)
    ax.add_patch(rect)
    ax.text(4.1, y, row["sigma_y"], ha="center", va="center", fontsize=10)

    # "G needed" bar — longer bar = stricter requirement
    bar_x = 5.8
    rect2 = mpatches.FancyBboxPatch((bar_x, y - 0.25), row["bar_width"], 0.5,
                                     boxstyle="round,pad=0.05",
                                     edgecolor=row["bar_color"],
                                     facecolor=row["bar_color"],
                                     alpha=0.3, linewidth=1.5)
    ax.add_patch(rect2)
    ax.text(bar_x + row["bar_width"] + 0.15, y, row["g_needed"],
            ha="left", va="center", fontsize=10, color="#333")

    # Checkmarks / X marks for example G's
    ex_x_positions = [6.0, 7.2, 8.8]
    for x_pos, ex, ok in zip(ex_x_positions, row["examples"], row["check"]):
        if y == rows[-1]["y"]:  # header only on top row... actually put above
            pass
        symbol = "  $\\checkmark$" if ok else "  $\\times$"
        color = "#4caf50" if ok else "#d93025"
        ax.text(x_pos, y - 0.55, ex, ha="center", va="center", fontsize=8.5,
                color="#555")
        ax.text(x_pos, y + 0.45, symbol, ha="center", va="center", fontsize=12,
                color=color, fontweight="bold")

# Column header
ax.text(4.1, 6.7, "$\\sigma(Y)$", ha="center", fontsize=11, fontweight="bold",
        color="#555")
ax.text(7.5, 6.7, "requirement on $\\mathcal{G}$", ha="center", fontsize=11,
        fontweight="bold", color="#555")

# Bottom annotation
ax.text(5.25, -0.2,
        "Bar length = how large $\\mathcal{G}$ must be for $Y$ to be "
        "$\\mathcal{G}$-measurable",
        ha="center", fontsize=10, style="italic", color="#666")

fig.tight_layout()
fig.savefig("/Users/farleyknight/Research/double_q_learning/self-study/measurability_asymmetry.png",
            dpi=150, bbox_inches="tight")
print("Saved measurability_asymmetry.png")
