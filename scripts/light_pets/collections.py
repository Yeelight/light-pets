"""生成公开 collection 文档和 overview 资产。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import COLLECTION_DOCS
from .io import rel


def write_collection_readmes(collections: list[dict[str, Any]], pets: list[dict[str, Any]]) -> None:
    COLLECTION_DOCS.mkdir(parents=True, exist_ok=True)
    by_collection = {collection["id"]: [] for collection in collections}
    for pet in pets:
        by_collection.setdefault(pet["collection"], []).append(pet)

    for collection in collections:
        collection_dir = COLLECTION_DOCS / collection["id"]
        collection_dir.mkdir(parents=True, exist_ok=True)
        rows = [
            "| Pet | ID | Kind | Package | QA |",
            "| --- | --- | --- | --- | --- |",
        ]
        for pet in by_collection.get(collection["id"], []):
            rows.append(
                f"| {pet['display_name']} | `{pet['id']}` | `{pet['kind']}` | "
                f"[package](../../{pet['package_dir']}/) | [qa](../../{Path(pet['contact_sheet']).parent.as_posix()}/) |"
            )

        overview = ""
        if collection.get("overview_image"):
            overview = f"\n![{collection['title']} overview](../../{collection['overview_image']})\n"

        readme = f"""# {collection['title']}

{collection['summary']}
{overview}
Pet count: {collection['pet_count']}

## Pets

{chr(10).join(rows)}
"""
        (collection_dir / "README.md").write_text(readme, encoding="utf-8")
