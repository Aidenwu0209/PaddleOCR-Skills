# PaddleOCR Skills

[English](./README.md) | [简体中文](./README_cn.md)

[![skills.sh](https://skills.sh/b/aidenwu0209/paddleocr-skills)](https://skills.sh/aidenwu0209/paddleocr-skills)

> **Upstream refactored the skills in [PR #18090](https://github.com/PaddlePaddle/PaddleOCR/pull/18090)
> (2026-06-03)** — it removed the bundled `scripts/` and `references/` and switched to the
> official `paddleocr api` CLI. **This mirror intentionally keeps the script-based version**
> (which still works and is offline-friendly via `uv`), and additionally documents the CLI as an
> alternative path. See [Two Ways to Run the Skills](#two-ways-to-run-the-skills) below.

## Discover

- [skills.sh listing](https://skills.sh/aidenwu0209/paddleocr-skills) — **4.3K+ installs**
  across supported AI agents.
- [PaddleOCR official website](https://www.paddleocr.com) — API access, tokens, and
  official product documentation.
- [DeepSeek Harness GUI edition](https://github.com/Aidenwu0209/dsh-PaddleOCR-Skills) —
  native tools plus a visual **Settings → PaddleOCR** configuration panel.

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

Use the [skills.sh CLI](https://skills.sh/docs/cli) to choose skills and target agents
interactively:

```shell
npx skills add Aidenwu0209/PaddleOCR-Skills
```

Or install both included skills globally for a specific agent:

| Agent | Command |
| --- | --- |
| Codex | `npx skills add Aidenwu0209/PaddleOCR-Skills --agent codex --skill '*' -g -y` |
| Claude Code | `npx skills add Aidenwu0209/PaddleOCR-Skills --agent claude-code --skill '*' -g -y` |
| GitHub Copilot | `npx skills add Aidenwu0209/PaddleOCR-Skills --agent github-copilot --skill '*' -g -y` |
| OpenClaw | `npx skills add Aidenwu0209/PaddleOCR-Skills --agent openclaw --skill '*' -g -y` |

GitHub CLI 2.90.0+ also provides native Agent Skills installation:

```shell
gh skill install Aidenwu0209/PaddleOCR-Skills --all --agent github-copilot --scope user
```

For Claude Code plugin development or local testing, clone the repository and load its
[`plugin.json`](./.claude-plugin/plugin.json):

```shell
git clone https://github.com/Aidenwu0209/PaddleOCR-Skills.git
claude --plugin-dir ./PaddleOCR-Skills
```

To install directly from a local checkout instead:

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
