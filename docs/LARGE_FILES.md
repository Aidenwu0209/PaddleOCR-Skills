# 大文件处理指南 - PaddleOCR-VL

## 问题说明

当你尝试处理大于20MB的本地文件时，会遇到错误：
```
File too large: 25.3MB (max 20MB). Use --file-url or increase VL_MAX_FILE_SIZE_MB
```

这是为了防止上传超大文件导致超时或内存问题。

---

## 🚀 快速解决方案

### 方案1️⃣: 使用URL（最简单）⭐ 推荐

**适用场景**: 任何大小的文件

```bash
# 步骤1: 上传文件到任何可访问的URL
# - 你的网站服务器
# - 云存储（S3, Google Drive, 阿里云OSS等）
# - 临时文件分享服务

# 步骤2: 使用URL处理
python scripts/paddleocr-vl/vl_caller.py \
  --file-url "https://your-server.com/large_document.pdf" \
  --pretty
```

**优势**:
- ✅ 无大小限制
- ✅ 无需本地上传
- ✅ API服务器直接下载（更快）
- ✅ 适合超大文件（>100MB）

---

### 方案2️⃣: 提高大小限制（最快）

**适用场景**: 文件只是稍微超过20MB（如25-40MB）

```bash
# 编辑 .env 文件
echo "VL_MAX_FILE_SIZE_MB=50" >> .env

# 或者设置环境变量
export VL_MAX_FILE_SIZE_MB=50  # Linux/Mac
set VL_MAX_FILE_SIZE_MB=50     # Windows CMD
$env:VL_MAX_FILE_SIZE_MB=50    # Windows PowerShell

# 然后正常处理
python scripts/paddleocr-vl/vl_caller.py --file-path "large_file.pdf"
```

**注意**: API服务器可能仍有上传限制，请咨询你的VL API提供商。

---

### 方案3️⃣: 压缩优化（最彻底）⭐ 推荐

**适用场景**: 图片质量要求不极端高，或PDF包含大量图片

#### 安装依赖
```bash
pip install -r scripts/paddleocr-vl/requirements-optimize.txt
# 安装 Pillow (图片) 和 PyMuPDF (PDF)
```

#### 优化图片
```bash
# 基础压缩（质量85，通常足够）
python scripts/paddleocr-vl/optimize_file.py \
  input.png \
  output.png

# 高压缩（质量70，更小但仍可读）
python scripts/paddleocr-vl/optimize_file.py \
  input.jpg \
  output.jpg \
  --quality 70

# 目标特定大小
python scripts/paddleocr-vl/optimize_file.py \
  input.tiff \
  output.jpg \
  --target-size 15  # 目标15MB
```

**效果示例**:
```
Original size: 35.2MB
Original dimensions: 4000x3000
Optimized size: 12.8MB
Reduction: 63.6%
```

#### 优化PDF
```bash
# 压缩PDF（降低图片DPI）
python scripts/paddleocr-vl/optimize_file.py \
  input.pdf \
  output.pdf \
  --target-size 18

# 处理优化后的文件
python scripts/paddleocr-vl/vl_caller.py \
  --file-path "output.pdf" \
  --pretty
```

**PDF优化原理**:
- 将PDF中的图片降低到150 DPI
- 应用最大压缩
- 清理元数据
- 通常可减少50-70%大小

---

### 方案4️⃣: 提取特定页面

**适用场景**: 大PDF文档，只需要部分页面

#### 使用Python脚本
```python
import fitz  # PyMuPDF

# 打开PDF
doc = fitz.open('large_document.pdf')

# 提取特定页面（例如第1-10页）
writer = fitz.open()
writer.insert_pdf(doc, from_page=0, to_page=9)  # 0-based index
writer.save('pages_1_10.pdf')
writer.close()
doc.close()
```

#### 一行命令
```bash
python -c "import fitz; doc=fitz.open('large.pdf'); w=fitz.open(); w.insert_pdf(doc,0,9); w.save('extract.pdf')"
```

#### 然后处理提取的页面
```bash
python scripts/paddleocr-vl/vl_caller.py --file-path "extract.pdf"
```

---

### 方案5️⃣: 使用云存储

**适用场景**: 超大文件（>100MB）或需要长期存储

#### AWS S3 示例
```bash
# 上传到S3
aws s3 cp large_file.pdf s3://your-bucket/documents/ --acl public-read

# 获取公共URL
# https://your-bucket.s3.amazonaws.com/documents/large_file.pdf

# 处理
python scripts/paddleocr-vl/vl_caller.py \
  --file-url "https://your-bucket.s3.amazonaws.com/documents/large_file.pdf"
```

#### 阿里云OSS示例
```bash
# 上传到OSS
ossutil cp large_file.pdf oss://your-bucket/documents/

# 获取URL（配置公共读）
# https://your-bucket.oss-cn-beijing.aliyuncs.com/documents/large_file.pdf

# 处理
python scripts/paddleocr-vl/vl_caller.py \
  --file-url "https://your-bucket.oss-cn-beijing.aliyuncs.com/documents/large_file.pdf"
```

---

## 📊 方案对比

| 方案 | 最大文件 | 处理时间 | 需要工具 | 复杂度 | 推荐场景 |
|------|---------|---------|----------|-------|---------|
| **URL上传** | ∞ | 快 | 网盘/服务器 | 低 | 任何大文件 ⭐ |
| **提高限制** | 可配置 | 中 | 无 | 极低 | 稍超限（25-40MB） |
| **压缩优化** | 减少70% | 慢 | Pillow/PyMuPDF | 中 | 图片/PDF优化 ⭐ |
| **提取页面** | 灵活 | 快 | PyMuPDF | 低 | 大PDF部分处理 |
| **云存储** | ∞ | 快 | 云服务账户 | 高 | 超大文件(>100MB) |

---

## 🛠️ 实战示例

### 示例1: 30MB的扫描PDF

**问题**: 发票扫描PDF，30MB

```bash
# 方案A: 压缩优化（推荐）
pip install PyMuPDF
python scripts/paddleocr-vl/optimize_file.py invoice.pdf invoice_compressed.pdf
python scripts/paddleocr-vl/vl_caller.py --file-path "invoice_compressed.pdf"

# 方案B: 提高限制
echo "VL_MAX_FILE_SIZE_MB=35" >> .env
python scripts/paddleocr-vl/vl_caller.py --file-path "invoice.pdf"
```

### 示例2: 50MB的高清产品图

**问题**: 产品手册图片，50MB PNG

```bash
# 方案A: 压缩为JPEG（大幅减少）
pip install Pillow
python scripts/paddleocr-vl/optimize_file.py product.png product.jpg --quality 85
# 结果: 通常减少到5-10MB

# 方案B: 上传到图床
# 上传到 imgur.com, imgbb.com 等
# 然后使用返回的URL
```

### 示例3: 150MB的技术白皮书

**问题**: 多页技术文档，150MB

```bash
# 方案A: 上传到云（最佳）
# 1. 上传到云存储获取URL
# 2. 直接处理
python scripts/paddleocr-vl/vl_caller.py --file-url "https://storage/whitepaper.pdf"

# 方案B: 提取关键页面
python -c "import fitz; doc=fitz.open('whitepaper.pdf'); w=fitz.open(); w.insert_pdf(doc,0,19); w.save('first20pages.pdf')"
python scripts/paddleocr-vl/vl_caller.py --file-path "first20pages.pdf"
```

---

## 🔧 故障排查

### 问题1: 压缩后仍然太大

```bash
# 尝试更低的质量
python scripts/paddleocr-vl/optimize_file.py input.jpg output.jpg --quality 60

# 或更小的目标尺寸
python scripts/paddleocr-vl/optimize_file.py input.pdf output.pdf --target-size 10
```

### 问题2: 优化工具报错 "Pillow not installed"

```bash
# 安装完整依赖
pip install -r scripts/paddleocr-vl/requirements-optimize.txt

# 或单独安装
pip install Pillow PyMuPDF
```

### 问题3: URL上传仍失败

**原因**: API服务器可能也有大小限制

**解决**:
1. 联系API提供商确认限制
2. 使用压缩方案先减小文件
3. 分页处理（PDF）

### 问题4: 压缩后识别质量下降

```bash
# 使用更高的质量（牺牲文件大小）
python scripts/paddleocr-vl/optimize_file.py input.jpg output.jpg --quality 90

# 或使用无损格式
# PNG → PNG (只优化，不降质量)
```

---

## 📝 最佳实践

### 1. 优先使用URL
对于生产环境，始终推荐上传到稳定的URL：
- 减少本地上传时间
- 避免超时问题
- 便于批量处理

### 2. 合理设置限制
根据实际API限制设置：
```bash
# .env
VL_MAX_FILE_SIZE_MB=50  # 根据你的API调整
```

### 3. 自动化压缩
在工作流中集成自动压缩：
```bash
#!/bin/bash
# process_document.sh
OPTIMIZED="optimized_$1"
python scripts/paddleocr-vl/optimize_file.py "$1" "$OPTIMIZED"
python scripts/paddleocr-vl/vl_caller.py --file-path "$OPTIMIZED" --pretty
rm "$OPTIMIZED"  # 清理
```

### 4. 监控文件大小
处理前检查：
```python
import os
size_mb = os.path.getsize('file.pdf') / 1024 / 1024
if size_mb > 20:
    print(f"Warning: File is {size_mb:.1f}MB, consider optimization")
```

---

## 🆘 需要帮助？

如果遇到问题：

1. **检查配置**: `cat .env | grep VL_MAX`
2. **查看日志**: 使用 `--log-level DEBUG` 查看详细信息
3. **测试API**: 运行 `python scripts/paddleocr-vl/smoke_test.py`
4. **联系支持**: 咨询你的VL API服务提供商关于上传限制

---

**记住**: 大多数情况下，使用URL上传或压缩优化就能完美解决问题！⭐
