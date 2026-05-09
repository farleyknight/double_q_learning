# Double Q-Learning Counterexample

A counterexample to general convergence of symmetric Double Q-learning under linear function approximation. On a single-state, two-action MDP with zero rewards — where the optimal action-value function Q\* ≡ 0 is exactly representable — the parameter vector diverges almost surely from every strictly positive initialization.

## Status and authorship

This repository is the artifact of an AI-orchestrated investigation. Concretely:

- The **proof** (`proof.tex`, `proof.md`, `proof.pdf`) was drafted by ChatGPT.
- The **literature review** (`literature_review.md`) was drafted by Claude.
- The **Lean 4 / Mathlib formalization** of the martingale convergence step (`LeanProof/`) was written by Claude Code.
- I (Farley Knight) framed the question, prompted each piece, and assembled the repository. I have not yet independently verified the martingale argument in detail, and have not yet audited the Lean formalization against the prose proof. Treat the result accordingly until that work is done.

Intended use: a public scratchpad for working through the result and its formalization. Not a peer-reviewed paper, and currently not claiming to be one.

## The result

**Theorem.** There exists a finite discounted MDP, a stationary off-policy behavior distribution, a bounded linear feature map, and a Robbins–Monro stepsize sequence such that symmetric Double Q-learning with linear function approximation is unbounded almost surely from every strictly positive initialization — even though Q\* ≡ 0 is exactly representable by the feature map.

The example is one state, two actions, zero rewards, one scalar feature, and a fixed off-policy behavior policy. See `proof.md` for the full argument.

## Where this sits in the literature

Convergence of the symmetric two-estimator Double Q-learning algorithm under linear function approximation is repeatedly described as open in the recent literature — Weng et al. (2020), Xiong et al. (2020), Zhao et al. (2021), Lee & He (2019/2020). This note resolves the negative side of that question: no fully general convergence theorem can exist.

The instability mechanism is the classical Tsitsiklis–Van Roy (1996) off-policy TD example, restaged in the action space. The contribution is therefore not the *phenomenon* — which has been suspected for years and observed empirically by van Hasselt et al. (2018) for related variants — but the formal almost-sure statement for the specific symmetric two-estimator algorithm, and the positive-quadrant invariance argument that pins the greedy action and reduces the analysis to a tractable linear stochastic recursion.

See `literature_review.md` for the careful placement, including the framing caveats a reviewer would raise.

## Documents

- **`proof.tex`** / **`proof.pdf`** / **`proof.md`** — the proof. Constructs the MDP, establishes positivity invariance of the parameters, and uses a martingale decomposition on log Sₙ (where Sₙ = θ_{A,n} + θ_{B,n}) to turn mean-field instability into almost-sure divergence.
- **`literature_review.md`** — where the result sits relative to existing work: what's clearly established, what's genuinely new, and where the framing could be sharpened.
- **`LeanProof/`** — Lean 4 / Mathlib formalization of the martingale convergence step (Section 7 of the proof). See `LeanProof/README.md` for the module map.
- **`simulate.py`** / **`divergence.png`** — numerical simulation confirming divergence from 4 initializations × 20 seeds × 100k steps.

## What's verified, what isn't

- The almost-sure divergence claim has been **verified by simulation** (`simulate.py`). From four initializations (θ₀ ∈ {0.01, 0.1, 1.0, 10.0}) and 20 seeds each, all trajectories diverge, with log Sₙ tracking the theoretical drift 0.34a·Hₙ. See `divergence.png`.
- The proof has been read end-to-end but **not deeply verified by a human**; the spot-checks done so far (mean-drift averaging in Section 6, positivity bound in Section 4) are the obvious ones, not exhaustive.
- The Lean formalization **compiles**, but a human-readable correspondence between the Lean lemmas and Section 7 of the prose proof has not yet been written.

## Open items

- ~~Numerical simulation confirming Sₙ → ∞ for representative initializations and stepsize choices.~~ Done (`simulate.py`).
- A documented mapping from Lean lemma names to `proof.md` section numbers.
- Removing or weakening the strictly-positive initialization assumption.
- Extending the analysis to non-symmetric, target-network, or asynchronous variants of Double Q-learning.
- Sharper framing of the contribution against Tsitsiklis–Van Roy (1996), per the caveats in `literature_review.md`.
