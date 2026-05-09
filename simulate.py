"""
Simulation confirming almost-sure divergence of symmetric Double Q-learning
with linear function approximation on the counterexample MDP.

MDP: one state, two actions, zero rewards, gamma=0.9
Features: phi(a1)=1, phi(a2)=2
Behavior policy: mu(a1)=0.9, mu(a2)=0.1
Stepsize: alpha_n = a/(n+1), a=1/16
"""

import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt

# MDP and algorithm parameters
GAMMA = 0.9
PHI = np.array([1.0, 2.0])  # phi(a1), phi(a2)
MU_A1 = 0.9                  # behavior policy probability of a1
A = 1.0 / 16.0               # stepsize constant
N_STEPS = 100_000
INITS = [0.01, 0.1, 1.0, 10.0]  # theta_A = theta_B at t=0
N_SEEDS = 20


def run_double_q(theta_a0, theta_b0, n_steps, seed):
    rng = np.random.default_rng(seed)
    theta_a, theta_b = theta_a0, theta_b0
    log_sigma = np.empty(n_steps + 1)
    log_sigma[0] = np.log(theta_a + theta_b)

    for n in range(n_steps):
        alpha = A / (n + 1)
        # Sample action from behavior policy
        x = PHI[0] if rng.random() < MU_A1 else PHI[1]
        # Both parameters positive => greedy action is a2 => target feature is 2
        target_feature = PHI[1]
        if rng.random() < 0.5:
            # Update estimator A
            td = GAMMA * target_feature * theta_b - x * theta_a
            theta_a += alpha * x * td
        else:
            # Update estimator B
            td = GAMMA * target_feature * theta_a - x * theta_b
            theta_b += alpha * x * td
        log_sigma[n + 1] = np.log(theta_a + theta_b)

    return log_sigma


# Theoretical drift: sum_{k=0}^{n-1} 0.34 * a/(k+1)
steps = np.arange(N_STEPS + 1)
theory = np.zeros(N_STEPS + 1)
theory[1:] = 0.34 * A * np.cumsum(1.0 / np.arange(1, N_STEPS + 1))

fig, axes = plt.subplots(len(INITS), 1, figsize=(10, 3 * len(INITS)), sharex=True)

for ax, init in zip(axes, INITS):
    for seed in range(N_SEEDS):
        log_s = run_double_q(init, init, N_STEPS, seed)
        ax.plot(steps, log_s, alpha=0.3, linewidth=0.5)
    # Overlay theoretical drift (shifted to match initial value)
    log_s0 = np.log(2 * init)
    ax.plot(steps, log_s0 + theory, "k--", linewidth=1.5, label="theoretical drift")
    ax.set_ylabel("log Sₙ")
    ax.set_title(f"θ_A(0) = θ_B(0) = {init}")
    ax.legend(loc="upper left", fontsize=8)

axes[-1].set_xlabel("step n")
fig.suptitle("Double Q-learning divergence (20 seeds per initialization)", y=1.01)
fig.tight_layout()
fig.savefig("divergence.png", dpi=150, bbox_inches="tight")
print("Saved divergence.png")

# Print final S_n summary for one initialization
init = 1.0
finals = []
for seed in range(N_SEEDS):
    log_s = run_double_q(init, init, N_STEPS, seed)
    finals.append(np.exp(log_s[-1]))
finals = np.array(finals)
print(f"\nθ_A(0)=θ_B(0)=1.0, {N_SEEDS} seeds, {N_STEPS} steps:")
print(f"  S_N  min={finals.min():.2f}  median={np.median(finals):.2f}  max={finals.max():.2f}")
