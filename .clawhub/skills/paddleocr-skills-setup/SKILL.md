---
name: paddleocr-skills-setup
description: Install, configure, and verify both Agent Skills from Aidenwu0209/PaddleOCR-Skills. Use when a user wants the script-based PaddleOCR text-recognition and document-parsing skills installed in Codex, Claude Code, Cursor, OpenCode, OpenClaw, or another skills-compatible agent.
license: MIT-0
metadata:
  author: Aidenwu0209
  repository: https://github.com/Aidenwu0209/PaddleOCR-Skills
  version: "1.0.1"
  openclaw:
    emoji: "🧰"
    homepage: https://github.com/Aidenwu0209/PaddleOCR-Skills
---

# Set up PaddleOCR Skills

Install and verify the two skills from the linked repository. Treat this setup
skill as an installer guide; run OCR with the installed target skills.

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
