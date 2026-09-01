# PREMISES: Physical, Ingestion, and Model Foundations

**Repository:** `willow-decoder-audit-s1`  
**Target Telemetry Source:** Google 105Q Surface Code Dataset  
**Persistent Identifier (DOI):** [`10.5281/zenodo.13273331`](https://doi.org/10.5281/zenodo.13273331)  
**Target Archive:** `google_105Q_surface_code_d3_d5_d7.zip` (MD5: `21fa6ad35b395d838ebcdbc92e364a12`)  
**Primary Published Paper:** Google Quantum AI and Collaborators, *Quantum error correction below the surface code threshold*, Nature 638, 920–926 (2025). DOI: [`10.1038/s41586-024-08449-y`](https://doi.org/10.1038/s41586-024-08449-y). Preprint: [arXiv:2408.13687v1](https://arxiv.org/abs/2408.13687).  
**Date Frozen:** 2026-09-01  

---

## 1. Primary Paper Headline Claims & Published Figures (Verbatim from LaTeX Source)

From `main.tex` (lines 121–140) and `supplement.tex` / `text_sm/`:

### A. Headline Figures Produced by the **Neural Network Decoder** (Main Text lines 124–126, Fig. 1c-d):
* **Distance-7 Logical Error Rate per Cycle:**
  $$\varepsilon_7 = (1.43 \pm 0.03) \times 10^{-3} \quad (0.143\% \pm 0.003\%)$$
  *(Location: `main.tex:125`, `text_sm/decoder_intro.tex:17`, `text_sm/uncertainty.tex:30` Table 1).*
* **Error Suppression Factor ($\Lambda$):**
  $$\Lambda = 2.14 \pm 0.02$$
  *(Location: `main.tex:125`, abstract line 23. Computed via linear regression of $\ln(\varepsilon_d)$ versus $d$ across $d \in \{3, 5, 7\}$).*

### B. Secondary Figures Produced by **Ensembled Matching Synthesis (Libra)** (Main Text lines 127–128, Table S1):
* **Distance-7 Logical Error Rate per Cycle:**
  $$\varepsilon_7 = (1.71 \pm 0.03) \times 10^{-3} \quad (0.171\% \pm 0.003\%)$$
  *(Location: `main.tex:128`, `text_sm/decoder_intro.tex:17` Table S1 column 1).*
* **Error Suppression Factor ($\Lambda$):**
  $$\Lambda = 2.04 \pm 0.02$$
  *(Location: `main.tex:128`).*

### C. Break-Even Lifetime Factor:
* **Factor:** $2.4 \pm 0.3$
  *(Location: `main.tex:139`. Distance-7 logical qubit lifetime $291 \pm 6\ \mu\text{s}$ exceeding best physical qubit lifetime $119 \pm 13\ \mu\text{s}$ by $2.4 \pm 0.3$).*

---

## 2. Definitive Decoding Pipeline Identification & Distinction

The paper makes an explicit distinction between offline decoders (Table S1, `text_sm/decoder_intro.tex:13–22`):

```
+-------------------------------------------------------------------------------------------------------+
| 1. Neural Network Decoder (Bausch et al. 2023, recurrent attention-based NN):                         |
|    - Produces the Headline: e_7 = (1.43 +/- 0.03) x 10^-3, Lambda = 2.14 +/- 0.02                    |
|    - NOT shipped in Zenodo dataset predictions (requires separate NN checkpoint / weights).          |
+-------------------------------------------------------------------------------------------------------+
                                                   │
+-------------------------------------------------------------------------------------------------------+
| 2. Libra Decoder Ensemble (Jones 2024, matching synthesis with ensemble size = 51):                   |
|    - Produces the Matching Benchmark: e_7 = (1.71 +/- 0.03) x 10^-3, Lambda = 2.04 +/- 0.02           |
|    - Shipped in Zenodo dataset under decoding_results/libra_decoder_with_rl_optimized_prior/         |
+-------------------------------------------------------------------------------------------------------+
                                                   │
+-------------------------------------------------------------------------------------------------------+
| 3. Correlated Matching (Fowler 2013, Sparse Blossom with 2-step re-weighting):                       |
|    - Used for Real-Time & Sensitivity Budgeting (Fig. 4c, error budget simulations).                  |
|    - Shipped in Zenodo dataset under decoding_results/correlated_matching_decoder_with_rl_optimized_prior/ |
+-------------------------------------------------------------------------------------------------------+
```

---

## 3. Mathematical Definitions & Decay Conventions (Verbatim from `text_sm/uncertainty.tex`)

From `text_sm/uncertainty.tex` (lines 38–40):

### A. Logical Error Rate per Experiment ($p_L$)
For $N = 10^5$ repetitions per point:
$$p_L(d, \text{patch}, \text{basis}, t) = \frac{1}{N} \sum_{i=1}^{N} (\text{obs\_flips\_actual}_i \oplus \text{obs\_flips\_predicted}_i)$$
Statistical uncertainty per point: $\sigma_{p_L} = \sqrt{p_L (1 - p_L) / N}$.

### B. Fitting Formula for Logical Error per Cycle ($\varepsilon_d$)
The logical observable expectation value decays as:
$$\langle P \rangle(t) = 1 - 2 p_L(t) = (1 - 2 \varepsilon_{\text{init}}) (1 - 2 \varepsilon_d)^t$$
$$\ln(1 - 2 p_L(t)) = \ln(1 - 2 \varepsilon_{\text{init}}) + t \ln(1 - 2 \varepsilon_d)$$

* **Linear Regression:** $\varepsilon_d$ is obtained by fitting a straight line $y = m t + c$ to $y = \ln(1 - 2 p_L(t))$ versus cycle count $t \in [10, 250]$:
  $$\text{slope } m = \ln(1 - 2 \varepsilon_d) \implies \varepsilon_d = \frac{1 - e^m}{2}$$
* **SPAM Infidelity ($\varepsilon_{\text{init}}$):** Obtained from the intercept $c = \ln(1 - 2 \varepsilon_{\text{init}}) \implies \varepsilon_{\text{init}} = \frac{1 - e^c}{2}$ as a free parameter of the linear fit.

### C. Averaging & $\Lambda$ Scaling Convention
1. $\varepsilon_d$ and its uncertainty are computed individually for each patch and basis ($X$ and $Z$).
2. Mean $\bar{\varepsilon}_d$ is obtained by averaging over both bases ($X, Z$) and across all available patches for that distance:
   * $d=3$: 9 subgrid patches (center qubits `q2_7`, `q4_5`, `q4_9`, `q6_3`, `q6_7`, `q6_11`, `q8_5`, `q8_9`, `q10_7`).
   * $d=5$: 4 subgrid patches (`q4_7`, `q6_5`, `q6_9`, `q8_7`).
   * $d=7$: 1 center patch (`q6_7`).
3. Suppression factor $\Lambda$ is obtained via linear regression of $\ln(\bar{\varepsilon}_d)$ versus $d$ for $d \in \{3, 5, 7\}$:
   $$\ln(\bar{\varepsilon}_d) = -\frac{d}{2} \ln(\Lambda) + C \implies \bar{\varepsilon}_d \propto \Lambda^{-d/2}$$

---

## 4. Scope and Ground Truth Coordinates for Audit Targets

From Table S1 (`text_sm/decoder_intro.tex:15–17`) and Table 1 (`text_sm/uncertainty.tex:15–31`):

### Target V-A1: Neural Network Headline ($\varepsilon_7 = 1.43 \times 10^{-3}$, $\Lambda = 2.14$)
* **Distance $d=7$ ($X$ basis, patch `q6_7`):** Reported $\varepsilon_{7, X} = (1.55 \pm 0.04) \times 10^{-3}$
* **Distance $d=7$ ($Z$ basis, patch `q6_7`):** Reported $\varepsilon_{7, Z} = (1.30 \pm 0.04) \times 10^{-3}$
* **Mean across bases:** $\bar{\varepsilon}_7 = \frac{1.55 + 1.30}{2} \times 10^{-3} = 1.425 \times 10^{-3} \approx (1.43 \pm 0.03) \times 10^{-3}$.

### Target V-A2: Libra Matching Benchmark ($\varepsilon_7 = 1.71 \times 10^{-3}$, $\Lambda = 2.04$)
* **Shipped Predictions:** Shipped directly in Zenodo dataset under `google_105Q_surface_code_d3_d5_d7/d7_at_q6_7/{X,Z}/r{...}/decoding_results/libra_decoder_with_rl_optimized_prior/obs_flips_predicted.b8`.
* **Reported Mean:** $\bar{\varepsilon}_7 = (1.71 \pm 0.03) \times 10^{-3}$.
