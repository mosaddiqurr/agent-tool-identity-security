import math
from pathlib import Path

import pandas as pd
from scipy.stats import fisher_exact


ROOT = Path(__file__).resolve().parent.parent

INPUT = (
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

df = pd.read_csv(INPUT)


def is_unauthorized(value):
    return (
        value
        == "UNAUTHORIZED_TOOL_SELECTED"
    )


df["unauthorized"] = (
    df["result_label"]
    .apply(is_unauthorized)
)


def wilson_interval(k, n, z=1.96):

    if n == 0:
        return 0.0, 0.0

    p = k / n

    denominator = (
        1
        + (z * z / n)
    )

    centre = (
        p
        + (z * z / (2 * n))
    ) / denominator

    margin = (
        z
        * math.sqrt(
            (p * (1 - p) / n)
            + (
                z * z
                / (4 * n * n)
            )
        )
        / denominator
    )

    return (
        centre - margin,
        centre + margin
    )


# -------------------------------------------------
# Summary by condition
# -------------------------------------------------

condition_rows = []

for condition, group in df.groupby(
    "condition"
):

    total = len(group)

    unauthorized = int(
        group["unauthorized"].sum()
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

    rate = unauthorized / total

    low, high = wilson_interval(
        unauthorized,
        total
    )

    condition_rows.append(
        {
            "condition":
                condition,

            "trials":
                total,

            "authorized":
                authorized,

            "unauthorized":
                unauthorized,

            "no_tool":
                no_tool,

            "unauthorized_rate":
                rate,

            "ci95_low":
                low,

            "ci95_high":
                high
        }
    )


condition_summary = pd.DataFrame(
    condition_rows
)

condition_summary.to_csv(
    OUTPUT_DIR
    / "summary_by_condition.csv",
    index=False
)


# -------------------------------------------------
# Summary by condition + message class
# -------------------------------------------------

class_summary = (
    df.groupby(
        [
            "condition",
            "message_class"
        ]
    )
    .agg(
        trials=(
            "unauthorized",
            "size"
        ),

        unauthorized=(
            "unauthorized",
            "sum"
        )
    )
    .reset_index()
)

class_summary[
    "unauthorized_rate"
] = (
    class_summary["unauthorized"]
    / class_summary["trials"]
)

class_summary.to_csv(
    OUTPUT_DIR
    / "summary_by_message_class.csv",
    index=False
)


# -------------------------------------------------
# Summary by condition + tool order
# -------------------------------------------------

order_summary = (
    df.groupby(
        [
            "condition",
            "tool_order"
        ]
    )
    .agg(
        trials=(
            "unauthorized",
            "size"
        ),

        unauthorized=(
            "unauthorized",
            "sum"
        )
    )
    .reset_index()
)

order_summary[
    "unauthorized_rate"
] = (
    order_summary["unauthorized"]
    / order_summary["trials"]
)

order_summary.to_csv(
    OUTPUT_DIR
    / "summary_by_tool_order.csv",
    index=False
)


# -------------------------------------------------
# Fisher exact tests
# -------------------------------------------------

counts = {}

for _, row in condition_summary.iterrows():

    counts[
        row["condition"]
    ] = (
        int(row["unauthorized"]),
        int(
            row["trials"]
            - row["unauthorized"]
        )
    )


comparisons = [
    (
        "C1_name_similarity",
        "C0_control"
    ),
    (
        "C2_metadata_deception",
        "C0_control"
    ),
    (
        "C3_combined",
        "C0_control"
    ),
    (
        "C3_combined",
        "C2_metadata_deception"
    )
]


test_rows = []

for a, b in comparisons:

    a_bad, a_good = counts[a]
    b_bad, b_good = counts[b]

    table = [
        [a_bad, a_good],
        [b_bad, b_good]
    ]

    odds_ratio, p_value = (
        fisher_exact(
            table,
            alternative="two-sided"
        )
    )

    test_rows.append(
        {
            "comparison":
                f"{a} vs {b}",

            "odds_ratio":
                odds_ratio,

            "p_value":
                p_value
        }
    )


tests = pd.DataFrame(
    test_rows
)

tests.to_csv(
    OUTPUT_DIR
    / "fisher_exact_tests.csv",
    index=False
)


# -------------------------------------------------
# Print results
# -------------------------------------------------

print()
print("=" * 70)
print("CONDITION SUMMARY")
print("=" * 70)

print(
    condition_summary.to_string(
        index=False
    )
)

print()
print("=" * 70)
print("MESSAGE CLASS SUMMARY")
print("=" * 70)

print(
    class_summary.to_string(
        index=False
    )
)

print()
print("=" * 70)
print("TOOL ORDER SUMMARY")
print("=" * 70)

print(
    order_summary.to_string(
        index=False
    )
)

print()
print("=" * 70)
print("FISHER EXACT TESTS")
print("=" * 70)

print(
    tests.to_string(
        index=False
    )
)
