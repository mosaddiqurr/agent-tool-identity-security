# Design History

This note preserves the methodological context needed to interpret the frozen experiments. [Methodology](METHODOLOGY.md) defines the final design, and [Results](RESULTS.md) contains the verified numerical summaries.

## V1: preliminary experiment

V1 crossed untrusted name similarity and deceptive descriptions across 16 synthetic email requests, giving 64 scenario-condition trials. It used Qwen3 4B through Ollama, temperature 0, seed 42, and a recorded API setting of `think=False`.

The policy referred to authorized company tools without defining authorization as explicitly as V2. The trusted description also referred to internal employee email. The retained control failure discussed interpreting a recipient and choosing an external connector; that text suggests possible semantic ambiguity but is not a causal trace of the model's computation.

V1 therefore remains preliminary evidence. Its observed selections cannot establish an isolated metadata attack effect under the later explicit policy.

## V2: primary tool-calling experiment

V2 retained the 16 requests and four conditions, but made the permitted `company.internal` source claim explicit and treated all requests as company email. Trusted and untrusted descriptions also changed.

The revision corrected design ambiguity; it was not a single-factor policy intervention. Cross-stage comparisons remain descriptive. Source claims were still text in tool descriptions, with no authenticated provenance or source-forgery test.

## MCP-backed validation

The MCP client added local stdio discovery and simulated invocation to a six-scenario V2 subset. The subset is frozen and verifiable, but its prospective selection timing is not independently attested. Alternating order uses position in the subset rather than position in the full V2 list.

This stage checks the local integration. It does not supply an independent sample, evaluate a multi-turn interaction after tool results, or enforce production authorization before invocation.

## Development context outside the reported evidence

Earlier notes described a `think=True` smoke-test plan, CPU runtime concerns, and a proposed smaller thinking-mode robustness experiment. Those pilot records and timing measurements are absent from the supplied evidence. No runtime comparison or robustness conclusion is drawn from them.

All three reported stages record a false API thinking setting, but reasoning-style markers remain in most responses. The setting does not establish the model's internal reasoning mode.

Overlapping design notes and release/website documents were archived separately during publication preparation. This consolidation changed documentation only. Frozen prompts, scenarios, configurations, experiment/analysis implementations, records, CSVs, figures, environment captures, and all 13 manifests retain their original bytes. Historical filenames remain for traceability.
