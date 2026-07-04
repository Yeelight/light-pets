#!/usr/bin/env python3
"""Validate the generated open-source project surface."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "pets.json"
COLLECTIONS = ROOT / "catalog" / "collections.json"
DEMO = ROOT / "demo" / "index.html"
ATLAS_SIZE = (1536, 1872)
REQUIRED_ROOT_FILES = [
    ".gitattributes",
    ".gitignore",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "Makefile",
    "NOTICE.md",
    "SECURITY.md",
    "requirements.txt",
    ".github/workflows/validate.yml",
    "assets/overviews/yeelight-hatch-pet-full-batch.png",
    "assets/overviews/yeelight-pro-hatch-pet-batch.png",
    "docs/ASSET_CONTRACT.md",
    "docs/PROJECT_STRUCTURE.md",
    "docs/PUBLISHING.md",
    "docs/VALIDATION.md",
    "scripts/build_project.py",
    "scripts/validate_project.py",
]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.links.append(value)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing file: {path.relative_to(ROOT)}")


def validate_image(path: Path, errors: list[str]) -> None:
    require_file(path, errors)
    if not path.exists():
        return
    with Image.open(path) as image:
        if image.size != ATLAS_SIZE:
            errors.append(f"invalid atlas size {path.relative_to(ROOT)}: {image.size}")


def validate_demo_links(errors: list[str]) -> None:
    if not DEMO.exists():
        return
    parser = LinkParser()
    parser.feed(DEMO.read_text(encoding="utf-8"))
    for link in parser.links:
        parsed = urlparse(link)
        if parsed.scheme in {"data", "http", "https", "mailto"} or link.startswith("#"):
            continue
        path = (DEMO.parent / parsed.path).resolve()
        try:
            rel_path = path.relative_to(ROOT)
        except ValueError:
            errors.append(f"demo link escapes repository: {link}")
            continue
        if rel_path.parts and rel_path.parts[0] == "resources":
            errors.append(f"demo link references ignored raw resources: {link}")
        require_file(path, errors)


def main() -> None:
    errors: list[str] = []
    for rel_path in REQUIRED_ROOT_FILES:
        require_file(ROOT / rel_path, errors)
    require_file(CATALOG, errors)
    require_file(COLLECTIONS, errors)
    require_file(DEMO, errors)

    if CATALOG.exists():
        catalog = load_json(CATALOG)
        pets = catalog.get("pets", [])
        if catalog.get("pet_count") != len(pets):
            errors.append("catalog pet_count does not match pets length")
        for pet in pets:
            if any(str(pet.get(key, "")).startswith("resources/") for key in pet):
                errors.append(f"{pet['id']} still references ignored raw resources")
            for key in ("pet_json", "spritesheet_webp", "contact_sheet", "validation", "review"):
                require_file(ROOT / pet[key], errors)
            validate_image(ROOT / pet["spritesheet_webp"], errors)
            previews = pet.get("state_previews", {})
            if len(previews) != 9:
                errors.append(f"{pet['id']} has {len(previews)} state previews, expected 9")
            for preview in previews.values():
                require_file(ROOT / preview, errors)

    if COLLECTIONS.exists() and CATALOG.exists():
        collections = load_json(COLLECTIONS).get("collections", [])
        pet_ids = {pet["id"] for pet in load_json(CATALOG).get("pets", [])}
        indexed = set()
        for collection in collections:
            if collection.get("overview_image"):
                require_file(ROOT / collection["overview_image"], errors)
            indexed.update(collection.get("pets", []))
            if collection.get("pet_count") != len(collection.get("pets", [])):
                errors.append(f"collection count mismatch: {collection.get('id')}")
        missing = pet_ids - indexed
        if missing:
            errors.append(f"pets missing from collections: {sorted(missing)[:5]}")

    if DEMO.exists() and CATALOG.exists():
        card_count = DEMO.read_text(encoding="utf-8").count('class="pet-card"')
        pet_count = load_json(CATALOG).get("pet_count")
        if card_count != pet_count:
            errors.append(f"demo card count {card_count} does not match catalog {pet_count}")
        validate_demo_links(errors)

    if errors:
        print("validation failed")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    pet_count = load_json(CATALOG).get("pet_count", 0)
    collection_count = len(load_json(COLLECTIONS).get("collections", []))
    print(f"validation passed: {pet_count} pets, {collection_count} collections")


if __name__ == "__main__":
    main()
