# PaddleOCR-SKILLs

<p align="center">
  <strong>为 Claude Code 打造的多模型 OCR 技能套件</strong>
</p>

<p align="center">
  基于百度飞桨的智能文字提取与文档解析
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

## 🎯 两个技能，一套方案

本仓库提供两个互补的 OCR 技能，覆盖不同文档处理需求：

### 1. paddleocr-text-recognition - 快速文字提取

**适用于**：图片和 PDF 的文字识别

- ⚡ **快速识别** - 3 种质量模式（快速 / 高质量 / 自适应）
- 📝 **80+ 语言** - 全面的多语言支持
- 🎛️ **自适应质量** - 自动重试与渐进式质量增强
- 📊 **质量评分** - 内置识别置信度指标

**使用场景**：截图、扫描件等简单文档的快速文字提取

### 2. paddleocr-doc-parsing - 高级文档解析

**适用于**：包含表格、公式和复杂版式的文档

- 📊 **表格识别** - 从表格中提取结构化数据
- 🔢 **公式检测** - 识别数学公式（LaTeX 输出）
- 📐 **版面分析** - 自动检测文档结构
- 🌍 **109 种语言** - 增强的多语言能力
- 📄 **结构化输出** - JSON 或 Markdown 格式

**使用场景**：发票、学术论文、财务报表等复杂结构文档的解析

---

## 📦 安装部署

> **前置条件**：Node.js >= 14、Python 3.8+、[Claude Code CLI](https://claude.ai/code)

### 安装技能

安装所有技能：
```bash
npx skills add Aidenwu0209/PaddleOCR-Skills
```

安装特定技能：
```bash
# 仅文字识别
npx skills add Aidenwu0209/PaddleOCR-Skills --skill paddleocr-text-recognition

# 仅文档解析
npx skills add Aidenwu0209/PaddleOCR-Skills --skill paddleocr-doc-parsing
```

安装后，安装器会提示您选择要安装到哪些 AI 代理（Claude Code、Cursor、Cline 等）。

### 配置 API 凭证

前往 [Paddle AI Studio](https://paddleocr.com) 获取 API 凭证，然后进行配置：

**paddleocr-text-recognition：**
```bash
python ~/.claude/skills/paddleocr-text-recognition/scripts/configure.py
```

**paddleocr-doc-parsing：**
```bash
python ~/.claude/skills/paddleocr-doc-parsing/scripts/configure.py
```

<details>
<summary>备选：手动安装</summary>

```bash
git clone https://github.com/Aidenwu0209/PaddleOCR-Skills.git
cd PaddleOCR-Skills

# paddleocr-text-recognition
pip install -r skills/paddleocr-text-recognition/scripts/requirements.txt
python skills/paddleocr-text-recognition/scripts/configure.py

# paddleocr-doc-parsing
pip install -r skills/paddleocr-doc-parsing/scripts/requirements.txt
python skills/paddleocr-doc-parsing/scripts/configure.py
```

</details>

---

## 🚀 快速开始

安装完成后，用自然语言描述你的需求即可：

**简单文字提取**：
> "帮我识别这张图片的文字：screenshot.png"

Claude 会使用 **paddleocr-text-recognition** 进行快速文字识别。

**复杂文档解析**：
> "帮我解析这张发票的表格：invoice.pdf"

Claude 会使用 **paddleocr-doc-parsing** 进行结构化数据提取。

---

## 📊 功能对比

| 功能 | paddleocr-text-recognition | paddleocr-doc-parsing |
|------|:--------:|:------------:|
| **主要用途** | 文字提取 | 文档解析 |
| **速度** | 快速 ⚡ | 中等 🐢 |
| **语言数** | 80+ | 109 |
| **质量模式** | 3 种模式 | 自动 |
| **表格识别** | ❌ | ✅ |
| **公式检测** | ❌ | ✅ |
| **版面分析** | ❌ | ✅ |
| **输出格式** | 纯文本 + JSON | JSON / Markdown |
| **最佳场景** | 截图、扫描件 | 发票、论文 |

---

## 📚 文档

### paddleocr-text-recognition 文档
- [技能指南](./skills/paddleocr-text-recognition/SKILL.md) - 文字识别使用说明
- [输出规范](./skills/paddleocr-text-recognition/references/output_schema.md) - 输出格式定义
- [API 接口](./skills/paddleocr-text-recognition/references/provider_api.md) - API 详情

### paddleocr-doc-parsing 文档
- [技能指南](./skills/paddleocr-doc-parsing/SKILL.md) - 文档解析使用说明
- [输出规范](./skills/paddleocr-doc-parsing/references/output_schema.md) - 输出格式定义
- [API 接口](./skills/paddleocr-doc-parsing/references/provider_api.md) - API 详情

> **说明**：模型版本和能力由 API 端点决定。前往 [Paddle AI Studio](https://paddleocr.com) 获取最新 API。

---

## 🔍 如何选择技能？

```
┌─────────────────────────────────────┐
│  你需要提取什么内容？               │
└───────────┬─────────────────────────┘
            │
    ┌───────┴────────┐
    │  只需要文字？  │
    └───┬────────┬───┘
        │        │
       是       否
        │        │
        ▼        ▼
   text-       ┌──────────────────────┐
   recognition │ 表格 / 公式 /       │
               │ 复杂版面？          │
               └──────┬───────────────┘
                      │
                     是
                      │
                      ▼
                doc-parsing
```

### 快速选择指南

| 你的需求 | 推荐技能 |
|---------|---------|
| "帮我识别这张截图的文字" | **paddleocr-text-recognition** |
| "提取这份扫描文档的文字" | **paddleocr-text-recognition** |
| "解析这张发票的表格" | **paddleocr-doc-parsing** |
| "提取这份财务报表的数据" | **paddleocr-doc-parsing** |
| "识别这篇论文中的公式" | **paddleocr-doc-parsing** |
| "快速 OCR 这张照片" | **paddleocr-text-recognition** |

---

## 🧪 测试

**测试 paddleocr-text-recognition**：
```bash
python skills/paddleocr-text-recognition/scripts/smoke_test.py
```

**测试 paddleocr-doc-parsing**：
```bash
python skills/paddleocr-doc-parsing/scripts/smoke_test.py
```

---

## 💡 使用示例

### paddleocr-text-recognition 示例

**基础文字提取**：
```bash
python skills/paddleocr-text-recognition/scripts/ocr_caller.py --file-url "https://example.com/image.jpg" --pretty
```

**快速模式（清晰图片）**：
```bash
python skills/paddleocr-text-recognition/scripts/ocr_caller.py --file-path "screenshot.png" --preset fast
```

**高质量模式**：
```bash
python skills/paddleocr-text-recognition/scripts/ocr_caller.py --file-path "scan.pdf" --preset quality
```

### paddleocr-doc-parsing 示例

**解析含表格的文档**：
```bash
python skills/paddleocr-doc-parsing/scripts/vl_caller.py --file-path "invoice.pdf" --pretty
```

**导出为 Markdown**：
```bash
python skills/paddleocr-doc-parsing/scripts/vl_caller.py --file-url "URL" --format markdown --pretty
```

**保存结果到文件**：
```bash
python skills/paddleocr-doc-parsing/scripts/vl_caller.py --file-path "document.pdf" --output result.json
```

---

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

---

## 📄 许可证

[MIT License](./LICENSE)

---

## 🙏 致谢

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - 百度飞桨 OCR 项目
- [Paddle AI Studio](https://paddleocr.com) - API 服务提供

---

## 📮 支持

- **问题反馈**：[GitHub Issues](https://github.com/Aidenwu0209/PaddleOCR-SKILLs/issues)
- **文档**：查看 [skills](./skills/) directory
- **API 状态**：[Paddle AI Studio](https://paddleocr.com)

---

<p align="center">
  Made with ❤️ for Claude Code
</p>
