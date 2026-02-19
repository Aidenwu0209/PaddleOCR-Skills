# PaddleOCR-Skills

<p align="center">
  <strong>OCR Skills Suite for Claude Code</strong>
</p>

<p align="center">
  Text recognition and document parsing powered by PaddleOCR APIs
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Claude%20Code-Skills-purple.svg" alt="Claude Code Skills">
</p>

<p align="center">
  <a href="./README-cn.md">简体中文</a> | <strong>English</strong>
</p>

---

## Overview

This repository provides two complementary skills:

1. `paddleocr-text-recognition`
- Fast OCR for images and PDFs
- Returns unified JSON: `ok`, `text`, `result`, `error`

2. `paddleocr-doc-parsing`
- Advanced layout parsing for complex documents
- Extracts full text plus raw structured parsing result

---

## Feature Comparison

| Dimension | paddleocr-text-recognition | paddleocr-doc-parsing |
|-----------|----------------------------|-----------------------|
| Best for | Plain text extraction | Complex layout documents |
| Extracted `text` source | `prunedResult.rec_texts` joined by line/page | `layoutParsingResults[].markdown.text` (fallback: concatenated blocks) |
| Raw `result` granularity | Line-level OCR (`rec_texts`, `rec_scores`, `rec_boxes`, `rec_polys`) | Page/block-level parsing (`prunedResult.parsing_res_list`, `markdown`) |
| CLI input | `--file-url` or `--file-path` | `--file-url` or `--file-path`, plus `--file-type {0,1}` |
| Default timeout | `PADDLEOCR_TIMEOUT=120` | `PADDLEOCR_DOC_PARSING_TIMEOUT=600` |
| Large-file helper script | No | Yes (`skills/paddleocr-doc-parsing/scripts/optimize_file.py`, image optimization) |

---

## Installation

> Prerequisites: Node.js >= 14, Python 3.8+, [Claude Code CLI](https://claude.ai/code)

Install all skills:

```bash
npx skills add Aidenwu0209/PaddleOCR-Skills
```

Install one skill only:

```bash
npx skills add Aidenwu0209/PaddleOCR-Skills --skill paddleocr-text-recognition
npx skills add Aidenwu0209/PaddleOCR-Skills --skill paddleocr-doc-parsing
```

Manual install:

```bash
git clone https://github.com/Aidenwu0209/PaddleOCR-Skills.git
cd PaddleOCR-Skills

pip install -r skills/paddleocr-text-recognition/scripts/requirements.txt
pip install -r skills/paddleocr-doc-parsing/scripts/requirements.txt
```

---

## Configuration

Get API credentials at [Paddle AI Studio](https://paddleocr.com), then run:

```bash
python skills/paddleocr-text-recognition/scripts/configure.py
python skills/paddleocr-doc-parsing/scripts/configure.py
```

Core environment variables:

```bash
PADDLEOCR_OCR_API_URL=
PADDLEOCR_DOC_PARSING_API_URL=
PADDLEOCR_ACCESS_TOKEN=
```

Optional timeouts used by current code:

```bash
PADDLEOCR_TIMEOUT=120
PADDLEOCR_DOC_PARSING_TIMEOUT=600
```

---

## Quick Start

Text recognition:

```bash
python skills/paddleocr-text-recognition/scripts/ocr_caller.py \
  --file-path "./doc.png" \
  --pretty
```

Document parsing:

```bash
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-path "./invoice.pdf" \
  --pretty
```

Save output to file:

```bash
python skills/paddleocr-text-recognition/scripts/ocr_caller.py \
  --file-url "https://example.com/image.jpg" \
  --output result.json \
  --pretty

python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-url "https://example.com/document.pdf" \
  --output result.json \
  --pretty
```

---

## Output Contract

Both CLIs return the same envelope:

```json
{
  "ok": true,
  "text": "...",
  "result": { "...": "raw provider response" },
  "error": null
}
```

On error:

```json
{
  "ok": false,
  "text": "",
  "result": null,
  "error": { "code": "API_ERROR", "message": "..." }
}
```

---

## Large Files

For large files with document parsing:

- Prefer `--file-url` to avoid local base64 overhead.
- For large images, use `skills/paddleocr-doc-parsing/scripts/optimize_file.py`.
- For large PDFs, extract needed pages first, then parse.

See:
- [Quick Reference](./docs/QUICK_REFERENCE.md)
- [Large File Guide](./docs/LARGE_FILES.md)

---

## Testing

```bash
python skills/paddleocr-text-recognition/scripts/smoke_test.py --skip-api-test
python skills/paddleocr-doc-parsing/scripts/smoke_test.py --skip-api-test
```

---

## Documentation

- [Text Recognition Skill Guide](./skills/paddleocr-text-recognition/SKILL.md)
- [Text Recognition Output Schema](./skills/paddleocr-text-recognition/references/output_schema.md)
- [Doc Parsing Skill Guide](./skills/paddleocr-doc-parsing/SKILL.md)
- [Doc Parsing Output Schema](./skills/paddleocr-doc-parsing/references/output_schema.md)

---

## License

[MIT License](./LICENSE)

---

## Support

- Issues: [GitHub Issues](https://github.com/Aidenwu0209/PaddleOCR-Skills/issues)
- API service: [Paddle AI Studio](https://paddleocr.com)
