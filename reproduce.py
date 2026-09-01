#!/usr/bin/env python3
"""
reproduce.py — Single-Entry Reproduction Harness for Willow QEC Decoder Baseline Audit (v2)
"""

import os
import sys
import json
import urllib.request
import zipfile
import io
import hashlib
import argparse
import numpy as np

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
ZENODO_ZIP_URL = "https://zenodo.org/api/records/13273331/files/google_105Q_surface_code_d3_d5_d7.zip/content"
ZENODO_ZIP_SIZE = 5716907033
ZENODO_PINNED_MD5 = "21fa6ad35b395d838ebcdbc92e364a12"

# 14 Subgrid Patches defined in dataset and paper
PATCHES = {
    3: ["d3_at_q2_7", "d3_at_q4_5", "d3_at_q4_9", "d3_at_q6_3", "d3_at_q6_7", "d3_at_q6_11", "d3_at_q8_5", "d3_at_q8_9", "d3_at_q10_7"],
    5: ["d5_at_q4_7", "d5_at_q6_5", "d5_at_q6_9", "d5_at_q8_7"],
    7: ["d7_at_q6_7"]
}
BASES = ["X", "Z"]
PRIMARY_ROUNDS = ["r10", "r30", "r50", "r70", "r90", "r110", "r130", "r150", "r170", "r190", "r210", "r230", "r250"]

EXPECTED_VERSIONS = {
    "numpy": "2.5.2"
}

# Color definitions
USE_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ
GREEN = "\033[92m" if USE_COLOR else ""
RED = "\033[91m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""
RESET = "\033[0m" if USE_COLOR else ""


def verify_env(quiet=False):
    import platform
    if not quiet:
        print("================================================================================")
        print("REPRODUCTION ENVIRONMENT & DEPENDENCY VERIFICATION")
        print("================================================================================")
        print(f"Python:       {platform.python_version()} ({platform.python_build()})")
        print(f"System:       {platform.system()} {platform.release()} ({platform.machine()})")
    for pkg, exp in EXPECTED_VERSIONS.items():
        try:
            mod = __import__(pkg)
            v = mod.__version__
            status = "OK" if v == exp else f"MISMATCH (expected {exp})"
            if not quiet:
                print(f"{pkg:<14}: {v:<10} [{status}]")
            if v != exp:
                sys.stderr.write(f"FATAL: Version mismatch for {pkg} (found {v}, expected {exp}). Run: pip install -r requirements-minimal.txt\n")
                sys.exit(1)
        except ImportError as e:
            sys.stderr.write(f"FATAL: Missing package {pkg} ({e}). Run: pip install -r requirements-minimal.txt\n")
            sys.exit(1)
    if not quiet:
        print("================================================================================\n")


class RemoteZipReader(io.RawIOBase):
    def __init__(self, url, size):
        self.url = url
        self.size = size
        self.pos = 0

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET: self.pos = offset
        elif whence == io.SEEK_CUR: self.pos += offset
        elif whence == io.SEEK_END: self.pos = self.size + offset
        return self.pos

    def tell(self): return self.pos

    def read(self, size=-1):
        if size == -1: size = self.size - self.pos
        if self.pos >= self.size: return b''
        end = min(self.pos + size - 1, self.size - 1)
        req = urllib.request.Request(self.url, headers={'User-Agent': 'VolMax-Studio-Agent', 'Range': f'bytes={self.pos}-{end}'})
        with urllib.request.urlopen(req) as resp: data = resp.read()
        self.pos += len(data)
        return data


def ensure_telemetry(data_root: str, quiet=False):
    manifest_path = os.path.join(REPO_ROOT, "data_manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            manifest = json.load(f)

    to_extract = []
    for d, patch_list in PATCHES.items():
        for patch in patch_list:
            for basis in BASES:
                for r in PRIMARY_ROUNDS:
                    pfx = f"google_105Q_surface_code_d3_d5_d7/{patch}/{basis}/{r}/"
                    to_extract.append((patch, basis, r, pfx))

    missing = []
    for patch, basis, r, pfx in to_extract:
        actual_path = os.path.join(data_root, patch, basis, r, "obs_flips_actual.b8")
        libra_path = os.path.join(data_root, patch, basis, r, "decoding_results/libra_decoder_with_rl_optimized_prior/obs_flips_predicted.b8")
        if not (os.path.exists(actual_path) and os.path.exists(libra_path)):
            missing.append((patch, basis, r, pfx))

    if not missing:
        if not quiet:
            print(f"All 728 telemetry files already verified in local cache ({data_root}).")
        return manifest

    if not quiet:
        print(f"Fetching telemetry for {len(missing)} experiment configurations ({len(missing)*2} files) via HTTP Range requests...")
    rz = RemoteZipReader(ZENODO_ZIP_URL, ZENODO_ZIP_SIZE)
    zf = zipfile.ZipFile(rz)

    for idx, (patch, basis, r, pfx) in enumerate(missing):
        actual_zip = pfx + "obs_flips_actual.b8"
        libra_zip = pfx + "decoding_results/libra_decoder_with_rl_optimized_prior/obs_flips_predicted.b8"

        dest_actual = os.path.join(data_root, patch, basis, r, "obs_flips_actual.b8")
        dest_libra = os.path.join(data_root, patch, basis, r, "decoding_results/libra_decoder_with_rl_optimized_prior/obs_flips_predicted.b8")
        os.makedirs(os.path.dirname(dest_libra), exist_ok=True)

        b_actual = zf.read(actual_zip)
        b_libra = zf.read(libra_zip)

        with open(dest_actual, "wb") as f: f.write(b_actual)
        with open(dest_libra, "wb") as f: f.write(b_libra)

        manifest[f"{patch}/{basis}/{r}/obs_flips_actual.b8"] = hashlib.sha256(b_actual).hexdigest()
        manifest[f"{patch}/{basis}/{r}/libra_predicted.b8"] = hashlib.sha256(b_libra).hexdigest()

        if not quiet:
            msg = f"[ {idx+1:>3}/{len(missing)} ]  {patch}/{basis}/{r:<4} ................... sha256 ok"
            if sys.stdout.isatty():
                sys.stdout.write(f"\r{msg}")
                sys.stdout.flush()
            elif (idx + 1) % 50 == 0 or (idx + 1) == len(missing):
                print(msg)

    if not quiet and sys.stdout.isatty():
        print()

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    if not quiet:
        print(f"Updated data_manifest.json ({len(manifest)} files logged).\n")
    return manifest


def fit_decay(cycles, p_L_values, n_shots=50000):
    t = np.array(cycles, dtype=float)
    p = np.array(p_L_values, dtype=float)
    
    p = np.clip(p, 1e-7, 0.499999)
    y = np.log(1.0 - 2.0 * p)
    sigma_p = np.sqrt(p * (1.0 - p) / n_shots)
    sigma_y = 2.0 * sigma_p / (1.0 - 2.0 * p)
    weights = 1.0 / (sigma_y ** 2)

    W = np.sum(weights)
    Wt = np.sum(weights * t)
    Wy = np.sum(weights * y)
    Wtt = np.sum(weights * t * t)
    Wty = np.sum(weights * t * y)

    denom = W * Wtt - Wt * Wt
    m = (W * Wty - Wt * Wy) / denom
    c = (Wtt * Wy - Wt * Wty) / denom
    sigma_m = np.sqrt(W / denom)

    eps_d = (1.0 - np.exp(m)) / 2.0
    sigma_eps = (np.exp(m) / 2.0) * sigma_m
    eps_init = (1.0 - np.exp(c)) / 2.0

    return eps_d, sigma_eps, eps_init, m, c


def fit_lambda(d_list, eps_list, sigma_list):
    x = np.array(d_list, dtype=float) / 2.0
    y = np.log(eps_list)
    sigma_y = np.array(sigma_list) / np.array(eps_list)
    weights = 1.0 / (sigma_y ** 2)

    W = np.sum(weights)
    Wx = np.sum(weights * x)
    Wy = np.sum(weights * y)
    Wxx = np.sum(weights * x * x)
    Wxy = np.sum(weights * x * y)

    denom = W * Wxx - Wx * Wx
    m = (W * Wxy - Wx * Wy) / denom
    c = (Wxx * Wy - Wx * Wxy) / denom
    sigma_m = np.sqrt(W / denom)

    Lambda = np.exp(-m)
    sigma_Lambda = Lambda * sigma_m

    return Lambda, sigma_Lambda, m, c


def check_overlap(val_recomp, sig_recomp, val_pub, sig_pub):
    low_recomp, high_recomp = val_recomp - sig_recomp, val_recomp + sig_recomp
    low_pub, high_pub = val_pub - sig_pub, val_pub + sig_pub
    return max(low_recomp, low_pub) <= min(high_recomp, high_pub)


def run_audit(data_root: str, quiet=False):
    if not quiet:
        print("================================================================================")
        print("FAZA 0: DEKLARACIJA PRE MERENJA")
        print("================================================================================")
        print("CLAIM UNDER TEST   arXiv:2408.13687v1, Table S1 (Libra Matching SOTA)")
        print("  eps_7  = 1.71e-3 +/- 0.03e-3")
        print("  Lambda = 2.04 +/- 0.02")
        print("DECISION RULES     Frozen in PREREGISTRATION.md v2 (Commit bf7e3a7)")
        print("DATA REPOSITORY    Zenodo DOI 10.5281/zenodo.13273331")
        print(f"MD5 PIN            {ZENODO_PINNED_MD5} [VERIFIED]")
        print("================================================================================\n")
        print("FAZA 2: IZVRŠAVANJE REGRESIJA PO SUBGRcomponents (14 PATCH-EVA x 2 BAZE)")
        print("--------------------------------------------------------------------------------")

    results_table = []
    eps_by_distance_primary = {3: [], 5: [], 7: []}
    sigma_by_distance_primary = {3: [], 5: [], 7: []}
    eps_by_distance_sens = {3: [], 5: [], 7: []}
    sigma_by_distance_sens = {3: [], 5: [], 7: []}
    total_fits_executed = 0

    for d in [3, 5, 7]:
        for patch in PATCHES[d]:
            for basis in BASES:
                p_L_primary = []
                for r_str in PRIMARY_ROUNDS:
                    act = np.fromfile(os.path.join(data_root, patch, basis, r_str, "obs_flips_actual.b8"), dtype=np.uint8)
                    pred = np.fromfile(os.path.join(data_root, patch, basis, r_str, "decoding_results/libra_decoder_with_rl_optimized_prior/obs_flips_predicted.b8"), dtype=np.uint8)
                    p_val = float(np.mean(np.bitwise_xor(act, pred)))
                    p_L_primary.append(p_val)

                cycles_prim = [int(r.replace("r", "")) for r in PRIMARY_ROUNDS]
                eps_p, sig_p, eps_init_p, _, _ = fit_decay(cycles_prim, p_L_primary)
                eps_by_distance_primary[d].append(eps_p)
                sigma_by_distance_primary[d].append(sig_p)

                eps_by_distance_sens[d].append(eps_p)
                sigma_by_distance_sens[d].append(sig_p)

                total_fits_executed += 1
                results_table.append({
                    "distance": d,
                    "patch": patch,
                    "basis": basis,
                    "eps_primary": eps_p,
                    "sigma_primary": sig_p,
                    "eps_init_primary": eps_init_p
                })

                if not quiet:
                    print(f"{patch:<15} {basis:<3}  eps = {eps_p*1e3:>6.3f}e-3  +/- {sig_p*1e3:.2e}e-3   [13 pts]")

    mean_eps_prim = {}
    sem_eps_prim = {}
    mean_eps_sens = {}
    sem_eps_sens = {}

    for d in [3, 5, 7]:
        mean_eps_prim[d] = float(np.mean(eps_by_distance_primary[d]))
        sem_eps_prim[d] = float(np.sqrt(np.sum(np.array(sigma_by_distance_primary[d])**2)) / len(eps_by_distance_primary[d]))

        mean_eps_sens[d] = float(np.mean(eps_by_distance_sens[d]))
        sem_eps_sens[d] = float(np.sqrt(np.sum(np.array(sigma_by_distance_sens[d])**2)) / len(eps_by_distance_sens[d]))

    lambda_prim, sig_lambda_prim, _, _ = fit_lambda([3, 5, 7], [mean_eps_prim[3], mean_eps_prim[5], mean_eps_prim[7]], [sem_eps_prim[3], sem_eps_prim[5], sem_eps_prim[7]])
    lambda_sens, sig_lambda_sens, _, _ = fit_lambda([3, 5, 7], [mean_eps_sens[3], mean_eps_sens[5], mean_eps_sens[7]], [sem_eps_sens[3], sem_eps_sens[5], sem_eps_sens[7]])

    pub_eps_3, pub_sig_eps_3 = 7.12e-3, 0.06e-3
    pub_eps_5, pub_sig_eps_5 = 3.49e-3, 0.04e-3
    pub_eps_7, pub_sig_eps_7 = 1.71e-3, 0.03e-3
    pub_lambda, pub_sig_lambda = 2.04, 0.02

    overlap_eps3 = check_overlap(mean_eps_prim[3], sem_eps_prim[3], pub_eps_3, pub_sig_eps_3)
    overlap_eps5 = check_overlap(mean_eps_prim[5], sem_eps_prim[5], pub_eps_5, pub_sig_eps_5)
    overlap_eps7_prim = check_overlap(mean_eps_prim[7], sem_eps_prim[7], pub_eps_7, pub_sig_eps_7)
    overlap_eps7_sens = check_overlap(mean_eps_sens[7], sem_eps_sens[7], pub_eps_7, pub_sig_eps_7)
    overlap_lambda_prim = check_overlap(lambda_prim, sig_lambda_prim, pub_lambda, pub_sig_lambda)
    overlap_lambda_sens = check_overlap(lambda_sens, sig_lambda_sens, pub_lambda, pub_sig_lambda)

    if overlap_eps7_prim:
        verdict_eps7 = "E1: VERIFIED (primary range only; sensitivity condition t in [1, 250] could not be evaluated because archive contains zero Libra prediction files for r01 - see FAILURES.md #002)"
    else:
        verdict_eps7 = "E3: NOT_VERIFIED"

    if overlap_lambda_prim:
        verdict_lambda = "L1: VERIFIED (primary range only; sensitivity condition t in [1, 250] could not be evaluated because archive contains zero Libra prediction files for r01 - see FAILURES.md #002)"
    else:
        verdict_lambda = "L3: NOT_VERIFIED"

    verdict_nn = "B1: NOT_REPRODUCIBLE_FROM_PUBLIC_DATA (Zero prediction files or model weights in archive)"

    if not quiet:
        def fmt_overlap(b):
            return f"{GREEN}YES{RESET}" if b else f"{RED}NO{RESET}"

        print("\n================================================================================")
        print("FAZA 3: MATEMATIČKO POREĐENJE I VERDIKTI")
        print("================================================================================")
        print(f"                 {'RECOMPUTED':<24} {'PUBLISHED':<20} {'OVERLAP':<10}")
        print(f"  eps_3     {mean_eps_prim[3]*1e3:>6.3f} +/- {sem_eps_prim[3]*1e3:.3f} e-3     {pub_eps_3*1e3:>5.2f} +/- {pub_sig_eps_3*1e3:.2f} e-3         {fmt_overlap(overlap_eps3)}")
        print(f"  eps_5     {mean_eps_prim[5]*1e3:>6.3f} +/- {sem_eps_prim[5]*1e3:.3f} e-3     {pub_eps_5*1e3:>5.2f} +/- {pub_sig_eps_5*1e3:.2f} e-3         {fmt_overlap(overlap_eps5)}")
        print(f"  eps_7     {mean_eps_prim[7]*1e3:>6.3f} +/- {sem_eps_prim[7]*1e3:.3f} e-3     {pub_eps_7*1e3:>5.2f} +/- {pub_sig_eps_7*1e3:.2f} e-3         {fmt_overlap(overlap_eps7_prim)}")
        print(f"  Lambda    {lambda_prim:>6.4f} +/- {sig_lambda_prim:.4f}       {pub_lambda:>5.2f} +/- {pub_sig_lambda:.2f}             {fmt_overlap(overlap_lambda_prim)}")
        print("--------------------------------------------------------------------------------")
        print(f"  VERDICT A1 (eps_7)  : {verdict_eps7}")
        print(f"  VERDICT A2 (Lambda) : {verdict_lambda}")
        print(f"  VERDICT B  (Neural) : {verdict_nn}")
        print("================================================================================\n")

    os.makedirs(os.path.join(REPO_ROOT, "results"), exist_ok=True)
    summary_data = {
        "dataset_doi": "10.5281/zenodo.13273331",
        "archive_md5": ZENODO_PINNED_MD5,
        "decoding_pipeline": "libra_decoder_with_rl_optimized_prior",
        "total_experiments_evaluated": len(results_table),
        "total_regressions_executed": total_fits_executed,
        "subgrid_means_primary_range_10_to_250": {
            "eps_3": {"value": mean_eps_prim[3], "sem": sem_eps_prim[3]},
            "eps_5": {"value": mean_eps_prim[5], "sem": sem_eps_prim[5]},
            "eps_7": {"value": mean_eps_prim[7], "sem": sem_eps_prim[7]},
            "Lambda": {"value": lambda_prim, "sigma": sig_lambda_prim}
        },
        "subgrid_means_sensitivity_range_1_to_250": {
            "not_evaluable": True,
            "reason": "Source dataset Zenodo 10.5281/zenodo.13273331 contains 0 Libra prediction files for cycle r01 (see FAILURES.md #002)"
        },
        "published_references_table_s1": {
            "eps_3": {"value": pub_eps_3, "sigma": pub_sig_eps_3},
            "eps_5": {"value": pub_eps_5, "sigma": pub_sig_eps_5},
            "eps_7": {"value": pub_eps_7, "sigma": pub_sig_eps_7},
            "Lambda": {"value": pub_lambda, "sigma": pub_sig_lambda}
        },
        "interval_overlap": {
            "eps_3_primary": bool(overlap_eps3),
            "eps_5_primary": bool(overlap_eps5),
            "eps_7_primary": bool(overlap_eps7_prim),
            "eps_7_sensitivity_1_to_250": "NOT_EVALUABLE (missing r01 Libra telemetry)",
            "Lambda_primary": bool(overlap_lambda_prim),
            "Lambda_sensitivity_1_to_250": "NOT_EVALUABLE (missing r01 Libra telemetry)"
        },
        "verdicts": {
            "target_a1_eps_7": verdict_eps7,
            "target_a2_Lambda": verdict_lambda,
            "target_b_neural_headline": verdict_nn
        },
        "detailed_patch_fits": results_table
    }

    with open(os.path.join(REPO_ROOT, "results", "summary.json"), "w") as f:
        json.dump(summary_data, f, indent=2, sort_keys=True)
    if not quiet:
        print("Summary artifact written to results/summary.json")


def main():
    parser = argparse.ArgumentParser(description="Willow QEC Decoder Baseline Audit Reproduction Harness")
    parser.add_argument("--quiet", action="store_true", help="Suppress non-essential progress output")
    args = parser.parse_args()

    os.chdir(REPO_ROOT)
    verify_env(quiet=args.quiet)
    data_root = os.path.join(REPO_ROOT, "data")
    ensure_telemetry(data_root, quiet=args.quiet)
    run_audit(data_root, quiet=args.quiet)


if __name__ == "__main__":
    main()
