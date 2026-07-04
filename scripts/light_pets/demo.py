"""生成可直接打开的静态 demo 页面。"""

from __future__ import annotations

import html
from typing import Any

from .config import DEMO, ROOT
from .io import demo_rel


def pet_card(pet: dict[str, Any]) -> str:
    fields = ("id", "display_name", "title_zh", "reference_device", "kind")
    text = " ".join(str(pet.get(k, "")) for k in fields)
    previews = "\n".join(
        f'<figure><img loading="lazy" src="{demo_rel(ROOT / path)}" alt="{html.escape(pet["display_name"])} {state}"><figcaption>{state}</figcaption></figure>'
        for state, path in pet["state_previews"].items()
    )
    tags = " ".join(f"<span>{html.escape(str(tag))}</span>" for tag in pet.get("tags", [])[:4])
    features = " ".join(f"<span>{html.escape(str(feature))}</span>" for feature in pet.get("features", [])[:3])
    pills = tags or features or f"<span>{html.escape(str(pet['kind']))}</span>"
    return f"""
<article class="pet-card" data-collection="{pet['collection']}" data-kind="{html.escape(str(pet['kind']))}" data-text="{html.escape(text.lower())}">
  <a class="image-link" href="{demo_rel(ROOT / pet['pet_json'])}">
    <img loading="lazy" src="{demo_rel(ROOT / pet['contact_sheet'])}" alt="{html.escape(pet['display_name'])} contact sheet">
  </a>
  <div class="pet-main">
    <p class="eyebrow">{html.escape(pet['collection'])}</p>
    <h3>{html.escape(pet['display_name'])}</h3>
    <p class="identity">{html.escape(pet['id'])}</p>
    <p class="desc">{html.escape(pet.get('reference_device') or pet.get('description', ''))}</p>
    <div class="pills">{pills}</div>
    <div class="links">
      <a href="{demo_rel(ROOT / pet['pet_json'])}">pet.json</a>
      <a href="{demo_rel(ROOT / pet['spritesheet_webp'])}">spritesheet</a>
      <a href="{demo_rel(ROOT / pet['validation'])}">validation</a>
    </div>
    <details>
      <summary>9 状态预览</summary>
      <div class="state-grid">{previews}</div>
    </details>
  </div>
</article>"""


def stylesheet() -> str:
    return """
    :root {
      --paper: #f5f1e8; --ink: #18212a; --muted: #68727f;
      --line: #d7d0c3; --panel: #fffaf0; --teal: #2f7773;
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--paper); color: var(--ink); font-family: "Avenir Next", "Gill Sans", "Trebuchet MS", sans-serif; }
    header { min-height: 88vh; display: grid; grid-template-columns: minmax(280px, .88fr) minmax(320px, 1.12fr); gap: clamp(24px, 5vw, 72px); align-items: center; padding: clamp(28px, 5vw, 72px); border-bottom: 1px solid var(--line); }
    h1 { font-family: Georgia, "Times New Roman", serif; font-size: clamp(42px, 8vw, 108px); line-height: .88; margin: 0 0 24px; letter-spacing: 0; }
    .lead { max-width: 680px; color: #3d4852; font-size: 18px; line-height: 1.65; }
    .stats { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 28px; }
    .stats span { border: 1px solid var(--line); padding: 9px 12px; background: #fff7e6; }
    .hero-board { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; align-items: start; }
    .hero-board img { width: 100%; border: 1px solid #b9b0a1; background: white; box-shadow: 10px 10px 0 #2f777322; }
    .hero-board img:first-child { grid-row: span 2; }
    main { padding: 28px clamp(18px, 4vw, 58px) 70px; }
    .toolbar { position: sticky; top: 0; z-index: 2; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; padding: 14px 0; background: color-mix(in srgb, var(--paper) 92%, transparent); backdrop-filter: blur(12px); }
    .chip, input { min-height: 40px; border: 1px solid #bdb4a6; background: #fffaf0; color: var(--ink); padding: 0 13px; font: inherit; }
    .chip { cursor: pointer; } .chip.is-active { background: var(--teal); border-color: var(--teal); color: white; }
    input { margin-left: auto; min-width: min(360px, 100%); }
    .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 18px; align-items: start; }
    .pet-card { border: 1px solid var(--line); background: var(--panel); display: grid; grid-template-rows: auto 1fr; min-height: 100%; }
    .image-link { display: block; aspect-ratio: 4 / 3; overflow: hidden; background: #e9e0d1; border-bottom: 1px solid var(--line); }
    .image-link img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .pet-main { padding: 16px; }
    .eyebrow { margin: 0 0 9px; color: var(--teal); text-transform: uppercase; font-size: 11px; letter-spacing: .08em; font-weight: 700; }
    h3 { margin: 0; font-size: 22px; line-height: 1.18; }
    .identity { margin: 5px 0 12px; color: var(--muted); font-size: 13px; overflow-wrap: anywhere; }
    .desc { min-height: 42px; margin: 0 0 12px; color: #3e4851; line-height: 1.45; }
    .pills { display: flex; flex-wrap: wrap; gap: 6px; min-height: 28px; }
    .pills span { background: #e6f0ed; border: 1px solid #b9d2cc; padding: 4px 8px; font-size: 12px; }
    .links { display: flex; gap: 12px; flex-wrap: wrap; margin: 14px 0; }
    a { color: #9a3f34; text-decoration-thickness: 1px; text-underline-offset: 3px; }
    details { border-top: 1px solid var(--line); padding-top: 10px; }
    summary { cursor: pointer; color: var(--ink); font-weight: 700; }
    .state-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 12px; }
    figure { margin: 0; background: #20272f; padding: 6px; }
    figure img { width: 100%; display: block; }
    figcaption { color: #f5f1e8; font-size: 11px; margin-top: 4px; text-align: center; }
    .is-hidden { display: none; }
    @media (max-width: 780px) { header { grid-template-columns: 1fr; min-height: auto; } .hero-board { grid-template-columns: 1fr 1fr; } input { margin-left: 0; width: 100%; } }
"""


def write_demo(pets: list[dict[str, Any]], collections: list[dict[str, Any]]) -> None:
    DEMO.mkdir(parents=True, exist_ok=True)
    chips = ['<button class="chip is-active" data-filter="all">全部</button>']
    chips.extend(f'<button class="chip" data-filter="{c["id"]}">{html.escape(c["title"])} · {c["pet_count"]}</button>' for c in collections)
    cards = "\n".join(pet_card(p) for p in pets)
    overview_images = "\n".join(
        f'      <img src="{demo_rel(ROOT / collection["overview_image"])}" alt="{html.escape(collection["title"])} overview">'
        for collection in collections
        if collection.get("overview_image")
    )
    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <title>Light Pets Gallery</title>
  <style>{stylesheet()}</style>
</head>
<body>
  <header>
    <section>
      <h1>Light Pets</h1>
      <p class="lead">A public-ready collection of Codex hatch pets inspired by smart lighting forms, with installable packages, QA sheets, animated state previews, and machine-readable catalog files.</p>
      <div class="stats"><span>{len(pets)} pets</span><span>8 x 9 atlas</span><span>192 x 208 cells</span><span>9 states</span></div>
    </section>
    <section class="hero-board" aria-label="overview images">
{overview_images}
    </section>
  </header>
  <main>
    <nav class="toolbar" aria-label="gallery filters">{''.join(chips)}<input id="search" type="search" placeholder="搜索 id、名称、类型或设备语义" aria-label="Search pets"></nav>
    <section class="gallery" id="gallery">{cards}</section>
  </main>
  <script>
    const chips = [...document.querySelectorAll('.chip')];
    const cards = [...document.querySelectorAll('.pet-card')];
    const search = document.querySelector('#search');
    let active = 'all';
    function applyFilter() {{
      const q = search.value.trim().toLowerCase();
      cards.forEach(card => {{
        const collectionOk = active === 'all' || card.dataset.collection === active;
        const searchOk = !q || card.dataset.text.includes(q);
        card.classList.toggle('is-hidden', !(collectionOk && searchOk));
      }});
    }}
    chips.forEach(chip => chip.addEventListener('click', () => {{
      active = chip.dataset.filter;
      chips.forEach(item => item.classList.toggle('is-active', item === chip));
      applyFilter();
    }}));
    search.addEventListener('input', applyFilter);
  </script>
</body>
</html>
"""
    (DEMO / "index.html").write_text(html_doc, encoding="utf-8")
