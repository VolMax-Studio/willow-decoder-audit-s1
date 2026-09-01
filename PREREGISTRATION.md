# PREREGISTRATION v1: Google Willow QEC Baseline Audit

**Instance:** `willow-decoder-audit-s1`  
**Specification Version:** v1 (Pre-Registered & Frozen Prior to Execution)  
**Date Frozen:** 2026-09-01  
**Source Literature Lock:** `arXiv:2408.13687v1` / *Nature* 638, 920–926 (2025)  
**Telemetry Lock:** Zenodo DOI `10.5281/zenodo.13273331` (`google_105Q_surface_code_d3_d5_d7.zip`, MD5: `21fa6ad35b395d838ebcdbc92e364a12`)  
**Software Lock:** `stim==1.16.0`, `PyMatching==2.4.0`, `numpy==2.5.2`  

---

## 1. Targets Under Evaluation

### TARGET A (Measurable Reproduction): Google Libra Matching SOTA Baseline
* **Published Figures to Replicate:**
  $$\varepsilon_7 = (1.71 \pm 0.03) \times 10^{-3} \quad (0.171\% \pm 0.003\%)$$
  $$\Lambda = 2.04 \pm 0.02$$
* **Input Artifacts:** Shipped prediction files `libra_decoder_with_rl_optimized_prior/obs_flips_predicted.b8` and `obs_flips_actual.b8` across $d \in \{3, 5, 7\}$, both bases ($X, Z$), and cycle sweep $t \in [10, 250]$.

### TARGET B (Structural / Scope Finding): Google Neural Network Headline Metric
* **Published Figures:** $\varepsilon_7 = (1.43 \pm 0.03) \times 10^{-3}$, $\Lambda = 2.14 \pm 0.02$.
* **Audit Assessment:** Formally evaluated against the dataset contents of Zenodo `10.5281/zenodo.13273331`.

---

## 2. Pre-Frozen Decision Rules

Evaluation follows strict hierarchical rules:

```
========================================================================================
DECISION RULES FOR TARGET A (Libra Matching SOTA Benchmark)
========================================================================================

R1: RECOMPUTED_WITHIN_PUBLISHED_UNCERTAINTY
    Recomputed epsilon_7 lies within [1.68e-3, 1.74e-3] (1.71 +/- 0.03 x 10^-3)
    AND Recomputed Lambda lies within [2.02, 2.06] (2.04 +/- 0.02)
    using the primary cycle range t in [10, 250].
    -> VERIFIED (The published matching synthesis benchmark is reproduced from shipped predictions).

R2: VERIFIED_WITH_LIMITATIONS_FIT_RANGE_SENSITIVITY
    Recomputed epsilon_7 lies within published uncertainty under t in [10, 250],
    BUT shifts outside uncertainty when including r01 (t in [1, 250]).
    -> VERIFIED_WITH_LIMITATIONS (Outcome is sensitive to the inclusion of single-cycle SPAM point r01).

R3: DISCREPANCY_OUTSIDE_UNCERTAINTY
    Recomputed epsilon_7 is < 1.68e-3 OR > 1.74e-3 under primary cycle range t in [10, 250],
    with no documented convention accounting for the shift.
    -> NOT_VERIFIED (Discrepancy exceeds published experimental standard deviation).

========================================================================================
DECISION RULES FOR TARGET B (Neural Network Headline Metric)
========================================================================================

R4: UNSFALSIFIABLE_FROM_PUBLIC_DATA
    Zero prediction files or model weights for the Neural Network decoder exist
    within the public Zenodo archive (10.5281/zenodo.13273331).
    -> NOT_REPRODUCIBLE_FROM_PUBLIC_DATA
       (Factual statement of archive scope; the headline neural figure is unsupported
        by public prediction artifacts).
```

---

## 3. Mathematical Execution Protocol

1. **Step 1 (Per-Point Error Rate $p_L$):**
   $$p_L(d, \text{patch}, \text{basis}, t) = \frac{1}{N} \sum_{i=1}^N (\text{obs\_flips\_actual}_i \oplus \text{obs\_flips\_predicted}_i)$$
2. **Step 2 (Per-Patch Linear Fit):**
   Fit $\ln(1 - 2 p_L(t)) = c + m t$ over $t \in [10, 250]$:
   $$\varepsilon_d(\text{patch}, \text{basis}) = \frac{1 - e^m}{2}$$
3. **Step 3 (Averaging across Patches & Bases):**
   * $\bar{\varepsilon}_3 = \text{mean}(\varepsilon_3 \text{ over 9 patches and } X, Z)$
   * $\bar{\varepsilon}_5 = \text{mean}(\varepsilon_5 \text{ over 4 patches and } X, Z)$
   * $\bar{\varepsilon}_7 = \text{mean}(\varepsilon_7 \text{ over 1 patch and } X, Z)$
4. **Step 4 ($\Lambda$ Linear Fit):**
   Fit $\ln(\bar{\varepsilon}_d) = c_{\Lambda} - \frac{d}{2} \ln(\Lambda)$ across $d \in \{3, 5, 7\}$:
   $$\Lambda = \exp(-m_{\Lambda}) \quad \text{where } m_{\Lambda} \text{ is slope over } x = d/2.$$
