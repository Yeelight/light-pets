# Contributing

## 基本原则

- 保持 pet 资源可直接安装：每只 pet 至少包含 `pet.json` 和 `spritesheet.webp`。
- 保持 QA 可复核：新增或修改 spritesheet 后运行 `python3 scripts/build_project.py`。
- 保持索引一致：提交前运行 `python3 scripts/validate_project.py`。
- 不提交系统垃圾文件、临时产物和本地虚拟环境。
- 不提交维护过程中的原始 `resources/` 资料；公开仓库只保留整理后的 `packages/`、`qa/`、`catalog/`、`collections/` 和 `demo/`。

## 新增单只 pet

1. 在本地被忽略的 `resources/<pet-id>/` 放入 `pet.json` 和 `spritesheet.webp`。
2. 在 `scripts/light_pets/config.py` 的 `SINGLE_METADATA` 中补充该 pet 的设计元数据。
3. 运行 `python3 scripts/build_project.py`。
4. 运行 `python3 scripts/validate_project.py`。
5. 确认新 pet 已出现在 `packages/<pet-id>/`、`qa/<pet-id>/` 和 `catalog/pets.json`。

## 新增批量 collection

批量原始目录只放在本地 `resources/<collection>/`，不进入 Git。结构应尽量复用现有 batch：

```text
resources/<collection>/
├── README.md
├── batch_manifest.json
├── batch_validation.json
├── catalog.html
├── overview_contact_sheets.png
├── pet_packages/<pet_id>/pet.json
├── pet_packages/<pet_id>/spritesheet.webp
├── pet_packages/<pet_id>/spritesheet.png
└── qa/<pet_id>/
    ├── contact-sheet.png
    ├── validation.json
    ├── review.json
    └── previews/*.gif
```

然后在 `scripts/light_pets/config.py` 的 `BATCH_COLLECTIONS` 中登记 collection，并运行构建/校验脚本。最终提交的是归一化后的公开目录。

## 设计避让

请提交原创形象。不要复制第三方 logo、可读品牌文字、UI 截图、宣传海报或官方产品图片像素。
