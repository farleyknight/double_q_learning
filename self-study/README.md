# Self-Study: Martingales for the Double Q-Learning Counterexample

## Why this exists

Section 8 of `proof.md` is the technical core of the divergence argument, and it's the piece I have not yet independently verified. It invokes a "martingale convergence theorem for square-integrable martingales with summable conditional variances" without proof. This document is my plan for getting to the point where I can state, verify, and defend that step on my own — without the textbook open.

The success criterion is a single paragraph, written in my own words, that:

1. Names the theorem being invoked.
2. States it precisely.
3. Verifies its hypotheses against the construction in Sections 7–8 of the proof.

Everything below is the path to writing that paragraph.

## The target paragraph

This is what passing the bar looks like. After completing this study plan, I should be able to write something close to this from memory:

> Section 8 invokes the L² martingale convergence theorem in its conditional-variance form (Williams Ch 12): if $(M_n)$ is a martingale with $M_0 = 0$ and the predictable quadratic variation $\langle M \rangle_\infty := \sum_n \mathbb{E}[(M_{n+1} - M_n)^2 \mid \mathcal{F}_n]$ is almost surely finite, then $M_n$ converges almost surely to a finite limit.
>
> The proof applies this to the partial-sum martingale $S_N = \sum_{n=0}^{N-1} M_{n+1}$, where each $M_{n+1} = \Delta L_{n+1} - \mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n]$ is centered by construction. The two hypotheses are verified as follows:
>
> (i) **$S_N$ is a martingale with $S_0 = 0$.** By construction $\mathbb{E}[M_{n+1} \mid \mathcal{F}_n] = 0$, so $\mathbb{E}[S_{n+1} - S_n \mid \mathcal{F}_n] = 0$.
>
> (ii) **$\langle S \rangle_\infty < \infty$ a.s.** The proof shows the pathwise bound $|M_{n+1}| \leq 16\alpha_n$, hence $\mathbb{E}[M_{n+1}^2 \mid \mathcal{F}_n] \leq 256\alpha_n^2$. Since $\alpha_n = a/(n+1)$ satisfies $\sum_n \alpha_n^2 < \infty$ (one of the standard Robbins–Monro conditions), $\langle S \rangle_\infty \leq 256 \sum_n \alpha_n^2 < \infty$ deterministically — much stronger than the a.s. version the theorem requires.
>
> Hence $S_N$ converges a.s. to a finite limit. Combined with the divergent-drift bound $\sum_n \mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n] \to +\infty$ established in Section 7, the Doob decomposition $L_N = L_0 + \sum_n \mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n] + S_N$ yields $L_N \to +\infty$ a.s., and therefore $W_N \to \infty$ a.s.

If I can write that without notes — name the right theorem, state it correctly, and point at the lines of the proof that verify each hypothesis — the proof's central technical step is no longer something I'm taking on faith.

## Scope

Williams covers roughly four things relevant to this proof:

- **Conditional expectation** (Ch 9) — the tool used to define every "given $\mathcal{F}_n$" quantity.
- **Martingale definitions, Doob decomposition** (Ch 10) — the algebraic setup.
- **Almost-sure martingale convergence** (Ch 11) — Doob's theorem for L¹-bounded martingales. Not directly invoked, but the technique generalizes.
- **Square-integrable martingales** (Ch 12) — *this is the theorem actually used in Section 8.*

Out of scope: optional stopping (Williams Ch 10 §10.10 onward and Ch 13), uniform integrability beyond a basic acquaintance, continuous-time martingales, backward martingales. The proof doesn't need them. If something I'm reading turns out to require them, that's a sign I've drifted off-plan.

## Reading plan

Five to seven sessions of 60–90 minutes each. Total commute time roughly 8–12 hours. Each session ends with a checkpoint to satisfy before moving on.

### Session 1 — Conditional expectation (Williams Ch 9)

Read for the definition (§9.1–9.3) and the tower property (§9.7). Skim the existence/uniqueness proof — important to know it's there, not crash-blocking to follow every line.

The proof uses conditional expectation everywhere: $\mathbb{E}[Y_{n+1} \mid \mathcal{F}_n]$, $\mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n]$, $\mathbb{E}[M_{n+1}^2 \mid \mathcal{F}_n]$.

**Checkpoint.** I should be comfortable with:

- What "$\mathbb{E}[Y \mid \mathcal{F}]$ is the best $\mathcal{F}$-measurable approximation of $Y$ in $L^2$" means.
- The tower property $\mathbb{E}[\mathbb{E}[Y \mid \mathcal{G}] \mid \mathcal{F}] = \mathbb{E}[Y \mid \mathcal{F}]$ when $\mathcal{F} \subseteq \mathcal{G}$. *This is what justifies the "first average over the estimator choice, then over the action" two-step calculation in Section 7 of the proof.*

### Session 2 — Martingales and the Doob decomposition (Williams Ch 10, §10.1–10.10)

Read for definitions: filtration, adapted process, predictable process, martingale, sub/supermartingale.

The Doob decomposition (§10.10) is the one piece of Ch 10 that's directly invoked. Any adapted integrable process $X_n$ has a unique decomposition $X_n = X_0 + A_n + M_n$ where $A_n$ is predictable (the "drift") and $M_n$ is a martingale (the "noise"). This is exactly the decomposition Section 9 of the proof writes down for $L_N$.

Skip §10.11 onward (optional stopping) for now.

**Checkpoint.** Identify the two pieces of the Doob decomposition of $L_N$ explicitly: the predictable part is $A_N = \sum_{n=0}^{N-1} \mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n]$ and the martingale part is $S_N = \sum_{n=0}^{N-1} M_{n+1}$ in the proof's notation.

### Session 3 — Almost-sure convergence (Williams Ch 11)

Doob's a.s. martingale convergence theorem: every L¹-bounded supermartingale converges almost surely. The proof technique uses upcrossings; it's beautiful and worth understanding once.

The theorem itself isn't invoked directly in our proof, but the *technique* — using monotonicity or boundedness to force convergence — is the same family, and Ch 12 builds on it.

**Checkpoint.** State the theorem, and explain at high level why an L¹-bounded supermartingale can't oscillate forever. (Each completed upcrossing of a fixed interval $[a, b]$ "costs" something monotone, so only finitely many fit inside any L¹ bound.)

### Sessions 4–5 — Square-integrable martingales (Williams Ch 12)

The main event. Read carefully — these two sessions are the highest-leverage ones in the plan.

- §12.0–12.5: L²-bounded martingales, the predictable quadratic variation $\langle M \rangle_n$, orthogonality of martingale differences.
- The conditional-variance form of convergence — *if $\langle M \rangle_\infty < \infty$ a.s. then $M_n$ converges a.s.* Williams presents this in Ch 12; find it and mark it. **This is the theorem used in Section 8 of the proof.**

**Checkpoint.** I should be able to:

- State both the L²-bounded form ($\sup_n \mathbb{E}[M_n^2] < \infty \Rightarrow$ $M_n$ converges in L² and a.s.) and the conditional-variance form ($\langle M \rangle_\infty < \infty$ a.s. $\Rightarrow M_n$ converges a.s.).
- Explain how they relate. The conditional version is *stronger*: the L²-bounded version is essentially the special case where $\mathbb{E}[\langle M \rangle_\infty] < \infty$.
- Notice that in our proof, $\langle S \rangle_\infty \leq 256 \sum_n \alpha_n^2$, which is a *deterministic* finite number. So even the simpler L²-bounded form would work — Section 8 invokes a stronger theorem than it needs. Worth flagging in the writeup if I ever clean it up.

### Session 6 — Apply to the proof

With Williams Ch 12 fresh, work through Sections 7–9 of `proof.md` line by line. For each line, ask:

- What is being computed?
- Which theorem (Doob decomposition, conditional Jensen, L² convergence, $\sigma$-additivity of conditional expectation) is being invoked?
- Are the hypotheses satisfied? Where, exactly?

This is the session where the target paragraph gets drafted, with the textbook still open.

### Session 7 — Write the target paragraph from memory

Close the books. Open a blank file. Write the paragraph from the top of this README. Then check it against `proof.md` and Williams Ch 12. Iterate until it's right.

If I can't do this without notes, I haven't actually understood it, and one or more earlier sessions need to be revisited. That's fine — it's the diagnostic.

## Exercises worth doing

Pick the ones that feel hard. Not all of them.

1. **Doob decomposition of $L_N$.** Write out the predictable process $A_N$ and the martingale $S_N$ for the proof's $L_N = \log W_N$. Verify directly from the definition that $S_N$ is a martingale (i.e., $\mathbb{E}[S_{n+1} - S_n \mid \mathcal{F}_n] = 0$). This is the cleanest sanity check that you understand the decomposition.

2. **Where does the 256 come from?** The proof claims $\mathbb{E}[M_{n+1}^2 \mid \mathcal{F}_n] \leq 256 \alpha_n^2$. Trace the bound: $|M_{n+1}| \leq |\Delta L_{n+1}| + |\mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n]| \leq 8\alpha_n + 8\alpha_n = 16\alpha_n$, so $M_{n+1}^2 \leq 256\alpha_n^2$. Is this tight? What would a more careful bound give? (Hint: it's loose by a noticeable factor, because $|Y_{n+1}|$ is rarely close to its worst-case value of 4.)

3. **The $\log(1 + t) \geq t - t^2$ inequality.** Used in Section 7. Prove it for $|t| \leq 1/4$. Where does the requirement $\alpha_n \leq 1/16$ come from? (Hint: $|\alpha_n Y_{n+1}| \leq 4\alpha_n \leq 1/4$ requires $\alpha_n \leq 1/16$. So the small-stepsize requirement is bookkeeping — it exists to make the second-order Taylor inequality valid pathwise.)

4. **The "uniform in $r_n$" cancellation.** Section 7 shows $\mathbb{E}[Y_{n+1} \mid \mathcal{F}_n] = 0.34$ regardless of the current ratio $r_n = \theta_{A,n}/W_n$. Verify this calculation by hand and identify the *structural* reason the $r_n$ dependence cancels: the symmetric Bernoulli choice between A and B updates exchanges the roles of $r_n$ and $1 - r_n$ in expectation, so the linear-in-$r_n$ term drops out. *This is the slick part of the whole proof.* If you don't see why it works, you don't yet see the proof.

5. **Empirical sanity check (optional).** The simulation in `simulate.py` already tracks $\log W_n$. Modify it to also output the running partial sum $S_N = \sum_{n<N} M_{n+1}$ alongside the running drift $A_N = \sum_{n<N} \mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n]$. The first should look bounded (converging) across seeds; the second should grow like $0.34 \cdot \sum_{n<N} \alpha_n$. Watching this directly is a different kind of conviction than reading the theorem statement — it's the empirical face of the Doob decomposition.

## After this

Once the target paragraph is in hand, the natural next read is **Borkar 2008**, *Stochastic Approximation: A Dynamical Systems Viewpoint* (short monograph, freely available from the author's site). Borkar generalizes the kind of argument in `proof.md` to broad stochastic approximation schemes and is the standard reference for ODE-method convergence proofs in RL. It's where the link between Section 10 of `proof.md` (the ODE) and Sections 7–9 (the almost-sure argument) gets made systematic.

But that's a future commute. The goal of this directory is the paragraph at the top.
