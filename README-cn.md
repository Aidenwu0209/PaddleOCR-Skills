# PaddleOCR-Skills

<p align="center">
  <strong>Claude Code OCR 技能套件</strong>
</p>

<p align="center">
  基于 PaddleOCR API 的文本识别与文档解析
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Claude%20Code-Skills-purple.svg" alt="Claude Code Skills">
</p>

<p align="center">
  <a href="./README.md">English</a> | <strong>简体中文</strong>
</p>

---

## 仓库概览

本仓库包含两个互补的技能：

1. `paddleocr-text-recognition`
- 面向图片 / PDF 的快速 OCR 文本提取
- 返回统一 JSON：`ok`、`text`、`result`、`error`

2. `paddleocr-doc-parsing`
- 面向复杂版面（表格、多栏、图文混排）的文档解析
- 返回完整文本和原始结构化结果

---

## 功能对比

| 维度 | paddleocr-text-recognition | paddleocr-doc-parsing |
|------|----------------------------|-----------------------|
| 适合场景 | 纯文本提取 | 复杂版面文档解析 |
| 提取 `text` 来源 | 按页拼接 `prunedResult.rec_texts` | 优先 `layoutParsingResults[].markdown.text`（兜底拼接 block） |
| 原始 `result` 粒度 | 行级 OCR（`rec_texts`、`rec_scores`、`rec_boxes`、`rec_polys`） | 页/块级解析（`prunedResult.parsing_res_list`、`markdown`） |
| CLI 输入 | `--file-url` 或 `--file-path` | `--file-url` 或 `--file-path`，另有 `--file-type {0,1}` |
| 默认超时 | `PADDLEOCR_TIMEOUT=120` | `PADDLEOCR_DOC_PARSING_TIMEOUT=600` |
| 大文件辅助脚本 | 无 | 有（`skills/paddleocr-doc-parsing/scripts/optimize_file.py`，仅图片压缩） |

---

## 安装

> 前置条件：Node.js >= 14、Python 3.8+、[Claude Code CLI](https://claude.ai/code)

安装全部技能：

```bash
npx skills add Aidenwu0209/PaddleOCR-Skills
```

按需安装单个技能：

```bash
npx skills add Aidenwu0209/PaddleOCR-Skills --skill paddleocr-text-recognition
npx skills add Aidenwu0209/PaddleOCR-Skills --skill paddleocr-doc-parsing
```

手动安装：

```bash
git clone https://github.com/Aidenwu0209/PaddleOCR-Skills.git
cd PaddleOCR-Skills

pip install -r skills/paddleocr-text-recognition/scripts/requirements.txt
pip install -r skills/paddleocr-doc-parsing/scripts/requirements.txt
```

---

## 配置

在 [Paddle AI Studio](https://paddleocr.com) 获取 API 凭证后，运行：

```bash
python skills/paddleocr-text-recognition/scripts/configure.py
python skills/paddleocr-doc-parsing/scripts/configure.py
```

核心环境变量：

```bash
PADDLEOCR_OCR_API_URL=
PADDLEOCR_DOC_PARSING_API_URL=
PADDLEOCR_ACCESS_TOKEN=
```

当前代码支持的可选超时变量：

```bash
PADDLEOCR_TIMEOUT=120
PADDLEOCR_DOC_PARSING_TIMEOUT=600
```

---

## 快速开始

文本识别：

```bash
python skills/paddleocr-text-recognition/scripts/ocr_caller.py \
  --file-path "./doc.png" \
  --pretty
```

文档解析：

```bash
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-path "./invoice.pdf" \
  --pretty
```

保存结果到文件：

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

## 输出约定

两个 CLI 都返回同一层结构：

```json
{
  "ok": true,
  "text": "...",
  "result": { "...": "原始 API 返回" },
  "error": null
}
```

失败时：

```json
{
  "ok": false,
  "text": "",
  "result": null,
  "error": { "code": "API_ERROR", "message": "..." }
}
```

---

## 大文件建议

针对文档解析：

- 优先使用 `--file-url`，减少本地 base64 编码开销。
- 大图片可用 `skills/paddleocr-doc-parsing/scripts/optimize_file.py` 压缩。
- 大 PDF 建议先按页拆分后再调用解析。

详见：
- [快速参考](./docs/QUICK_REFERENCE.md)
- [大文件指南](./docs/LARGE_FILES.md)

---

## 测试

```bash
python skills/paddleocr-text-recognition/scripts/smoke_test.py --skip-api-test
python skills/paddleocr-doc-parsing/scripts/smoke_test.py --skip-api-test
```

---

## 文档索引

- [文本识别技能说明](./skills/paddleocr-text-recognition/SKILL.md)
- [文本识别输出结构](./skills/paddleocr-text-recognition/references/output_schema.md)
- [文档解析技能说明](./skills/paddleocr-doc-parsing/SKILL.md)
- [文档解析输出结构](./skills/paddleocr-doc-parsing/references/output_schema.md)

---

## 许可证

[MIT License](./LICENSE)

---

## 支持

- 问题反馈：[GitHub Issues](https://github.com/Aidenwu0209/PaddleOCR-Skills/issues)
- API 服务：[Paddle AI Studio](https://paddleocr.com)
