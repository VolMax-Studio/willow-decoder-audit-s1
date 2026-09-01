# LIMITATIONS: Scope, Non-Claims, and Epistemic Boundaries

**Repository:** `willow-decoder-audit-s1`  
**Date:** 2026-09-01  

---

## 1. Scope and Non-Claims on Dataset Completeness

* **No Allegation Regarding Unshipped Neural Network Predictions:**
  The finding that the headline Neural Network decoder predictions ($\varepsilon_7 = 1.43 \times 10^{-3}, \Lambda = 2.14$) are not included in the Zenodo dataset (`10.5281/zenodo.13273331`) is a factual statement about **dataset distribution scope**, NOT an allegation of wrongdoing or an assertion that the published numbers are incorrect. Large neural network weights and experimental training pipelines are routinely distributed in separate domain artifacts.
* **Separation of Claims:**
  * **Target A (Measurable Verification):** Recomputing $\varepsilon_7$ and $\Lambda$ from Google's shipped `libra_decoder_with_rl_optimized_prior` prediction files against the published matching benchmark ($\varepsilon_7 = (1.71 \pm 0.03) \times 10^{-3}, \Lambda = 2.04 \pm 0.02$).
  * **Target B (Scope Finding):** The headline Neural Network figure cannot be directly recalculated from `10.5281/zenodo.13273331` alone.

---

## 2. Pinned Source Risk (Preprint vs. Nature Final Version)

* All citations, line numbers, and equation forms in this repository are cryptographically pinned against the LaTeX source of **`arXiv:2408.13687v1`** (extracted in `docs/arxiv_source/`).
* If typographical differences, minor errata, or updated parameter conventions exist in the final journal version (*Nature* 638, 920–926, 2025), all verdicts in this instance strictly apply to the pinned preprint version `arXiv:2408.13687v1`.
