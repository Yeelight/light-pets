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

REFINED_COLLECTION = {
    "id": "yeelight-refined-hatch-pets",
    "title": "Yeelight Refined Hatch Pets",
    "summary": "12 high-polish Codex pets inspired by Yeelight scenes, controls, sensors, lightstrips, panels, and comfort lighting.",
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

REFINED_METADATA = {
    "yeelight-prism-scene-buddy": {
        "title_zh": "场景棱光仔",
        "reference_device": "whole-home scenes / ambient scene control",
        "personality": "playful, polished, and cinematic",
        "design_notes": "A translucent prism diffuser buddy with scene-button ears and warm-to-cool light core.",
        "tags": ["scene", "prism", "ambient"],
        "features": ["whole-home scenes", "smooth dimming", "color ambience"],
    },
    "yeelight-matter-bridge-sprite": {
        "title_zh": "万联光桥灵",
        "reference_device": "smart-home bridge / cross-platform compatibility",
        "personality": "friendly, connective, and precise",
        "design_notes": "A small bridge-like robot with soft connection-node ears and a tidy hub body.",
        "tags": ["bridge", "matter", "ecosystem"],
        "features": ["compatibility", "smart-home linking", "stable control"],
    },
    "yeelight-qingkong-cloud-whale": {
        "title_zh": "青空云窗鲸",
        "reference_device": "Qingkong skylight / natural daylight",
        "personality": "gentle, calm, and airy",
        "design_notes": "A plush skylight whale carrying a soft blue-sky window in its belly.",
        "tags": ["qingkong", "daylight", "plush"],
        "features": ["natural sky light", "soft daylight", "calming scenes"],
    },
    "yeelight-magnetic-track-dragon": {
        "title_zh": "磁轨闪龙",
        "reference_device": "magnetic track lighting / modular light modules",
        "personality": "cool, agile, and modular",
        "design_notes": "A compact dragon assembled from magnetic-track modules, graphite rails, and tiny lens eyes.",
        "tags": ["track-light", "dragon", "modular"],
        "features": ["magnetic track", "modular layout", "precision lighting"],
    },
    "yeelight-radar-peek-cat": {
        "title_zh": "雷达偷看猫",
        "reference_device": "presence sensor / automatic lighting",
        "personality": "goofy, curious, and alert",
        "design_notes": "A round sensor cat with a radar-disc forehead and mischievous peeking expression.",
        "tags": ["sensor", "presence", "cat"],
        "features": ["presence sensing", "automation trigger", "hands-free lighting"],
    },
    "yeelight-rgb-jelly-strip": {
        "title_zh": "RGB 果冻带",
        "reference_device": "RGB lightstrip / flexible ambience",
        "personality": "playful, colorful, and elastic",
        "design_notes": "A translucent jelly ribbon folded into a compact lightstrip creature.",
        "tags": ["lightstrip", "rgb", "jelly"],
        "features": ["RGB scenes", "flexible install", "music mood lighting"],
    },
    "yeelight-micro-dim-bean": {
        "title_zh": "微光豆豆",
        "reference_device": "micro dimming / low-brightness night light",
        "personality": "quiet, tiny, and careful",
        "design_notes": "A minimal glowing bean with a tiny dimmer dial belly and sleepy bright eyes.",
        "tags": ["dimming", "night", "minimal"],
        "features": ["low-brightness control", "sleep-friendly light", "fine dimming"],
    },
    "yeelight-night-guide-firefly": {
        "title_zh": "守夜地脚萤",
        "reference_device": "footlight / night guidance",
        "personality": "warm, helpful, and low-key",
        "design_notes": "A small wall-footlight firefly with a low lamp belly and attached wings.",
        "tags": ["footlight", "guidance", "firefly"],
        "features": ["night navigation", "low glare", "warm guidance"],
    },
    "yeelight-bath-bubble-whale": {
        "title_zh": "浴暖泡泡鲸",
        "reference_device": "bath heater / bathroom comfort lighting",
        "personality": "funny, warm, and reassuring",
        "design_notes": "A round bath-heater whale with a vent-smile, towel fin, and clean bathroom-light palette.",
        "tags": ["bath-heater", "bathroom", "whale"],
        "features": ["warm airflow", "bath comfort", "fresh bathroom light"],
    },
    "yeelight-art-panel-spirit": {
        "title_zh": "艺面纹理灵",
        "reference_device": "art panel / premium material texture",
        "personality": "elegant, clever, and decorative",
        "design_notes": "A pearl-and-copper panel spirit with carved texture and ornamental trim.",
        "tags": ["art-panel", "texture", "decorative"],
        "features": ["material texture", "premium decor", "surface design"],
    },
    "yeelight-scene-screen-commander": {
        "title_zh": "智屏小司令",
        "reference_device": "scene screen / smart interaction panel",
        "personality": "focused, confident, and tech-cool",
        "design_notes": "A glossy black command-screen robot with cyan face strokes and warm accent lights.",
        "tags": ["screen", "scene-control", "robot"],
        "features": ["whole-home control", "scene interaction", "smart panel"],
    },
    "yeelight-knob-dance-disk": {
        "title_zh": "旋钮舞盘仔",
        "reference_device": "knob control / tactile dimming",
        "personality": "cheeky, rhythmic, and tactile",
        "design_notes": "A modern pixel-style knob mascot with ridged rim, mechanical ears, and dancing feet.",
        "tags": ["knob", "dimming", "pixel"],
        "features": ["tactile control", "scene adjustment", "precise rotation"],
    },
}
