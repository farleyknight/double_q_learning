"""
Diagram: Radon-Nikodym theorem gives existence/uniqueness of E[X | G].

Shows: X and P on (Omega, F) => define nu(G) = int_G X dP on (Omega, G)
       => nu << P|_G => Radon-Nikodym => derivative Z = E[X | G].
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(-0.5, 12)
ax.set_ylim(-1.5, 7)
ax.axis("off")

# Title
ax.text(6, 6.7,
        "Radon\u2013Nikodym theorem $\\Rightarrow$ existence and uniqueness of "
        "$E[X \\mid \\mathcal{G}]$",
        ha="center", fontsize=14, fontweight="bold")

# --- Box 1: The setup ---
box1 = mpatches.FancyBboxPatch((0.3, 4.2), 3.5, 2.0,
                                boxstyle="round,pad=0.15",
                                edgecolor="#1a73e8", facecolor="#e8f0fe",
                                linewidth=2)
ax.add_patch(box1)
ax.text(2.05, 5.85, "Given", ha="center", fontsize=11, fontweight="bold",
        color="#1a73e8")
ax.text(2.05, 5.35, "$X$ on $(\\Omega, \\mathcal{F}, \\mathbb{P})$",
        ha="center", fontsize=12)
ax.text(2.05, 4.75, "$\\mathcal{G} \\subseteq \\mathcal{F}$ (sub-$\\sigma$-algebra)",
        ha="center", fontsize=11)

# Arrow 1
ax.annotate("", xy=(5.0, 5.2), xytext=(3.9, 5.2),
            arrowprops=dict(arrowstyle="-|>", color="#333", lw=2))
ax.text(4.45, 5.55, "define", ha="center", fontsize=10, style="italic", color="#555")

# --- Box 2: Define nu ---
box2 = mpatches.FancyBboxPatch((5.0, 4.2), 3.2, 2.0,
                                boxstyle="round,pad=0.15",
                                edgecolor="#ff9800", facecolor="#fef7e0",
                                linewidth=2)
ax.add_patch(box2)
ax.text(6.6, 5.85, "New measure on $\\mathcal{G}$",
        ha="center", fontsize=11, fontweight="bold", color="#ff9800")
ax.text(6.6, 5.2, "$\\nu(G) = \\int_G X \\, d\\mathbb{P}$",
        ha="center", fontsize=13)
ax.text(6.6, 4.6, "for each $G \\in \\mathcal{G}$",
        ha="center", fontsize=10, color="#555")

# Arrow 2
ax.annotate("", xy=(9.3, 5.2), xytext=(8.3, 5.2),
            arrowprops=dict(arrowstyle="-|>", color="#333", lw=2))
ax.text(8.8, 5.55, "check", ha="center", fontsize=10, style="italic", color="#555")

# --- Box 3: Absolute continuity ---
box3 = mpatches.FancyBboxPatch((9.3, 4.2), 2.4, 2.0,
                                boxstyle="round,pad=0.15",
                                edgecolor="#9c27b0", facecolor="#f3e5f5",
                                linewidth=2)
ax.add_patch(box3)
ax.text(10.5, 5.85, "Key condition", ha="center", fontsize=11,
        fontweight="bold", color="#9c27b0")
ax.text(10.5, 5.2, "$\\nu \\ll \\mathbb{P}|_{\\mathcal{G}}$",
        ha="center", fontsize=14)
ax.text(10.5, 4.55, "$\\mathbb{P}(G)=0 \\Rightarrow \\nu(G)=0$",
        ha="center", fontsize=9.5, color="#555")

# Big arrow down
ax.annotate("", xy=(6.0, 3.5), xytext=(10.5, 4.1),
            arrowprops=dict(arrowstyle="-|>", color="#d93025", lw=2.5,
                            connectionstyle="arc3,rad=0.3"))
ax.text(9.5, 3.5, "Radon\u2013Nikodym\ntheorem", ha="center", fontsize=11,
        fontweight="bold", color="#d93025")

# --- Box 4: The result ---
box4 = mpatches.FancyBboxPatch((2.5, 1.5), 7.0, 1.8,
                                boxstyle="round,pad=0.15",
                                edgecolor="#4caf50", facecolor="#e6f4ea",
                                linewidth=2.5)
ax.add_patch(box4)
ax.text(6.0, 2.95, "Conclusion", ha="center", fontsize=11,
        fontweight="bold", color="#4caf50")
ax.text(6.0, 2.3,
        "$\\exists\\, Z$ ($\\mathcal{G}$-measurable, unique a.s.) such that "
        "$\\nu(G) = \\int_G Z \\, d\\mathbb{P}$  for all $G \\in \\mathcal{G}$",
        ha="center", fontsize=11.5)
ax.text(6.0, 1.75,
        "This $Z = \\dfrac{d\\nu}{d\\mathbb{P}}$ is exactly $E[X \\mid \\mathcal{G}]$",
        ha="center", fontsize=12, color="#333")

# --- Bottom: finite case note ---
ax.text(6.0, 0.5,
        "Finite case: just average $X$ on each $\\mathcal{G}$-atom. "
        "Radon\u2013Nikodym is what makes it work on arbitrary probability spaces.",
        ha="center", fontsize=10, style="italic", color="#888",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#f9f9f9",
                  edgecolor="#ddd", linewidth=1))

fig.tight_layout()
fig.savefig("/Users/farleyknight/Research/double_q_learning/self-study/radon_nikodym.png",
            dpi=150, bbox_inches="tight")
print("Saved radon_nikodym.png")
