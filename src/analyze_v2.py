import math
from pathlib import Path

import pandas as pd
from scipy.stats import binomtest


ROOT = Path(__file__).resolve().parent.parent

INPUT = (
    ROOT
    / "results"
    / "processed"
    / "v2_trials_nothink.csv"
)

OUTPUT = (
    ROOT
    / "results"
    / "processed"
)

df = pd.read_csv(INPUT)

df["unauthorized"] = (
    df["result_label"]
    == "UNAUTHORIZED_TOOL_SELECTED"
)


def wilson_interval(k, n, z=1.96):

    if n == 0:
        return 0.0, 0.0

    p = k / n

    denominator = (
        1 + z**2 / n
    )

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


# -------------------------------------------------
# Summary by condition
# -------------------------------------------------

summary_rows = []

for condition, group in df.groupby("condition"):

    n = len(group)

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

    rate = unauthorized / n

    low, high = wilson_interval(
        unauthorized,
        n
    )

    summary_rows.append(
        {
            "condition": condition,
            "trials": n,
            "authorized": authorized,
            "unauthorized": unauthorized,
            "no_tool": no_tool,
            "unauthorized_rate": rate,
            "ci95_low": low,
            "ci95_high": high
        }
    )


summary = pd.DataFrame(
    summary_rows
)

summary.to_csv(
    OUTPUT / "v2_summary_by_condition.csv",
    index=False
)


# -------------------------------------------------
# Summary by message class
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

class_summary["unauthorized_rate"] = (
    class_summary["unauthorized"]
    / class_summary["trials"]
)

class_summary.to_csv(
    OUTPUT
    / "v2_summary_by_message_class.csv",
    index=False
)


# -------------------------------------------------
# Summary by tool order
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

order_summary["unauthorized_rate"] = (
    order_summary["unauthorized"]
    / order_summary["trials"]
)

order_summary.to_csv(
    OUTPUT
    / "v2_summary_by_tool_order.csv",
    index=False
)


# -------------------------------------------------
# Paired exact tests
# -------------------------------------------------

pivot = (
    df.pivot(
        index="scenario_id",
        columns="condition",
        values="unauthorized"
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


paired_rows = []


for a, b in comparisons:

    pair = pivot[
        [a, b]
    ].dropna()

    a_only = int(
        (
            (pair[a] == True)
            &
            (pair[b] == False)
        ).sum()
    )

    b_only = int(
        (
            (pair[a] == False)
            &
            (pair[b] == True)
        ).sum()
    )

    discordant = (
        a_only + b_only
    )

    if discordant == 0:

        p_value = 1.0

    else:

        smaller = min(
            a_only,
            b_only
        )

        p_value = binomtest(
            smaller,
            discordant,
            p=0.5,
            alternative="two-sided"
        ).pvalue


    paired_rows.append(
        {
            "comparison":
                f"{a} vs {b}",

            "a_only_failures":
                a_only,

            "b_only_failures":
                b_only,

            "discordant_pairs":
                discordant,

            "mcnemar_exact_p":
                p_value
        }
    )


paired_tests = pd.DataFrame(
    paired_rows
)

paired_tests.to_csv(
    OUTPUT
    / "v2_paired_tests.csv",
    index=False
)


# -------------------------------------------------
# Print results
# -------------------------------------------------

print()
print("=" * 72)
print("V2 CONDITION SUMMARY")
print("=" * 72)

print(
    summary.to_string(
        index=False
    )
)

print()
print("=" * 72)
print("MESSAGE CLASS SUMMARY")
print("=" * 72)

print(
    class_summary.to_string(
        index=False
    )
)

print()
print("=" * 72)
print("TOOL ORDER SUMMARY")
print("=" * 72)

print(
    order_summary.to_string(
        index=False
    )
)

print()
print("=" * 72)
print("PAIRED EXACT TESTS")
print("=" * 72)

print(
    paired_tests.to_string(
        index=False
    )
)
