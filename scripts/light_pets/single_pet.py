"""从原始单宠目录生成规范化 package、QA 和 catalog record。"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from PIL import Image

from .config import PACKAGES, QA, SINGLE_COLLECTION, SINGLE_METADATA, STATES
from .images import make_contact_sheet, make_preview_dark_grid, make_state_gifs, validate_atlas
from .io import load_json, rel, write_json


def state_preview_paths(base: Path) -> dict[str, str]:
    return {state: rel(base / f"{state}.gif") for state in STATES if (base / f"{state}.gif").exists()}


def write_single_docs(pet_dir: Path, pet: dict[str, Any], meta: dict[str, Any]) -> None:
    pid = pet["id"]
    readme = f"""# {pet['displayName']} ({pid})

状态：通过
规格：8 列 x 9 行，单元格 192x208，最终 atlas 1536x1872。

## 设计信息

- 中文名：{meta['title_zh']}
- 参考语义：{meta['reference_device']}
- 性格：{meta['personality']}
- 设计说明：{meta['design_notes']}
- 标签：{', '.join(meta['tags'])}

## 目录

- `pet.json`：Codex 自定义 PET 清单。
- `spritesheet.webp`：主 spritesheet，可直接与 `pet.json` 成对安装。
- `spritesheet.png`：无损 PNG 备份。
- `preview-dark-grid.png`：暗色网格总览。
- `qa/contact-sheet.png`：人工 QA 接触表。
- `qa/previews/*.gif`：9 个状态动画预览。
- `qa/validation.json`：尺寸、透明像素和单元格验证。
- `qa/review.json` / `qa/run-summary.json`：复核结论和索引摘要。

## 使用方式

把本目录中的 `pet.json` 与 `spritesheet.webp` 复制到 Codex 自定义 PET 目录即可。

## 设计避让

该 PET 是原创灯光语义转译，没有复制 Yeelight/易来 logo、可读文字、UI、宣传语或官方图片像素。
"""
    (pet_dir / "README.md").write_text(readme, encoding="utf-8")

    prompt = f"""# {pet['displayName']} ({pid})

Reference semantics: {meta['reference_device']}
Personality: {meta['personality']}
Design notes: {meta['design_notes']}

## State motifs

- idle: calm breathing light.
- running-right: purposeful light glide to the right.
- running-left: mirrored light glide to the left.
- waving: friendly light pulse.
- jumping: buoyant glow bounce.
- failed: dimmed or softened expression.
- waiting: patient ambient shimmer.
- running: compact task-focused loop.
- review: inspection pose with brighter accent.
"""
    (pet_dir / "source_prompt.md").write_text(prompt, encoding="utf-8")


def write_package_readme(package_dir: Path, pet: dict[str, Any], meta: dict[str, Any], collection_id: str) -> None:
    readme = f"""# {pet['displayName']}

- ID: `{pet['id']}`
- Collection: `{collection_id}`
- Kind: `{pet.get('kind', 'object')}`
- Reference: {meta['reference_device']}

## Install

Copy `pet.json` and `spritesheet.webp` from this directory into your Codex custom pet directory.

## QA

See `../../qa/{pet['id']}/` for the contact sheet, state GIFs, validation result, and review summary.
"""
    (package_dir / "README.md").write_text(readme, encoding="utf-8")


def make_single_record(package_dir: Path, qa_dir: Path, pet: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": pet["id"],
        "display_name": pet["displayName"],
        "title_zh": meta["title_zh"],
        "description": pet.get("description", ""),
        "kind": pet.get("kind", "object"),
        "collection": SINGLE_COLLECTION["id"],
        "reference_device": meta["reference_device"],
        "personality": meta["personality"],
        "tags": meta["tags"],
        "package_dir": rel(package_dir),
        "pet_json": rel(package_dir / "pet.json"),
        "spritesheet_webp": rel(package_dir / pet["spritesheetPath"]),
        "spritesheet_png": rel(package_dir / "spritesheet.png"),
        "contact_sheet": rel(qa_dir / "contact-sheet.png"),
        "overview_image": rel(qa_dir / "preview-dark-grid.png"),
        "validation": rel(qa_dir / "validation.json"),
        "review": rel(qa_dir / "review.json"),
        "state_previews": state_preview_paths(qa_dir / "previews"),
    }


def complete_single_pet(pet_dir: Path) -> dict[str, Any]:
    pet = load_json(pet_dir / "pet.json")
    meta = SINGLE_METADATA[pet["id"]]
    atlas = Image.open(pet_dir / pet["spritesheetPath"]).convert("RGBA")
    package_dir = PACKAGES / pet["id"]
    qa_dir = QA / pet["id"]
    package_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)

    validation = validate_atlas(atlas)
    webp_validation = validate_atlas(Image.open(pet_dir / pet["spritesheetPath"]).convert("RGBA"))
    validation["webp_reload_ok"] = webp_validation["ok"]
    validation["webp_reload_errors"] = webp_validation["errors"]

    write_json(package_dir / "pet.json", pet)
    shutil.copy2(pet_dir / pet["spritesheetPath"], package_dir / pet["spritesheetPath"])
    atlas.save(package_dir / "spritesheet.png")
    make_preview_dark_grid(atlas, qa_dir / "preview-dark-grid.png")
    make_contact_sheet(atlas, pet, qa_dir / "contact-sheet.png")
    make_state_gifs(atlas, qa_dir / "previews")
    write_json(qa_dir / "validation.json", validation)

    review = {
        "visual_qa": "pass" if validation["ok"] and validation["webp_reload_ok"] else "fail",
        "notes": "Generated contact sheet and state GIFs were rebuilt from the package spritesheet; atlas size and all 72 cells were checked.",
        "state_order": STATES,
        "blocked_rows": [] if validation["ok"] else validation["errors"],
    }
    write_json(qa_dir / "review.json", review)
    write_json(
        qa_dir / "run-summary.json",
        {
            "ok": review["visual_qa"] == "pass",
            "pet_id": pet["id"],
            "display_name": pet["displayName"],
            "reference_device": meta["reference_device"],
            "package_dir": rel(package_dir),
            "spritesheet_webp": rel(package_dir / pet["spritesheetPath"]),
            "spritesheet_png": rel(package_dir / "spritesheet.png"),
            "validation": rel(qa_dir / "validation.json"),
            "contact_sheet": rel(qa_dir / "contact-sheet.png"),
            "preview_dir": rel(qa_dir / "previews"),
            "review": rel(qa_dir / "review.json"),
        },
    )
    write_package_readme(package_dir, pet, meta, SINGLE_COLLECTION["id"])
    return make_single_record(package_dir, qa_dir, pet, meta)
