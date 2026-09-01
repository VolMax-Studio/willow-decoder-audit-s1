# Willow QEC Decoder Audit (willow-decoder-audit-s1)

[![Source Dataset DOI](https://img.shields.io/badge/Source%20Dataset%20DOI-10.5281%2Fzenodo.13273331-blue)](https://doi.org/10.5281/zenodo.13273331)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](LICENSE_L0.md)

Pre-registered independent reproduction and baseline audit of Google Quantum AI's Willow processor QEC benchmark numbers (*Nature* 638, 920–926, 2025 / arXiv:2408.13687v1) from raw physical hardware predictions in Zenodo dataset `10.5281/zenodo.13273331`.

---

## 1. Audit Summary & Formal Verdicts

```
==================================================================================================================
WILLOW QEC DECODER AUDIT RESULTS (14 Patches, 2 Bases, 13 Cycle Sweeps = 28 Regressions)
==================================================================================================================
d=3 Subgrid Mean (9 patches x 2 bases): eps_3 = 7.116 +/- 0.011 x 10^-3  (Published Table S1: 7.12 +/- 0.06 x 10^-3)
d=5 Subgrid Mean (4 patches x 2 bases): eps_5 = 3.494 +/- 0.006 x 10^-3  (Published Table S1: 3.49 +/- 0.04 x 10^-3)
d=7 Center Patch (1 patch   x 2 bases): eps_7 = 1.711 +/- 0.005 x 10^-3  (Published Table S1: 1.71 +/- 0.03 x 10^-3)
Error Suppression Factor Lambda       : Lambda = 2.0383 +/- 0.0032             (Published Table S1: 2.04 +/- 0.02)
FORMAL VERDICT [TARGET A1 - eps_7] : E1: VERIFIED (primary range only)
    Sensitivity condition t in [1,250] could not be evaluated:
    the archive contains zero Libra prediction files for r01.
    See FAILURES.md #002.
FORMAL VERDICT [TARGET A2 - Lambda]: L1: VERIFIED (primary range only)
    Sensitivity condition t in [1,250] could not be evaluated:
    the archive contains zero Libra prediction files for r01.
    See FAILURES.md #002.
FORMAL VERDICT [TARGET B  - Neural]: B1: NOT_REPRODUCIBLE_FROM_PUBLIC_DATA (Zero prediction files in archive)
==================================================================================================================
```

---

## 2. Key Findings

1. **Reproduction Within Published Uncertainty of Google's Libra Matching SOTA:**
   * Direct re-calculation from 728 physical hardware prediction files (`libra_decoder_with_rl_optimized_prior`) across all 14 subgrid patches reproduces `eps_7 = 1.711e-3` and `Lambda = 2.0383 +/- 0.0032`, matching published values (`eps_7 = 1.71 +/- 0.03 e-3`, `Lambda = 2.04 +/- 0.02`) within 1-sigma experimental uncertainty.
2. **Dataset Scope Separation (Neural Network Headline):**
   * The headline metric (`eps_7 = 1.43e-3`, `Lambda = 2.14`) was produced exclusively by a recurrent attention Neural Network decoder whose model weights and prediction files are omitted from the public Zenodo archive.
   * The public archive contains prediction files for three matching-family decoders across five prior configurations, but zero predictions from the Neural Network decoder. Any recomputation from this archive alone therefore benchmarks against the matching-family SOTA (`eps_7 = 1.71e-3`), not against the headline `1.43e-3`.
   * *Note: Neural network model weights are a separate domain artifact and are routinely distributed separately; this is a statement of dataset archive scope, not an allegation regarding the published results.*

---

## 3. Reproduction Instructions

### Dependencies
```bash
pip install -r requirements-minimal.txt
```

### Self-Contained Execution
```bash
python3 reproduce.py
```

### Determinism Test
```bash
mv results results_bak && python3 reproduce.py && diff -r results results_bak
```

### Optional: Publication Figure Generation
```bash
pip install -r requirements-figure.txt
python3 tools/make_figure.py
```
Generated figure is saved to [`figures/willow_qec_audit_verification.png`](figures/willow_qec_audit_verification.png).

---

## 4. Governance & Specification Artifacts

* [`PREMISES.md`](PREMISES.md): Verbatim LaTeX citations, mathematical decay models, and decoder taxonomy.
* [`PREREGISTRATION.md`](PREREGISTRATION.md): Pre-frozen disjoint decision rules (`E1..E3`, `L1..L3`, `B1`).
* [`LICENSE_L0.md`](LICENSE_L0.md): CC-BY-4.0 attribution terms and MD5 archive pin.
* [`LIMITATIONS.md`](LIMITATIONS.md): Non-claims disclosure regarding dataset distribution scope.
* [`QXL_CLAIM_EVALUATION.md`](QXL_CLAIM_EVALUATION.md): Primary-source evaluation of Quantum X Labs press release.
* [`results/summary.json`](results/summary.json): Complete machine-readable audit artifact with all 28 patch regressions.
