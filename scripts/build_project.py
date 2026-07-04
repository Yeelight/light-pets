#!/usr/bin/env python3
"""构建公开目录、demo 页面，并补齐单只 pet 的 QA 资产。"""

from __future__ import annotations

from light_pets.catalog import build_catalog


def main() -> None:
    pet_count, collection_count = build_catalog()
    print(f"built {pet_count} pets across {collection_count} collections")


if __name__ == "__main__":
    main()
