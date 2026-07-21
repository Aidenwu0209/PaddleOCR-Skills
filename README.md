# PaddleOCR Skills

[English](./README.md) | [简体中文](./README_cn.md)

Standalone mirror of the official PaddleOCR Agent Skills from
[PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/tree/main/skills).

Synced source: `PaddlePaddle/PaddleOCR` commit `f0d83fafe9598134e5ac46aca62a4738f0eabac0`
(2026-05-06), checked against upstream `main` HEAD `211989f0` (2026-06-26).

> **Upstream refactored the skills in [PR #18090](https://github.com/PaddlePaddle/PaddleOCR/pull/18090)
> (2026-06-03)** — it removed the bundled `scripts/` and `references/` and switched to the
> official `paddleocr api` CLI. **This mirror intentionally keeps the script-based version**
> (which still works and is offline-friendly via `uv`), and additionally documents the CLI as an
> alternative path. See [Two Ways to Run the Skills](#two-ways-to-run-the-skills) below.

## Included Skills

| Skill | Use case | Entry script |
| --- | --- | --- |
| `paddleocr-text-recognition` | Extract text from images, scans, and PDF files | `ocr_caller.py` |
| `paddleocr-doc-parsing` | Parse complex documents into Markdown/structured output | `layout_caller.py` |

## Two Ways to Run the Skills

Each skill can be invoked in two ways. The **bundled scripts are the default path** in this
mirror; the **`paddleocr` CLI is the upstream-canonical alternative** introduced in #18090.

| | Scripts (default) | `paddleocr` CLI (alternative) |
| --- | --- | --- |
| Install | Just `uv` — deps are resolved from PEP 723 inline metadata | `pip install "paddleocr>=3.7.0"` |
| Required env vars | Per-skill `PADDLEOCR_OCR_API_URL` / `PADDLEOCR_DOC_PARSING_API_URL` + `PADDLEOCR_ACCESS_TOKEN` | `PADDLEOCR_ACCESS_TOKEN` only (the CLI resolves the endpoint internally) |
| Output format | `{ok, text, result, error}` envelope, auto-saved to a temp file | `{jobId, pages:[...]}` printed to stdout |
| Page selection (PDF) | Pre-split with `scripts/split_pdf.py` | Native `--page_ranges "1-5,10"` |
| Best for | Skills runtimes, airgapped / offline-friendly setups, no extra install | Environments that already ship `paddleocr`, or where you want the upstream flow |

> The two paths return **different output shapes** and read **different environment variables** —
> they are not output-compatible. Pick one per workflow.

Detailed usage and per-skill examples live in each SKILL.md:

- [paddleocr-text-recognition/SKILL.md](./skills/paddleocr-text-recognition/SKILL.md)
- [paddleocr-doc-parsing/SKILL.md](./skills/paddleocr-doc-parsing/SKILL.md)

## Requirements

- Python 3.9 or later
- [`uv`](https://docs.astral.sh/uv/)
- Internet access
- PaddleOCR official API credentials from [paddleocr.com](https://www.paddleocr.com)

The scripts use PEP 723 inline dependency metadata, so there are no separate
`requirements.txt` files to install.

## Configuration

Set the environment variables required by the skill you want to use:

| Skill | Required | Optional |
| --- | --- | --- |
| `paddleocr-text-recognition` | `PADDLEOCR_OCR_API_URL` ending with `/ocr`, `PADDLEOCR_ACCESS_TOKEN` | `PADDLEOCR_OCR_TIMEOUT` |
| `paddleocr-doc-parsing` | `PADDLEOCR_DOC_PARSING_API_URL` ending with `/layout-parsing`, `PADDLEOCR_ACCESS_TOKEN` | `PADDLEOCR_DOC_PARSING_TIMEOUT` |

> The `PADDLEOCR_*_API_URL` variables above are only required by the **bundled scripts**. If you
> use the `paddleocr` CLI instead, only `PADDLEOCR_ACCESS_TOKEN` is needed — see the "Alternative:
> paddleocr CLI" section in each SKILL.md.

## Local Usage

Run commands from the corresponding skill directory.

```shell
cd skills/paddleocr-text-recognition
uv run scripts/ocr_caller.py --file-path "/path/to/image-or-document.pdf" --pretty
```

```shell
cd skills/paddleocr-doc-parsing
uv run scripts/layout_caller.py --file-path "/path/to/document.pdf" --pretty
```

## Install into AI Apps

From this repository root:

```shell
npx skills add ./skills/paddleocr-text-recognition -g -y
npx skills add ./skills/paddleocr-doc-parsing -g -y
```

Or install through OpenClaw:

```shell
clawhub install paddleocr-text-recognition
clawhub install paddleocr-doc-parsing
```

## Documentation

- Official documentation mirror: [docs/version3.x/deployment/skills.en.md](./docs/version3.x/deployment/skills.en.md)
- Chinese official documentation mirror: [docs/version3.x/deployment/skills.md](./docs/version3.x/deployment/skills.md)
- Quick reference: [docs/QUICK_REFERENCE.md](./docs/QUICK_REFERENCE.md)
- Large file guide: [docs/LARGE_FILES.md](./docs/LARGE_FILES.md)

## License

Apache-2.0. See [LICENSE](./LICENSE).
