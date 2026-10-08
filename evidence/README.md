# Evidence Verification

Raw JSON is canonical. Processed trial CSVs flatten the records; summary CSVs and charts are derived from them. The public repository preserves all **152 trials**, **16 processed CSVs**, three PNG/SVG chart pairs, original experimental inputs and implementations, and environment captures.

## Verify the frozen experiment

Run from the repository root:

```bash
python -B scripts/verify_checksums.py
python -B scripts/audit_results.py
```

The default checksum verifier checks **176 entries across 12 experimental manifests**. It covers frozen inputs, runners, raw records, trial CSVs, and selected analysis outputs. The result auditor also checks embedded input hashes, every selected call, all CSV fields, rates, Wilson intervals, subgroup summaries, and exact-test arithmetic.

The verified unauthorized-selection counts are 10/64 for V1 (preliminary experiment), 0/64 for V2 (primary tool-calling experiment), and 0/24 for MCP-backed validation. [Results](../docs/RESULTS.md) documents the statistical assumptions and retained fidelity anomalies.

## Historical package snapshot

`release_manifest.sha256` is the **original package snapshot**. All 234 entries matched at initial audit intake. It remains unchanged.

Publication prose and audit helpers were subsequently revised; redundant design notes, release-management documents, and website-handoff material were preserved outside the public working tree. The historical manifest therefore contains intentionally different or absent publication-document paths. It is not a checksum of this release.

The optional `--release-snapshot` flag strictly checks that historical manifest and is expected to fail on those differences. Use the default command above to verify the experiments. No manifest was rewritten to conceal publication changes.

## Names and provenance boundaries

- `final_runner_v2_checksum.sha256` covers the V1 preliminary runner's historical revision. It does not denote the V2 experiment.
- `v2_runner_checksum.sha256` covers the V2 primary tool-calling experiment runner.
- Environment captures remain at their original `docs/*.txt` paths. They are not per-trial runtime attestations.
- Earlier excluded checksums, pilot records, development logs, and screenshots are absent from the supplied evidence. Their original contents and exclusion history cannot be independently verified.

Hashes establish byte agreement, not authorship, authenticity, collection time, or independently verified preregistration. [Limitations](../docs/LIMITATIONS.md) covers the unsynchronized clock and incomplete model/runtime provenance. [Design history](../docs/DESIGN_HISTORY.md) preserves the relevant revision context.

Use [Reproducibility](../docs/REPRODUCIBILITY.md) for safe analysis/chart reproduction and separately preserved future runs.
