# Literature Review: Status of the Result

## Bottom line

I could not find this exact theorem — an almost-sure divergence proof for symmetric two-estimator Double Q-learning with linear function approximation — published anywhere. The convergence question for this algorithm is repeatedly and explicitly described as **open** in the recent literature. So as a formal statement, the result appears to be genuinely new.

That said, the result is conceptually anticipated by older work, and the *mechanism* of divergence is essentially a re-staging of a classical example. I'll lay out both sides.

---

## What's clearly established in the literature

**1. Convergence of symmetric Double Q-learning with linear FA is an explicitly stated open problem.**

Several recent papers say this in essentially the same words:

- Weng, Gupta, He, Ying & Srikant (2020), *The Mean-Squared Error of Double Q-Learning*: "To the best of our knowledge, establishing the convergence of double Q-learning with linear function approximation remains an open problem." Their entire analysis carries the assumption *"both the algorithms converge"* as a hypothesis, not a conclusion.
- Xiong, Zhang, Sun & Liang (2020), *Finite-Time Analysis for Double Q-learning*: "Regarding double Q-learning, it is still an open topic on how to design double Q-learning algorithms under function approximation and under what conditions they have theoretically guaranteed convergence." Their finite-time results are for the **tabular** case only.
- Zhao et al. (2021), *Faster Non-asymptotic Convergence for Double Q-learning*: "The convergence analysis of double Q-learning with function approximation raises new technical challenges and is an interesting topic for our future study."
- Lee & He (2019/2020), *Switching System Perspective…*: explicitly note that their stability machinery "does not immediately extend to other Q-learning variants, such as double Q-learning."

So the user's theorem resolves the *negative* direction of this open question: no fully general convergence theorem can exist.

**2. The mechanism is the classical Tsitsiklis–Van Roy "θ → 2θ" example, restaged.**

Tsitsiklis & Van Roy (1996/1997) constructed a 2-state policy-evaluation example with scalar feature φ(s₁)=1, φ(s₂)=2, all-zero rewards (so V*≡0 is representable), and an off-policy sampling distribution. With γ > 1/2, the expected TD update is ∆w ∝ (2γ − 1)w, which drives w to ±∞. The user's MDP is the natural **single-state, two-action** restaging of this: features φ(a₁)=1, φ(a₂)=2, zero rewards, and an off-policy behavior distribution that oversamples the lower-feature action while the greedy bootstrap target always lands on the higher-feature action. Section 9 of the user's proof essentially reproduces the Tsitsiklis–Van Roy mean-field instability calculation, getting D − C = 0.68 > 0 in place of TVR's 2γ − 1 = 0.98 > 0.

This isn't a criticism — TVR didn't cover Double Q-learning, and adapting it requires real work — but it's important context. The example is not pulling instability from somewhere new; it's showing that double estimation, which fixes maximization bias, does not fix the deadly triad.

**3. Empirical (not formal) observations of Double Q-learning divergence already exist.**

Van Hasselt, Doron, Strub, Hessel, Sonnerat & Modayil (2018), *Deep Reinforcement Learning and the Deadly Triad*, ran the Tsitsiklis–Van Roy example with linear FA and a target-network variant of Double Q-learning, and reports: *"Q-learning diverges most, and double Q-learning diverges least, with the other variants in between."* In their Atari studies they report soft-divergence on ~10% of double-Q runs. So the empirical claim "Double Q-learning can diverge under the deadly triad" is roughly 8 years old.

Two important caveats: (i) van Hasselt et al. tested the **DQN-style target-network** variant — one online net, one slow target net — not the symmetric two-estimator Hasselt-2010 algorithm the user analyzes. (ii) Their statement is empirical, not a theorem; soft divergence on Atari with deep networks is not the same object as almost-sure parameter divergence on a constructed MDP.

---

## What's genuinely new in the user's note

A few things appear to be new contributions, not just re-skins of older work:

- **The algorithm itself**. Symmetric two-estimator Double Q-learning (the actual Hasselt 2010 algorithm) is what's analyzed, not the target-network surrogate that gets called "Double DQN." The classical TVR example doesn't immediately apply because you have to handle the random Bernoulli choice of which estimator updates, and the cross-bootstrap structure that decorrelates the estimators (which is precisely what was hoped to fix the deadly triad).
- **The almost-sure conclusion**, not just expected-update instability. The Lyapunov-style analysis on log Sₙ with Robbins–Siegmund-style martingale control of fluctuations turns the mean-field instability into a probability-one statement uniform in initialization (within the positive quadrant). This is the technically substantive part — getting from "the ODE has an unstable equilibrium" to "the iterates almost surely escape to infinity" requires showing the noise doesn't save you.
- **The positive-quadrant invariance argument** that pins the greedy action throughout the trajectory, removing the nonlinearity from the analysis on this specific event. It's a small but elegant trick that makes the proof work.

I did not find any paper — including the most recent ones I checked through Feb 2026 (Mehta & Meyn's *Optimistic Training and Convergence of Q-Learning*, Liu, Xie & Zhang's *Linear Q-Learning Does Not Diverge in L²*, Lim & Lee 2025 on PBE properties, Lee 2024 multi-step TD, the *Simultaneous Double Q-learning* paper) — that states or proves this. The Mehta–Meyn paper has a one-dimensional example showing instability of vanilla Q-learning under oblivious training, which is the closest counterpart in spirit, but it's vanilla Q-learning, not Double Q-learning.

---

## Honest caveats and places the framing could be sharpened

A few things a reviewer is likely to push on:

1. **The off-policy mismatch is the real culprit, not anything specific to Double Q-learning.** Section 9 makes this clear (the average mode is unstable, the difference mode is contracting), but the abstract and Section 1 frame it as a Double Q-learning result. A skeptic could say: "you've reproved TVR — of course Double Q-learning inherits divergence from the underlying TD instability." The honest framing is that the result *resolves an open question that the literature kept asking*, not that it reveals a surprising new failure mode. The proof should probably acknowledge this directly to land well.

2. **Comparison to TVR should probably be more explicit.** Section 9 hints at it ("explains the source of the instability") but doesn't say "this MDP is the action-space restatement of Tsitsiklis–Van Roy 1996, and the instability mechanism is the same." Calling that out makes the contribution clearer (a careful almost-sure proof under symmetric Double Q-learning), not weaker.

3. **Empirical observations of Double Q divergence under deadly-triad conditions** (van Hasselt et al. 2018) should be cited. Currently, Section 1's "Double Q-learning is convergent in the tabular case under standard assumptions" makes it sound like nothing was previously known about the FA case beyond "open." That's not quite right — it's been *empirically observed* to diverge, just not formally proven for the symmetric algorithm.

4. **The constraint that the *optimal policy is unique* matters.** Weng et al. 2020's theorem requires this (and breaks on Baird's zero-reward case where it doesn't hold, which is exactly your zero-reward setup). Worth noting: your example sits in the regime their theorem explicitly *cannot* cover, which makes it a clean complement to their work rather than a contradiction of it.

5. **The note that 0 < a ≤ 1/16 is "Robbins–Monro"** is fine, but readers will want to know whether the result is sensitive to the small-stepsize requirement or whether it's just bookkeeping. From the proof it's clearly bookkeeping (you need 1 + αY > 0 to take logs), but stating that explicitly will help.

---

## Where to place it in the literature

If you write this up for publication, the natural framing is: *"Weng et al. (2020), Xiong et al. (2020), and others have left open whether symmetric Double Q-learning converges with linear function approximation. We resolve this in the negative: even on a single-state, two-action MDP with zero rewards and Q* exactly representable, the iterates diverge almost surely from any positive initialization. The example is a control-style restaging of Tsitsiklis & Van Roy (1996), and complements van Hasselt et al.'s (2018) empirical observations with a rigorous almost-sure statement."*

That framing is accurate, defensible, and avoids overselling. The main thing is not to claim more novelty than the result actually has — the **theorem** is new, but the **phenomenon** has been suspected and partially observed for years.