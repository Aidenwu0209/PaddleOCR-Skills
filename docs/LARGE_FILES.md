# 大文件处理指南（paddleocr-doc-parsing）

本指南针对 `skills/paddleocr-doc-parsing/scripts/vl_caller.py`。

---

## 核心建议

1. 优先使用 `--file-url`
- 服务端直接拉取文件，避免本地文件转 base64 的开销。

2. 本地大图片先压缩
- 使用 `optimize_file.py` 将图片压缩到目标体积。

3. 大 PDF 先按页拆分
- 先抽取需要的页，再调用解析，提升成功率和速度。

---

## 方案 A：使用 URL（首选）

```bash
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-url "https://your-server.com/large_document.pdf" \
  --pretty
```

适用场景：
- 文件较大
- 本地上传慢
- 已有可访问链接

---

## 方案 B：压缩大图片

> 仅支持图片输入：`PNG/JPG/JPEG/BMP/TIFF/TIF`

安装依赖：

```bash
pip install -r skills/paddleocr-doc-parsing/scripts/requirements-optimize.txt
```

压缩图片：

```bash
python skills/paddleocr-doc-parsing/scripts/optimize_file.py \
  input.png \
  output.jpg \
  --quality 80 \
  --target-size 20
```

解析压缩后的文件：

```bash
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-path "./output.jpg" \
  --pretty
```

调参建议：
- `--quality` 越低，体积越小（建议 70~90）
- `--target-size` 控制目标体积（MB）

---

## 方案 C：拆分大 PDF 后解析

安装依赖：

```bash
pip install pypdfium2
```

示例：抽取前 10 页为新文件

```bash
python -c "import pypdfium2 as pdfium; d=pdfium.PdfDocument('large.pdf'); n=pdfium.PdfDocument.new(); n.import_pages(d, list(range(min(10, len(d))))); n.save('first_10_pages.pdf')"
```

解析拆分后的 PDF：

```bash
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-path "./first_10_pages.pdf" \
  --pretty
```

---

## CLI 选项速查

`vl_caller.py` 当前有效参数：

```bash
--file-url "..."      # 与 --file-path 二选一
--file-path "..."     # 与 --file-url 二选一
--file-type 0|1        # 可选，0=PDF，1=Image
--pretty               # 美化 JSON 输出
--output result.json   # 保存到文件
```

---

## 结果格式

`vl_caller.py` 输出统一结构：

```json
{
  "ok": true,
  "text": "...",
  "result": { "...": "raw provider response" },
  "error": null
}
```

错误示例：

```json
{
  "ok": false,
  "text": "",
  "result": null,
  "error": {
    "code": "API_ERROR",
    "message": "Authentication failed (403). Check your token."
  }
}
```

---

## 常见问题

### 1) 认证失败（401/403）
- 检查 `PADDLEOCR_ACCESS_TOKEN` 是否正确。
- 重新执行：

```bash
python skills/paddleocr-doc-parsing/scripts/configure.py
```

### 2) 请求超时
- 增大文档解析超时：

```bash
# .env
PADDLEOCR_DOC_PARSING_TIMEOUT=900
```

### 3) 结果文件过大
- 使用 `--output` 写入 JSON 文件，避免终端滚屏。

```bash
python skills/paddleocr-doc-parsing/scripts/vl_caller.py \
  --file-path "./document.pdf" \
  --output "./result.json" \
  --pretty
```

---

## 关联文档

- [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- [skills/paddleocr-doc-parsing/SKILL.md](../skills/paddleocr-doc-parsing/SKILL.md)
