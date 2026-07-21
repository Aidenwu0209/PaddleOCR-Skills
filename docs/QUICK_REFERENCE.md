# PaddleOCR Skills 快速参考

## 技能选择

| 需求 | 推荐 Skill | 入口脚本 |
| --- | --- | --- |
| 提取图片、截图、扫描件、PDF 中的纯文本 | `paddleocr-text-recognition` | `ocr_caller.py` |
| 保留表格、公式、多栏、图表、阅读顺序等结构 | `paddleocr-doc-parsing` | `layout_caller.py` |

## 运行前准备

1. 安装 Python 3.9+ 和 `uv`。
2. 从 [PaddleOCR 官网](https://www.paddleocr.com) 获取 API URL 和 Token。
3. 配置环境变量：

```bash
export PADDLEOCR_ACCESS_TOKEN="<ACCESS_TOKEN>"
export PADDLEOCR_OCR_API_URL="<OCR_API_URL_ENDING_WITH_/ocr>"
export PADDLEOCR_DOC_PARSING_API_URL="<DOC_PARSING_API_URL_ENDING_WITH_/layout-parsing>"
```

可选超时变量：

```bash
export PADDLEOCR_OCR_TIMEOUT=300
export PADDLEOCR_DOC_PARSING_TIMEOUT=900
```

## 冒烟测试

```bash
cd skills/paddleocr-text-recognition
uv run scripts/smoke_test.py --skip-api-test
```

```bash
cd skills/paddleocr-doc-parsing
uv run scripts/smoke_test.py --skip-api-test
```

去掉 `--skip-api-test` 会实际调用 API。也可以用 `--test-url "https://..."` 指定测试文件。

## 文本识别

```bash
cd skills/paddleocr-text-recognition
```

```bash
# URL
uv run scripts/ocr_caller.py \
  --file-url "https://example.com/image.jpg" \
  --pretty
```

```bash
# 本地文件
uv run scripts/ocr_caller.py \
  --file-path "./doc.pdf" \
  --pretty
```

```bash
# 指定输出文件
uv run scripts/ocr_caller.py \
  --file-path "./doc.pdf" \
  --output "./result_text.json" \
  --pretty
```

## 文档解析

```bash
cd skills/paddleocr-doc-parsing
```

```bash
# URL
uv run scripts/layout_caller.py \
  --file-url "https://example.com/document.pdf" \
  --pretty
```

```bash
# 本地文件
uv run scripts/layout_caller.py \
  --file-path "./invoice.pdf" \
  --pretty
```

```bash
# 显式指定文件类型：0=PDF，1=Image
uv run scripts/layout_caller.py \
  --file-path "./invoice.pdf" \
  --file-type 0 \
  --pretty
```

```bash
# 指定输出文件
uv run scripts/layout_caller.py \
  --file-path "./invoice.pdf" \
  --output "./result_doc.json" \
  --pretty
```

## 输出结构

两个 Skill 都返回统一 envelope：

```json
{
  "ok": true,
  "text": "...",
  "result": { "...": "raw provider response" },
  "error": null
}
```

错误时：

```json
{
  "ok": false,
  "text": "",
  "result": null,
  "error": {
    "code": "CONFIG_ERROR",
    "message": "..."
  }
}
```

默认情况下，脚本会把完整 JSON 保存到系统临时目录，并在 stderr 打印 `Result saved to: ...`。如需直接输出到 stdout，添加 `--stdout`。

## CLI 方式（paddleocr api）

如果已经安装 `paddleocr` 包（`pip install "paddleocr>=3.7.0"`），可以直接用官方 CLI，无需 `uv run` 和本地脚本：

```bash
# 文本识别
paddleocr api --model_type ocr --file_path "./doc.pdf"

# 文档解析
paddleocr api --model_type doc_parsing --file_path "./doc.pdf"
```

常用选项：`--file_url` / `--file_path`、`--model`、`--page_ranges "1-5,10"`、`--use_doc_unwarping False`、`--output result.json`、（doc-parsing 专属）`--save_resources ./resources`、`--prettify_markdown True`。

### 与脚本的差异

| | 内置脚本 | `paddleocr` CLI |
| --- | --- | --- |
| 必填环境变量 | `PADDLEOCR_OCR_API_URL` 或 `PADDLEOCR_DOC_PARSING_API_URL` + `PADDLEOCR_ACCESS_TOKEN` | 仅 `PADDLEOCR_ACCESS_TOKEN` |
| 输出格式 | `{ok, text, result, error}` envelope | `{jobId, pages:[...]}` |
| 结果保存 | 默认写临时文件，stderr 打印路径 | 默认输出到 stdout |
| PDF 按页 | 用 `split_pdf.py` 预拆 | 原生 `--page_ranges` |

两种路径**输出不兼容**，切换时需同步调整解析逻辑。完整命令清单见各 SKILL.md 的「Alternative: paddleocr CLI」章节。

## 大文件快速处理

优先使用可访问 URL：

```bash
cd skills/paddleocr-doc-parsing
uv run scripts/layout_caller.py \
  --file-url "https://your-server.com/large.pdf" \
  --pretty
```

大图片先压缩：

```bash
cd skills/paddleocr-doc-parsing
uv run scripts/optimize_file.py large.png large_optimized.jpg --quality 80 --target-size 20
uv run scripts/layout_caller.py --file-path "./large_optimized.jpg" --pretty
```

大 PDF 按页拆分：

```bash
cd skills/paddleocr-doc-parsing
uv run scripts/split_pdf.py large.pdf first_10_pages.pdf --pages "1-10"
uv run scripts/layout_caller.py --file-path "./first_10_pages.pdf" --pretty
```

更多说明见 [LARGE_FILES.md](./LARGE_FILES.md)。
