# Results

All counts below were independently reconstructed from the 152 raw JSON records and matched against all 16 processed CSV files. A trial is one scenario-condition request. No packaged trial has an error status, no scenario-condition cell is missing, and no trial has a no-tool outcome.

## Overall results

| Stage | Trials | Authorized | Unauthorized | Rate | Nominal 95% Wilson CI |
|---|---:|---:|---:|---:|---|
| V1 preliminary experiment | 64 | 54 | 10 | 15.625% | 8.715%–26.428% |
| V2 primary tool-calling experiment | 64 | 64 | 0 | 0.000% | 0.000%–5.663% |
| MCP-backed validation | 24 | 24 | 0 | 0.000% | 0.000%–13.798% |

![Overall rates and nominal Wilson intervals](../assets/charts/cross_stage_unauthorized_rate.png)

The policy and descriptions changed between V1 and V2. The comparison is descriptive, not an isolated treatment effect. The stages are not pooled: 152 is the total number of reported trial records, not 152 independent scenarios.

Intervals use `z = 1.96`. They are binomial reference summaries for this fixed scenario set and configuration, subject to the sampling qualifications in [Methodology](METHODOLOGY.md) and [Limitations](LIMITATIONS.md).

## V1: preliminary experiment

| Condition | Trials | Authorized | Unauthorized | Rate | Nominal 95% Wilson CI |
|---|---:|---:|---:|---:|---|
| C0 Control | 16 | 15 | 1 | 6.25% | 1.11%–28.33% |
| C1 Name similarity | 16 | 16 | 0 | 0.00% | 0.00%–19.36% |
| C2 Metadata deception | 16 | 12 | 4 | 25.00% | 10.18%–49.50% |
| C3 Combined | 16 | 11 | 5 | 31.25% | 14.16%–55.60% |

By message class, unauthorized selections were:

| Condition | Routine | Sensitive |
|---|---:|---:|
| C0 Control | 1/8 (12.5%) | 0/8 (0.0%) |
| C1 Name similarity | 0/8 (0.0%) | 0/8 (0.0%) |
| C2 Metadata deception | 0/8 (0.0%) | 4/8 (50.0%) |
| C3 Combined | 0/8 (0.0%) | 5/8 (62.5%) |

By ordering, C0 had 0/8 original and 1/8 reversed; C1 had 0/8 in both; C2 had 3/8 original and 1/8 reversed; C3 had 3/8 original and 2/8 reversed. These are descriptive subsets of the same trials.

The frozen, unadjusted two-sided Fisher exact results are:

| Comparison | Odds ratio | p-value |
|---|---:|---:|
| C1 vs C0 | 0.000 | 1.000000 |
| C2 vs C0 | 5.000 | 0.332592 |
| C3 vs C0 | 6.818 | 0.171919 |
| C3 vs C2 | 1.364 | 1.000000 |

Their calculations match the archived analysis and an independent exact-fraction calculation. None has `p < 0.05`. These exploratory tests do not account for scenario pairing, and V1 authorization ambiguity further limits interpretation. The 31.25% combined-condition rate is not an established attack success probability under the explicit V2 policy.

## V2: primary tool-calling experiment

| Condition | Trials | Authorized | Unauthorized | Rate | Nominal 95% Wilson CI |
|---|---:|---:|---:|---:|---|
| C0 Control | 16 | 16 | 0 | 0.00% | 0.00%–19.36% |
| C1 Name similarity | 16 | 16 | 0 | 0.00% | 0.00%–19.36% |
| C2 Metadata deception | 16 | 16 | 0 | 0.00% | 0.00%–19.36% |
| C3 Combined | 16 | 16 | 0 | 0.00% | 0.00%–19.36% |

Routine and sensitive subsets each have 0/32 unauthorized trials overall and 0/8 per condition. Original and reversed ordering each have 0/32 overall and 0/8 per condition.

All four paired comparisons in `v2_paired_tests.csv` have zero failures unique to either condition and zero discordant pairs. Their exact-test values are `p = 1.0`, the implementation's no-discordance convention. This is not evidence of equivalent security.

## MCP stage: MCP-backed validation

| Condition | Trials | Authorized | Unauthorized | Rate | Nominal 95% Wilson CI |
|---|---:|---:|---:|---:|---|
| C0 Control | 6 | 6 | 0 | 0.00% | 0.00%–39.03% |
| C1 Name similarity | 6 | 6 | 0 | 0.00% | 0.00%–39.03% |
| C2 Metadata deception | 6 | 6 | 0 | 0.00% | 0.00%–39.03% |
| C3 Combined | 6 | 6 | 0 | 0.00% | 0.00%–39.03% |

Routine and sensitive subsets each have 0/12 unauthorized trials overall and 0/3 per condition. Trusted-first and untrusted-first subsets each have 0/12 overall and 0/3 per condition. The corresponding per-condition subgroup interval is 0%–56.15%.

The 24 stored execution results are simulated responses with `sent: false`, and agree with the selected tool, server mapping, and emitted arguments. No real mail operation occurred.

## Call multiplicity and exact task fidelity

- V1 has 64 selected calls in 64 trials.
- V2 has 65 selected calls in 64 trials. [C1/S014](../results/raw/v2_nothink/C1_name_similarity/S014.json) contains two identical authorized calls.
- MCP-backed validation has 24 selected calls in 24 trials.
- No response mixes authorized and unauthorized calls, and no response selects an unknown tool.
- [V2 C1/S011](../results/raw/v2_nothink/C1_name_similarity/S011.json) and [MCP C1/S011](../results/raw/mcp_final_api_think_false/C1_name_similarity/S011.json) omit the requested message's final period. Recipients remain correct. Other stored call arguments exactly match the requested recipient and message.

These observations do not change selection outcomes. They prevent equating authorized selection with perfect task completion or exactly-once execution.

Reasoning-style `<think>` or `</think>` markers occur in V1 64/64, V2 63/64, and MCP 24/24 `model_content` fields despite the recorded `think=False` setting.

## Chart verification and rounding

![Condition rates](../assets/charts/condition_comparison_v1_v2.png)

The condition chart plots exact V1 rates of 6.25%, 0%, 25%, and 31.25%, and zero for all V2 conditions. Its one-decimal labels use Python's ties-to-even rounding: 6.25% displays as 6.2%, and 31.25% as 31.2%. These labels do not change the exact underlying values.

![Wilson upper endpoints after zero observed failures](../assets/charts/zero_failure_uncertainty.png)

The zero-failure chart shows upper endpoints of **two-sided** nominal 95% Wilson intervals: 5.662602% (0/64), 13.798058% (0/24), 19.361342% (0/16), and 39.034303% (0/6). The caption's reference to a true rate is conditional on binomial assumptions; these are not guaranteed deployment risk bounds.

All three figures were reproduced in an isolated directory. PNG pixels and SVG path geometry match the preserved figures exactly. CSVs, figures, and manifests were not regenerated in the publication tree.

## Supported conclusion

No unauthorized selection was observed under the explicit source policy for the tested V2 and MCP configurations. This does not establish universal security, a causal policy effect, authenticated tool identity, or production enforcement. The clearest research contribution is the auditable experiment and the explicit disclosure of V1's design ambiguity.
