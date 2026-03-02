# PaddleOCR Skills 快速参考

## 技能选择

| 需求 | 推荐技能 | 命令 |
|------|----------|------|
| 快速提取文本（截图、照片、扫描件） | `paddleocr-text-recognition` | `ocr_caller.py` |
| 解析复杂文档（多栏、表格、图文混排） | `paddleocr-doc-parsing` | `vl_caller.py` |

---

## 常用命令

### 1) 配置凭证

```bash
python skills/paddleocr-text-recognition/scripts/configure.py
python skills/paddleocr-doc-parsing/scripts/configure.py
```

### 2) 冒烟测试

```bash
python skills/paddleocr-text-recognition/scripts/smoke_test.py --skip-api-test
python skills/paddleocr-doc-parsing/scripts/smoke_test.py --skip-api-test
```

### 3) 文本识别

```bash
# URL
python skills/paddleocr-text-recognition/scripts/ocr_caller.py \
  --file-url "https://example.com/image.jpg" \
  --pretty

# 本地文件
python skills/paddleocr-text-recognition/scripts/ocr_caller.py \
  --file-path "./doc.pdf" \
  --pretty

# 输出到 JSON 文件
python skills/paddleocr-text-recognition/scripts/ocr_caller.py \
  --file-path "./doc.pdf" \
  --output "./result_text.json" \
  --pretty
```

### 4) 文档解析

```bash
# URL
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-url "https://example.com/document.pdf" \
  --pretty

# 本地文件
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-path "./invoice.pdf" \
  --pretty

# 显式指定文件类型（可选）
# --file-type 0: PDF
# --file-type 1: Image
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-path "./invoice.pdf" \
  --file-type 0 \
  --pretty

# 输出到 JSON 文件
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-path "./invoice.pdf" \
  --output "./result_doc.json" \
  --pretty
```

---

## 输出结构（两个技能一致）

```json
{
  "ok": true,
  "text": "...",
  "result": { "...": "raw response" },
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

---

## 大文件快速处理

### 优先方案：`--file-url`

```bash
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-url "https://your-server.com/large.pdf" \
  --pretty
```

### 大图片压缩（仅图片）

> `optimize_file.py` 仅支持图片格式：PNG/JPG/JPEG/BMP/TIFF/TIF

```bash
pip install -r skills/paddleocr-doc-parsing/scripts/requirements-optimize.txt

python skills/paddleocr-doc-parsing/scripts/optimize_file.py \
  large.png \
  large_optimized.jpg \
  --quality 80 \
  --target-size 20

python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-path "./large_optimized.jpg" \
  --pretty
```

### 大 PDF 按页拆分后再解析

```bash
pip install pypdfium2

python -c "import pypdfium2 as pdfium; d=pdfium.PdfDocument('large.pdf'); n=pdfium.PdfDocument.new(); n.import_pages(d, list(range(min(10, len(d))))); n.save('first_10_pages.pdf')"

python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-path "./first_10_pages.pdf" \
  --pretty
```

更多说明见：[LARGE_FILES.md](./LARGE_FILES.md)
