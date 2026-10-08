# Third-Party Notices

The repository contains project code, synthetic research evidence, documentation, and charts. Model weights and installed dependency distributions are not included. The project licenses in [LICENSING.md](LICENSING.md) do not replace upstream licenses.

## Model

The experiment used Qwen3 4B through Ollama, with the captured identifier and configuration documented in [Reproducibility](docs/REPRODUCIBILITY.md). The [Qwen team's Qwen3-4B model repository](https://huggingface.co/Qwen/Qwen3-4B) identifies its model license as [Apache License 2.0](https://huggingface.co/Qwen/Qwen3-4B/blob/main/LICENSE).

[docs/qwen3-4b-info.txt](docs/qwen3-4b-info.txt) preserves the original Ollama model-information capture, including a short upstream license excerpt. That excerpt retains its upstream terms. An unmodified copy of the [Apache License 2.0](LICENSES/Apache-2.0.txt) is included for reference. No model weights are redistributed, and the capture is not a full model provenance or licensing attestation.

## Software dependencies

The pinned versions are recorded in [requirements.txt](requirements.txt). Installed package metadata was reviewed; upstream license links below are authoritative for each dependency, including bundled components and notices.

| Dependency | Role | Upstream licensing |
|---|---|---|
| [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | Local MCP discovery and invocation | [MIT](https://github.com/modelcontextprotocol/python-sdk/blob/main/LICENSE) |
| [Ollama Python client](https://github.com/ollama/ollama-python) | Local model requests | [MIT](https://github.com/ollama/ollama-python/blob/main/LICENSE) |
| [Ollama](https://github.com/ollama/ollama) | External local model runtime | [MIT](https://github.com/ollama/ollama/blob/main/LICENSE) |
| [pandas](https://github.com/pandas-dev/pandas) | CSV analysis | [BSD 3-Clause and bundled notices](https://github.com/pandas-dev/pandas/blob/main/LICENSE) |
| [SciPy](https://github.com/scipy/scipy) | Statistical calculations | [BSD 3-Clause and bundled notices](https://github.com/scipy/scipy/blob/main/LICENSE.txt) |
| [NumPy](https://github.com/numpy/numpy) | Numerical chart arrays | [BSD 3-Clause and bundled component licenses](https://github.com/numpy/numpy/blob/main/LICENSE.txt) |
| [Matplotlib](https://github.com/matplotlib/matplotlib) | Research figures | [Matplotlib license agreement and historical notices](https://matplotlib.org/3.10.8/project/license.html) |

The generated figures are project research material under CC BY 4.0; using Matplotlib does not change the licenses of Matplotlib's own code. No dependency license text is being removed from a redistributed dependency, because no dependency distribution is bundled here.

## Font outlines in the SVG charts

The SVG charts contain `DejaVuSans` glyph outlines produced by Matplotlib. Retain the accompanying [DejaVu font license and notices](LICENSES/DejaVu-Fonts.txt) when redistributing these outlines. The included text is copied unchanged from Matplotlib 3.10.8's `LICENSE_DEJAVU` file and agrees with the [DejaVu project's license notice](https://dejavu-fonts.github.io/License.html).

The notices credit Bitstream, Inc. (2003), state that DejaVu changes are in the public domain, and retain the Arev notice for Tavmjong Bah (2006) included upstream. CC BY 4.0 covers the project's figure composition and research content; it does not replace the font terms. The frozen SVG files are unchanged.

## CI and publication tooling

The workflow references [actions/checkout](https://github.com/actions/checkout) and [actions/setup-python](https://github.com/actions/setup-python), each under [MIT](https://github.com/actions/checkout/blob/main/LICENSE) ([setup-python license](https://github.com/actions/setup-python/blob/main/LICENSE)). GitHub downloads these separately when the workflow runs.

The Mermaid block in [Methodology](docs/METHODOLOGY.md) is project documentation under CC BY 4.0. Mermaid's renderer is external tooling ([MIT](https://github.com/mermaid-js/mermaid/blob/develop/LICENSE)); its implementation is not bundled. Temporary rendering and audit dependencies are excluded from the publication tree.

Upstream project names identify the tools used; no endorsement by their authors is claimed.
