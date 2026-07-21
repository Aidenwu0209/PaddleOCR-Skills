# PaddleOCR Skills

[English](./README.md) | [简体中文](./README_cn.md)

这是一个从 [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/tree/main/skills)
官方 `skills/` 目录同步出来的独立仓库。

同步来源：`PaddlePaddle/PaddleOCR` commit `f0d83fafe9598134e5ac46aca62a4738f0eabac0`
（2026-05-06），已与上游 `main` HEAD `211989f0`（2026-06-26）核对。

> **上游在 [PR #18090](https://github.com/PaddlePaddle/PaddleOCR/pull/18090)（2026-06-03）对
> skills 做了重构** —— 删除了内置的 `scripts/` 与 `references/`，改用官方 `paddleocr api`
> CLI。**本镜像有意保留脚本版**（仍然可用，且通过 `uv` 离线友好），并额外补充 CLI 作为
> 备选路径。详见下文[两种运行方式](#两种运行方式)。

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

在本仓库根目录执行：

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
