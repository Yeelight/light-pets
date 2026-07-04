"""汇总原始 batch 与单宠资源，输出规范化公开目录。"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .config import (
    ATLAS_H,
    ATLAS_W,
    ASSETS,
    BATCH_COLLECTIONS,
    CATALOG,
    COLLECTION_DOCS,
    COLS,
    DURATIONS,
    FRAME_COUNTS,
    H,
    OVERVIEWS,
    PACKAGES,
    QA,
    REFINED_COLLECTION,
    REFINED_METADATA,
    RESOURCES,
    ROWS,
    SINGLE_COLLECTION,
    STATES,
    W,
)
from .collections import write_collection_readmes
from .demo import write_demo
from .io import load_json, rel, write_json
from .single_pet import complete_single_pet, state_preview_paths


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def write_batch_package_readme(package_dir: Path, pet: dict[str, Any], collection: dict[str, Any]) -> None:
    readme = f"""# {pet['display_name']}

- ID: `{pet['id']}`
- Collection: `{collection['id']}`
- Kind: `{pet['kind']}`
- Reference: {pet['reference_device']}

## Install

Copy `pet.json` and `spritesheet.webp` from this directory into your Codex custom pet directory.

## QA

See `../../qa/{pet['id']}/` for the contact sheet, state GIFs, validation result, and review summary.
"""
    (package_dir / "README.md").write_text(readme, encoding="utf-8")


def write_refined_package_readme(package_dir: Path, pet: dict[str, Any], collection: dict[str, Any]) -> None:
    feature_text = ", ".join(pet.get("features", [])) or pet.get("reference_device", "")
    readme = f"""# {pet['display_name']}

- ID: `{pet['id']}`
- Collection: `{collection['id']}`
- Kind: `{pet['kind']}`
- Reference: {pet['reference_device']}
- Highlights: {feature_text}

## Install

Copy `pet.json` and `spritesheet.webp` from this directory into your Codex custom pet directory.

## Preview

See `../../qa/{pet['id']}/contact-sheet.png` for the full 9-state sheet, and `../../qa/{pet['id']}/previews/` for animated GIFs.
"""
    (package_dir / "README.md").write_text(readme, encoding="utf-8")


def normalize_batch_pet(batch_dir: Path, item: dict[str, Any], collection: dict[str, Any]) -> dict[str, Any]:
    pid = item.get("package_id") or item["id"]
    source_package = batch_dir / "pet_packages" / pid
    source_qa = batch_dir / "qa" / pid
    package_dir = PACKAGES / pid
    qa_dir = QA / pid
    package_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)

    pet_json = load_json(source_package / "pet.json")
    copy_file(source_package / "pet.json", package_dir / "pet.json")
    copy_file(source_package / "spritesheet.webp", package_dir / "spritesheet.webp")
    copy_file(source_package / "spritesheet.png", package_dir / "spritesheet.png")
    copy_file(source_qa / "contact-sheet.png", qa_dir / "contact-sheet.png")
    copy_file(source_qa / "validation.json", qa_dir / "validation.json")
    copy_file(source_qa / "review.json", qa_dir / "review.json")
    if (source_qa / "run-summary.json").exists():
        copy_file(source_qa / "run-summary.json", qa_dir / "run-summary.json")
    for preview in sorted((source_qa / "previews").glob("*.gif")):
        copy_file(preview, qa_dir / "previews" / preview.name)

    kind = item.get("archetype") or item.get("style_preset") or pet_json.get("kind", "object")
    record = {
        "id": pid,
        "display_name": item.get("display_name") or pet_json["displayName"],
        "title_zh": item.get("display_name") or pet_json["displayName"],
        "description": pet_json.get("description", ""),
        "kind": kind,
        "collection": collection["id"],
        "reference_device": item.get("reference_device", ""),
        "personality": "",
        "tags": item.get("tags", []),
        "features": item.get("features", []),
        "package_dir": rel(package_dir),
        "pet_json": rel(package_dir / "pet.json"),
        "spritesheet_webp": rel(package_dir / "spritesheet.webp"),
        "spritesheet_png": rel(package_dir / "spritesheet.png"),
        "contact_sheet": rel(qa_dir / "contact-sheet.png"),
        "overview_image": rel(OVERVIEWS / f"{collection['id']}.png"),
        "validation": rel(qa_dir / "validation.json"),
        "review": rel(qa_dir / "review.json"),
        "state_previews": state_preview_paths(qa_dir / "previews"),
    }
    write_batch_package_readme(package_dir, record, collection)
    return record


def collect_batch_pets(batch_dir: Path) -> list[dict[str, Any]]:
    manifest = load_json(batch_dir / "batch_manifest.json")
    collection = BATCH_COLLECTIONS[batch_dir.name]
    copy_file(batch_dir / "overview_contact_sheets.png", OVERVIEWS / f"{collection['id']}.png")
    return [normalize_batch_pet(batch_dir, item, collection) for item in manifest["pets"]]


def collect_single_pets() -> list[dict[str, Any]]:
    pets = []
    for pet_dir in sorted(RESOURCES.iterdir()):
        if pet_dir.is_dir() and (pet_dir / "pet.json").exists():
            pets.append(complete_single_pet(pet_dir))
    return pets


def collect_refined_pets() -> list[dict[str, Any]]:
    pets = []
    for pid, meta in REFINED_METADATA.items():
        package_dir = PACKAGES / pid
        qa_dir = QA / pid
        pet_json_path = package_dir / "pet.json"
        if not pet_json_path.exists():
            continue

        pet_json = load_json(pet_json_path)
        record = {
            "id": pid,
            "display_name": pet_json.get("displayName", meta["title_zh"]),
            "title_zh": meta["title_zh"],
            "description": pet_json.get("description", ""),
            "kind": pet_json.get("kind", "refined"),
            "collection": REFINED_COLLECTION["id"],
            "reference_device": meta["reference_device"],
            "personality": meta["personality"],
            "tags": meta["tags"],
            "features": meta["features"],
            "package_dir": rel(package_dir),
            "pet_json": rel(pet_json_path),
            "spritesheet_webp": rel(package_dir / pet_json.get("spritesheetPath", "spritesheet.webp")),
            "spritesheet_png": rel(package_dir / "spritesheet.png"),
            "contact_sheet": rel(qa_dir / "contact-sheet.png"),
            "overview_image": rel(OVERVIEWS / f"{REFINED_COLLECTION['id']}.png"),
            "validation": rel(qa_dir / "validation.json"),
            "review": rel(qa_dir / "review.json"),
            "state_previews": state_preview_paths(qa_dir / "previews"),
        }
        write_refined_package_readme(package_dir, record, REFINED_COLLECTION)
        pets.append(record)
    return pets


def build_collections(pets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    collections = [SINGLE_COLLECTION, *BATCH_COLLECTIONS.values(), REFINED_COLLECTION]
    output = []
    for collection in collections:
        members = [pet for pet in pets if pet["collection"] == collection["id"]]
        overview = f"assets/overviews/{collection['id']}.png"
        if not (OVERVIEWS / f"{collection['id']}.png").exists():
            overview = members[0]["overview_image"] if members else ""
        output.append({**collection, "overview_image": overview, "pet_count": len(members), "pets": [pet["id"] for pet in members]})
    return output


def catalog_payload(pets: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "name": "light-pets",
        "pet_count": len(pets),
        "atlas_contract": {
            "cell_size": [W, H],
            "atlas_size": [ATLAS_W, ATLAS_H],
            "columns": COLS,
            "rows": ROWS,
            "state_order": STATES,
            "frame_counts": FRAME_COUNTS,
            "durations_ms": DURATIONS,
        },
        "pets": pets,
    }


def build_catalog() -> tuple[int, int]:
    if not all((RESOURCES / batch_name).exists() for batch_name in BATCH_COLLECTIONS):
        catalog = load_json(CATALOG / "pets.json")
        collections = load_json(CATALOG / "collections.json")["collections"]
        write_collection_readmes(collections, catalog["pets"])
        write_demo(catalog["pets"], collections)
        return len(catalog["pets"]), len(collections)

    for directory in (ASSETS, CATALOG, COLLECTION_DOCS, PACKAGES, QA):
        directory.mkdir(parents=True, exist_ok=True)

    batch_pets = []
    for batch_name in BATCH_COLLECTIONS:
        batch_pets.extend(collect_batch_pets(RESOURCES / batch_name))

    pets = sorted([*collect_single_pets(), *batch_pets, *collect_refined_pets()], key=lambda p: (p["collection"], p["id"]))
    collections = build_collections(pets)
    write_json(CATALOG / "pets.json", catalog_payload(pets))
    write_json(CATALOG / "collections.json", {"collections": collections})
    write_collection_readmes(collections, pets)
    write_demo(pets, collections)
    return len(pets), len(collections)
