# PREMISES: Physical, Ingestion, and Model Foundations

**Repository:** `willow-decoder-audit-s1`  
**Target Telemetry Source:** Google 105Q Surface Code Dataset  
**Persistent Identifier (DOI):** [`10.5281/zenodo.13273331`](https://doi.org/10.5281/zenodo.13273331)  
**Target Archive:** `google_105Q_surface_code_d3_d5_d7.zip` (MD5: `21fa6ad35b395d838ebcdbc92e364a12`)  
**Pinned Primary Publication:** Google Quantum AI and Collaborators, *Quantum error correction below the surface code threshold*, Preprint: [arXiv:2408.13687v1](https://arxiv.org/abs/2408.13687) (Extracted in `docs/arxiv_source/`). Journal Version: Nature 638, 920–926 (2025), DOI: [`10.1038/s41586-024-08449-y`](https://doi.org/10.1038/s41586-024-08449-y).  
**Date Frozen:** 2026-09-01  

---

## 1. Primary Paper Headline Claims & Published Figures (Verbatim from LaTeX Source)

From `docs/arxiv_source/main.tex` (lines 121–140) and `docs/arxiv_source/text_sm/`:

### A. Headline Figures Produced by the **Neural Network Decoder**
* **Verbatim Citation (`main.tex:124–126`):**
  > *„With our neural network decoder, we observe $\Lambda = 2.14 \pm 0.02$ and $\varepsilon_7$ = $(1.43 \pm 0.03)\times 10^{-3}$ (see Fig. 1c-d).”*
* **Table 1 Breakdown (`text_sm/uncertainty.tex:30`, Caption line 33: „...using the neural network decoder”):**
  * $d=7\ (0,0)$ $X$ basis: $\varepsilon_{7,X} = 0.00155 \pm 0.00004$
  * $d=7\ (0,0)$ $Z$ basis: $\varepsilon_{7,Z} = 0.00130 \pm 0.00004$
  * Average across bases: $\bar{\varepsilon}_7 = \frac{0.00155 + 0.00130}{2} = 0.001425 \approx (1.43 \pm 0.03) \times 10^{-3}$.

### B. Matching SOTA Figures Produced by **Ensembled Matching Synthesis (Libra)**
* **Verbatim Citation (`main.tex:127–128`):**
  > *„With ensembled matching synthesis, we observe $\Lambda = 2.04 \pm 0.02$ and $\varepsilon_7$ = $(1.71 \pm 0.03)\times 10^{-3}$.”*
* **Table S1 Breakdown (`text_sm/decoder_intro.tex:15–20`):**
  * $\varepsilon_3 = (7.12 \pm 0.06) \times 10^{-3}$
  * $\varepsilon_5 = (3.49 \pm 0.04) \times 10^{-3}$
  * $\varepsilon_7 = (1.71 \pm 0.03) \times 10^{-3}$

---

## 2. Definitive Decoder Taxonomy & Reporting Status for 105Q Dataset

From `text_sm/decoder_intro.tex` (lines 25–33), `text_sm/decode_priors.tex` (lines 11–15), and verbatim scan of Zenodo archive TOC:

| Decoder Name | Architecture / Reference | Ensemble Size | Shipped in 105Q Zenodo Archive? | $\varepsilon_7$ & $\Lambda$ Reported for 105Q in Paper? |
|---|---|---|---|---|
| **Neural Network** | Recurrent attention-based NN (Bausch et al. 2023) | N/A | **NO (0 prediction files in archive)** | **YES ($\varepsilon_7 = 1.43 \times 10^{-3}, \Lambda = 2.14$)** |
| **Libra** | Ensembled matching synthesis (Jones 2024) | **51** | **YES (`libra_decoder_with_rl_optimized_prior`)** | **YES ($\varepsilon_7 = 1.71 \times 10^{-3}, \Lambda = 2.04$)** |
| **Harmony** | Ensembled matching (Shutty et al. 2024) | **101** | **YES (`harmony_decoder_with_rl_optimized_prior`)** | **NOT REPORTED FOR 105Q** *(Used for 72Q dataset characterization in Table S2)* |
| **Correlated Matching** | Sparse blossom 2-step re-weighting (Fowler 2013) | 1 | **YES (`correlated_matching_decoder_with_rl_optimized_prior`)** | Used for real-time/error budget; no headline 105Q $\varepsilon_7$ tabulated |
| **Stock PyMatching** | Standard decomposed 2-weight matching | 1 | Generated locally via Stim `circuit_noisy_si1000.stim` | Baseline example in dataset README (Example 2) |

---

## 3. Mathematical Definitions, Fitting Protocol & $\Lambda$ Convention

From `docs/arxiv_source/text_sm/uncertainty.tex` (lines 38–40) and `main.tex:121–123`:

### A. Fitting Formula for Logical Error per Cycle ($\varepsilon_d$)
* **Verbatim Citation (`text_sm/uncertainty.tex:38`):**
  > *„To determine the logical error per cycle $\varepsilon_d$, we fit exponentials to $p_L$ versus number of cycles $t$ (technically, by fitting a line to $\ln(1-2p_L)$ versus $t$) for each code... We compute $\varepsilon_d$ and an uncertainty for each code and logical basis and then average over basis and code for data reported in the manuscript.”*
* **Linear Model:**
  $$\ln(1 - 2 p_L(t)) = \ln(1 - 2 \varepsilon_{\text{init}}) + t \ln(1 - 2 \varepsilon_d)$$
  $$\text{Fitted slope } m = \ln(1 - 2 \varepsilon_d) \implies \varepsilon_d = \frac{1 - e^m}{2}$$
  $$\text{Fitted intercept } c = \ln(1 - 2 \varepsilon_{\text{init}}) \implies \varepsilon_{\text{init}} = \frac{1 - e^c}{2} \quad (\text{free parameter})$$

### B. Fit Range Pre-Registration (R-1 Resolution)
* **Primary Scope (`main.tex:121`, `uncertainty.tex:43`):** Sweeps from 10 to 250 cycles:  
  $$t \in [10, 250] \quad (\text{cycles: } r10, r30, r50, r70, r90, r110, r130, r150, r170, r190, r210, r230, r250)$$
* **Pre-Registered Sensitivity Variation:** $t \in [1, 250]$ (including $r01$).
* **Decision Boundary:** If inclusion/exclusion of $r01$ shifts $\varepsilon_d$ outside the published $\pm 0.03 \times 10^{-3}$ uncertainty, the outcome is classified as `Verified with Limitations — fit range sensitivity on r01`.

### C. $\Lambda$ Error Suppression Scaling Convention (R-2 Resolution & Sanity Check)
* **Definition:** $\Lambda$ is the suppression factor per distance increase of 2 ($\Delta d = 2$):
  $$\bar{\varepsilon}_d = C \cdot \Lambda^{-d/2} \iff \ln(\bar{\varepsilon}_d) = \ln(C) - \frac{d}{2} \ln(\Lambda)$$
* **Linear Regression:** Regressing $\ln(\bar{\varepsilon}_d)$ versus $x = \frac{d}{2}$ yields slope $m_{\Lambda} = -\ln(\Lambda) \implies \Lambda = \exp(-m_{\Lambda})$.
* **Mathematical Sanity Check on Published Figures:**
  * For Libra ($\varepsilon_3 = 7.12 \times 10^{-3}, \varepsilon_5 = 3.49 \times 10^{-3}, \varepsilon_7 = 1.71 \times 10^{-3}$):
    $$\frac{\varepsilon_3}{\varepsilon_5} = 2.0401, \quad \frac{\varepsilon_5}{\varepsilon_7} = 2.0409 \implies \text{Regression } \Lambda = 2.0405 \quad (\text{Matches published } 2.04 \pm 0.02 \text{ exactly}).$$

---

## 4. Subgrid Patches & Scope

* **$d=3$ (9 Subgrid Patches):** `d3_at_q2_7`, `d3_at_q4_5`, `d3_at_q4_9`, `d3_at_q6_3`, `d3_at_q6_7`, `d3_at_q6_11`, `d3_at_q8_5`, `d3_at_q8_9`, `d3_at_q10_7`.
* **$d=5$ (4 Subgrid Patches):** `d5_at_q4_7`, `d5_at_q6_5`, `d5_at_q6_9`, `d5_at_q8_7`.
* **$d=7$ (1 Center Patch):** `d7_at_q6_7`.
* **Bases:** Both $X$ and $Z$ bases for all patches.
