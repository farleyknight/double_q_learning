# A Counterexample to General Convergence of Double Q-Learning with Linear Function Approximation

## 1. Claim

Double Q-learning is convergent in the tabular case under standard assumptions. This proof shows that the same is not true for arbitrary linear function approximation.

**Theorem.** *There exists a finite discounted Markov decision process, a stationary behavior policy, a bounded linear feature map, and a Robbins–Monro stepsize sequence such that symmetric Double Q-learning with linear function approximation is unbounded almost surely from any strictly positive initialization. This holds even though the optimal action-value function is identically zero and is exactly representable by the feature map.*

The example has one state, two actions, zero rewards, and one scalar feature.

## 2. Preliminaries

**Definition (Stochastic process).** A *stochastic process* is a collection of random variables $\{Z_n\}_{n \geq 0}$ defined on a common probability space $(\Omega, \mathcal{F}, \mathbb{P})$, each taking values in a measurable space $\mathcal{E}$. The index $n$ typically represents discrete time, so $Z_n$ is the random state of the process at time $n$.

**Definition (Markov Decision Process).** A *finite discounted Markov decision process* is a tuple $(\mathcal{S}, \mathcal{U}, P, r, \gamma)$ where $\mathcal{S}$ is a finite state space, $\mathcal{U}$ is a finite action space, $P(x' \mid x, u)$ is a transition kernel giving the probability of moving to state $x' \in \mathcal{S}$ from state $x \in \mathcal{S}$ under action $u \in \mathcal{U}$, $r \colon \mathcal{S} \times \mathcal{U} \to \mathbb{R}$ is a bounded reward function, and $\gamma \in [0,1)$ is the discount factor.

**Definition (State process and input process).** The *state process* $\{X_n\}_{n \geq 0}$ is an $\mathcal{S}$-valued stochastic process satisfying $\mathbb{P}(X_{n+1} = x' \mid X_0, U_0, \ldots, X_n, U_n) = P(x' \mid X_n, U_n)$. The *input process* $\{U_n\}_{n \geq 0}$ is a $\mathcal{U}$-valued process representing the sequence of actions taken by the agent. Under a stationary behavior policy $\mu$, the input process satisfies $U_n \sim \mu(\cdot \mid X_n)$ for each $n$.

The action-value function under a policy $\mu$ is $Q^\mu(x,u) = \mathbb{E}\bigl[\sum_{k=0}^{\infty} \gamma^k\, r(X_{n+k}, U_{n+k}) \mid X_n = x,\, U_n = u\bigr]$, and the optimal action-value function is $Q^\ast(x,u) = \max_\mu Q^\mu(x,u)$. Q-learning and its variants seek to estimate $Q^\ast$ from observed transitions.

In the remainder of this paper, both $\mathcal{S}$ and $\mathcal{U}$ are assumed to be finite.

## 3. The MDP, features, and behavior policy

Consider the discounted MDP with one state $s$, two actions $a_1, a_2$, deterministic self-transition, zero rewards, and discount factor $\gamma = 0.9$. Thus $P(s \mid s,a) = 1$ and $r(s,a) = 0$ for both actions $a \in \{a_1, a_2\}$. Since all rewards are zero,

$$Q^\ast(s,a_1) = Q^\ast(s,a_2) = 0.$$

Use one-dimensional linear features $\phi(s,a_1) = 1$ and $\phi(s,a_2) = 2$. The two Double-Q estimators are parameterized by scalars $\theta_A, \theta_B$:

$$Q_A(s,a) = \theta_A \phi(s,a), \qquad Q_B(s,a) = \theta_B \phi(s,a).$$

The optimal function $Q^\ast \equiv 0$ is exactly representable by the parameter value $\theta_A = \theta_B = 0$.

Let the stationary behavior policy be $\mu(a_1 \mid s) = 0.9$ and $\mu(a_2 \mid s) = 0.1$. At time $n$, sample an action from $\mu$, and write $X_{n+1} = \phi(s, A_{n+1}) \in \{1, 2\}$. Hence

$$\mathbb{P}(X_{n+1} = 1) = 0.9, \qquad \mathbb{P}(X_{n+1} = 2) = 0.1.$$

Independently of the sampled action and of the past, choose estimator $A$ or estimator $B$ for update with probability $1/2$ each. Use the global stepsize sequence

$$\alpha_n = \frac{a}{n+1}, \qquad 0 < a \leq \frac{1}{16}.$$

Then $\sum_{n=0}^{\infty} \alpha_n = \infty$ and $\sum_{n=0}^{\infty} \alpha_n^2 < \infty$. Initialize with arbitrary strictly positive parameters: $\theta_{A,0} > 0$ and $\theta_{B,0} > 0$.

## 4. The Double Q-learning updates

We use the standard symmetric Double Q-learning update. If estimator $A$ is selected at time $n$, then

$$\theta_{A,n+1} = \theta_{A,n} + \alpha_n \phi(s, A_{n+1}) \bigl[\gamma\, Q_B\bigl(s, \arg\max_{a'} Q_A(s,a')\bigr) - Q_A(s, A_{n+1})\bigr],$$

while $\theta_B$ is unchanged. If estimator $B$ is selected, the roles are reversed:

$$\theta_{B,n+1} = \theta_{B,n} + \alpha_n \phi(s, A_{n+1}) \bigl[\gamma\, Q_A\bigl(s, \arg\max_{a'} Q_B(s,a')\bigr) - Q_B(s, A_{n+1})\bigr],$$

while $\theta_A$ is unchanged. Because the state never changes and the reward is zero, these are the full updates.

## 5. Positivity is invariant

We first show that the positive quadrant is invariant. This will imply that the greedy action is fixed throughout the entire trajectory.

Suppose $\theta_A > 0$. Then $Q_A(s,a_2) = 2\theta_A > \theta_A = Q_A(s,a_1)$, so the greedy action under $Q_A$ is uniquely $a_2$. Similarly, if $\theta_B > 0$, the greedy action under $Q_B$ is uniquely $a_2$. Thus no tie-breaking convention is needed as long as the parameters remain strictly positive.

Assume $\theta_A, \theta_B > 0$, and let $X \in \{1, 2\}$ be the sampled feature. If estimator $A$ is updated, then the target action is $a_2$, whose feature is $2$. Therefore

$$\theta_A^+ = \theta_A + \alpha X(\gamma \cdot 2\theta_B - X\theta_A) = (1 - \alpha X^2)\theta_A + 1.8\,\alpha X\,\theta_B.$$

Because $X \leq 2$ and $\alpha_n \leq 1/16$, we have $1 - \alpha_n X^2 \geq 1 - 4\alpha_n \geq 3/4 > 0$. Thus $\theta_A^+ > 0$. The same argument applies when estimator $B$ is updated:

$$\theta_B^+ = (1 - \alpha X^2)\theta_B + 1.8\,\alpha X\,\theta_A > 0.$$

Therefore, since $\theta_{A,0} > 0$ and $\theta_{B,0} > 0$, we have $\theta_{A,n} > 0$ and $\theta_{B,n} > 0$ for every $n$. Consequently, the greedy action is always $a_2$ for both estimators. Along this trajectory, the nonlinear maximization in the Double-Q target reduces to a fixed linear target.

## 6. Dynamics of the parameter sum

Define $W_n = \theta_{A,n} + \theta_{B,n}$. By positivity invariance, $W_n > 0$ for all $n$. We will prove that $W_n \to \infty$ almost surely. This implies that the Double-Q parameter vector is unbounded and therefore cannot converge to $(0,0)$, which represents $Q^\ast$.

Let $r_n = \theta_{A,n} / W_n \in (0,1)$. If estimator $A$ is updated at time $n$, then

$$W_{n+1} = W_n + \alpha_n X_{n+1}(1.8\,\theta_{B,n} - X_{n+1}\,\theta_{A,n}).$$

Dividing by $W_n$, this becomes $W_{n+1} = W_n(1 + \alpha_n Y_{n+1})$, where, in the case of an $A$-update,

$$Y_{n+1} = X_{n+1}\bigl(1.8(1 - r_n) - X_{n+1}\,r_n\bigr).$$

If estimator $B$ is updated, then similarly $W_{n+1} = W_n(1 + \alpha_n Y_{n+1})$, where

$$Y_{n+1} = X_{n+1}\bigl(1.8\,r_n - X_{n+1}(1 - r_n)\bigr).$$

For both possible updates, because $r_n \in (0,1)$ and $X_{n+1} \in \{1, 2\}$, we have $-4 \leq Y_{n+1} \leq 3.6$. Therefore $|\alpha_n Y_{n+1}| \leq 1/4$ and $1 + \alpha_n Y_{n+1} \geq 3/4 > 0$. Thus the logarithm of $W_n$ is well defined for every $n$.

## 7. Positive drift of the logarithm

Let $\mathcal{F}_n$ be the history up to time $n$, including $\theta_{A,n}$ and $\theta_{B,n}$, but not the fresh action sample or estimator choice at time $n$. Conditional on $\mathcal{F}_n$, the ratio $r_n$ is fixed.

First average over the independent choice of which estimator is updated. For a fixed sampled feature $X$,

$$\begin{aligned}
\mathbb{E}[Y_{n+1} \mid \mathcal{F}_n, X_{n+1} = X]
&= \tfrac{1}{2}\, X\bigl(1.8(1 - r_n) - X\,r_n\bigr) + \tfrac{1}{2}\, X\bigl(1.8\,r_n - X(1 - r_n)\bigr) \\
&= \tfrac{1}{2}\, X(1.8 - X).
\end{aligned}$$

Now average over the behavior policy:

$$\begin{aligned}
\mathbb{E}[Y_{n+1} \mid \mathcal{F}_n]
&= 0.9 \cdot \tfrac{1}{2} \cdot 1 \cdot (1.8 - 1) + 0.1 \cdot \tfrac{1}{2} \cdot 2 \cdot (1.8 - 2) \\
&= 0.9 \cdot 0.4 + 0.1 \cdot (-0.2) \\
&= 0.36 - 0.02 = 0.34.
\end{aligned}$$

Thus $Y_{n+1}$ has a strictly positive conditional mean, uniformly over the current parameters.

Define $L_n = \log W_n$. Since $W_{n+1} = W_n(1 + \alpha_n Y_{n+1})$, we have $L_{n+1} - L_n = \log(1 + \alpha_n Y_{n+1})$. For $|t| \leq 1/4$, the elementary inequality $\log(1 + t) \geq t - t^2$ holds. Applying this with $t = \alpha_n Y_{n+1}$, and using $|Y_{n+1}| \leq 4$, gives

$$\mathbb{E}[L_{n+1} - L_n \mid \mathcal{F}_n] \geq \alpha_n\,\mathbb{E}[Y_{n+1} \mid \mathcal{F}_n] - \alpha_n^2\,\mathbb{E}[Y_{n+1}^2 \mid \mathcal{F}_n] \geq 0.34\,\alpha_n - 16\,\alpha_n^2.$$

Because $\sum_{n=0}^{\infty} \alpha_n = \infty$ and $\sum_{n=0}^{\infty} \alpha_n^2 < \infty$, we have $\sum_{n=0}^{N-1}(0.34\,\alpha_n - 16\,\alpha_n^2) \to +\infty$. So the predictable drift of $L_n$ has a deterministic lower bound whose partial sums diverge to $+\infty$.

## 8. Martingale fluctuations are negligible

Let $\Delta L_{n+1} = L_{n+1} - L_n = \log(1 + \alpha_n Y_{n+1})$, and define the martingale difference

$$M_{n+1} = \Delta L_{n+1} - \mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n].$$

For $|t| \leq 1/4$, there is a universal constant $K$ such that $|\log(1+t)| \leq K|t|$. For example, one may take $K = 2$. Therefore $|\Delta L_{n+1}| \leq 2\alpha_n |Y_{n+1}| \leq 8\alpha_n$. Consequently,

$$\bigl|\mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n]\bigr| \leq \mathbb{E}\bigl[|\Delta L_{n+1}| \mid \mathcal{F}_n\bigr] \leq 8\alpha_n.$$

Hence $|M_{n+1}| \leq |\Delta L_{n+1}| + |\mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n]| \leq 16\alpha_n$. It follows that $\mathbb{E}[M_{n+1}^2 \mid \mathcal{F}_n] \leq 256\,\alpha_n^2$. Since $\sum_n \alpha_n^2 < \infty$,

$$\sum_{n=0}^{\infty} \mathbb{E}[M_{n+1}^2 \mid \mathcal{F}_n] < \infty.$$

By the martingale convergence theorem for square-integrable martingales with summable conditional variances, the martingale partial sums $\sum_{n=0}^{N-1} M_{n+1}$ converge almost surely to a finite random limit.

## 9. Almost-sure divergence

Using the decomposition

$$L_N = L_0 + \sum_{n=0}^{N-1} \mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n] + \sum_{n=0}^{N-1} M_{n+1},$$

and the lower bound from Section 7,

$$\sum_{n=0}^{N-1} \mathbb{E}[\Delta L_{n+1} \mid \mathcal{F}_n] \geq \sum_{n=0}^{N-1} (0.34\,\alpha_n - 16\,\alpha_n^2) \to +\infty.$$

The martingale term converges almost surely to a finite limit. Therefore $L_N \to +\infty$ almost surely. Since $L_N = \log W_N$, this implies $W_N \to \infty$ almost surely. Since both parameters remain positive,

$$\max\{\theta_{A,N},\, \theta_{B,N}\} \geq \frac{W_N}{2} \to \infty.$$

Thus the parameter vector is unbounded almost surely. In particular, the Double-Q iterates cannot converge to the representable optimum $(\theta_A, \theta_B) = (0,0)$. This proves the theorem. ∎

## 10. Relation to the expected linear dynamics

This section is not needed for the almost-sure proof, but it explains the source of the instability. In the positive quadrant, the greedy action is always $a_2$. Therefore the expected update is linear. Let $C = \mathbb{E}[X^2]$ and $D = \gamma\,\mathbb{E}[2X]$. In this example, $C = 0.9 \cdot 1^2 + 0.1 \cdot 2^2 = 1.3$ and $D = 0.9(0.9 \cdot 2 \cdot 1 + 0.1 \cdot 2 \cdot 2) = 1.98$. The expected Double-Q update has the form

$$\mathbb{E}[\Delta \theta_A] = \frac{\alpha}{2}(D\,\theta_B - C\,\theta_A), \qquad \mathbb{E}[\Delta \theta_B] = \frac{\alpha}{2}(D\,\theta_A - C\,\theta_B).$$

Equivalently,

$$\mathbb{E} \begin{bmatrix} \Delta \theta_A \\ \Delta \theta_B \end{bmatrix} = \frac{\alpha}{2} \begin{bmatrix} -C & D \\ D & -C \end{bmatrix} \begin{bmatrix} \theta_A \\ \theta_B \end{bmatrix}.$$

Introduce the average and difference coordinates $u = (\theta_A + \theta_B)/2$ and $v = (\theta_A - \theta_B)/2$. The corresponding mean ODE decouples as

$$\dot{u} = \tfrac{1}{2}(D - C)\,u, \qquad \dot{v} = -\tfrac{1}{2}(C + D)\,v.$$

Since $D - C = 1.98 - 1.3 = 0.68 > 0$, we obtain $\dot{u} = 0.34\,u$. Thus the average mode is unstable. The almost-sure argument above turns this mean-dynamics instability into a genuine stochastic nonconvergence result.

## 11. What the counterexample shows and does not show

This counterexample shows that there cannot be a general convergence theorem for Double Q-learning with arbitrary linear function approximation under off-policy sampling and bootstrapping.

It does not show that Double Q-learning always diverges. Double Q-learning is convergent in tabular settings under the usual assumptions, and it may converge in restricted linear settings with additional structure. The point is that Double Q-learning does not, by itself, remove the instability caused by the combination of bootstrapping, off-policy sampling, and function approximation.

The example is deliberately minimal: one state, two actions, zero rewards, one scalar feature, and a fixed behavior policy. Despite this simplicity, the Double-Q parameter norm diverges almost surely from every strictly positive initialization.
