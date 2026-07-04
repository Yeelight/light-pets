"""图像验证、contact sheet 和状态 GIF 生成。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from .config import ATLAS_H, ATLAS_W, COLS, DURATIONS, FRAME_COUNTS, H, ROWS, STATES, W


def font(size: int) -> ImageFont.ImageFont:
    for candidate in (
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def checker(size: tuple[int, int], dark: bool = False) -> Image.Image:
    a, b = ((34, 39, 45), (48, 55, 64)) if dark else ((244, 247, 249), (226, 232, 237))
    out = Image.new("RGB", size, a)
    draw = ImageDraw.Draw(out)
    step = 16
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill=b)
    return out


def cell_image(atlas: Image.Image, row: int, col: int) -> Image.Image:
    return atlas.crop((col * W, row * H, (col + 1) * W, (row + 1) * H)).convert("RGBA")


def composite_on_checker(cell: Image.Image, dark: bool = False) -> Image.Image:
    bg = checker(cell.size, dark=dark).convert("RGBA")
    bg.alpha_composite(cell)
    return bg.convert("RGB")


def validate_atlas(atlas: Image.Image) -> dict[str, Any]:
    atlas = atlas.convert("RGBA")
    errors: list[str] = []
    if atlas.size != (ATLAS_W, ATLAS_H):
        errors.append(f"expected {ATLAS_W}x{ATLAS_H}, got {atlas.width}x{atlas.height}")

    cells: list[dict[str, Any]] = []
    for row, state in enumerate(STATES):
        for col in range(COLS):
            cell = cell_image(atlas, row, col)
            alpha = cell.getchannel("A")
            bbox = alpha.getbbox()
            alpha_area = sum(1 for px in alpha.getdata() if px)
            non_empty = bbox is not None
            if not non_empty:
                errors.append(f"empty cell: row={row}, col={col}, state={state}")
            cells.append(
                {
                    "row": row,
                    "col": col,
                    "state": state,
                    "nonEmpty": non_empty,
                    "alphaArea": alpha_area,
                    "bbox": list(bbox) if bbox else None,
                    "margin": [
                        bbox[0] if bbox else W,
                        bbox[1] if bbox else H,
                        W - bbox[2] if bbox else W,
                        H - bbox[3] if bbox else H,
                    ],
                }
            )

    residue = any(a == 0 and (r or g or b) for r, g, b, a in atlas.getdata())
    return {
        "ok": not errors,
        "width": atlas.width,
        "height": atlas.height,
        "columns": COLS,
        "rows": ROWS,
        "cellWidth": W,
        "cellHeight": H,
        "states": STATES,
        "cells": cells,
        "transparentRgbResidue": residue,
        "errors": errors,
    }


def make_contact_sheet(atlas: Image.Image, pet: dict[str, Any], out_path: Path) -> None:
    scale = 0.58
    tw, th = int(W * scale), int(H * scale)
    pad, label_h, header_h = 18, 24, 86
    out = Image.new("RGB", (pad * 2 + COLS * tw, header_h + ROWS * (th + label_h) + pad), (248, 246, 240))
    draw = ImageDraw.Draw(out)
    draw.text((pad, 18), f"{pet['displayName']} / {pet['id']}", fill=(26, 32, 38), font=font(24))
    draw.text((pad, 52), "Codex hatch-pet 8x9 atlas contact sheet", fill=(87, 96, 105), font=font(13))
    for row, state in enumerate(STATES):
        y = header_h + row * (th + label_h)
        draw.text((pad, y), state, fill=(60, 73, 86), font=font(13))
        for col in range(COLS):
            cell = composite_on_checker(cell_image(atlas, row, col)).resize((tw, th), Image.Resampling.LANCZOS)
            out.paste(cell, (pad + col * tw, y + label_h))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(out_path)


def make_preview_dark_grid(atlas: Image.Image, out_path: Path) -> None:
    bg = checker(atlas.size, dark=True).convert("RGBA")
    bg.alpha_composite(atlas.convert("RGBA"))
    preview = bg.convert("RGB").resize((768, 936), Image.Resampling.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    preview.save(out_path)


def make_state_gifs(atlas: Image.Image, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for row, state in enumerate(STATES):
        frames = [composite_on_checker(cell_image(atlas, row, col), dark=True) for col in range(FRAME_COUNTS[state])]
        frames[0].save(
            out_dir / f"{state}.gif",
            save_all=True,
            append_images=frames[1:],
            duration=DURATIONS[state],
            loop=0,
            optimize=False,
        )
