# Publishing Checklist

发布到 GitHub 前建议按顺序执行：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/build_project.py
python3 scripts/validate_project.py
open "demo/index.html"
```

检查点：

- README 能说明项目价值、安装方式、资源契约和商标边界。
- `demo/index.html` 能展示所有 pet，并能筛选、搜索、查看状态 GIF。
- `catalog/pets.json` 中的 `pet_count` 与 demo 卡片数量一致。
- 每只 pet 的 `spritesheet.webp` 是 `1536 x 1872`。
- 每只 pet 有 9 个状态 GIF 预览。
- 仓库没有 `.DS_Store`、`__pycache__`、本地虚拟环境或临时构建目录。
- `resources/` 原始资料被 `.gitignore` 排除，不进入公开仓库。
- 当前验证记录见 `docs/VALIDATION.md`。

如果启用 GitHub Pages，可把发布源设置为仓库根目录，然后使用 `/demo/` 作为展示入口。
