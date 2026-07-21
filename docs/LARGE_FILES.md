# 大文件处理指南（paddleocr-doc-parsing）

本指南针对 `skills/paddleocr-doc-parsing/scripts/layout_caller.py`。

> **关于 `paddleocr` CLI 用户**：本文档的命令面向内置脚本路径。若改用官方 `paddleocr api`
> CLI，部分步骤可简化：
> - **按页抽取**：CLI 原生支持 `--page_ranges "1-5,10"`，多数情况下可直接替代
>   `split_pdf.py`，无需先拆分文件。
> - **图片压缩**：`optimize_file.py` 与 CLI 路径无关，仍可在上传前用于压缩超大图片。
> - **大文件**：CLI 同样支持 `--file_url`（参数名为下划线），优先用它避免 base64 开销。
>
> CLI 与脚本的输出格式和所需环境变量不同，详见各 SKILL.md 的「Alternative: paddleocr
> CLI」章节。

## 核心建议

1. 优先使用 `--file-url`，让服务端直接拉取文件，避免本地文件转 base64 的开销。
2. 本地大图片先用 `optimize_file.py` 压缩。
3. 大 PDF 先用 `split_pdf.py` 抽取需要的页，再调用解析。

## 方案 A：使用 URL（首选）

```bash
cd skills/paddleocr-doc-parsing
uv run scripts/layout_caller.py \
  --file-url "https://your-server.com/large_document.pdf" \
  --pretty
```

适用场景：

- 文件较大
- 本地上传慢
- 已有服务可访问的文件链接

## 方案 B：压缩大图片

`optimize_file.py` 通过 PEP 723 内联声明依赖，直接用 `uv run` 执行即可。

```bash
cd skills/paddleocr-doc-parsing
uv run scripts/optimize_file.py \
  input.png \
  output.jpg \
  --quality 80 \
  --target-size 20
```

解析压缩后的文件：

```bash
uv run scripts/layout_caller.py \
  --file-path "./output.jpg" \
  --pretty
```

调参建议：

- `--quality` 越低，体积越小，通常建议 70-90。
- `--target-size` 控制目标体积，单位 MB。

## 方案 C：拆分大 PDF 后解析

```bash
cd skills/paddleocr-doc-parsing
uv run scripts/split_pdf.py large.pdf selected_pages.pdf --pages "1-5,8,10-12"
```

解析拆分后的 PDF：

```bash
uv run scripts/layout_caller.py \
  --file-path "./selected_pages.pdf" \
  --pretty
```

## CLI 选项速查

`layout_caller.py` 常用参数：

```bash
--file-url "..."      # 与 --file-path 二选一
--file-path "..."     # 与 --file-url 二选一
--file-type 0|1       # 可选，0=PDF，1=Image
--pretty              # 美化 JSON
--output result.json  # 保存到指定 JSON 文件
--stdout              # 直接输出 JSON，不保存文件
```

本地文件如果扩展名不是 `.pdf`、`.png`、`.jpg`、`.jpeg`、`.bmp`、`.tiff`、`.tif` 或 `.webp`，请显式传入 `--file-type`。

## 结果格式

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

默认情况下，脚本会把完整 JSON 保存到系统临时目录，并在 stderr 打印 `Result saved to: ...`。指定 `--output` 可改写保存位置；指定 `--stdout` 可直接输出到 stdout。

## 常见问题

### 认证失败（401/403）

检查 `PADDLEOCR_ACCESS_TOKEN` 是否正确，并确认 `PADDLEOCR_DOC_PARSING_API_URL` 是以 `/layout-parsing` 结尾的完整端点 URL。

### 请求超时

增大文档解析超时时间：

```bash
export PADDLEOCR_DOC_PARSING_TIMEOUT=900
```

### 结果文件过大

使用 `--output` 写入 JSON 文件，避免终端滚屏：

```bash
cd skills/paddleocr-doc-parsing
uv run scripts/layout_caller.py \
  --file-path "./document.pdf" \
  --output "./result.json" \
  --pretty
```

## 关联文档

- [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- [skills/paddleocr-doc-parsing/SKILL.md](../skills/paddleocr-doc-parsing/SKILL.md)
- [官方中文文档镜像](./version3.x/deployment/skills.md)
