# Formal model — working draft (§5)

Status: Proposition 1 (ε-only ceiling) is fully proved. Proposition 2 (the
corr(w,Z)-scaled realistic ceiling) is set up but the closed-form rate is
not yet derived — flagged explicitly below rather than guessed at. Revisit
after reading Elmachtoub et al. (2026) in full (README §4.1 action item).

---

## 1. Setup

- Population of $n$ i.i.d. draws $(X_i, \theta_i, w_i)$, $i=1,\dots,n$.
- $\theta_i \in \{0,1\}$: true risk/default outcome (also the training label $Y_i$).
- $w_i \in [0,1]$: elasticity index, $w_i = 0$ fully captive, $w_i = 1$ fully price-sensitive. Independent of $\theta_i$. Generated from an observable, legitimately-used feature $Z_i \subset X_i$ via $w_i = \sigma(\beta Z_i + \eta_i)$, $\eta_i$ independent noise, $\sigma$ the logistic sigmoid (matches README §6.1).
- Canonical classifier $\hat r^*: X \to \{0,1\}$ minimizes validation 0-1 loss $L(r) = \frac{1}{n}\sum_i \mathbb 1\{r(X_i)\neq\theta_i\}$.
- **Rashomon set** (standard definition, Marx, Calmon & Ustun 2020): $\mathcal R_\varepsilon = \{r : L(r) \le L(\hat r^*) + \varepsilon\}$.
- **Premium schedule**, fixed across every candidate model: $\pi(1) = \pi_1$ (predicted-high-risk tier), $\pi(0)=\pi_0$, $\pi_1 > \pi_0 \ge 0$.
- **Retention**: an individual assigned tier $0$ never leaves (normalize $\rho_0 \equiv 1$ — status quo). An individual assigned tier $1$ retains with probability $\rho_1(w_i) = 1 - w_i$ (more price-sensitive $\Rightarrow$ more likely to leave when moved to the expensive tier). If they leave, the firm earns $0$ from them.

Firm's expected profit under classifier $r$:
$$\Pi(r) = \frac{1}{n}\sum_i \big[(1-r_i)\pi_0 + r_i\,\pi_1(1-w_i)\big] = \pi_0 + \frac{1}{n}\sum_i r_i\, b_i, \qquad b_i := \pi_1(1-w_i) - \pi_0.$$

$b_i$ is the profit gain from moving individual $i$ into the high tier. It is **strictly decreasing in $w_i$**: profitable ($b_i>0$) iff $w_i < \bar w := (\pi_1-\pi_0)/\pi_1$. So "captive" (low $w_i$) individuals are exactly the profitable ones to move up — this is the formal version of the FCA loyalty-penalty story.

The firm's problem is $\max_{r \in \mathcal R_\varepsilon} \Pi(r) \iff \max_{r\in\mathcal R_\varepsilon} \sum_i r_i b_i$.

---

## 2. A tractable inner approximation of $\mathcal R_\varepsilon$

Directly optimizing over all of $\mathcal R_\varepsilon$ requires committing to a hypothesis class. To get a **closed-form, training-free** ceiling (README §6.2: "no need to train a real Rashomon set to get the theoretical ceiling"), we instead optimize over the *Hamming-ball* of classifiers reachable by flipping at most $\varepsilon n$ of $\hat r^*$'s own predictions:

$$\mathcal R_\varepsilon^H := \Big\{ r \in \{0,1\}^n : \tfrac{1}{n}\big|\{i : r_i \ne \hat r^*_i\}\big| \le \varepsilon \Big\}.$$

**Lemma 1.** $\mathcal R_\varepsilon^H \subseteq \mathcal R_\varepsilon$.

*Proof.* Let $r \in \mathcal R_\varepsilon^H$ differ from $\hat r^*$ on a set $S$, $|S| \le \varepsilon n$. Split $S = (S\cap C) \cup (S\cap W)$ where $C=\{i:\hat r^*_i=\theta_i\}$ (correct) and $W = [n]\setminus C$ (wrong). Flipping $i \in S\cap C$ turns a correct prediction into an error ($+1/n$ to loss); flipping $i\in S\cap W$ fixes an error ($-1/n$). So
$$L(r) = L(\hat r^*) + \tfrac{1}{n}\big(|S\cap C| - |S\cap W|\big) \le L(\hat r^*) + \tfrac{1}{n}|S\cap C| \le L(\hat r^*) + \tfrac{|S|}{n} \le L(\hat r^*)+\varepsilon. \qquad\blacksquare$$

So any surplus achievable within $\mathcal R_\varepsilon^H$ is achievable within the true Rashomon set — a valid, conservative, closed-form lower bound on the true adversarial ceiling, and exactly what Experiment 1 computes without ever training a model.

We restrict the flip set to individuals currently at the low tier, $S \subseteq \{i : \hat r^*_i = 0\}$ (the "price-walking" direction: strategically upgrading captive customers, rather than also discounting price-shoppers already at the high tier — the latter is a real, symmetric, second-order effect worth a remark but out of scope for the base proposition).

---

## 3. Proposition 1 (oracle ceiling, closed form in $\varepsilon$)

**Assumptions.**
- (A1) Flip set restricted to $S \subseteq \{i : \hat r^*_i = 0\}$, as above.
- (A2) $F$ = CDF of $w_i$ among individuals with $\hat r^*_i = 0$; $F$ has a density and $\bar w \in (0,1)$ is an interior point (i.e. some but not all low-tier individuals are profitable to flip).
- (A3, regularity) $\varepsilon \le F(\bar w)$ — the flip budget doesn't exceed the mass of profitable (captive-enough) individuals available. Holds for any $\varepsilon$ in the empirical grid (§6.2: $\varepsilon \le 5\%$) as long as captive types aren't vanishingly rare.

**Proposition 1.** Under (A1)–(A3), the maximum profit gain over $\hat r^*$ achievable within $\mathcal R_\varepsilon^H$ is
$$\Delta\Pi^*(\varepsilon) = n\Big[\varepsilon(\pi_1-\pi_0) - \pi_1 \int_0^{Q(\varepsilon)} w\, dF(w)\Big], \qquad Q(\varepsilon) := F^{-1}(\varepsilon),$$
i.e. exactly $\varepsilon n$ flips of the $\varepsilon n$ *lowest-$w_i$* (most captive) individuals among $\{\hat r^*_i=0\}$.

*Proof.* Maximizing $\sum_{i\in S} b_i$ over $|S|=\varepsilon n$, $S\subseteq\{\hat r^*_i=0\}$, with $b_i$ strictly decreasing in $w_i$: by a standard exchange argument, any optimal $S$ must consist of the $\varepsilon n$ individuals with the smallest $w_i$ (swapping a higher-$w$ member of $S$ for a lower-$w$ non-member weakly increases $\sum b_i$, strictly if $b$ is strictly decreasing, contradicting optimality unless already sorted). Summing $b_i = \pi_1(1-w_i)-\pi_0$ over that bottom-$\varepsilon$ quantile and passing to the integral form gives the stated expression. $\blacksquare$

**Corollary (uniform special case).** If $w_i \mid \hat r^*_i=0 \sim \text{Uniform}[0,1]$, then $Q(\varepsilon)=\varepsilon$ and
$$\Delta\Pi^*(\varepsilon) = n\varepsilon\Big[(\pi_1-\pi_0) - \tfrac{\pi_1}{2}\varepsilon\Big].$$
For small $\varepsilon$ this is $\approx n\varepsilon(\pi_1-\pi_0)$ — **linear in $\varepsilon$** with slope equal to the full premium gap, matching the headline-plot intuition in §6.4: extractable surplus grows (to first order) proportionally with the accuracy tolerance a regulator/auditor is willing to permit, with a curvature correction of order $\varepsilon^2$ from the fact that the *marginal* captive individual gets less captive as you dig deeper into the ranking.

---

## 4. Proposition 2 (realistic, $Z$-only ceiling) — setup only, rate TBD

In practice the firm does not observe $w_i$, only $Z_i$ (and, if it fits the generative model, an estimate $\hat\beta$). Ranking by $\hat\sigma(\hat\beta Z_i)$ instead of the true $w_i$ means the top-$\varepsilon n$ selected set is a noisy version of the oracle set in Prop. 1, and achieved surplus is bounded above by $\Delta\Pi^*(\varepsilon)$ and degrades toward $n\varepsilon\cdot\mathbb E[b_i]$ (no better than random selection among low-tier individuals) as $\mathrm{corr}(w,Z)\to 0$.

**What's proved:** the two endpoints (perfect correlation recovers Prop. 1; zero correlation gives the population-average, no-information baseline) and monotonicity in between (more correlation cannot hurt, since the firm can always ignore extra signal).

**What's not yet proved:** the exact closed-form *rate* connecting $\rho:=\mathrm{corr}(w,Z)$ to achieved surplus. This needs either (a) a specific joint distribution for $(w,Z)$ (e.g. a bivariate-Gaussian/probit approximation, giving achieved-precision-at-top-$\varepsilon$-quantile in terms of $\rho$ via the standard signal-detection formulas), or (b) an empirical calibration instead of a fully closed form. Leaving this open rather than asserting an unverified formula.

**To do before finalizing:** decide (a) vs (b) after the Elmachtoub et al. read-through (they may have reusable machinery here — README §4.1 action item), then fill in this section.

---

## 5. Toy 2-type sanity check (by hand)

$n=10$. $\pi_0=100$, $\pi_1=150$ (so $\bar w = 50/150 = 1/3$). Two elasticity types instead of continuous $w$: captive ($w=0$, "$L$") and price-shopper ($w=1$, "$H$"), with retention $\rho_1(L)=0.9$, $\rho_1(H)=0.2$ (a discrete stand-in for $\rho_1(w)=1-w$, not literally $1-w$, to make the arithmetic transparent).

- $b_L = \pi_1\rho_1(L) - \pi_0 = 150(0.9) - 100 = 35$.
- $b_H = \pi_1\rho_1(H) - \pi_0 = 150(0.2) - 100 = -70$.

Confirms $b_L > 0 > b_H$ (A2-analogue): profitable to flip captives up, unprofitable to flip price-shoppers up.

Population: 6 individuals at $\hat r^*_i=0$, of which 4 are captive ($L$) and 2 are price-shoppers ($H$); 4 individuals at $\hat r^*_i=1$. Take $\varepsilon = 0.2 \Rightarrow \varepsilon n = 2$ flips.

Regularity check (A3-analogue): need $\varepsilon n \le |\{i:\hat r^*_i=0, w_i=L\}| = 4$. Holds ($2\le4$).

Oracle firm flips any 2 of the 4 captive, low-tier individuals: gain $= 2\times 35 = 70$.

Check against the two flipped individuals' effect on loss: both were previously correctly classified ($\hat r^*_i=\theta_i=0$), so flipping turns both into errors: $L(r) = L(\hat r^*) + 2/10 = L(\hat r^*)+0.2 = L(\hat r^*)+\varepsilon$ — lands exactly on the boundary of $\mathcal R_\varepsilon$, confirming Lemma 1's bound is tight here and the flip is a legal move.

**Matches Proposition 1's discrete analogue** $\Delta\Pi^*(\varepsilon) = \varepsilon n\, b_L = 0.2\times10\times35=70$. ✓
