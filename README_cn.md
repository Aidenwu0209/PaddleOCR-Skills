# PaddleOCR Skills

[English](./README.md) | [简体中文](./README_cn.md)

这是一个从 [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/tree/main/skills)
官方 `skills/` 目录同步出来的独立仓库。

同步来源：`PaddlePaddle/PaddleOCR` commit `f0d83fafe9598134e5ac46aca62a4738f0eabac0`
（2026-05-06）。

## 包含的 Skills

| Skill | 用途 | 入口脚本 |
| --- | --- | --- |
| `paddleocr-text-recognition` | 识别图片、扫描件、PDF 中的文字 | `ocr_caller.py` |
| `paddleocr-doc-parsing` | 将复杂文档解析为 Markdown / 结构化结果 | `layout_caller.py` |

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
