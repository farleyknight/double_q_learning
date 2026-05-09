import LeanProof.MartingaleConvergence

/-!
# Bounded-difference martingale convergence

The proof in Section 7 of `proof.tex` cites the L²-bounded martingale
convergence theorem applied to the partial sums of a centered, bounded martingale-difference
sequence. The conversion from "bounded differences with summable squared bounds" to
"L²-bounded" is done inline in the paper via the orthogonality identity for martingale
increments.

This file closes that gap. The main result is `martingale_ae_tendsto_of_bdd_diff_summable_sq`:

  Given a martingale `f : ℕ → Ω → ℝ` on a probability space, with `f 0 = 0` a.s.,
  `|f(n+1) - f n| ≤ c n` a.s. for each `n`, and `Summable (fun n => (c n)^2)`,
  there exists a finite limit `f n ω → L(ω)` for almost every `ω`.

The proof is the standard one: orthogonality of increments gives
`∫ (f N)² dμ = Σ_{n<N} ∫ (f(n+1) - f n)² dμ ≤ Σ_{n<N} (c n)²`, uniformly in `N`. So `f` is
L²-bounded, and the conclusion follows from
`DoubleQ.martingale_ae_tendsto_of_eLpNorm_two_bdd`.
-/

open MeasureTheory Filter Topology
open scoped ENNReal NNReal

namespace DoubleQ

variable {Ω : Type*} {m0 : MeasurableSpace Ω} {μ : Measure Ω}
  {ℱ : Filtration ℕ m0} {f : ℕ → Ω → ℝ}

section CondExpHelpers

variable [IsFiniteMeasure μ]

/-- The conditional expectation of a martingale increment with respect to the past is `0`. -/
lemma condExp_diff_eq_zero (hf : Martingale f ℱ μ) (n : ℕ) :
    μ[(fun ω => f (n + 1) ω - f n ω) | ℱ n] =ᵐ[μ] (0 : Ω → ℝ) := by
  have hf1 : Integrable (f (n + 1)) μ := hf.integrable _
  have hfn : Integrable (f n) μ := hf.integrable _
  have hsub : (fun ω => f (n + 1) ω - f n ω) = f (n + 1) - f n := rfl
  rw [hsub]
  refine (condExp_sub hf1 hfn (ℱ n)).trans ?_
  have h1 : μ[f (n + 1) | ℱ n] =ᵐ[μ] f n := hf.condExp_ae_eq (Nat.le_succ n)
  have h2 : μ[f n | ℱ n] =ᵐ[μ] f n := by
    rw [condExp_of_stronglyMeasurable (ℱ.le n) (hf.stronglyMeasurable n) hfn]
  filter_upwards [h1, h2] with ω hω₁ hω₂
  simp [Pi.sub_apply, hω₁, hω₂]

end CondExpHelpers

section L2Bound

variable [IsFiniteMeasure μ]

/-- For a martingale `f` with `f n` and `f(n+1)` in `L²`, the cross term integrates to zero:
`∫ f n · (f(n+1) - f n) dμ = 0`. -/
lemma integral_mul_diff_eq_zero (hf : Martingale f ℱ μ) (n : ℕ)
    (h2n : MemLp (f n) 2 μ) (h2sn : MemLp (f (n + 1)) 2 μ) :
    ∫ ω, f n ω * (f (n + 1) ω - f n ω) ∂μ = 0 := by
  have hdiff_mem : MemLp (f (n + 1) - f n) 2 μ := h2sn.sub h2n
  have h_prod : Integrable (f n * (f (n + 1) - f n)) μ :=
    MemLp.integrable_mul h2n hdiff_mem
  have h_diff_int : Integrable (f (n + 1) - f n) μ := hdiff_mem.integrable (by norm_num)
  have h_pull :
      μ[f n * (f (n + 1) - f n) | ℱ n] =ᵐ[μ] f n * μ[f (n + 1) - f n | ℱ n] :=
    condExp_mul_of_stronglyMeasurable_left (hf.stronglyMeasurable n) h_prod h_diff_int
  have h_diff_zero : μ[f (n + 1) - f n | ℱ n] =ᵐ[μ] (0 : Ω → ℝ) := condExp_diff_eq_zero hf n
  have h_zero : μ[f n * (f (n + 1) - f n) | ℱ n] =ᵐ[μ] (0 : Ω → ℝ) := by
    refine h_pull.trans ?_
    filter_upwards [h_diff_zero] with ω hω
    simp [Pi.mul_apply, hω]
  calc ∫ ω, f n ω * (f (n + 1) ω - f n ω) ∂μ
      = ∫ ω, (f n * (f (n + 1) - f n)) ω ∂μ := rfl
    _ = ∫ ω, μ[f n * (f (n + 1) - f n) | ℱ n] ω ∂μ := (integral_condExp (ℱ.le n)).symm
    _ = ∫ _, (0 : ℝ) ∂μ := integral_congr_ae h_zero
    _ = 0 := integral_zero _ _

/-- Pythagorean identity for one martingale step:
`∫ (f(n+1))² = ∫ (f n)² + ∫ (f(n+1) - f n)²`. -/
lemma integral_sq_succ (hf : Martingale f ℱ μ) (n : ℕ)
    (h2n : MemLp (f n) 2 μ) (h2sn : MemLp (f (n + 1)) 2 μ) :
    ∫ ω, (f (n + 1) ω) ^ 2 ∂μ
      = ∫ ω, (f n ω) ^ 2 ∂μ + ∫ ω, (f (n + 1) ω - f n ω) ^ 2 ∂μ := by
  have hdiff_mem : MemLp (f (n + 1) - f n) 2 μ := h2sn.sub h2n
  have h_int_fn_sq : Integrable (fun ω => (f n ω) ^ 2) μ := by
    simpa [sq] using h2n.integrable_mul h2n
  have h_int_diff_sq : Integrable (fun ω => (f (n + 1) ω - f n ω) ^ 2) μ := by
    have := hdiff_mem.integrable_mul hdiff_mem
    simpa [sq, Pi.sub_apply] using this
  have h_int_cross : Integrable (fun ω => f n ω * (f (n + 1) ω - f n ω)) μ := by
    have := h2n.integrable_mul hdiff_mem
    simpa [Pi.sub_apply] using this
  have h_expand : (fun ω => (f (n + 1) ω) ^ 2) =
      (fun ω => (f n ω) ^ 2 + 2 * (f n ω * (f (n + 1) ω - f n ω))
        + (f (n + 1) ω - f n ω) ^ 2) := by
    funext ω; ring
  rw [h_expand]
  have e1 : ∫ ω, ((f n ω) ^ 2 + 2 * (f n ω * (f (n + 1) ω - f n ω)))
              + (f (n + 1) ω - f n ω) ^ 2 ∂μ
            = ∫ ω, (f n ω) ^ 2 + 2 * (f n ω * (f (n + 1) ω - f n ω)) ∂μ
              + ∫ ω, (f (n + 1) ω - f n ω) ^ 2 ∂μ :=
    integral_add (h_int_fn_sq.add (h_int_cross.const_mul 2)) h_int_diff_sq
  have e2 : ∫ ω, (f n ω) ^ 2 + 2 * (f n ω * (f (n + 1) ω - f n ω)) ∂μ
            = ∫ ω, (f n ω) ^ 2 ∂μ
              + ∫ ω, 2 * (f n ω * (f (n + 1) ω - f n ω)) ∂μ :=
    integral_add h_int_fn_sq (h_int_cross.const_mul 2)
  have e3 : ∫ ω, 2 * (f n ω * (f (n + 1) ω - f n ω)) ∂μ
            = 2 * ∫ ω, f n ω * (f (n + 1) ω - f n ω) ∂μ :=
    integral_const_mul _ _
  rw [e1, e2, e3, integral_mul_diff_eq_zero hf n h2n h2sn]
  ring

end L2Bound

section MainTheorem

variable [IsProbabilityMeasure μ]

/-- A martingale on a probability space, with `f 0 = 0` a.s. and bounded differences
`|f(n+1) - f n| ≤ c n` a.s., is `L²` at every step and satisfies
`∫ (f N)² dμ ≤ Σ_{n<N} (c n)²`. -/
lemma memLp_two_and_integral_sq_le_sum_of_bdd_diff (hf : Martingale f ℱ μ)
    (hf0 : f 0 =ᵐ[μ] 0) {c : ℕ → ℝ}
    (hbdd : ∀ n, ∀ᵐ ω ∂μ, |f (n + 1) ω - f n ω| ≤ c n) (N : ℕ) :
    MemLp (f N) 2 μ ∧
      ∫ ω, (f N ω) ^ 2 ∂μ ≤ ∑ n ∈ Finset.range N, (c n) ^ 2 := by
  induction N with
  | zero =>
    refine ⟨?_, ?_⟩
    · refine ⟨((hf.stronglyMeasurable 0).mono (ℱ.le 0)).aestronglyMeasurable, ?_⟩
      rw [eLpNorm_congr_ae hf0]; simp
    · rw [integral_congr_ae (g := fun _ => 0)]
      · simp
      · filter_upwards [hf0] with ω hω; simp [hω]
  | succ N ih =>
    obtain ⟨hL2N, hSumN⟩ := ih
    have hbN := hbdd N
    have hcN_nonneg : 0 ≤ c N := by
      rcases hbN.exists with ⟨ω, hω⟩
      exact (abs_nonneg _).trans hω
    have hdiff_meas : AEStronglyMeasurable (fun ω => f (N + 1) ω - f N ω) μ :=
      ((hf.stronglyMeasurable (N + 1)).mono (ℱ.le _)).aestronglyMeasurable.sub
        ((hf.stronglyMeasurable N).mono (ℱ.le _)).aestronglyMeasurable
    have hdiff_bdd : ∀ᵐ ω ∂μ, ‖f (N + 1) ω - f N ω‖ ≤ c N := by
      filter_upwards [hbN] with ω hω; simpa [Real.norm_eq_abs] using hω
    have hdiff_inf : MemLp (fun ω => f (N + 1) ω - f N ω) ∞ μ :=
      memLp_top_of_bound hdiff_meas (c N) hdiff_bdd
    have hdiff_mem : MemLp (fun ω => f (N + 1) ω - f N ω) 2 μ :=
      hdiff_inf.mono_exponent le_top
    have hL2sN : MemLp (f (N + 1)) 2 μ := by
      have hsum : MemLp (fun ω => (f (N + 1) ω - f N ω) + f N ω) 2 μ :=
        hdiff_mem.add hL2N
      refine hsum.ae_eq ?_
      refine Filter.Eventually.of_forall fun ω => ?_
      change f (N + 1) ω - f N ω + f N ω = f (N + 1) ω
      ring
    refine ⟨hL2sN, ?_⟩
    rw [integral_sq_succ hf N hL2N hL2sN, Finset.sum_range_succ]
    have h_diff_sq_le : ∫ ω, (f (N + 1) ω - f N ω) ^ 2 ∂μ ≤ (c N) ^ 2 := by
      have h_pt : ∀ᵐ ω ∂μ, (f (N + 1) ω - f N ω) ^ 2 ≤ (c N) ^ 2 := by
        filter_upwards [hbN] with ω hω
        rw [show (f (N + 1) ω - f N ω) ^ 2 = |f (N + 1) ω - f N ω| ^ 2 from (sq_abs _).symm]
        exact pow_le_pow_left₀ (abs_nonneg _) hω 2
      have h_int_diff_sq : Integrable (fun ω => (f (N + 1) ω - f N ω) ^ 2) μ := by
        have := hdiff_mem.integrable_mul hdiff_mem
        simpa [sq, Pi.sub_apply] using this
      calc ∫ ω, (f (N + 1) ω - f N ω) ^ 2 ∂μ
          ≤ ∫ _, (c N) ^ 2 ∂μ :=
            integral_mono_ae h_int_diff_sq (integrable_const _) h_pt
        _ = (c N) ^ 2 := by simp
    linarith

omit [IsProbabilityMeasure μ] in
/-- Convert an `L²` integral bound to an `eLpNorm` bound. -/
private lemma eLpNorm_two_le_ofReal_sqrt_of_integral_sq_le
    {g : Ω → ℝ} (hg : MemLp g 2 μ) {T : ℝ}
    (h : ∫ ω, (g ω) ^ 2 ∂μ ≤ T) :
    eLpNorm g 2 μ ≤ ENNReal.ofReal (Real.sqrt T) := by
  rw [hg.eLpNorm_eq_integral_rpow_norm (by norm_num : (2 : ℝ≥0∞) ≠ 0)
    (by norm_num : (2 : ℝ≥0∞) ≠ ∞)]
  apply ENNReal.ofReal_le_ofReal
  have h_two_toReal : ((2 : ℝ≥0∞).toReal) = (2 : ℝ) := by simp
  have h_norm_eq : ∀ ω, ‖g ω‖ ^ ((2 : ℝ≥0∞).toReal) = (g ω) ^ 2 := by
    intro ω
    rw [h_two_toReal, Real.norm_eq_abs]
    rw [show (2 : ℝ) = ((2 : ℕ) : ℝ) from by norm_cast]
    rw [Real.rpow_natCast]
    exact sq_abs _
  rw [integral_congr_ae (Filter.Eventually.of_forall h_norm_eq)]
  have h_inv : ((2 : ℝ≥0∞).toReal)⁻¹ = (1 / 2 : ℝ) := by rw [h_two_toReal]; norm_num
  rw [h_inv, ← Real.sqrt_eq_rpow]
  exact Real.sqrt_le_sqrt h

/-- **Bounded-difference martingale convergence**.

A real-valued martingale `f : ℕ → Ω → ℝ` adapted to a filtration `ℱ` on a probability space,
with `f 0 = 0` almost surely, increments bounded by `|f(n+1) - f n| ≤ c n` almost surely, and
`Σ (c n)² < ∞`, converges almost surely to a finite limit.

This is the precise lemma invoked in Section 7 of `proof.tex`, applied
with `c n = 16 · α n`: the centered log-increments `M_{n+1} = ΔL_{n+1} - 𝔼[ΔL_{n+1} | 𝓕_n]`
satisfy `|M_{n+1}| ≤ 16·α_n`, and `Σ α_n² < ∞`. -/
theorem martingale_ae_tendsto_of_bdd_diff_summable_sq (hf : Martingale f ℱ μ)
    (hf0 : f 0 =ᵐ[μ] 0) {c : ℕ → ℝ}
    (hbdd : ∀ n, ∀ᵐ ω ∂μ, |f (n + 1) ω - f n ω| ≤ c n)
    (hsum : Summable (fun n => (c n) ^ 2)) :
    ∀ᵐ ω ∂μ, ∃ L, Tendsto (fun N => f N ω) atTop (𝓝 L) := by
  set T : ℝ := ∑' n, (c n) ^ 2 with hTdef
  set R : ℝ≥0 := ⟨Real.sqrt T, Real.sqrt_nonneg _⟩ with hRdef
  have hL2_bdd : ∀ N, eLpNorm (f N) 2 μ ≤ (R : ℝ≥0∞) := by
    intro N
    obtain ⟨hMem, hSum⟩ := memLp_two_and_integral_sq_le_sum_of_bdd_diff hf hf0 hbdd N
    have h_int_le : ∫ ω, (f N ω) ^ 2 ∂μ ≤ T :=
      hSum.trans (hsum.sum_le_tsum (Finset.range N) (fun _ _ => sq_nonneg _))
    have h := eLpNorm_two_le_ofReal_sqrt_of_integral_sq_le hMem h_int_le
    -- Convert `ENNReal.ofReal (Real.sqrt T) = ↑R`.
    have hR_eq : ENNReal.ofReal (Real.sqrt T) = (R : ℝ≥0∞) :=
      ENNReal.ofReal_coe_nnreal (p := R)
    rw [← hR_eq]; exact h
  filter_upwards [martingale_ae_tendsto_of_eLpNorm_two_bdd hf hL2_bdd] with ω hω
  obtain ⟨L, hL⟩ := hω
  exact ⟨L, hL⟩

end MainTheorem

end DoubleQ
