# Light Pets

Light Pets 是一组可安装的 Codex hatch pets 资源集合，主题来自智能照明设备的形态、材质和状态语义。当前公开目录包含 82 只 pet：

- 5 只精选单宠：补齐了 README、PNG 备份、QA、状态 GIF、验证结果和设计提示。
- 12 只 Yeelight residential batch pets：已整理到 `packages/` 和 `qa/`。
- 65 只 Yeelight Pro batch pets：已整理到 `packages/` 和 `qa/`。

![Light Pets overview](assets/overviews/yeelight-hatch-pet-full-batch.png)

## 快速查看

直接打开本地 demo：

```bash
open "demo/index.html"
```

或用任意静态服务器预览：

```bash
python3 -m http.server 8080
```

然后访问 `http://localhost:8080/demo/`。

## 安装单只 pet

每只 pet 的可安装包只需要两个文件：

```text
pet.json
spritesheet.webp
```

把某个 pet 目录里的这两个文件复制到 Codex 自定义 pet 目录即可。`spritesheet.png`、`qa/`、`validation.json` 等文件用于复核与展示，不是运行时必需文件。

## 项目结构

```text
.
├── catalog/                  # 机器可读的统一索引
├── collections/              # collection 级说明文档
├── demo/                     # 静态 HTML 展示页
├── docs/                     # 资产契约、目录规范和发布说明
├── packages/                 # 可安装 pet 包
├── qa/                       # contact sheet、状态 GIF、验证结果
├── assets/overviews/         # collection 总览图
├── scripts/                  # 构建与校验脚本
└── .github/workflows/        # GitHub Actions 校验
```

更详细的目录约定见 [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)。

## 资源契约

所有 pet 遵循同一个 hatch-pet atlas 契约：

- atlas：`1536 x 1872`
- 网格：`8 列 x 9 行`
- 单元格：`192 x 208`
- 状态顺序：`idle`、`running-right`、`running-left`、`waving`、`jumping`、`failed`、`waiting`、`running`、`review`

完整契约见 [docs/ASSET_CONTRACT.md](docs/ASSET_CONTRACT.md)。

## 构建与验证

安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

重新生成 catalog、demo 和 collection 文档：

```bash
python3 scripts/build_project.py
```

也可以使用 Makefile：

```bash
make smoke
```

维护者本地如果保留了被忽略的 `resources/` 原始资料，脚本会从原始资料重新归一化输出；公开仓库克隆中没有 `resources/` 时，脚本会用已提交的 `catalog/`、`packages/` 和 `qa/` 重建 demo 与文档。

验证公开发布面：

```bash
python3 scripts/validate_project.py
```

## 开源与商标说明

本仓库提交的是整理后的公开资料；维护过程中的原始 batch/source 资料位于本地 `resources/`，已被 `.gitignore` 排除。

本仓库的 spritesheet 是原创的灯光语义转译，没有复制 Yeelight/易来 logo、可读文字、UI、宣传语或官方图片像素。`Yeelight` 名称仅用于说明灵感来源和资源命名；本项目不是 Yeelight 官方项目，也不代表 Yeelight 官方背书。

代码按 MIT License 发布。生成图片资产默认随仓库按同一许可证发布，除非后续维护者在特定资源目录中另行声明。

更多归属和商标边界见 [NOTICE.md](NOTICE.md)，安全反馈范围见 [SECURITY.md](SECURITY.md)。
