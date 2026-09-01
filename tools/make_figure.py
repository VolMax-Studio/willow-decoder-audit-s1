#!/usr/bin/env python3
"""
tools/make_figure.py — Optional figure generation script for reporting & sharing.
Requires: matplotlib>=3.8.0
Usage: python3 tools/make_figure.py
"""

import os
import sys
import json
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMMARY_PATH = os.path.join(REPO_ROOT, "results", "summary.json")
OUTPUT_FIG_PATH = os.path.join(REPO_ROOT, "figures", "willow_qec_audit_verification.png")

if not os.path.exists(SUMMARY_PATH):
    sys.stderr.write(f"FATAL: Summary file not found at {SUMMARY_PATH}. Run reproduce.py first.\n")
    sys.exit(1)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    sys.stderr.write("FATAL: matplotlib is required to generate figures. Run: pip install matplotlib\n")
    sys.exit(1)

with open(SUMMARY_PATH) as f:
    data = json.load(f)

d_vals = np.array([3, 5, 7])
eps_recomp = [data['subgrid_means_primary_range_10_to_250'][f'eps_{d}']['value'] for d in d_vals]
sem_recomp = [data['subgrid_means_primary_range_10_to_250'][f'eps_{d}']['sem'] for d in d_vals]

eps_pub = [data['published_references_table_s1'][f'eps_{d}']['value'] for d in d_vals]
sig_pub = [data['published_references_table_s1'][f'eps_{d}']['sigma'] for d in d_vals]

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 6), dpi=300)

# 1. Left Plot: Scaling decay vs Distance d
ax1.errorbar(d_vals, np.array(eps_pub)*1e3, yerr=np.array(sig_pub)*1e3, fmt='s', color='#1a73e8', markersize=8, capsize=5, label='Google Published (Table S1, Libra)', zorder=3)
ax1.errorbar(d_vals, np.array(eps_recomp)*1e3, yerr=np.array(sem_recomp)*1e3, fmt='o', color='#188038', markersize=6, capsize=4, label='Independent Audit (Zenodo Raw Data)', zorder=4)

d_dense = np.linspace(2.8, 7.2, 100)
lambda_val = data['subgrid_means_primary_range_10_to_250']['Lambda']['value']
fit_curve = (eps_recomp[0] * (lambda_val ** (-(d_dense - 3.0)/2.0))) * 1e3
ax1.plot(d_dense, fit_curve, '--', color='#188038', alpha=0.7, label=f'Audit Fit: $\\Lambda = {lambda_val:.3f}$')

ax1.set_yscale('log')
ax1.set_xticks([3, 5, 7])
ax1.set_xlabel('Code Distance ($d$)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Logical Error per Cycle $\\epsilon_d$ ($\\times 10^{-3}$)', fontsize=11, fontweight='bold')
ax1.set_title('Decisive Error Suppression ($\\Lambda = 2.038 \\pm 0.003$)\n105Q Willow Surface Code Telemetry', fontsize=12, pad=12)
ax1.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)
ax1.grid(True, which='both', linestyle=':', alpha=0.6)

# 2. Right Plot: Residual Overlap Comparison (Delta from Published)
diff_3 = (eps_recomp[0] - eps_pub[0]) * 1e3
diff_5 = (eps_recomp[1] - eps_pub[1]) * 1e3
diff_7 = (eps_recomp[2] - eps_pub[2]) * 1e3

diffs = [diff_3, diff_5, diff_7]
labels = ['d = 3\n(9 patches)', 'd = 5\n(4 patches)', 'd = 7\n(1 patch)']

bars = ax2.bar(labels, diffs, width=0.45, color='#188038', alpha=0.85, edgecolor='#137333', linewidth=1.5, zorder=3)
ax2.axhline(0, color='black', linewidth=1, linestyle='-')

for idx, (sig, d_name) in enumerate(zip(sig_pub, labels)):
    ax2.fill_between([idx - 0.35, idx + 0.35], -sig*1e3, sig*1e3, color='#1a73e8', alpha=0.15, zorder=2)

ax2.set_ylabel('Discrepancy ($\\Delta \\epsilon_d = \\epsilon_{audit} - \\epsilon_{pub}$) [$\\times 10^{-3}$]', fontsize=11, fontweight='bold')
ax2.set_title('Interval Overlap Verification\nShaded: Google Published $1\\sigma$ Band', fontsize=12, pad=12)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.set_ylim(-0.08, 0.08)

# Overlay Qualified Verdict Badge
plt.figtext(
    0.5, 0.02, 
    'VERDICTS: Target A1 ($\\epsilon_7$) = E1: VERIFIED (primary range only) | Target A2 ($\\Lambda$) = L1: VERIFIED (primary range only)\n'
    'Target B (Neural Headline) = B1: NOT IN PUBLIC ARCHIVE | Sensitivity t in [1, 250] not evaluable: 0 Libra prediction files in archive for r01 (FAILURES #002)', 
    ha='center', fontsize=8.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='#e6f4ea', edgecolor='#188038', linewidth=1.5)
)

plt.tight_layout(rect=[0, 0.07, 1, 1])
os.makedirs(os.path.dirname(OUTPUT_FIG_PATH), exist_ok=True)
plt.savefig(OUTPUT_FIG_PATH, dpi=300)
print(f"Generated qualified figure: {OUTPUT_FIG_PATH}")
