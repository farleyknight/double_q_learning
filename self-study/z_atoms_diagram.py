"""
Diagram: Z-atoms as the smallest pieces sigma(Z) can distinguish.
Die roll example with Z(omega) = omega mod 2.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

# --- Helper ---
def draw_omega_box(ax, title, atoms, atom_labels, atom_colors):
    """Draw Omega as a rectangle partitioned into atoms, with elements inside."""
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(-0.4, 1.4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=12, pad=12)

    # Outer box for Omega
    outer = mpatches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.03",
                                     edgecolor="black", facecolor="none", linewidth=2)
    ax.add_patch(outer)
    ax.text(0.5, 1.12, "$\\Omega = \\{1,2,3,4,5,6\\}$", ha="center", fontsize=11)

    total_parts = len(atoms)
    x_start = 0.03
    x_end = 0.97
    gap = 0.03
    usable = x_end - x_start - gap * (total_parts - 1)
    widths = [usable * len(a) / 6 for a in atoms]

    x = x_start
    for i, (atom, label, color) in enumerate(zip(atoms, atom_labels, atom_colors)):
        w = widths[i]
        rect = mpatches.FancyBboxPatch((x, 0.05), w, 0.9, boxstyle="round,pad=0.02",
                                        edgecolor="#555", facecolor=color, linewidth=1.5,
                                        alpha=0.5)
        ax.add_patch(rect)
        # Elements inside
        for j, el in enumerate(atom):
            ex = x + w * (j + 0.5) / len(atom)
            ax.text(ex, 0.55, f"${el}$", ha="center", va="center", fontsize=14, fontweight="bold")
        # Atom label below
        ax.text(x + w / 2, 0.18, label, ha="center", va="center", fontsize=9, color="#333")
        x += w + gap


# --- Panel 1: Z = omega mod 2 (two atoms) ---
draw_omega_box(axes[0],
               "$Z(\\omega) = \\omega \\mathrm{mod}\\ 2$\n(2 atoms — \"even or odd\")",
               [[1, 3, 5], [2, 4, 6]],
               ["odd atom", "even atom"],
               ["#e8f0fe", "#fce8e6"])

# --- Panel 2: Z = omega (six singleton atoms) ---
draw_omega_box(axes[1],
               "$Z(\\omega) = \\omega$\n(6 atoms — full resolution)",
               [[1], [2], [3], [4], [5], [6]],
               ["", "", "", "", "", ""],
               ["#e8f0fe", "#fce8e6", "#e6f4ea", "#fef7e0", "#e8f0fe", "#fce8e6"])

# --- Panel 3: Z = constant (one atom) ---
draw_omega_box(axes[2],
               "$Z \\equiv 0$\n(1 atom — everything hidden)",
               [[1, 2, 3, 4, 5, 6]],
               ["single atom = $\\Omega$"],
               ["#e6e6e6"])

fig.suptitle("$Z$-atoms: the smallest non-empty pieces $\\sigma(Z)$ can distinguish",
             fontsize=13, y=1.02)
fig.tight_layout()
fig.savefig("z_atoms.png", dpi=150, bbox_inches="tight")
print("Saved z_atoms.png")
