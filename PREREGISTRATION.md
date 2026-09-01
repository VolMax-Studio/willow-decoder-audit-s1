# PREREGISTRATION v2: Google Willow QEC Baseline Audit

**Instance:** `willow-decoder-audit-s1`  
**Specification Version:** v2 (Pre-Registered & Frozen Prior to Execution)  
**Date Frozen:** 2026-09-01  
**Supersedes:** `PREREGISTRATION_v1_OBSOLETE.md`  
**Source Literature Lock:** `arXiv:2408.13687v1` / *Nature* 638, 920–926 (2025)  
**Telemetry Lock:** Zenodo DOI `10.5281/zenodo.13273331` (`google_105Q_surface_code_d3_d5_d7.zip`, MD5: `21fa6ad35b395d838ebcdbc92e364a12`)  
**Software Lock:** `stim==1.16.0`, `PyMatching==2.4.0`, `numpy==2.5.2`  

---

## 1. Targets Under Evaluation

### TARGET A1 (Measurable Reproduction): Google Libra Distance-7 Matching SOTA
* **Published Value & Standard Deviation:**
  $$\varepsilon_{7,\text{pub}} = (1.71 \pm 0.03) \times 10^{-3} \quad [I_{\text{pub}} = 1.68 \times 10^{-3} \dots 1.74 \times 10^{-3}]$$
* **Target Coordinates:** Distance $d=7$, Patch `d7_at_q6_7`, Bases $X$ and $Z$, Primary cycle range $t \in [10, 250]$.

### TARGET A2 (Measurable Reproduction): Google Libra Suppression Factor $\Lambda$
* **Published Value & Standard Deviation:**
  $$\Lambda_{\text{pub}} = 2.04 \pm 0.02 \quad [I_{\text{pub}} = 2.02 \dots 2.06]$$
* **Target Coordinates:** Regressed over mean $\bar{\varepsilon}_3$ (9 subgrid patches), $\bar{\varepsilon}_5$ (4 subgrid patches), $\bar{\varepsilon}_7$ (1 patch) across both bases ($X, Z$) under $t \in [10, 250]$.

### TARGET B (Scope Finding): Google Neural Network Headline Metric
* **Published Value:** $\varepsilon_7 = (1.43 \pm 0.03) \times 10^{-3}, \Lambda = 2.14 \pm 0.02$.
* **Audit Assessment:** Formally evaluated against public artifact availability in Zenodo `10.5281/zenodo.13273331`.

---

## 2. Statistical Criteria: Interval Overlap

Given the recomputed value $\hat{\theta}$ with standard error of regression $\sigma_{\hat{\theta}}$, the recomputed 1-$\sigma$ confidence interval is defined as:
$$I_{\text{recomp}} = [\hat{\theta} - \sigma_{\hat{\theta}}, \hat{\theta} + \sigma_{\hat{\theta}}]$$
The published 1-$\sigma$ confidence interval is:
$$I_{\text{pub}} = [\theta_{\text{pub}} - \sigma_{\text{pub}}, \theta_{\text{pub}} + \sigma_{\text{pub}}]$$

* **Overlap Condition:** $\text{Overlap}(I_{\text{recomp}}, I_{\text{pub}}) \iff \max(\hat{\theta} - \sigma_{\hat{\theta}}, \theta_{\text{pub}} - \sigma_{\text{pub}}) \le \min(\hat{\theta} + \sigma_{\hat{\theta}}, \theta_{\text{pub}} + \sigma_{\text{pub}})$.

---

## 3. Disjoint Pre-Frozen Decision Rules

Evaluation yields two independent verdicts for $\varepsilon_7$ and $\Lambda$, plus the scope verdict for the Neural Network:

```
========================================================================================
DECISION MATRIX FOR TARGET A1: Distance-7 Logical Error Rate per Cycle (epsilon_7)
========================================================================================

E1: VERIFIED
    I_recomp(primary: [10, 250]) overlaps I_pub ([1.68e-3, 1.74e-3])
    AND I_recomp(sensitivity: [1, 250]) ALSO overlaps I_pub.
    -> VERIFIED (The published Libra distance-7 error rate is reproduced from shipped predictions).

E2: VERIFIED_WITH_LIMITATIONS_FIT_RANGE_SENSITIVITY
    I_recomp(primary: [10, 250]) overlaps I_pub ([1.68e-3, 1.74e-3]),
    BUT I_recomp(sensitivity: [1, 250]) does NOT overlap I_pub.
    -> VERIFIED_WITH_LIMITATIONS (Outcome reproduces published figure but is sensitive to r01).

E3: DISCREPANCY_OUTSIDE_UNCERTAINTY
    I_recomp(primary: [10, 250]) does NOT overlap I_pub ([1.68e-3, 1.74e-3]).
    -> NOT_VERIFIED (Recomputed distance-7 error rate deviates from published figure).

========================================================================================
DECISION MATRIX FOR TARGET A2: Error Suppression Factor (Lambda)
========================================================================================

L1: VERIFIED
    I_recomp(primary: [10, 250]) overlaps I_pub ([2.02, 2.06])
    AND I_recomp(sensitivity: [1, 250]) ALSO overlaps I_pub.
    -> VERIFIED (The published error suppression factor Lambda is reproduced from shipped predictions).

L2: VERIFIED_WITH_LIMITATIONS_FIT_RANGE_SENSITIVITY
    I_recomp(primary: [10, 250]) overlaps I_pub ([2.02, 2.06]),
    BUT I_recomp(sensitivity: [1, 250]) does NOT overlap I_pub.
    -> VERIFIED_WITH_LIMITATIONS (Lambda reproduces published figure but is sensitive to r01).

L3: DISCREPANCY_OUTSIDE_UNCERTAINTY
    I_recomp(primary: [10, 250]) does NOT overlap I_pub ([2.02, 2.06]).
    -> NOT_VERIFIED (Recomputed Lambda deviates from published scaling).

========================================================================================
DECISION MATRIX FOR TARGET B: Neural Network Headline Metric
========================================================================================

B1: NOT_REPRODUCIBLE_FROM_PUBLIC_DATA
    Zero prediction files or model weights for the Neural Network decoder exist
    within the public Zenodo archive (10.5281/zenodo.13273331).
    -> NOT_REPRODUCIBLE_FROM_PUBLIC_DATA
       (Factual statement of archive scope; the headline neural figure is
        not recomputable from artifacts in this archive).
```

---

## 4. Mathematical Execution Protocol

1. **Point Extraction ($p_L$):**
   $$p_L(d, \text{patch}, \text{basis}, t) = \frac{1}{N} \sum_{i=1}^N (\text{obs\_flips\_actual}_i \oplus \text{obs\_flips\_predicted}_i)$$
   with binomial standard error $\sigma_p = \sqrt{p_L(1 - p_L) / N}$.
2. **Per-Patch Linear Regression:**
   Fit $y(t) = \ln(1 - 2 p_L(t)) = c + m t$ using weighted linear regression.
   $$\varepsilon_d(\text{patch}, \text{basis}) = \frac{1 - e^m}{2}$$
   Standard error of regression slope $\sigma_m$ propagates to:
   $$\sigma_{\varepsilon_d} = \frac{e^m}{2} \sigma_m$$
3. **Subgrid Averaging:**
   * Mean $\bar{\varepsilon}_d = \frac{1}{2 K_d} \sum_{k=1}^{K_d} (\varepsilon_{d, X, k} + \varepsilon_{d, Z, k})$ across $K_3 = 9, K_5 = 4, K_7 = 1$.
   * Standard error of the mean: $\sigma_{\bar{\varepsilon}_d} = \frac{1}{2 K_d} \sqrt{\sum \sigma_{\varepsilon}^2}$.
4. **$\Lambda$ Linear Regression:**
   Fit $\ln(\bar{\varepsilon}_d) = c_{\Lambda} - \frac{d}{2} \ln(\Lambda)$ across $d \in \{3, 5, 7\}$.
   $$\Lambda = \exp(-m_{\Lambda}), \quad \sigma_{\Lambda} = \Lambda \cdot \sigma_{m_{\Lambda}}$$

---

## 5. Provenance, Data Manifest & Determinism Test Protocol

1. **Cryptographic Validation:**
   * Remote archive MD5 is verified (`21fa6ad35b395d838ebcdbc92e364a12`).
   * Every extracted `.b8` file is hashed (SHA-256) upon extraction and recorded in `data_manifest.json`.
2. **Deterministic Regeneration Test:**
   * Execution must be completely reproducible:
     ```bash
     mv results results_bak && python3 reproduce.py
     diff -u results/summary.json results_bak/summary.json
     ```
   * 0 byte differences required between independent executions.
