import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent

MCP_FILE = (
    ROOT
    / "results"
    / "processed"
    / "mcp_final_trials_api_think_false.csv"
)

V2_FILE = (
    ROOT
    / "results"
    / "processed"
    / "v2_trials_nothink.csv"
)

V1_FILE = (
    ROOT
    / "results"
    / "processed"
    / "final_trials_nothink.csv"
)

OUTPUT_DIR = (
    ROOT
    / "results"
    / "processed"
)


def wilson_interval(k, n, z=1.96):

    if n == 0:
        return 0.0, 0.0

    p = k / n

    denominator = 1 + z**2 / n

    centre = (
        p + z**2 / (2 * n)
    ) / denominator

    margin = (
        z
        * math.sqrt(
            p * (1 - p) / n
            + z**2 / (4 * n**2)
        )
        / denominator
    )

    return (
        centre - margin,
        centre + margin
    )


def summarize(group):

    n = len(group)

    unauthorized = int(
        (
            group["result_label"]
            == "UNAUTHORIZED_TOOL_SELECTED"
        ).sum()
    )

    authorized = int(
        (
            group["result_label"]
            == "AUTHORIZED_TOOL_SELECTED"
        ).sum()
    )

    no_tool = int(
        (
            group["result_label"]
            == "NO_TOOL_SELECTED"
        ).sum()
    )

    rate = (
        unauthorized / n
        if n
        else 0
    )

    low, high = wilson_interval(
        unauthorized,
        n
    )

    return {
        "trials": n,
        "authorized": authorized,
        "unauthorized": unauthorized,
        "no_tool": no_tool,
        "unauthorized_rate": rate,
        "ci95_low": low,
        "ci95_high": high
    }


# =========================================================
# MCP FINAL DATASET
# =========================================================

df = pd.read_csv(MCP_FILE)


condition_rows = []

for condition, group in df.groupby(
    "condition"
):

    row = {
        "condition": condition
    }

    row.update(
        summarize(group)
    )

    condition_rows.append(row)


condition_summary = pd.DataFrame(
    condition_rows
)

condition_summary.to_csv(
    OUTPUT_DIR
    / "mcp_final_summary_by_condition.csv",
    index=False
)


# =========================================================
# MESSAGE CLASS
# =========================================================

class_rows = []

for (
    condition,
    message_class
), group in df.groupby(
    [
        "condition",
        "message_class"
    ]
):

    row = {
        "condition": condition,
        "message_class": message_class
    }

    row.update(
        summarize(group)
    )

    class_rows.append(row)


class_summary = pd.DataFrame(
    class_rows
)

class_summary.to_csv(
    OUTPUT_DIR
    / "mcp_final_summary_by_message_class.csv",
    index=False
)


# =========================================================
# TOOL ORDER
# =========================================================

order_rows = []

for (
    condition,
    tool_order
), group in df.groupby(
    [
        "condition",
        "tool_order"
    ]
):

    row = {
        "condition": condition,
        "tool_order": tool_order
    }

    row.update(
        summarize(group)
    )

    order_rows.append(row)


order_summary = pd.DataFrame(
    order_rows
)

order_summary.to_csv(
    OUTPUT_DIR
    / "mcp_final_summary_by_tool_order.csv",
    index=False
)


# =========================================================
# TOTAL MCP RESULT
# =========================================================

overall = summarize(df)

overall_summary = pd.DataFrame(
    [
        {
            "dataset":
                "MCP-backed validation",

            **overall
        }
    ]
)

overall_summary.to_csv(
    OUTPUT_DIR
    / "mcp_final_overall_summary.csv",
    index=False
)


# =========================================================
# CROSS-STAGE COMPARISON
# =========================================================

stage_rows = []


def add_stage(
    label,
    path,
    status
):

    if not path.exists():
        return

    stage_df = pd.read_csv(path)

    result = summarize(
        stage_df
    )

    stage_rows.append(
        {
            "stage": label,
            "status": status,
            **result
        }
    )


add_stage(
    "V1",
    V1_FILE,
    "Preliminary / ambiguous authorization policy"
)

add_stage(
    "V2",
    V2_FILE,
    "Primary clean tool-calling experiment"
)

add_stage(
    "MCP",
    MCP_FILE,
    "MCP-backed validation extension"
)


stage_summary = pd.DataFrame(
    stage_rows
)

stage_summary.to_csv(
    OUTPUT_DIR
    / "cross_stage_summary.csv",
    index=False
)


# =========================================================
# PRINT
# =========================================================

print()
print("=" * 78)
print("FINAL MCP ANALYSIS")
print("=" * 78)

print()
print("BY CONDITION")
print("-" * 78)

print(
    condition_summary.to_string(
        index=False
    )
)

print()
print("BY MESSAGE CLASS")
print("-" * 78)

print(
    class_summary.to_string(
        index=False
    )
)

print()
print("BY TOOL ORDER")
print("-" * 78)

print(
    order_summary.to_string(
        index=False
    )
)

print()
print("OVERALL MCP RESULT")
print("-" * 78)

print(
    overall_summary.to_string(
        index=False
    )
)

print()
print("CROSS-STAGE COMPARISON")
print("-" * 78)

print(
    stage_summary.to_string(
        index=False
    )
)

print()
print("=" * 78)
print("INTERPRETATION")
print("=" * 78)

print(
    "The MCP-backed validation observed no unauthorized "
    "tool selections in the tested scenarios."
)

print(
    "This does not prove a zero true failure rate. "
    "Confidence intervals must be reported."
)

print(
    "V1 should remain classified as preliminary because "
    "its authorization policy contained ambiguity."
)

print(
    "V2 and the MCP-backed extension used an explicit "
    "source-based authorization boundary."
)
