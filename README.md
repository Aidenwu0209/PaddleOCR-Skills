# PaddleOCR Skills

[English](./README.md) | [简体中文](./README_cn.md)

Standalone mirror of the official PaddleOCR Agent Skills from
[PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/tree/main/skills).

Synced source: `PaddlePaddle/PaddleOCR` commit `f0d83fafe9598134e5ac46aca62a4738f0eabac0`
(2026-05-06).

## Included Skills

| Skill | Use case | Entry script |
| --- | --- | --- |
| `paddleocr-text-recognition` | Extract text from images, scans, and PDF files | `ocr_caller.py` |
| `paddleocr-doc-parsing` | Parse complex documents into Markdown/structured output | `layout_caller.py` |

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
