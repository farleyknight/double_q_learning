import Mathlib.Probability.Martingale.Convergence
import Mathlib.MeasureTheory.Function.LpSeminorm.CompareExp

/-!
# The martingale convergence theorem invoked in the Double Q-learning counterexample

The proof of unboundedness of Double Q-learning with linear function approximation
(Section 7 of `proof.tex`) appeals to:

> By the martingale convergence theorem for square-integrable martingales with summable
> conditional variances, the martingale partial sums `Σ_{n=0}^{N-1} M_{n+1}` converge
> almost surely to a finite random limit.

In that proof the martingale-difference sequence is bounded by `|M_{n+1}| ≤ 16·α_n`, so
`E[M_{n+1}^2 | 𝓕_n] ≤ 256·α_n^2`, and `Σ α_n^2 < ∞`. Hence the partial-sum martingale
`S_N = Σ_{n=0}^{N-1} M_{n+1}` satisfies `E[S_N^2] = Σ_{n=0}^{N-1} E[M_{n+1}^2] ≤ 256·Σ α_n^2`,
uniformly in `N`. So the appeal is really to:

  *An L²-bounded martingale on a probability space converges almost surely.*

The latter follows from Mathlib's a.e. martingale convergence theorem for L¹-bounded
submartingales, namely
`MeasureTheory.Submartingale.exists_ae_tendsto_of_bdd`
(an internal step of `MeasureTheory.Submartingale.ae_tendsto_limitProcess` in
`Mathlib.Probability.Martingale.Convergence`), by passing from L² to L¹ with
`MeasureTheory.eLpNorm_le_eLpNorm_of_exponent_le` on a probability measure.
-/

open MeasureTheory Filter Topology
open scoped ENNReal NNReal

namespace DoubleQ

variable {Ω : Type*} {m0 : MeasurableSpace Ω}

/-- **L²-bounded martingale convergence**.

A real-valued martingale `f : ℕ → Ω → ℝ` adapted to a filtration `ℱ` on a probability space,
whose `L²` norms are uniformly bounded by some `R < ∞`, converges almost surely to a finite
limit.

This is the precise lemma invoked in Section 7 of the Double Q-learning counterexample
proof, applied to the partial-sum martingale of the centered log-increments
`M_{n+1} = ΔL_{n+1} - 𝔼[ΔL_{n+1} | 𝓕_n]`. -/
theorem martingale_ae_tendsto_of_eLpNorm_two_bdd
    {μ : Measure Ω} [IsProbabilityMeasure μ]
    {ℱ : Filtration ℕ m0} {f : ℕ → Ω → ℝ} {R : ℝ≥0}
    (hf : Martingale f ℱ μ) (hbdd : ∀ n, eLpNorm (f n) 2 μ ≤ R) :
    ∀ᵐ ω ∂μ, ∃ c, Tendsto (fun n => f n ω) atTop (𝓝 c) := by
  refine hf.submartingale.exists_ae_tendsto_of_bdd (R := R) (fun n => ?_)
  have hmeas : AEStronglyMeasurable (f n) μ :=
    ((hf.stronglyMeasurable n).mono (ℱ.le n)).aestronglyMeasurable
  exact (eLpNorm_le_eLpNorm_of_exponent_le one_le_two hmeas).trans (hbdd n)

end DoubleQ
