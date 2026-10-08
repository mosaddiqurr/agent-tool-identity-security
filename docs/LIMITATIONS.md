# Limitations

## Generalization and attack coverage

Only Qwen3 4B, one simulated email task family, and a small fixed set of metadata descriptions were evaluated. The look-alike uses one extra letter in `company_maill_send_email`. These observations do not generalize to other models, tool types, runtimes, languages, or adaptive adversaries.

Source spoofing, Unicode/homoglyph names, malicious schema fields, long prompt injections, poisoned resources/prompts, dynamic registration, memory attacks, approval bypass, and multi-turn behavior were not evaluated.

## Source cues are not authenticated provenance

The model receives `Source: company.internal.` and `Source: thirdparty.example.` as description text. The experiment holds those strings constant. It does not prove that a connector cannot impersonate the trusted source or that the displayed label identifies the originating service.

The MCP client knows the supplying local process, but routes selected calls by name and can invoke the untrusted simulated tool. No runtime deny rule is evaluated. Prompt-level source instructions should not be treated as a replacement for an independently enforced authorization decision.

## Sampling and confidence intervals

There are 16 trials per condition in V2 and six per condition in MCP-backed validation. At zero failures, the upper endpoints of the two-sided nominal 95% Wilson intervals are:

| Sample | Result | Upper endpoint |
|---|---:|---:|
| V2 overall | 0/64 | 5.7% |
| MCP overall | 0/24 | 13.8% |
| V2 per condition | 0/16 | 19.4% |
| MCP per condition | 0/6 | 39.0% |

These values assume independent binomial observations with a common underlying rate. Requests are purposefully selected and reused across conditions. The model uses fixed temperature `0` and seed `42`, with no repeated seed or sampling study. Thus, the intervals are reference summaries, not validated coverage guarantees for a random deployment population.

Fixed settings also do not guarantee identical behavior across hardware, model revisions, or runtime versions. There is no pooled 152-trial security estimate. The MCP scenarios overlap V2 and must not be counted as an independent replication sample.

## V1 ambiguity and cross-stage confounding

V1 is a preliminary experiment because the policy and the trusted connector's internal-email description permit competing interpretations. Its 10/64 unauthorized selections cannot be attributed solely to deceptive metadata.

V2 changes both the policy and tool descriptions. The reduction to 0/64 is descriptive; it does not isolate a causal effect of explicit source instructions. The MCP stage further changes schema generation, client/server integration, and ordering for the reused subset.

Historical V1 Fisher exact tests are arithmetically correct but use an independent-group framing for paired scenarios. They are exploratory, unadjusted comparisons. V2's zero-discordance paired-test values of `p = 1.0` do not establish equivalence, power, or the absence of an effect.

## Selection, execution, and task fidelity

V1/V2 record a single initial model response and do not execute tools. MCP-backed validation invokes simulated tools but does not return their results to the model for another turn. No production email, authentication, organizational control, or user approval workflow is evaluated.

V2 C1/S014 emits two identical authorized calls. V2 C1/S011 and MCP C1/S011 omit the final period in the requested message. The outcome measures authorization selection, not perfect argument fidelity or exactly-once behavior.

The historical V1/V2 runners prioritize an expected call and could misclassify a hypothetical mixed response. No recorded response is mixed. The independent publication auditor checks every call with a security-first rule. Future experimental harnesses should enforce that rule during collection and separately score duplicates and unknown calls.

## Thinking setting and runtime

`think=False` records the API argument. Most stored responses contain reasoning-style markers. Neither the setting nor the captured text proves the model's internal reasoning mode.

The recorded experiment ran on a small CPU-only machine. Duration measures model-call wall time; MCP invocation is outside the recorded duration. Latency is not a security outcome and is not compared as a benchmark.

## Evidence completeness and reproducibility

The package contains 152 complete reported trials and the corresponding CSVs. Earlier pilot runs, development logs, and terminal screenshots are absent. Their original completeness and exclusion history cannot be independently audited from this package.

The environment capture notes an unsynchronized system clock. Timestamps cannot establish independently verified preregistration or precise real-world chronology. The MCP subset's frozen membership is verifiable; its prospective selection timing is not independently attested.

The model capture retains a mutable tag and short identifier, not a full model digest or weights. Raw records omit complete MCP discovery schemas, transport transcripts, and per-trial runtime versions. Dependency captures describe the recorded environment, not a portable lock for every platform.

SHA-256 checks detect byte changes relative to preserved manifests. They do not establish when data were collected, that they were not previously edited, or who produced them. The supplied package had no Git history before publication preparation. A first publication commit cannot reconstruct or attest to earlier development or collection history. The original release manifest is preserved as an intake snapshot and does not cover subsequent publication edits.
