# Double Q-Learning Counterexample

A counterexample to general convergence of symmetric Double Q-learning under linear
function approximation.

## Documents

- [proof.tex](proof.tex) ([pdf](proof.pdf), [md](proof.md)) — the paper. Constructs a
  one-state, two-action MDP with zero rewards on which Double Q-learning's parameters
  diverge almost surely from every strictly positive initialization.
- [literature_review.md](literature_review.md) — survey of where the result sits in the
  existing literature on off-policy convergence and the deadly triad.
- [LeanProof/](LeanProof/) — Lean 4 / Mathlib formalization of the martingale convergence
  step the paper invokes. See [LeanProof/README.md](LeanProof/README.md) for the module
  map.
