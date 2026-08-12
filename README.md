# Hidden in the Rashomon Set: Predictive Multiplicity as a Channel for Undetectable Price Discrimination

**Target venue:** EconML @ NeurIPS'26 Workshop (short paper track, 4 content pages)
**Submission deadline:** August 29, 2026 (AOE)
**Status:** Scoping complete, novelty check complete — moving to formal model + implementation

---

## 1. One-paragraph pitch

When many models achieve statistically indistinguishable accuracy on a risk-prediction task (a **Rashomon set**), a profit-maximizing firm can select — from that set — the specific model that best predicts *price sensitivity* rather than *risk*. This lets the firm extract extra surplus from captive, low-elasticity consumers while remaining fully defensible against any accuracy-based audit a regulator would run. No fairness constraint, protected attribute, or explicit discriminatory intent is required. We formalize this mechanism, derive a closed-form bound on extractable surplus as a function of the accuracy tolerance $\varepsilon$, and demonstrate it empirically on real credit-risk data with a semi-synthetic elasticity signal.

---

## 2. Motivation

- **Real regulatory precedent:** the UK FCA found that home and motor insurers were systematically charging renewing (captive/loyal) customers more than new customers for equivalent risk — "price walking" or the "loyalty penalty" — and banned the practice in 2021–2022, estimating consumers would have saved £1.2B in 2018 alone under uniform actuarial pricing. That was accomplished with a simple, easily detectable rule (charge more at renewal). **Our claim:** ordinary model multiplicity gives firms a way to reproduce the same economic pattern *invisibly*, through legitimate-looking risk models that pass any accuracy check.
- **Policy gap:** existing regulatory and legal scrutiny of algorithmic pricing/underwriting focuses almost entirely on protected-attribute discrimination (race, gender, proxy variables). Elasticity-based price discrimination is a different, largely unregulated axis — and, unlike protected-class discrimination, doesn't require the firm to touch anything a fairness audit would flag.

---

## 3. Research question & contribution

**RQ:** How much consumer surplus can a firm extract, purely through *model choice* within an accuracy-only Rashomon set, by favoring the model whose decision boundary best correlates with (unobserved) consumer price elasticity — and how does this scale with the accuracy tolerance $\varepsilon$ a firm/regulator is willing to accept?

**Contributions:**
1. A formal model showing that Rashomon-set "boundary" individuals (low marginal accuracy cost to reclassify) are exactly the ones a profit-maximizing firm will target, yielding a closed-form upper bound on extractable surplus as a function of $\varepsilon$ and the correlation between elasticity and legitimate features.
2. A constrained-optimization method ("adversarial ceiling") that computes this bound directly — no need to train many models to demonstrate the worst case.
3. An empirical demonstration that *ordinary* model selection (varying algorithm class, hyperparameters, seeds — no adversarial intent) already captures a meaningful fraction of this ceiling on real credit-risk data.
4. A policy result: standard group-fairness constraints do **not** close this gap unless elasticity happens to correlate with the protected attribute — i.e., fairness-audited models remain exploitable by default.

---

## 4. Related work & novelty positioning

| Line of work | What it shows | How we differ |
|---|---|---|
| Breiman (2001), Marx, Calmon & Ustun (2020), Black, Raghavan & Barocas (2022) — Rashomon effect / predictive & model multiplicity | Many equally-accurate models disagree on individuals; raises fairness/arbitrariness concerns | We reuse this machinery but apply it to **surplus extraction**, not fairness metrics |
| "Less discriminatory algorithm" search (Black, Koepke, Kim, Barocas & Hsu, *Geo. L.J.* 2024) and related FAccT work | Can a regulator/plaintiff find a *fairer* model within the Rashomon set? | We study the adversarial dual: can a *firm* find the most price-discriminatory model within the same set? |
| "Adversarial fairwashing" (Rashomon-set explanation evaluation, 2026) | A model can be swapped within the Rashomon set to mislead **explanation-based** audits | We apply the same adversarial-search logic to **accuracy-based** audits, targeting economic surplus rather than explanation quality |
| "Homogeneous Algorithms Can Reduce Competition in Personalized Pricing" | Algorithm correlation *across competing firms* affects price discrimination and competitive dynamics | Ours is a **single-firm** model-choice mechanism, not an inter-firm competition result |
| **Elmachtoub, Kim & Tan (2026), "Learning Fair Demand Models" — closest paper, cite prominently** | Imposing a group loss-fairness constraint in a 2-group linear demand pipeline produces exactly two optimal solutions with opposing welfare effects; multiplicity vanishes at zero fairness level | Our multiplicity requires **no fairness constraint at all** — it exists in ordinary accuracy-only model selection. Individual-level, not group-label-based. Real Rashomon sets of many models (from algorithm/hyperparameter/seed variation), not two closed-form roots of one quadratic. See §4.1 below for the full comparison. |
| Insurance/credit fairness literature (Lindholm, Richman, Tsanakas, Wüthrich, etc.) | Proxy discrimination against protected classes in underwriting | We study a legally distinct axis (elasticity, not protected-class status) that current fairness audits don't touch |

### 4.1 Related-work paragraph draft (for the paper)

> "Closest to our work, Elmachtoub et al. (2026) show that imposing group loss-fairness in a two-stage demand-estimation-then-pricing pipeline can itself produce multiple optimal solutions with opposing welfare effects. Our multiplicity arises from the opposite condition: ordinary accuracy-tolerance model selection with *no* fairness constraint imposed and *no* group label used, showing that the exploit survives even when a firm never engages with fairness considerations at all."

**Action item:** read Elmachtoub et al. (2026) in full during Week 1 (not just the sections summarized here) before finalizing the theory section — check whether their FEO/EFO machinery is reusable for a linear-demand robustness check.

---

## 5. Formal model (sketch — full proof to be drafted)

- Population of $n$ consumers, each with true risk $\theta_i \in \{0,1\}$ and unobserved elasticity $w_i \in \{\text{low}, \text{high}\}$ (low = captive, high = price-shopper), independent of $\theta_i$ but correlated with an observable, legitimately-used feature $Z_i \subset X_i$.
- Canonical classifier $\hat r^*$ minimizes validation loss. Rashomon set: $\mathcal{R}_\varepsilon = \{\hat r : \text{loss}(\hat r) \le \text{loss}(\hat r^*) + \varepsilon\}$.
- Premium tiers are fixed by predicted class, identical schedule across all models — isolates the pure model-choice effect.
- **Key move:** individuals "free" to reclassify without leaving $\mathcal{R}_\varepsilon$ are those near $\hat r^*$'s decision boundary. A profit-maximizing search over $\mathcal{R}_\varepsilon$ will, among boundary individuals, flip the ones with highest (premium gain × retention probability) — i.e., sort by elasticity/profitability, flip the top $\varepsilon n$.
- **Deliverable:** closed-form upper bound on extractable surplus as a function of $\varepsilon$ and $\text{corr}(w, Z)$, stated as a proposition with a short proof.
- **Practical implication:** this is computable directly as a constrained optimization ("flip up to $\varepsilon n$ predictions of $\hat r^*$ to maximize profit, subject to an accuracy-loss budget of $\varepsilon$") — no need to train a real Rashomon set to get the theoretical ceiling.

**To do:**
- [ ] Write out the full proposition statement
- [ ] Prove the closed-form bound
- [ ] Sanity-check against a toy 2-type example by hand

---

## 6. Empirical design

### 6.1 Data
- Primary: **"Give Me Some Credit"** (Kaggle, ~150k rows, binary default outcome) — free, small, well-known, trains in minutes on CPU.
- Robustness/extension candidates: UCI Taiwan credit default dataset, German Credit.
- Keep real $X_i$ (income, credit lines, utilization, delinquency history) and real default outcome $Y_i$.
- Synthesize elasticity: $w_i = \text{logit}^{-1}(\beta Z_i + \text{noise})$, where $Z_i$ is a real, legitimately-used feature that's economically plausible as an elasticity proxy (e.g., number of existing credit relationships — fewer alternatives ≈ more captive). Vary $\beta$ to control $\text{corr}(w, Z)$ as a clean experimental knob.
- Documented explicitly as semi-synthetic in the paper — real elasticity microdata isn't obtainable for free/at all.

### 6.2 Experiment 1 — Adversarial ceiling
Constrained-flip optimization: for a grid of $\varepsilon \in \{0.1\%, 0.5\%, 1\%, 2\%, 5\%\}$ accuracy tolerance, compute the maximum extractable surplus by optimally reclassifying boundary individuals. Runs in milliseconds; no model training required.

### 6.3 Experiment 2 — Realistic Rashomon set
Train ~100–300 models varying algorithm (logistic regression, random forest, gradient-boosted trees, shallow MLP), hyperparameters, and seeds. Keep only models within each $\varepsilon$ band of best validation AUC. For each model, compute:
- Profit under the fixed pricing schedule
- Exploitability alignment $\rho_m = \text{corr}(\hat r_m(X_i), w_i \mid \theta_i)$

Show the profit-maximizing model in this *realistic* set already captures a nontrivial fraction of the Experiment-1 ceiling — i.e., the exploit doesn't require adversarial intent, just ordinary model-selection practice.

### 6.4 Headline plot
X-axis: accuracy tolerance $\varepsilon$. Y-axis: maximum extractable discriminatory surplus (% over canonical model). Two lines: adversarial ceiling (Exp. 1) vs. realistic-search achieved (Exp. 2).

### 6.5 Policy robustness check
Add a group-fairness constraint (e.g., equalized odds w.r.t. a synthetic protected attribute uncorrelated with $w_i$) and show it does **not** close the surplus gap — directly supporting the differentiation from Elmachtoub et al. and making a genuinely useful policy point: accuracy *and* fairness audits together are still insufficient.

---

## 7. Paper structure (4 pages + references/appendix)

1. **Introduction** (~0.75p) — FCA price-walking anecdote → "less discriminatory algorithm" literature → our reversal → contribution bullets.
2. **Model** (~1p) — setup, Rashomon set, proposition + proof sketch.
3. **Experiments** (~1.5p) — data, Experiments 1 & 2, headline plot, exploitability-alignment result, fairness-constraint robustness check.
4. **Discussion & policy implications** (~0.5p) — why accuracy-based (and fairness-based) audits are insufficient; sketch of a "multiplicity-aware audit."
5. References / appendix (uncounted).

---

## 8. Proposed repo structure

```
econml26-rashomon-pricing/
├── README.md                  # this file
├── paper/                     # LaTeX source (NeurIPS 2026 style file, anonymized)
├── src/
│   ├── data.py                 # load + clean "Give Me Some Credit", synthesize elasticity
│   ├── rashomon_ceiling.py     # Experiment 1: constrained-flip optimizer
│   ├── rashomon_realistic.py   # Experiment 2: train model sweep, compute exploitability alignment
│   ├── metrics.py              # profit, surplus, exploitability alignment (rho_m)
│   └── fairness_check.py       # Section 6.5 robustness check
├── notebooks/
│   └── exploratory.ipynb       # scratch work, headline plot iteration
├── results/
│   ├── figures/                # headline plot + robustness plots
│   └── tables/
└── requirements.txt             # sklearn, xgboost, numpy, pandas, matplotlib
```

---

## 9. Timeline (2.5 weeks)

- [ ] **Days 1–3:** Read Elmachtoub et al. (2026) in full; confirm novelty gap holds; finalize formal model; write proposition + proof.
- [ ] **Days 4–6:** Build semi-synthetic data pipeline; implement constrained-flip optimizer (Experiment 1) — first submittable core result.
- [ ] **Days 7–10:** Realistic Rashomon-set sweep (Experiment 2); compute exploitability alignment; generate headline plot.
- [ ] **Days 11–12:** Fairness-constraint robustness check (§6.5).
- [ ] **Days 13–16:** Write against the 4-page limit; format to NeurIPS 2026 style file; anonymize.
- [ ] **Buffer (2–3 days):** OpenReview portal, formatting fixes, fresh read-through.

**Deadline:** August 29, 2026 (AOE).

---

## 10. Compute budget

Entirely `sklearn` / `xgboost` / `numpy` on tabular data (~150k rows). Runs comfortably on a free Colab CPU runtime or a laptop. No GPU, no API costs.

---

## 11. Open risks

- **Novelty risk (moderate, mitigated):** Elmachtoub et al. (2026) is close on vocabulary but structurally different (fairness-triggered 2-solution multiplicity vs. our fairness-free, many-model Rashomon multiplicity). Must cite and differentiate explicitly and early in the paper.
- **Semi-synthetic elasticity may draw reviewer skepticism.** Mitigate by being explicit about the limitation, grounding $Z_i$ choice in real underwriting/pricing economics literature, and framing results as a lower bound on what's achievable with real (unobserved) elasticity data.
- **Short-paper scope discipline.** Resist the urge to add a third experiment; the two-experiment + one-robustness-check design is deliberately sized for 4 pages.

---

## 12. Reading list (finalize citations against these)

- Breiman, L. (2001). "Statistical modeling: the two cultures." *Statistical Science*.
- Marx, C., Calmon, F., & Ustun, B. (2020). "Predictive multiplicity in classification." *ICML*.
- Black, E., Raghavan, M., & Barocas, S. (2022). "Model multiplicity: opportunities, concerns, and solutions." *FAccT*.
- Black, E., Koepke, J. L., Kim, P. T., Barocas, S., & Hsu, M. (2024). "Less discriminatory algorithms." *Georgetown Law Journal*.
- Elmachtoub, A. N., Kim, H., & Tan, J. Y. (2026). "Learning Fair Demand Models." arXiv:2606.06830.
- Cohen, M. C., Elmachtoub, A. N., & Lei, X. (2022). "Price discrimination with fairness constraints." *Management Science*.
- UK FCA (2020, 2021). General insurance pricing practices market study — final report and policy statement (PS21/5).
