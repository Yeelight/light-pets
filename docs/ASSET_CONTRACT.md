# Asset Contract

本项目采用 Codex hatch-pet atlas 契约。每只 pet 的运行时核心文件是 `pet.json` 与 `spritesheet.webp`。

## Atlas

- 尺寸：`1536 x 1872`
- 网格：`8 x 9`
- 单元格：`192 x 208`
- 透明背景：推荐 RGBA 或 lossless WebP 透明通道
- 未使用区域：保持透明

## 状态行顺序

| 行 | 状态 | 推荐帧数 | 默认时长 |
| --- | --- | ---: | --- |
| 0 | `idle` | 6 | `280, 110, 110, 140, 140, 320` |
| 1 | `running-right` | 8 | `120 x 7, 220` |
| 2 | `running-left` | 8 | `120 x 7, 220` |
| 3 | `waving` | 4 | `140, 140, 140, 280` |
| 4 | `jumping` | 5 | `140, 140, 140, 140, 280` |
| 5 | `failed` | 8 | `140 x 7, 240` |
| 6 | `waiting` | 6 | `150 x 5, 260` |
| 7 | `running` | 6 | `120 x 5, 220` |
| 8 | `review` | 6 | `150 x 5, 280` |

## `pet.json`

最小字段：

```json
{
  "id": "yeelight-lumi",
  "displayName": "Yeelight Lumi",
  "description": "A cute smart-light robot companion.",
  "spritesheetPath": "spritesheet.webp",
  "kind": "robot"
}
```

`spritesheetPath` 必须指向同一目录中的 WebP 文件。额外字段可以存在，但不应影响最小安装契约。

## QA 文件

推荐每只 pet 提供：

- `spritesheet.png`：PNG 备份
- `qa/<pet-id>/preview-dark-grid.png`：暗色网格预览
- `qa/<pet-id>/contact-sheet.png`：完整接触表
- `qa/<pet-id>/previews/<state>.gif`：状态动画预览
- `qa/<pet-id>/validation.json`：程序化验证结果
- `qa/<pet-id>/review.json`：人工或程序复核摘要
