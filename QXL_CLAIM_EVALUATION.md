# QXL Press Release Claim Evaluation (2026-08-21)

**Source Type:** Corporate Press Release via Newswire  
**Publisher:** Quantum X Labs (GlobeNewswire, Tel Aviv)  
**Publication Date & Time:** 2026-08-21 08:32 ET  
**Primary Source URL:** [`https://www.globenewswire.com/news-release/2026/08/21/...`](https://www.globenewswire.com/)  
**Evaluation Methodology:** P10 Claim Gate & Pre-Registration Standard  

---

## 1. Verbatim Claim Analysis

The press release states that Quantum X Labs achieved an error correction improvement against matching-family benchmarks, explicitly naming:
> *"...including Google's published correlated-matching and PyMatching results for the same configuration."*

The announcement includes an explicit scope limitation from Nir Sharon (Chief Quantum Technology Scientist):
> *"...emphasizing that this represents a single benchmark configuration, with next steps focused on replication across additional hardware devices and code configurations."*

---

## 2. Technical Parameter Inventory (Operating Point)

To evaluate whether the claim can be reproduced or falsified against the Google Willow dataset (`10.5281/zenodo.13273331`), the following operational parameters were checked against the text:

| Parameter | Required for Execution | Stated in Primary Source? |
|---|---|---|
| **Code Distance ($d$)** | Required | **NOT STATED** |
| **Patch Location (`patch_dir`)** | Required | **NOT STATED** |
| **Measurement Basis ($X$ or $Z$)** | Required | **NOT STATED** |
| **Cycle / Round Count ($r$)** | Required | **NOT STATED** |
| **Dataset File Identifier** | Required | **NOT STATED** |
| **Baseline Prior Configuration** | Required | **NOT STATED** |
| **Sample Split (Train / Test)** | Required | **NOT STATED** |
| **Numerical Error Rate ($P_L$)** | Required | **NOT STATED** |
| **Confidence Interval / Variance** | Required | **NOT STATED** |

---

## 3. Formal Verdict

```
+-----------------------------------------------------------------------------------------+
| FORMAL VERDICT: Unfalsifiable-as-Stated                                                 |
+-----------------------------------------------------------------------------------------+
```

### Rationale:
1. The primary press release provides **zero numerical values, zero dataset file identifiers, and zero operational coordinates** ($d, r, \text{patch}$).
2. No technical preprint, whitepaper, or code repository was linked or cited to establish the exact operating point.
3. The claim is categorically un-evaluable against the 420 experiments in the Google Willow dataset.
4. **No assertion is made regarding baseline cherry-picking:** The company explicitly limited its claim to the "matching-family" and cited correlated-matching. The observed inflation occurred at the media secondary reporting layer (e.g., Quantum Computing Report), not in the primary text.
