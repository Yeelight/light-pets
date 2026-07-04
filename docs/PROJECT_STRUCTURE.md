# Project Structure

本项目把“可安装资源”、“机器索引”、“展示 demo”和“构建脚本”分开，避免把 batch 产物、运行时安装文件和展示页面混在一起。

## 根目录

```text
README.md
LICENSE
CONTRIBUTING.md
requirements.txt
assets/
catalog/
collections/
demo/
docs/
packages/
qa/
scripts/
```

## `packages/`

`packages/` 是公开可安装包目录。每只 pet 使用扁平目录：

```text
packages/<pet-id>/
├── README.md
├── pet.json
├── spritesheet.webp
└── spritesheet.png
```

安装运行时只需要 `pet.json` 和 `spritesheet.webp`。

## `qa/`

`qa/` 是公开复核目录，每只 pet 对应一个 QA 目录：

```text
qa/<pet-id>/
├── contact-sheet.png
├── preview-dark-grid.png
├── validation.json
├── review.json
├── run-summary.json
└── previews/*.gif
```

## `catalog/`

`catalog/pets.json` 是统一索引，供 demo、脚本和外部用户读取。

`catalog/collections.json` 是 collection 索引，记录 collection 元信息和成员 pet id。

## `collections/`

`collections/<collection-id>/README.md` 是 collection 级说明文档，适合 GitHub 页面浏览。

## `demo/`

`demo/index.html` 是无需构建工具即可打开的静态页面。它不依赖远程 CDN，所有图片都从本仓库相对路径读取。

## `assets/`

`assets/overviews/` 存放 collection 总览图。

## `resources/`

`resources/` 是维护者本地原始资料目录，已被 `.gitignore` 排除。公开仓库提交的是归一化后的 `packages/`、`qa/`、`catalog/`、`collections/`、`assets/` 和 `demo/`。

## `scripts/`

`scripts/build_project.py` 是主构建入口，负责：

- 从本地原始资料生成规范化公开目录
- 生成 `catalog/*.json`
- 生成 `demo/index.html` 和 `collections/*/README.md`

公开仓库没有 `resources/` 时，构建脚本会使用已提交的 `catalog/`、`packages/` 和 `qa/` 重建 demo 与 collection 文档。

`scripts/validate_project.py` 是发布前校验入口，负责检查公开仓库所需文件、atlas 尺寸和 demo/card 数量一致性。
