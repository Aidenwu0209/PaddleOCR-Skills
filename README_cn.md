# PaddleOCR Skills

[English](./README.md) | [简体中文](./README_cn.md)

[![skills.sh](https://skills.sh/b/aidenwu0209/paddleocr-skills)](https://skills.sh/aidenwu0209/paddleocr-skills)

> **上游在 [PR #18090](https://github.com/PaddlePaddle/PaddleOCR/pull/18090)（2026-06-03）对
> skills 做了重构** —— 删除了内置的 `scripts/` 与 `references/`，改用官方 `paddleocr api`
> CLI。**本镜像有意保留脚本版**（仍然可用，且通过 `uv` 离线友好），并额外补充 CLI 作为
> 备选路径。详见下文[两种运行方式](#两种运行方式)。

## 发现与入口

- [skills.sh 收录页面](https://skills.sh/aidenwu0209/paddleocr-skills) —— 已有 **4.3K+ 次安装**，
  可用于多种 AI Agent。
- [PaddleOCR 官网](https://www.paddleocr.com) —— 获取 API、Token 与官方产品文档。
- [DeepSeek Harness GUI 版](https://github.com/Aidenwu0209/dsh-PaddleOCR-Skills) —— 提供原生
  Tool，以及可视化的 **Settings → PaddleOCR** 配置面板。

## 包含的 Skills

| Skill | 用途 | 入口脚本 |
| --- | --- | --- |
| `paddleocr-text-recognition` | 识别图片、扫描件、PDF 中的文字 | `ocr_caller.py` |
| `paddleocr-doc-parsing` | 将复杂文档解析为 Markdown / 结构化结果 | `layout_caller.py` |

## 两种运行方式

每个 Skill 都可以通过两种方式调用。**本镜像默认使用内置脚本**；**`paddleocr` CLI 是
#18090 引入的上游官方备选路径**。

| | 内置脚本（默认） | `paddleocr` CLI（备选） |
| --- | --- | --- |
| 安装 | 只需 `uv`，依赖通过 PEP 723 内联声明自动解析 | `pip install "paddleocr>=3.7.0"` |
| 必填环境变量 | 各 Skill 的 `PADDLEOCR_OCR_API_URL` / `PADDLEOCR_DOC_PARSING_API_URL` + `PADDLEOCR_ACCESS_TOKEN` | 仅 `PADDLEOCR_ACCESS_TOKEN`（端点由 CLI 内部解析） |
| 输出格式 | `{ok, text, result, error}` envelope，自动保存到临时文件 | `{jobId, pages:[...]}` 输出到 stdout |
| PDF 按页抽取 | 先用 `scripts/split_pdf.py` 预拆分 | 原生 `--page_ranges "1-5,10"` |
| 适用场景 | Skills 运行时、离线/隔离环境、不想额外安装 | 已经装有 `paddleocr`，或想用上游标准流程 |

> 两种路径的**输出结构不同**、**读取的环境变量也不同** —— 二者不兼容。每个工作流选其中一种即可。

每种方式的详细用法和分 Skill 示例见各自的 SKILL.md：

- [paddleocr-text-recognition/SKILL.md](./skills/paddleocr-text-recognition/SKILL.md)
- [paddleocr-doc-parsing/SKILL.md](./skills/paddleocr-doc-parsing/SKILL.md)

## 环境要求

- Python 3.9 或以上版本
- [`uv`](https://docs.astral.sh/uv/)
- 可访问网络
- 从 [paddleocr.com](https://www.paddleocr.com) 获取 PaddleOCR 官方 API 凭证

脚本已经通过 PEP 723 内联声明依赖，因此不再需要单独安装 `requirements.txt`。

## 配置

按需配置对应 Skill 的环境变量：

| Skill | 必填 | 可选 |
| --- | --- | --- |
| `paddleocr-text-recognition` | 以 `/ocr` 结尾的 `PADDLEOCR_OCR_API_URL`、`PADDLEOCR_ACCESS_TOKEN` | `PADDLEOCR_OCR_TIMEOUT` |
| `paddleocr-doc-parsing` | 以 `/layout-parsing` 结尾的 `PADDLEOCR_DOC_PARSING_API_URL`、`PADDLEOCR_ACCESS_TOKEN` | `PADDLEOCR_DOC_PARSING_TIMEOUT` |

> 上表中的 `PADDLEOCR_*_API_URL` 环境变量**仅内置脚本需要**。如果改用 `paddleocr` CLI，
> 只需 `PADDLEOCR_ACCESS_TOKEN` —— 详见各 SKILL.md 中的「Alternative: paddleocr CLI」章节。

## 本地使用

请在对应 Skill 目录下执行命令。

```shell
cd skills/paddleocr-text-recognition
uv run scripts/ocr_caller.py --file-path "/path/to/image-or-document.pdf" --pretty
```

```shell
cd skills/paddleocr-doc-parsing
uv run scripts/layout_caller.py --file-path "/path/to/document.pdf" --pretty
```

## 安装到 AI 应用

### 一段 Prompt 安装（最简单）

把下面整段复制给 Codex、Claude Code、Cursor、OpenCode、OpenClaw，或其他可以操作终端的 AI Agent：

```text
请在这台电脑上安装 https://github.com/Aidenwu0209/PaddleOCR-Skills 中的两个 Agent Skill。
1. 识别当前支持的 Agent，并检查 Node.js/npx、Python 3.9+ 和 uv。如果缺少依赖，先解释用途并只使用官方安装方式；未经我允许不要使用 sudo 或修改无关系统设置。
2. 为检测到的 Agent 执行：npx skills add Aidenwu0209/PaddleOCR-Skills --skill '*' -g -y
3. 执行 npx skills list -g --json，确认 paddleocr-text-recognition 和 paddleocr-doc-parsing 都已出现。
4. 不要编造、显示或记录 PaddleOCR Token。在凭据配置步骤停下来，向我展示官方 https://www.paddleocr.com 链接，并明确告诉我还需要填写哪些 API 地址和 Token。
5. 汇报实际执行的命令、安装路径与验证结果。
```

通过 [skills.sh CLI](https://skills.sh/docs/cli) 交互选择 Skill 和目标 Agent：

```shell
npx skills add Aidenwu0209/PaddleOCR-Skills
```

也可以将仓库内两个 Skill 全局安装到指定 Agent：

| Agent | 命令 |
| --- | --- |
| Codex | `npx skills add Aidenwu0209/PaddleOCR-Skills --agent codex --skill '*' -g -y` |
| Claude Code | `npx skills add Aidenwu0209/PaddleOCR-Skills --agent claude-code --skill '*' -g -y` |
| GitHub Copilot | `npx skills add Aidenwu0209/PaddleOCR-Skills --agent github-copilot --skill '*' -g -y` |
| OpenClaw | `npx skills add Aidenwu0209/PaddleOCR-Skills --agent openclaw --skill '*' -g -y` |

GitHub CLI 2.90.0 以上版本还支持原生 Agent Skills 安装：

```shell
gh skill install Aidenwu0209/PaddleOCR-Skills --all --agent github-copilot --scope user
```

如需在 Claude Code 中开发或本地测试插件，可克隆仓库并加载
[`plugin.json`](./.claude-plugin/plugin.json)：

```shell
git clone https://github.com/Aidenwu0209/PaddleOCR-Skills.git
claude --plugin-dir ./PaddleOCR-Skills
```

如需从本地检出目录直接安装：

```shell
npx skills add ./skills/paddleocr-text-recognition -g -y
npx skills add ./skills/paddleocr-doc-parsing -g -y
```

或者通过 OpenClaw 安装：

```shell
clawhub install paddleocr-text-recognition
clawhub install paddleocr-doc-parsing
```

## 文档

- 官方英文文档镜像：[docs/version3.x/deployment/skills.en.md](./docs/version3.x/deployment/skills.en.md)
- 官方中文文档镜像：[docs/version3.x/deployment/skills.md](./docs/version3.x/deployment/skills.md)
- 快速参考：[docs/QUICK_REFERENCE.md](./docs/QUICK_REFERENCE.md)
- 大文件处理指南：[docs/LARGE_FILES.md](./docs/LARGE_FILES.md)

## License

Apache-2.0。详见 [LICENSE](./LICENSE)。
