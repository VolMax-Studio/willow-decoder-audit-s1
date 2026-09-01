# PREMISES: Physical, Ingestion, and Model Foundations

**Repository:** `willow-decoder-audit-s1`  
**Target Telemetry Source:** Google 105Q Surface Code Dataset  
**Persistent Identifier (DOI):** [`10.5281/zenodo.13273331`](https://doi.org/10.5281/zenodo.13273331)  
**Target Archive:** `google_105Q_surface_code_d3_d5_d7.zip` (MD5: `21fa6ad35b395d838ebcdbc92e364a12`)  
**Primary Published Paper:** Google Quantum AI and Collaborators, *Quantum error correction below the surface code threshold*, Nature 638, 920–926 (2025). DOI: [`10.1038/s41586-024-08449-y`](https://doi.org/10.1038/s41586-024-08449-y). Preprint: [arXiv:2408.13687](https://arxiv.org/abs/2408.13687).  
**Date Frozen:** 2026-09-01  

---

## 1. Primary Paper Headline Claims & Published Figures (Verbatim)

From Nature 638, 920–926 (2025) and arXiv:2408.13687:

1. **Distance-7 Logical Error Rate per Cycle:**
   $$\epsilon_L(d=7) = 0.143\% \pm 0.003\% \quad (1.43 \times 10^{-3})$$
   *(Reported for the 101-qubit distance-7 surface code memory on the Willow processor).*
2. **Error Suppression Factor ($\Lambda_{5/7}$):**
   $$\Lambda = 2.14 \pm 0.02$$
   *(Measured as the ratio of logical error rates when increasing code distance by 2, from $d=5$ to $d=7$).*
3. **Break-Even Factor:**
   $$2.4 \pm 0.3$$
   *(Factor by which the logical memory lifetime exceeds that of the best constituent physical qubit).*

---

## 2. Published Decoding Pipeline Identification

From arXiv:2408.13687, Nature (2025), and dataset README:

* **Headline Real-Time Benchmark Pipeline:** **Correlated Matching with RL-Optimized Prior** (`correlated_matching_decoder_with_rl_optimized_prior`).
  * Decoder Engine: Sparse Blossom minimum-weight matching with Fowler 2-step correlated error re-weighting.
  * Prior: Calibrated using Reinforcement Learning over joint distance-3 and distance-5 13-cycle calibration data.
* **Secondary Ensemble Pipelines (Shipped in Dataset):**
  * `harmony_decoder_with_rl_optimized_prior` (51-decoder ensemble)
  * `libra_decoder_with_rl_optimized_prior` (Matching synthesis ensemble)
* **Stock Baseline (Example 2 in Dataset README):**
  * `stim analyze_errors --in circuit_noisy_si1000.stim --out error_model.dem`
  * `pymatching predict --dem error_model.dem --in detection_events.b8`

---

## 3. Physical Ingestion Formats & Per-Cycle Decay Convention

From `docs/ZENODO_DATASET_README.md`:

### A. Binary Formats
* **`detection_events.b8`:** Packed bits ($N_{\text{detectors}}$ bits/shot, little-endian, byte-aligned).
* **`obs_flips_actual.b8`:** 1 bit per shot (`0` = no flip, `1` = flipped).
* **`obs_flips_predicted.b8`:** 1 bit per shot predicted by decoder.
* **Logical Error Event:**
  $$\text{error}_i = \text{obs\_flips\_actual}_i \oplus \text{obs\_flips\_predicted}_i$$

### B. Logical Error Rate per Experiment ($P_L$)
For a given patch, basis, distance $d$, and cycle count $r$:
$$P_L(d, \text{basis}, \text{patch}, r) = \frac{1}{N_{\text{shots}}} \sum_{i=1}^{N_{\text{shots}}} (\text{actual}_i \oplus \text{predicted}_i)$$

### C. Expectation Value Decay & Per-Cycle Error Rate ($\epsilon_L$)
The logical observable expectation value $\langle P \rangle(r)$ decays with the number of QEC cycles $r$:
$$\langle P \rangle(r) = 1 - 2 P_L(r) = (1 - 2 \epsilon_{\text{init}}) (1 - 2 \epsilon_L)^r$$
where:
* $\epsilon_L$ is the **logical error rate per cycle**.
* $\epsilon_{\text{init}}$ accounts for state preparation and measurement (SPAM) infidelity.
* For small $\epsilon_L$, $(1 - 2 \epsilon_L)^r \approx e^{-2 r \epsilon_L}$, yielding:
  $$\epsilon_L = \frac{1}{2} \left(1 - e^{-2 / T_L}\right) \approx \frac{1}{2 r} \ln \left( \frac{1 - 2 \epsilon_{\text{init}}}{1 - 2 P_L(r)} \right)$$
