#!/usr/bin/env python3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/charts"
OUT.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=220, bbox_inches="tight")
    plt.close(fig)


# 1. Cross-stage overall unauthorized-selection rate with Wilson intervals.
stage = pd.read_csv(ROOT / "results/processed/cross_stage_summary.csv")
labels = ["V1\npreliminary", "V2\nexplicit policy", "MCP-backed\nvalidation"]
rates = stage["unauthorized_rate"].to_numpy() * 100
low = stage["ci95_low"].to_numpy() * 100
high = stage["ci95_high"].to_numpy() * 100
err = np.vstack([rates - low, high - rates])

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels, rates, yerr=err, capsize=6)
ax.set_ylabel("Unauthorized tool selections (%)")
ax.set_title("Unauthorized tool selection across experimental stages")
ax.set_ylim(0, max(high) * 1.25)
ax.grid(axis="y", alpha=0.25)
for bar, rate, n in zip(bars, rates, stage["trials"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        max(rate, 0) + 0.8,
        f"{rate:.1f}%\n(n={n})",
        ha="center",
        va="bottom",
        fontsize=10,
    )
fig.text(
    0.5,
    0.015,
    "Error bars: 95% Wilson confidence intervals. V1 used an ambiguous authorization policy, so cross-stage differences are descriptive rather than a causal estimate.",
    ha="center",
    fontsize=9,
)
fig.tight_layout(rect=(0, 0.06, 1, 1))
save(fig, "cross_stage_unauthorized_rate")


# 2. V1 vs V2 observed rates by condition.
v1 = pd.read_csv(ROOT / "results/processed/summary_by_condition.csv").set_index("condition")
v2 = pd.read_csv(ROOT / "results/processed/v2_summary_by_condition.csv").set_index("condition")
conditions = ["C0_control", "C1_name_similarity", "C2_metadata_deception", "C3_combined"]
condition_labels = ["Control", "Name similarity", "Metadata deception", "Combined"]
v1_rates = np.array([v1.loc[c, "unauthorized_rate"] * 100 for c in conditions])
v2_rates = np.array([v2.loc[c, "unauthorized_rate"] * 100 for c in conditions])
x = np.arange(len(conditions))
width = 0.36

fig, ax = plt.subplots(figsize=(11, 6))
b1 = ax.bar(x - width / 2, v1_rates, width, label="V1 preliminary")
b2 = ax.bar(x + width / 2, v2_rates, width, label="V2 explicit policy")
ax.set_xticks(x, condition_labels)
ax.set_ylabel("Unauthorized tool selections (%)")
ax.set_title("Observed unauthorized selection rate by condition")
ax.set_ylim(0, 36)
ax.grid(axis="y", alpha=0.25)
ax.legend()
for bars in (b1, b2):
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.8,
            f"{height:.1f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )
fig.text(
    0.5,
    0.015,
    "Each condition used 16 trials. V1 is retained as preliminary evidence; V2 is the clean primary tool-calling experiment.",
    ha="center",
    fontsize=9,
)
fig.tight_layout(rect=(0, 0.06, 1, 1))
save(fig, "condition_comparison_v1_v2")


# 3. Uncertainty remaining after zero observed failures.
categories = [
    "V2 overall\n0/64",
    "MCP overall\n0/24",
    "V2 per condition\n0/16",
    "MCP per condition\n0/6",
]
upper_bounds = [5.662602297115633, 13.798057582897535, 19.361341827271994, 39.03430336530645]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categories, upper_bounds)
ax.set_ylabel("Upper bound of 95% Wilson CI (%)")
ax.set_title("Zero observed failures still leave statistical uncertainty")
ax.set_ylim(0, 45)
ax.grid(axis="y", alpha=0.25)
for bar, upper in zip(bars, upper_bounds):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        upper + 0.8,
        f"{upper:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10,
    )
fig.text(
    0.5,
    0.015,
    "The bars show the upper 95% confidence bound on the true unauthorized-selection rate when no failures were observed.",
    ha="center",
    fontsize=9,
)
fig.tight_layout(rect=(0, 0.06, 1, 1))
save(fig, "zero_failure_uncertainty")

print(f"Charts written to {OUT}")
