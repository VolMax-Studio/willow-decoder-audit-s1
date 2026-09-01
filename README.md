# Willow QEC Decoder Audit (`willow-decoder-audit-s1`)

[![Source Dataset DOI](https://img.shields.io/badge/Source%20Dataset%20DOI-10.5281%2Fzenodo.13273331-blue)](https://doi.org/10.5281/zenodo.13273331)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](LICENSE_L0.md)

Pre-registered independent baseline audit and mathematical reproduction of Google Quantum AI's Willow processor quantum error correction benchmarks (*Nature* 638, 920–926, 2025 / arXiv:2408.13687v1) from 728 raw physical telemetry and prediction files in Zenodo dataset [`10.5281/zenodo.13273331`](https://doi.org/10.5281/zenodo.13273331).

---

## 1. Central Claim Under Audit

Google Quantum AI published a distance-7 logical error rate per cycle `eps_7 = (1.71 +/- 0.03) x 10^-3` and an error suppression factor `Lambda = 2.04 +/- 0.02` for its ensembled matching synthesis decoder (**Libra**, ensemble size 51) on the Willow 105-qubit processor. The Zenodo public repository ships raw detection events and decoder prediction files for this matching family. 

**This audit evaluates whether Google's published matching-family figures recompute directly from the shipped physical prediction files under decision rules frozen before the telemetry data was accessed.**

---

## 2. What Would Falsify It (Pre-Frozen Decision Rules)

Evaluation criteria were pre-registered and cryptographically locked prior to data extraction in [`PREREGISTRATION.md`](PREREGISTRATION.md) (Commit [`bf7e3a7`](https://github.com/VolMax-Studio/willow-decoder-audit-s1/commit/bf7e3a7)):

* **Target A1 (Distance-7 Logical Error `eps_7`):** Recomputed 1-sigma regression confidence interval fails to overlap published interval `[1.68e-3, 1.74e-3]` => **`E3: NOT_VERIFIED`**.
* **Target A2 (Error Suppression Factor `Lambda`):** Recomputed 1-sigma regression confidence interval fails to overlap published scaling `[2.02, 2.06]` => **`L3: NOT_VERIFIED`**.
* **Target B (Neural Network Headline Figure):** Published figure `eps_7 = (1.43 +/- 0.03) x 10^-3`, `Lambda = 2.14 +/- 0.02` evaluated against artifact availability in the public archive => **`B1: NOT_REPRODUCIBLE_FROM_PUBLIC_DATA`** if model weights/predictions are omitted from public release.

---

## 3. What Was Measured (Audit Results)

```
==================================================================================================================
WILLOW QEC DECODER AUDIT RESULTS (14 Patches, 2 Bases, 13 Cycle Sweeps = 28 Regressions)
==================================================================================================================
d=3 Subgrid Mean (9 patches x 2 bases): eps_3 = 7.116 +/- 0.011 x 10^-3  (Published Table S1: 7.12 +/- 0.06 x 10^-3)
d=5 Subgrid Mean (4 patches x 2 bases): eps_5 = 3.494 +/- 0.006 x 10^-3  (Published Table S1: 3.49 +/- 0.04 x 10^-3)
d=7 Center Patch (1 patch   x 2 bases): eps_7 = 1.711 +/- 0.005 x 10^-3  (Published Table S1: 1.71 +/- 0.03 x 10^-3)
Error Suppression Factor Lambda       : Lambda = 2.0383 +/- 0.0032             (Published Table S1: 2.04 +/- 0.02)
------------------------------------------------------------------------------------------------------------------
FORMAL VERDICT [TARGET A1 - eps_7] : E1: VERIFIED (primary range only)
    Sensitivity condition t in [1, 250] could not be evaluated:
    the archive contains zero Libra prediction files for r01.
    See FAILURES.md #002.
FORMAL VERDICT [TARGET A2 - Lambda]: L1: VERIFIED (primary range only)
    Sensitivity condition t in [1, 250] could not be evaluated:
    the archive contains zero Libra prediction files for r01.
    See FAILURES.md #002.
FORMAL VERDICT [TARGET B  - Neural]: B1: NOT_REPRODUCIBLE_FROM_PUBLIC_DATA (Zero prediction files in archive)
==================================================================================================================
```

---

## 4. Key Findings

1. **Reproduction Within Published Uncertainty of Google's Libra Matching SOTA:**
   * Direct re-calculation from 728 physical hardware prediction files (`libra_decoder_with_rl_optimized_prior`) across all 14 subgrid patches reproduces `eps_7 = 1.711e-3` and `Lambda = 2.0383 +/- 0.0032`, matching published values (`eps_7 = 1.71 +/- 0.03 e-3`, `Lambda = 2.04 +/- 0.02`) within 1-sigma experimental uncertainty.
2. **Dataset Scope Separation (Neural Network Headline):**
   * The headline metric (`eps_7 = 1.43e-3`, `Lambda = 2.14`) was produced exclusively by a recurrent attention Neural Network decoder whose model weights and prediction files are omitted from the public Zenodo archive.
   * The public archive contains prediction files for three matching-family decoders across five prior configurations, but zero predictions from the Neural Network decoder. Any recomputation from this archive alone therefore benchmarks against the matching-family SOTA (`eps_7 = 1.71e-3`), not against the headline `1.43e-3`.
   * *Note: Neural network model weights are a separate domain artifact and are routinely distributed separately; this is a statement of dataset archive scope, not an allegation regarding the published results.*

---

## 5. Limitations & Epistemic Boundaries

* **Sensitivity Range Omission (T-0 / Failures #002):** The secondary sensitivity check ($t \in [1, 250]$) could not be evaluated because Google's public archive ships Libra predictions only for $r \in [10, 250]$ (0 files for single-cycle $r01$).
* **Asymmetry in Published Uncertainty Composition (T-1):** Published $\sigma_{\text{pub}}$ for $\varepsilon_7$ ($\pm 0.03 \times 10^{-3}$) is smaller than the empirical $X/Z$ basis spread visible in Table 1 ($1.55$ vs $1.30 \times 10^{-3}$). Our $\sigma_{\text{recomp}}$ is the propagated linear regression standard error; the two $\sigma$ values measure distinct variance components.
* **Degree-of-Freedom Constraint (T-2):** Linear regression for $\Lambda$ across 3 distance points ($d \in \{3, 5, 7\}$) with 2 parameters has $\text{dof} = 1$; $\sigma_{\Lambda}$ is reported as indicative regression standard error.
* **Archive Scope vs Scientific Claim (Target B):** Verdict `B1` reflects dataset packaging scope, not a dispute regarding the scientific validity of the published neural network figures.
* **Execution Boundary:** Single-host execution; external cross-machine replication pending.

---

## 6. Operational Status

* **Status:** `CLOSED (Pre-registered reproduction complete; verdicts logged)`
* **Independently Reproduced Externally:** `NOT YET (Open obligation for external review)`
* **Defect & Anomaly Ledger:** Documented in [`FAILURES.md`](FAILURES.md) (4 logged anomaly/governance entries).

---

## 7. Provenance, Anchors & Software Lock

* **Telemetry Source:** Zenodo Record [`10.5281/zenodo.13273331`](https://doi.org/10.5281/zenodo.13273331)
* **Archive Pin:** `google_105Q_surface_code_d3_d5_d7.zip` (MD5: `21fa6ad35b395d838ebcdbc92e364a12`)
* **Primary Literature Lock:** arXiv:2408.13687v1 / *Nature* 638, 920–926 (2025)
* **Pre-Registration Lock:** Commit [`bf7e3a7`](https://github.com/VolMax-Studio/willow-decoder-audit-s1/commit/bf7e3a7) (Frozen on 2026-09-01 prior to telemetry ingestion)
* **Software Lock:** Python 3.12.3, `numpy==2.5.2` (stdlib only; zero additional runtime dependencies)
* **Legal Terms:** [`LICENSE_L0.md`](LICENSE_L0.md) (CC-BY-4.0 Attribution compliant)

---

## 8. Reproduce It

### Step 1: Install Minimal Dependencies
```bash
pip install -r requirements-minimal.txt
```

### Step 2: Run Deterministic Reproduction Harness
```bash
python3 reproduce.py
```

### Step 3: Run Determinism Test
```bash
mv results results_bak && python3 reproduce.py && diff -r results results_bak
```
*(Requires 0 byte differences across all generated artifacts in `results/`).*

### Optional: Generate Publication Verification Chart
```bash
pip install -r requirements-figure.txt
python3 tools/make_figure.py
```
*(Saves high-resolution plot to [`figures/willow_qec_audit_verification.png`](figures/willow_qec_audit_verification.png)).*
