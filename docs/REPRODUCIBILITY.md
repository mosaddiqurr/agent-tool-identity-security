# Reproducibility Guide

Run commands from the repository root. Verification is read-only. The historical analyses and experiment runners write results, so invoke them through the isolated reproduction helper.

## Verify the publication package

Python 3.10+ is sufficient; no third-party package, model, or MCP service is required:

```bash
python -B scripts/verify_checksums.py
python -B scripts/audit_results.py
python -B scripts/check_publication.py
python -B -m unittest discover -s tests -v
```

Expected findings: V1 preliminary experiment 64 trials / 10 unauthorized; V2 primary tool-calling experiment 64 / 0; MCP-backed validation 24 / 0. The audit also reports one V2 duplicate-call response and the two known message-punctuation differences. It independently checks all 16 CSVs, including interval endpoints and exact tests.

The checksum command checks 176 entries in 12 experimental manifests. The thirteenth manifest, `evidence/release_manifest.sha256`, is preserved as the **original package snapshot**. It matched at intake, but publication documentation and helpers have since changed, and overlapping/internal documents have been archived outside the public tree. The optional `--release-snapshot` flag checks that historical snapshot strictly and is expected to fail on those edits. It is not a current-release check.

## Recorded environment

The preserved captures report:

| Component | Recorded value |
|---|---|
| Python | 3.13.12 |
| Ollama server | 0.35.1 |
| Ollama Python client | 0.6.3 |
| MCP Python SDK | 2.3.0 |
| pandas / SciPy | 3.0.6 / 1.18.1 |
| Model | `qwen3:4b`, short ID `359d7dd4bcda`, Q4_K_M |
| Machine | Four vCPUs, approximately 4.7 GiB RAM, CPU-only |
| Explicit model options | Temperature 0, seed 42, `think=False` |

The capture in [environment.txt](environment.txt) predates the reported trial timestamps. [timezone.txt](timezone.txt) records an unsynchronized clock. Neither is a per-trial runtime attestation.

[requirements-lock.txt](requirements-lock.txt) is the preserved package-list capture. It is not a wheel-hash lock or a complete portable environment specification. Publication chart dependencies were added separately; the NumPy pin comes from the captured list.

The final audit installed the direct pins and reproduced all analysis values and charts on Windows with Python 3.12.14. This checks compatibility, not identical model inference on another runtime.

## Install dependencies for analysis and experiments

Use Python 3.12+ for the pinned third-party dependencies. The standard-library evidence checks above also support Python 3.10+.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\Activate.ps1
```

Activation is optional. If it is unavailable, substitute `.\.venv\Scripts\python.exe` for `python` in subsequent commands.

### POSIX shell

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Direct pins are in [requirements.txt](../requirements.txt). The MCP implementation uses SDK v2 APIs (`Client`, `MCPServer`, `input_schema`); a v1 SDK is not a substitute. See the [MCP SDK release](https://pypi.org/project/mcp/2.3.0/) and [Ollama Python client](https://pypi.org/project/ollama/0.6.3/) for upstream context.

## Reproduce analyses and figures safely

Each destination must be new. The helper refuses existing output directories and publication paths. Inside this repository, output is allowed only under ignored `replications/`.

```bash
python -B scripts/reproduce.py analysis --output-dir replications/analysis-01
python -B scripts/reproduce.py charts --output-dir replications/charts-01
```

For analysis, the helper copies the frozen processed CSVs and unchanged analysis source into a separate directory, then runs all three analyses there. New summary CSVs appear under that destination's `results/processed/`.

For charts, the helper copies the processed data and historical chart script. New PNG/SVG figures appear under the destination's `assets/charts/`. The chart script has four fixed zero-failure upper endpoints; the audit checked those against the Wilson formula and verified the resulting figures. Reproduction can differ in fonts or metadata on other environments.

Do not run `src/analyze_*.py` or `scripts/make_charts.py` directly in the publication tree: those paths are the frozen output destinations.

## Check MCP integration without model inference

With dependencies installed:

```bash
python -B scripts/smoke_mcp.py
```

This starts each of the five local server implementations in turn, verifies discovery and argument schemas, and invokes a synthetic operation. Every response must say `SIMULATED_ONLY` and `sent: false`. It writes no experimental results and has a 60-second timeout.

## Re-run experiments in a fresh directory

Install the Ollama server separately. Ensure it is running locally, then make the model available:

```bash
ollama pull qwen3:4b
ollama --version
ollama list
ollama show qwen3:4b
```

A fresh pull may resolve to a different model artifact. Compare the captured identifier and quantization before claiming a replication. Preserve a full model digest, server version, dependency list, and machine details alongside new runs; do not overwrite the published captures.

Primary V2 experiment, 16 scenarios × four conditions:

```bash
python -B scripts/reproduce.py v2 --output-dir replications/v2-01
```

MCP-backed validation, six scenarios × four conditions:

```bash
python -B scripts/reproduce.py mcp --output-dir replications/mcp-01
```

Optional V1 preliminary experiment:

```bash
python -B scripts/reproduce.py v1 --output-dir replications/v1-01
```

For a short initial run, add `--limit 1`; this runs the first scenario in **all four conditions**, not one total trial. Each destination contains unchanged inputs and runner source, initially empty results, and a log directory. The helper checks expected unique trial counts, error logs, and selection labels against all raw calls.

The historical runners skip raw records already marked `status: ok`, but rebuild their CSVs. A populated checkout is therefore not an independent replication. The helper always starts with a new destination. New runs remain separate evidence and must be rescored and reviewed before being reported.

The final publication audit did not repeat Qwen inference or change model outputs.

## Evidence preservation and Git

All original raw JSON, processed CSVs, scenarios, prompts, configs, experiment/analysis source, environment captures, figures, and manifests remain unchanged. `.gitattributes` disables text normalization for these paths so Git line-ending conversion does not invalidate SHA-256 checks.

After cloning, repeat the read-only checks. The CI matrix is configured for Linux and Windows. At publication preparation on 2026-10-08, neither hosted job had run; local checks and workflow validation do not establish a CI pass.

The original package had no development Git history. Publication history cannot reconstruct or independently attest to earlier data collection. [Evidence verification](../evidence/README.md) explains the preserved snapshot and its limits.
