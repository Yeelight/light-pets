"""项目常量与手工补齐的单宠元数据。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESOURCES = ROOT / "resources"
PACKAGES = ROOT / "packages"
QA = ROOT / "qa"
ASSETS = ROOT / "assets"
OVERVIEWS = ASSETS / "overviews"
COLLECTION_DOCS = ROOT / "collections"
CATALOG = ROOT / "catalog"
DEMO = ROOT / "demo"

W, H = 192, 208
COLS, ROWS = 8, 9
ATLAS_W, ATLAS_H = W * COLS, H * ROWS

STATES = [
    "idle",
    "running-right",
    "running-left",
    "waving",
    "jumping",
    "failed",
    "waiting",
    "running",
    "review",
]
FRAME_COUNTS = {
    "idle": 6,
    "running-right": 8,
    "running-left": 8,
    "waving": 4,
    "jumping": 5,
    "failed": 8,
    "waiting": 6,
    "running": 6,
    "review": 6,
}
DURATIONS = {
    "idle": [280, 110, 110, 140, 140, 320],
    "running-right": [120, 120, 120, 120, 120, 120, 120, 220],
    "running-left": [120, 120, 120, 120, 120, 120, 120, 220],
    "waving": [140, 140, 140, 280],
    "jumping": [140, 140, 140, 140, 280],
    "failed": [140, 140, 140, 140, 140, 140, 140, 240],
    "waiting": [150, 150, 150, 150, 150, 260],
    "running": [120, 120, 120, 120, 120, 220],
    "review": [150, 150, 150, 150, 150, 280],
}

BATCH_COLLECTIONS = {
    "yeelight_hatch_pet_full_batch": {
        "id": "yeelight-hatch-pet-full-batch",
        "title": "Yeelight Hatch Pet Full Batch",
        "summary": "12 pets inspired by residential Yeelight lighting categories.",
    },
    "yeelight_pro_hatch_pet_batch": {
        "id": "yeelight-pro-hatch-pet-batch",
        "title": "Yeelight Pro Hatch Pet Batch",
        "summary": "65 pets derived from Yeelight Pro product-series semantics.",
    },
}

SINGLE_COLLECTION = {
    "id": "featured-single-pets",
    "title": "Featured Single Pets",
    "summary": "Five standalone Codex pets with completed QA assets.",
}

SINGLE_METADATA = {
    "yeelight-cozy-glow": {
        "title_zh": "暖绒微光",
        "reference_device": "cozy bedside lamp / warm ambient light",
        "personality": "quiet, plush, and sleep-friendly",
        "design_notes": "A soft bunny-like companion hugging a warm lamp orb.",
        "tags": ["plush", "warm", "bedside"],
    },
    "yeelight-dot-lampy": {
        "title_zh": "点点灯灵",
        "reference_device": "minimal desk lamp / round light helper",
        "personality": "cheerful, compact, and tidy",
        "design_notes": "A round lamp mascot with a bright dot face and tiny sidekick.",
        "tags": ["lamp", "minimal", "desk"],
    },
    "yeelight-halo-bot": {
        "title_zh": "光环小机",
        "reference_device": "floating halo light / cyan smart robot",
        "personality": "cyber-cute, alert, and precise",
        "design_notes": "A hovering bot with a cyan halo ring and warm bulb companion.",
        "tags": ["robot", "halo", "cyan"],
    },
    "yeelight-lumi": {
        "title_zh": "流明光伴",
        "reference_device": "smart-light robot companion",
        "personality": "friendly, helpful, and balanced",
        "design_notes": "A clean smart-light robot carrying a small warm bulb friend.",
        "tags": ["robot", "smart-light", "warm"],
    },
    "yeelight-lumi-pixel": {
        "title_zh": "像素流明",
        "reference_device": "retro pixel smart-light robot",
        "personality": "crisp, playful, and nostalgic",
        "design_notes": "A pixel-art smart-light robot with a tiny warm bulb buddy.",
        "tags": ["robot", "pixel", "retro"],
    },
}
