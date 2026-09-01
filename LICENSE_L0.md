# LICENSE_L0: Legal, Citation, and Access Right Ledger

**Repository:** `willow-decoder-audit-s1`  
**Evaluation Target:** Data for *"Quantum error correction below the surface code threshold"*  
**Zenodo Record ID:** `13273331`  
**Digital Object Identifier (DOI):** [`10.5281/zenodo.13273331`](https://doi.org/10.5281/zenodo.13273331)  
**Date of Record Query:** 2026-09-01  
**Access URL:** `https://zenodo.org/records/13273331`  

---

## 1. Dataset License & Rights Specification

* **License Name:** Creative Commons Attribution 4.0 International (`CC-BY-4.0`)
* **License URL:** [`https://creativecommons.org/licenses/by/4.0/`](https://creativecommons.org/licenses/by/4.0/)
* **Rights Granted:**
  * **Share:** Copy and redistribute the material in any medium or format for any purpose, even commercially.
  * **Adapt:** Remix, transform, and build upon the material for any purpose, even commercially.
* **Requirements / Conditions:**
  * **Attribution (Mandatory Condition):** Appropriate credit must be given, a link to the license provided, and indication if changes were made.
  * **No Additional Restrictions:** No legal terms or technological measures applied that legally restrict others from doing anything the license permits.
* **Redistribution Policy in this Repo:**
  * **No Raw Hardware Binary Data in Git:** Raw `.b8`, `.stim`, and `.dem` files are excluded from this repository via `.gitignore` and downloaded deterministically by `reproduce.py` via HTTP Range requests with MD5 / SHA-256 validation logged in `data_manifest.json`.

---

## 2. Mandatory Citation & Attribution Format

As required by Google Quantum AI and CC-BY-4.0 provisions:

```text
Google Quantum AI (2024), Data for "Quantum error correction below the surface code threshold", Zenodo, DOI 10.5281/zenodo.13273331, CC BY 4.0
```

BibTeX Entry:
```bibtex
@dataset{google_quantum_ai_2024_13273331,
  author       = {{Google Quantum AI}},
  title        = {Data for "Quantum error correction below the surface code threshold"},
  month        = aug,
  year         = 2024,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.13273331},
  url          = {https://doi.org/10.5281/zenodo.13273331}
}
```

Primary Published Paper:
> Google Quantum AI and Collaborators. *Quantum error correction below the surface code threshold.* Nature 638, 920–926 (2025). DOI: [10.1038/s41586-024-08449-y](https://doi.org/10.1038/s41586-024-08449-y). Preprint: [arXiv:2408.13687](https://arxiv.org/abs/2408.13687).

---

## 3. Remote Dataset Archive Pin (Cryptographic Digest)

The exact target archive evaluated in this instance is cryptographically pinned from Zenodo metadata:

* **File Name:** `google_105Q_surface_code_d3_d5_d7.zip`
* **File Size:** `5,716,907,033` bytes (5.45 GB / 5.72 GB decimal)
* **Pinned MD5 Digest:** `21fa6ad35b395d838ebcdbc92e364a12`
* **Download URL:** `https://zenodo.org/api/records/13273331/files/google_105Q_surface_code_d3_d5_d7.zip/content`

---

## 4. Tool Dependency Licenses

* **Stim (`stim==1.16.0`):** Apache License 2.0 (Copyright Google LLC).
* **PyMatching (`PyMatching==2.4.0`):** Apache License 2.0 (Copyright Oscar Higgott).
* **Sinter (`sinter==1.16.0`):** Apache License 2.0 (Copyright Google LLC).
* **NumPy (`numpy==2.5.2`):** BSD 3-Clause License.

---

## 5. L0 Clearance Status

* **Status:** `CLEAR — CONDITIONAL ON ATTRIBUTION`
* The dataset is open under `CC-BY-4.0`, permitting derived calculation, reproduction, audit evaluation, and publication provided the mandatory attribution string in Section 2 is displayed.
