"""Fetch event images from Wikipedia by wiki_title, embed as base64, cache to disk."""
import asyncio
import base64
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

WIKI_SUMMARY_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
THUMB_SIZE = 200
HEADERS = {
    "User-Agent": "ResonanceHistory/1.0 (https://github.com/resonancehistory)",
    "Referer": "https://en.wikipedia.org/",
}

PORTRAIT_CACHE_DIR = Path.home() / ".cache" / "resonancehistory" / "portraits"
PORTRAIT_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_path(key: str) -> Path:
    h = hashlib.sha256(key.lower().strip().encode()).hexdigest()[:16]
    return PORTRAIT_CACHE_DIR / f"{h}.txt"


def _load_cache(key: str):
    p = _cache_path(key)
    if not p.exists():
        return False  # not cached
    val = p.read_text().strip()
    return None if val == "NONE" else val


def _save_cache(key: str, data_uri) -> None:
    _cache_path(key).write_text(data_uri if data_uri else "NONE")


def _fetch_wiki_image(wiki_title: str) -> str | None:
    cached = _load_cache(wiki_title)
    if cached is not False:
        return cached

    result = None
    try:
        encoded = urllib.parse.quote(wiki_title.replace(" ", "_"))
        req = urllib.request.Request(WIKI_SUMMARY_API.format(encoded), headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        thumb = data.get("originalimage") or data.get("thumbnail", {})
        src = thumb.get("source")
        if src:
            # Request a fixed width thumbnail via URL rewrite
            import re
            src = re.sub(r'/\d+px-', f'/{THUMB_SIZE}px-', src)
            img_req = urllib.request.Request(src, headers=HEADERS)
            with urllib.request.urlopen(img_req, timeout=8) as img_resp:
                img_bytes = img_resp.read()
                ct = img_resp.headers.get("Content-Type", "image/jpeg").split(";")[0]
            b64 = base64.b64encode(img_bytes).decode("ascii")
            result = f"data:{ct};base64,{b64}"
    except Exception as e:
        pass

    _save_cache(wiki_title, result)
    return result


async def _fetch_async(wiki_title: str) -> str | None:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _fetch_wiki_image, wiki_title)


async def _enrich_all(events: list) -> None:
    targets = [ev for ev in events if ev.wiki_title and not ev.image_url]
    if not targets:
        return

    fresh = sum(1 for ev in targets if _load_cache(ev.wiki_title) is False)
    print(f"[images] {len(targets)} events ({len(targets)-fresh} cached, {fresh} to fetch)...")

    results = await asyncio.gather(*[_fetch_async(ev.wiki_title) for ev in targets])
    found = sum(1 for r in results if r)
    for ev, url in zip(targets, results):
        if url:
            ev.image_url = url
    print(f"[images] {found}/{len(targets)} event images embedded")


def enrich_event_images(events: list) -> None:
    asyncio.run(_enrich_all(events))
