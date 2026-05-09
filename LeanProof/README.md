# LeanProof

Lean 4 / Mathlib formalization of the martingale convergence step used in
[../proof.tex](../proof.tex).

## What is formalized

The paper's Section 7 ("Martingale fluctuations are negligible") appeals to two facts:

1. The martingale convergence theorem for L²-bounded (equivalently, summable conditional
   variance) martingales.
2. The orthogonality identity that converts a bounded-difference martingale with summable
   squared bounds into an L²-bounded one.

Both are formalized here against Mathlib `v4.29.1`.

## Module map

| Lean declaration | Paper reference | Statement |
|---|---|---|
| [`DoubleQ.martingale_ae_tendsto_of_eLpNorm_two_bdd`](LeanProof/MartingaleConvergence.lean) | Section 7, "the martingale convergence theorem for square-integrable martingales" | An L²-bounded real martingale on a probability space converges almost surely. |
| [`DoubleQ.condExp_diff_eq_zero`](LeanProof/L2BoundedMartingale.lean) | (used inline in Section 7) | $\mathbb{E}[f_{n+1} - f_n \mid \mathcal{F}_n] = 0$ a.s. |
| [`DoubleQ.integral_mul_diff_eq_zero`](LeanProof/L2BoundedMartingale.lean) | Section 7, orthogonality of increments | $\int f_n (f_{n+1} - f_n) \, d\mu = 0$. |
| [`DoubleQ.integral_sq_succ`](LeanProof/L2BoundedMartingale.lean) | Pythagorean identity | $\int f_{n+1}^2 = \int f_n^2 + \int (f_{n+1} - f_n)^2$. |
| [`DoubleQ.memLp_two_and_integral_sq_le_sum_of_bdd_diff`](LeanProof/L2BoundedMartingale.lean) | "the partial-sum martingale satisfies $\mathbb{E}[S_N^2] \le 256 \sum \alpha_n^2$" | $f_0 = 0$ + $\lvert f_{n+1} - f_n \rvert \le c_n$ implies $\int f_N^2 \le \sum_{n<N} c_n^2$ and $f_N \in L^2$. |
| [`DoubleQ.martingale_ae_tendsto_of_bdd_diff_summable_sq`](LeanProof/L2BoundedMartingale.lean) | Section 7 conclusion | Real martingale on a probability space, $f_0 = 0$ a.s., $\lvert f_{n+1} - f_n \rvert \le c_n$ a.s., $\sum c_n^2 < \infty$ ⟹ $f_N$ converges a.s. |

## Mathlib dependencies

Reduces to the following Mathlib theorems, in order of distance from the leaf:

- [`MeasureTheory.Submartingale.exists_ae_tendsto_of_bdd`](.lake/packages/mathlib/Mathlib/Probability/Martingale/Convergence.lean) — almost-sure convergence of L¹-bounded submartingales.
- [`MeasureTheory.eLpNorm_le_eLpNorm_of_exponent_le`](.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSeminorm/CompareExp.lean) — L² ⟹ L¹ on a probability space.
- [`MeasureTheory.condExp_mul_of_stronglyMeasurable_left`](.lake/packages/mathlib/Mathlib/MeasureTheory/Function/ConditionalExpectation/PullOut.lean) — pull-out property for the cross term.
- [`Martingale.condExp_ae_eq`](.lake/packages/mathlib/Mathlib/Probability/Martingale/Basic.lean) — defining property of a martingale.

## Build

```bash
cd LeanProof
lake build
```

The first build downloads Mathlib's prebuilt cloud cache (~2 GB on disk). Subsequent builds
are incremental.

## IDE notes

Open the `LeanProof/` directory itself as the VSCode workspace root, not the parent. The
Lean extension expects a `lakefile.toml` and `lake-manifest.json` at the workspace root,
and gets confused if it has to walk down to find them.

If the editor shows a long `git fetch --tags` trace ending in
`Failed to configure the Lake workspace. Please restart the server after fixing the error
above.` — it is replaying a cached error from an earlier broken-state startup. Run
**`Lean 4: Server: Restart Server`** from the command palette and the cache clears.
