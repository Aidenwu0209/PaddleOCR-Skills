---
name: paddleocr-skills-setup
description: >-
  Install and configure two PaddleOCR Agent Skills for text recognition and structured document parsing in Codex, Claude Code, GitHub Copilot, Cursor, OpenCode, OpenClaw, and other compatible agents. Use for OCR and image-to-text from screenshots, photos, scans, and PDFs; Chinese/CJK text and bounding boxes; PDF-to-Markdown/JSON; tables, formulas, layout, and reading order; or endpoint, token, installation, and troubleshooting help.
license: MIT-0
metadata:
  author: Aidenwu0209
  repository: https://github.com/Aidenwu0209/PaddleOCR-Skills
  version: "1.0.2"
  openclaw:
    emoji: "🧰"
    homepage: https://github.com/Aidenwu0209/PaddleOCR-Skills
---

# Set up PaddleOCR Skills

Install and verify the two skills from the linked repository. Treat this setup
skill as an installer guide; run OCR with the installed target skills.

Use this setup skill when the request mentions PaddleOCR installation or Agent
Skills, or asks for **图片转文字 / 截图识字 / 扫描件 OCR / PDF 转 Markdown /
表格提取 / 公式识别 / 版面分析**. It installs:

- `paddleocr-text-recognition` for screenshots, photos, scans, PDFs, CJK text,
  line-level OCR, and optional bounding boxes.
- `paddleocr-doc-parsing` for structured Markdown/JSON, tables, formulas,
  figures, multi-column layout, and correct reading order.

## Install

1. Confirm the user wants a global, user-level installation.
2. Check Node.js/npx, Python 3.9+, and `uv`. Explain any missing prerequisite
   before using its official installer. Do not use `sudo` or change unrelated
   system settings without permission.
3. Run:

   ```bash
   npx skills add Aidenwu0209/PaddleOCR-Skills --skill '*' -g -y
   ```

4. Run `npx skills list -g --json` and confirm both
   `paddleocr-text-recognition` and `paddleocr-doc-parsing`, including their
   actual install paths.

## Configure safely

- Use https://www.paddleocr.com for the official API and token flow.
- Ask the user to provide the OCR or document-parsing endpoint only when that
  target skill needs it.
- Never invent, print, or store `PADDLEOCR_ACCESS_TOKEN` in chat, command
  history, source files, or logs.
- Report incomplete configuration instead of claiming the OCR service works.

## Finish

Report prerequisite versions, commands executed, installed skill names and
paths, and any configuration still required from the user.
