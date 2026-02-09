# PaddleOCR-VL 快速参考卡片

## 🚨 大文件问题？

文件大于20MB？选择最适合你的方案：

```
┌─────────────────────────────────────────────────┐
│ 你的情况是？                                      │
├─────────────────────────────────────────────────┤
│                                                 │
│ □ 文件可以上传到网上                             │
│   → 使用 --file-url (最简单！)                   │
│   → 无大小限制                                   │
│                                                 │
│ □ 文件只是稍微超限（25-40MB）                     │
│   → 设置 VL_MAX_FILE_SIZE_MB=50                 │
│   → 30秒解决                                    │
│                                                 │
│ □ 图片或PDF包含图片                              │
│   → 使用优化工具                                 │
│   → 通常减少50-70%                              │
│                                                 │
│ □ 大PDF但只需部分页面                            │
│   → 提取特定页面                                 │
│   → 按需处理                                    │
│                                                 │
│ □ 超大文件 (>100MB)                             │
│   → 上传云存储                                  │
│   → 使用公共URL                                 │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## ⚡ 1分钟解决方案

### 方案A: URL上传（90%的情况适用）

```bash
# 上传到任何可访问URL
# 然后：
python scripts/paddleocr-vl/vl_caller.py \
  --file-url "https://your-url/file.pdf"
```

### 方案B: 提高限制（最快）

```bash
echo "VL_MAX_FILE_SIZE_MB=50" >> .env
# 完成！
```

### 方案C: 压缩文件（最彻底）

```bash
# 安装（仅需一次）
pip install Pillow PyMuPDF

# 优化
python scripts/paddleocr-vl/optimize_file.py input.pdf output.pdf

# 处理
python scripts/paddleocr-vl/vl_caller.py --file-path output.pdf
```

---

## 📋 命令速查

### 基本使用
```bash
# 处理URL文件
python scripts/paddleocr-vl/vl_caller.py --file-url "URL"

# 处理本地文件
python scripts/paddleocr-vl/vl_caller.py --file-path "file.pdf"

# 显示质量评估
python scripts/paddleocr-vl/vl_caller.py --file-path "file.pdf" --show-quality

# 禁用缓存
python scripts/paddleocr-vl/vl_caller.py --file-path "file.pdf" --no-cache
```

### 文件优化
```bash
# 压缩图片（质量85）
python scripts/paddleocr-vl/optimize_file.py input.png output.png

# 高压缩（质量70）
python scripts/paddleocr-vl/optimize_file.py input.jpg output.jpg --quality 70

# 压缩PDF
python scripts/paddleocr-vl/optimize_file.py input.pdf output.pdf

# 目标特定大小（15MB）
python scripts/paddleocr-vl/optimize_file.py input.pdf output.pdf --target-size 15
```

### 配置管理
```bash
# 初次配置
python scripts/paddleocr-vl/configure.py

# 测试配置
python scripts/paddleocr-vl/smoke_test.py

# 修改大小限制
echo "VL_MAX_FILE_SIZE_MB=50" >> .env
```

---

## 🎯 决策树

```
文件大小？
  │
  ├─ ≤20MB
  │   └─ 直接处理 ✓
  │
  ├─ 20-40MB
  │   ├─ 有URL？
  │   │   └─ 用 --file-url ⭐
  │   └─ 无URL？
  │       ├─ 能压缩？用优化工具
  │       └─ 不能压缩？提高限制
  │
  ├─ 40-100MB
  │   ├─ PDF？
  │   │   ├─ 提取部分页面
  │   │   └─ 压缩优化
  │   └─ 图片？
  │       └─ 压缩优化（效果明显）
  │
  └─ >100MB
      └─ 上传云存储 + URL ⭐
```

---

## 💡 常见场景

### 场景1: 30MB 发票PDF
```bash
# 最佳方案：压缩
python scripts/paddleocr-vl/optimize_file.py invoice.pdf invoice_small.pdf
# 结果：通常 8-12MB
```

### 场景2: 50MB 产品图片
```bash
# 最佳方案：转JPEG + 压缩
python scripts/paddleocr-vl/optimize_file.py product.png product.jpg --quality 80
# 结果：通常 5-10MB
```

### 场景3: 150MB 技术文档
```bash
# 最佳方案：上传URL
# 1. 上传到云存储
# 2. 获取公共URL
# 3. 处理：
python scripts/paddleocr-vl/vl_caller.py --file-url "https://storage/doc.pdf"
```

---

## 🔍 故障排查

### 问题：仍然显示文件太大
```bash
# 检查配置
cat .env | grep VL_MAX

# 如果没有，添加：
echo "VL_MAX_FILE_SIZE_MB=50" >> .env
```

### 问题：优化工具报错
```bash
# 安装依赖
pip install -r scripts/paddleocr-vl/requirements-optimize.txt
```

### 问题：压缩后质量下降
```bash
# 使用更高质量
python scripts/paddleocr-vl/optimize_file.py input.jpg output.jpg --quality 90
```

### 问题：URL也失败
原因：API服务器也有限制
解决：先压缩，再上传URL

---

## 📞 获取帮助

详细文档：[docs/LARGE_FILES.md](./LARGE_FILES.md)

---

**记住这三招就够了**：
1. **有URL？用URL！** 🌐
2. **能压缩？压缩！** 📦
3. **不行？提限制！** ⚙️
