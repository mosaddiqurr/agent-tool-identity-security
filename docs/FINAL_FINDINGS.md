# Findings

The [results](RESULTS.md) report every count, interval, subgroup, and exact test. This document states what those observations support.

## Supported observations

1. **V1 remains preliminary.** Its authorization policy and trusted tool's internal-email semantics were ambiguous. Metadata-deception conditions had higher observed unauthorized-selection rates, but the exploratory Fisher tests were not significant at 0.05, did not account for paired scenarios, and could not resolve the design ambiguity.
2. **V2 recorded no unauthorized selection in 64 trials.** The primary tool-calling experiment used an explicit textual source policy. Both the policy and tool descriptions changed from V1, so the cross-stage difference does not isolate a causal policy effect.
3. **MCP-backed validation recorded no unauthorized selection in 24 trials.** This verifies the tested local discovery-and-invocation integration using a V2 scenario subset. It is not an independent sample or a general result about MCP security.
4. **Selection and task fidelity differ.** One V2 response duplicated an authorized call. One V2 and one MCP response omitted a final period from the requested message. These retained records prevent treating authorized selection as perfect or exactly-once completion.

The source labels were description text. The experiment did not evaluate authenticated identity, forged trusted source labels, or a runtime authorization gate. Zero observed failures do not establish zero risk or security equivalence.

## Research implications

Authorization and tool semantics need to be explicit before behavior is attributed to an adversarial cue. Preserving the preliminary design makes that methodological correction visible.

Tool-selection evaluations should inspect every call, disclose duplicate or unknown calls, preserve raw records, and state sampling assumptions. These fixed, purposefully chosen scenarios support a bounded observation; the Wilson intervals do not establish deployment coverage.

Production systems need authorization decisions that do not depend on untrusted description text. This study motivates that distinction but provides no evaluation of such enforcement.

See [Methodology](METHODOLOGY.md), [Limitations](LIMITATIONS.md), and [Design history](DESIGN_HISTORY.md).
