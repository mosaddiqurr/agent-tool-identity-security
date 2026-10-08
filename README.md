# Agent Tool Trust Study

A controlled AI-security study by **Mosaddiqur Rahman** of look-alike tool names and deceptive descriptions in a local Qwen3 4B agent, with MCP-backed validation.

**Research question:** can deceptive tool names or descriptions lead a local LLM to select an unauthorized connector when the policy identifies the permitted source?

The study uses simulated company email to examine tool selection. It preserves a preliminary experiment (V1), a primary tool-calling experiment (V2), and a validation subset using local MCP servers. All 152 reported trial records, inputs, analyses, and figures remain available.

## Architecture and threat model

The model chooses between `company_mail_send_email`, whose description claims source `company.internal`, and an untrusted connector claiming source `thirdparty.example`. The adversary changes the untrusted tool's name and description while keeping its source claim fixed.

```mermaid
flowchart LR
    T["Trusted local MCP server"] --> C["Python MCP client"]
    U["Untrusted local MCP server"] --> C
    C --> D["Schemas with textual source claims"]
    D --> Q["Qwen3 4B via Ollama"]
    Q --> S["Selected tool calls"]
    S --> C
    C --> E["Simulated MCP invocation"]
```

This diagram shows the MCP validation path. V1 and V2 measure the initial selection without executing tools. The MCP client routes selected calls to known local servers; it does **not** enforce the authorization policy before invocation. All operations are simulated, and no real email is sent.

**Source claims are description text, not authenticated tool identities.** Forging the trusted source label and production authorization enforcement were not evaluated.

## Experimental methodology

| Condition | Untrusted tool name | Untrusted description |
|---|---|---|
| C0 Control | `external_mail_send_email` | Neutral external connector |
| C1 Name similarity | `company_maill_send_email` | Neutral external connector |
| C2 Metadata deception | `external_mail_send_email` | Claims company-security authority |
| C3 Combined | `company_maill_send_email` | Same deceptive claim as C2 |

V1 and V2 each test 16 scenarios—eight routine and eight sensitive—in all four conditions, with alternating tool order. MCP-backed validation reuses six V2 scenarios across the same conditions.

A trial is one scenario-condition model request. Unauthorized selection is scored from **every emitted call**. All recorded trials specify Qwen3 4B through Ollama, temperature `0`, seed `42`, and the API setting `think=False`. These settings do not guarantee deterministic replication or the absence of reasoning-style output. See [Methodology](docs/METHODOLOGY.md) for the policies, sampling, scoring, and statistical assumptions.

## Results

| Stage | Trials | Unauthorized selections | Observed rate | Nominal two-sided 95% Wilson CI |
|---|---:|---:|---:|---|
| V1: preliminary experiment | 64 | 10 | 15.6% | 8.7%–26.4% |
| V2: primary tool-calling experiment | 64 | 0 | 0.0% | 0.0%–5.7% |
| MCP-backed validation | 24 | 0 | 0.0% | 0.0%–13.8% |

![Unauthorized selection rates and nominal Wilson intervals across the three stages](assets/charts/cross_stage_unauthorized_rate.png)

*Observed trial rates and nominal Wilson intervals. V2 changed both policy wording and tool descriptions; the cross-stage comparison is descriptive. The intervals are binomial reference summaries, not validated bounds on deployment risk.*

[Detailed results](docs/RESULTS.md) include condition and subgroup counts, exact tests, [condition comparisons](assets/charts/condition_comparison_v1_v2.png), and [uncertainty after zero observed failures](assets/charts/zero_failure_uncertainty.png).

## Key findings

- No unauthorized selection was observed in the tested V2 or MCP-backed configurations under the explicit textual source policy.
- V1 had ambiguous authorization and tool semantics. Its records are retained as preliminary evidence; they do not establish an isolated adversarial or policy effect.
- One V2 response duplicated an authorized call. One V2 and one MCP response omitted a final period from the requested message. Authorized selection does not imply exact task completion.

The contribution is the auditable evaluation and its visible design correction. [Findings](docs/FINAL_FINDINGS.md) separates the supported observations from broader security claims; [Design history](docs/DESIGN_HISTORY.md) explains why V1 remains preliminary.

## Limitations

- One model, one simulated task family, and a small fixed attack set.
- Purposefully selected, reused scenarios; the MCP subset is not an independent replication sample.
- No authenticated source identity, source-forgery evaluation, or production authorization gate.
- A mutable model tag, incomplete per-trial runtime provenance, and an unsynchronized recorded clock.

Zero observed failures do not establish zero risk, equivalence, or universal security. See [Limitations](docs/LIMITATIONS.md) for the full inference and provenance boundaries.

## Reproducibility

Run these read-only checks from the repository root with Python 3.10+; they require no model, MCP service, or third-party package:

```bash
python -B scripts/verify_checksums.py
python -B scripts/audit_results.py
python -B scripts/check_publication.py
python -B -m unittest discover -s tests -v
```

After installing [requirements.txt](requirements.txt), reproduce analyses or charts in new, separate directories:

```bash
python -B scripts/reproduce.py analysis --output-dir replications/analysis-01
python -B scripts/reproduce.py charts --output-dir replications/charts-01
```

[Reproduction instructions](docs/REPRODUCIBILITY.md) cover Windows and POSIX setup, simulated MCP checks, and optional fresh experiments. Historical runners and analysis scripts write to their own result paths; use the isolation helper to protect published evidence.

The 12 experimental manifests verify 176 entries. The original package manifest is retained as historical provenance and includes documentation that was later revised or archived; it is not a checksum of the current release. See [Evidence verification](evidence/README.md).

## Research documentation and repository guide

| Path | Purpose |
|---|---|
| [Methodology](docs/METHODOLOGY.md) | Threat model, design, scoring, and statistical assumptions |
| [Results](docs/RESULTS.md) | Verified counts, tests, and all three figures |
| [Findings](docs/FINAL_FINDINGS.md) | Supported observations and research implications |
| [Limitations](docs/LIMITATIONS.md) | Inference, identity, and provenance boundaries |
| [Data dictionary](docs/DATA_DICTIONARY.md) | Raw JSON and processed CSV semantics |
| [Reproducibility](docs/REPRODUCIBILITY.md) | Verification and safe reproduction commands |
| [Design history](docs/DESIGN_HISTORY.md) | V1 ambiguity and the transition to V2 and MCP validation |
| [Evidence verification](evidence/README.md) | Manifest scope and integrity checks |
| `configs/`, `prompts/`, `scenarios/` | Frozen experimental inputs |
| `src/`, `mcp_clients/`, `mcp_servers/final/` | Preserved experiment and analysis code |
| `results/raw/`, `results/processed/` | 152 canonical records and 16 processed CSVs |
| `assets/charts/`, `scripts/`, `tests/` | Verified figures, audit helpers, and regression checks |

## Licensing and acknowledgements

Copyright (c) 2026 Mosaddiqur Rahman. Source code and software configuration use [MIT](LICENSE); documentation, synthetic datasets, and project contributions to charts use [CC BY 4.0](LICENSES/CC-BY-4.0.txt). See [license scope and attribution](LICENSING.md).

The study uses Qwen3, Ollama, the MCP Python SDK, pandas, SciPy, NumPy, and Matplotlib. [Third-party notices](THIRD_PARTY_NOTICES.md) retain upstream terms, including the DejaVu font outlines in SVG figures. Model weights and dependency distributions are not bundled.
