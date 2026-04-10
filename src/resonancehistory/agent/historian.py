import asyncio
import hashlib
import json
import os
from pathlib import Path

from google import genai
from google.genai import types

from resonancehistory.data.schema import HistoricalEvent

# ── Cache ──────────────────────────────────────────────────────────────────
CACHE_DIR = Path.home() / ".cache" / "resonancehistory"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_key(region: str, era: str, count: int) -> str:
    raw = f"{region}|{era}|{count}".lower().strip()
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _load_cache(key: str) -> list[dict] | None:
    path = CACHE_DIR / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())
    return None


def _save_cache(key: str, data: list[dict]) -> None:
    path = CACHE_DIR / f"{key}.json"
    path.write_text(json.dumps(data, indent=2))


def _normalize_figures(figures: list) -> list[dict]:
    """Normalize figures whether Gemini returns strings or dicts."""
    result = []
    for f in figures:
        if isinstance(f, dict):
            result.append({
                "name": f.get("name", ""),
                "role": f.get("role", "") or f.get("title", "") or f.get("position", ""),
                "portrait_url": None,
            })
        elif isinstance(f, str):
            f = f.strip()
            if '(' in f and f.endswith(')'):
                name, role = f[:-1].rsplit('(', 1)
            elif ' — ' in f:
                name, role = f.split(' — ', 1)
            elif ' - ' in f:
                name, role = f.split(' - ', 1)
            elif ': ' in f:
                role, name = f.split(': ', 1)
            else:
                name, role = f, ''
            result.append({"name": name.strip(), "role": role.strip(), "portrait_url": None})
    return result


def _parse_events(data: list[dict], region: str) -> list[HistoricalEvent]:
    events = []
    for e in data:
        e.setdefault("region", region)
        e.setdefault("title", e.get("id", "unknown").replace("-", " ").title())
        e.setdefault("description", "")
        if "figures" in e:
            e["figures"] = _normalize_figures(e["figures"])
        # Normalise any field that should be a list or dict but isn't
        for field in ("resonances", "figures"):
            if not isinstance(e.get(field), list):
                e[field] = []
        for field in ("resonance_reasons", "resonance_reasons_zh"):
            if not isinstance(e.get(field), dict):
                e[field] = {}
        try:
            events.append(HistoricalEvent(**e))
        except Exception as ex:
            print(f"[warn] Skipping malformed event {e.get('id', '?')}: {ex}")
    return events
SYSTEM_PROMPT = """You are a careful, factual historian and pattern-recognition scholar. Your task is to generate historically accurate events as structured JSON.

STRICT RULES — follow these exactly:
1. Only include events that are well-documented in mainstream historical scholarship.
2. Only include real, historically verified figures. Do NOT invent people. "figures" must be an array of objects with exactly these keys: {"name": "...", "role": "...", "portrait_url": null}. Never use strings.
3. Set "confidence" to:
   - "high"        — event and date are well-established in primary/secondary sources
   - "medium"      — event is accepted but exact date or details are debated
   - "speculative" — event is plausible but evidence is limited or contested
4. Always set "portrait_url" to null. Never generate or guess image URLs.
5. "year" must be an integer. Use negative numbers for BCE (e.g. -264 for 264 BCE).
6. "lat" and "lng" must be the precise coordinates of the SPECIFIC city, site, or battlefield where the event occurred. Examples: An Lushan Rebellion → Beijing (39.9042, 116.4074), Battle of Thermopylae → Thermopylae (38.7953, 22.5337). Never use country or region centroids.
7. "resonances" must only reference "id" values of OTHER events in the same response array.
   Only include resonances that are genuinely striking cross-civilizational echoes — limit to 1 resonance per event maximum, only for high-confidence events.
   "resonance_reasons" must be an object mapping each resonance id to a deep, analytical 1-2 sentence explanation in ENGLISH of the STRUCTURAL PATTERN that connects these two events — not surface similarity, but the underlying historical dynamic. Focus on how economic collapse, imperial overreach, peasant revolt, plague, climate shock, or ideological rupture created the same cascading pattern in different civilizations that had no contact with each other. Example: "Both empires collapsed not from external conquest alone, but from the same internal spiral: currency debasement funding endless frontier wars, which triggered tax revolts among peasants, which starved the military of recruits, accelerating the very collapse the taxes were meant to prevent." Avoid generic statements like "both were revolutions" or "both marked the rise of new powers."
   "resonance_reasons_zh" must be the same object but with the explanation translated into Simplified Chinese.
8. "id" must be a lowercase hyphenated slug, unique within the array.
9. "category" must be one of: collapse, revolution, cultural_peak, war, discovery, migration, pandemic, disaster, technology, diplomacy, economic_crisis, economic_boom, reform, independence, civil_war, colonization.
   Choose the most specific category. Use "technology" for scientific/technological breakthroughs, "diplomacy" for treaties/alliances/international relations, "economic_crisis" for recessions/depressions/hyperinflation, "economic_boom" for trade expansions/industrial growth, "reform" for major policy/legal reforms, "independence" for independence movements, "civil_war" for internal armed conflicts, "colonization" for colonial expansion.
10. For East Asian regions (China, Japan, Korea, Vietnam, Mongolia), populate "title_local" and "description_local" in the region's native script.
    For ALL events regardless of region, also populate:
    - "title_zh": the event title translated into Simplified Chinese
    - "description_zh": a 1-2 sentence description in Simplified Chinese
    For all other regions, set "title_local" and "description_local" to null.
11. "wiki_title" must be the exact English Wikipedia article title for this event. If no dedicated article exists, set to null.
12. Include major dynasty changes, pandemics, famines, natural disasters, economic crises, and social upheavals — not just wars and political events.

Return ONLY a valid JSON array. No markdown fences, no explanation, no commentary."""


def _user_prompt(region: str, era: str, count: int) -> str:
    return (
        f"Generate exactly {count} significant historical events for the region '{region}' "
        f"during the era '{era}'. "
        f"Prioritize events with high historical confidence. "
        f"Include key figures where well-documented. "
        f"Note resonances with other events in the list where patterns genuinely recur."
    )


# ── Historian ──────────────────────────────────────────────────────────────
class Historian:
    def __init__(self, model: str = "gemini-2.5-flash-lite"):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = model

    def generate(self, region: str, era: str, count: int = 12) -> list[HistoricalEvent]:
        """Generate events for a single region/era, with caching."""
        key = _cache_key(region, era, count)
        cached = _load_cache(key)
        if cached:
            print(f"[cache hit] {region} / {era}")
            return _parse_events(cached, region)

        print(f"[api call] {region} / {era}")
        data = self._call_gemini(region, era, count)
        _save_cache(key, data)
        return _parse_events(data, region)

    def generate_batch(
        self, requests: list[tuple[str, str, int]]
    ) -> list[HistoricalEvent]:
        """
        Generate events for multiple (region, era, count) tuples.
        Cache hits are resolved immediately; remaining requests are sent
        as parallel async Gemini calls (one call per uncached request).
        """
        results: list[HistoricalEvent] = []
        uncached: list[tuple[str, str, int]] = []

        for region, era, count in requests:
            key = _cache_key(region, era, count)
            cached = _load_cache(key)
            if cached:
                print(f"[cache hit] {region} / {era}")
                results.extend(_parse_events(cached, region))
            else:
                uncached.append((region, era, count))

        if uncached:
            fresh = asyncio.run(self._batch_async(uncached))
            results.extend(fresh)
        return results

    async def _batch_async(
        self, requests: list[tuple[str, str, int]]
    ) -> list[HistoricalEvent]:
        # Sequential with delay to avoid rate limits
        events = []
        for i, (r, e, c) in enumerate(requests):
            print(f"[api call {i+1}/{len(requests)}] {r} / {e}")
            for attempt in range(5):
                try:
                    data = await self._call_gemini_async(r, e, c)
                    _save_cache(_cache_key(r, e, c), data)
                    events.extend(_parse_events(data, r))
                    break
                except Exception as ex:
                    if attempt == 4:
                        print(f"[FAILED] {r} after 5 attempts: {ex}")
                        break
                    wait = 15 * (attempt + 1)
                    print(f"  [retry {attempt+1}] {ex.__class__.__name__}, waiting {wait}s...")
                    await asyncio.sleep(wait)
            await asyncio.sleep(2)  # pause between regions
        return events

    def _call_gemini(self, region: str, era: str, count: int) -> list[dict]:
        response = self.client.models.generate_content(
            model=self.model,
            contents=_user_prompt(region, era, count),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
                response_mime_type="application/json",
            ),
        )
        return _parse_response(response.text)

    async def _call_gemini_async(
        self, region: str, era: str, count: int
    ) -> list[dict]:
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=_user_prompt(region, era, count),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
                response_mime_type="application/json",
            ),
        )
        return _parse_response(response.text)


def _parse_response(text: str) -> list[dict]:
    if not text or not text.strip():
        raise ValueError("Gemini returned an empty response")
    raw = text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        # Gemini sometimes returns multiple concatenated JSON arrays — merge them
        import re as _re
        chunks = _re.split(r'\]\s*\[', raw)
        if len(chunks) > 1:
            merged = []
            for i, chunk in enumerate(chunks):
                if i > 0: chunk = '[' + chunk
                if i < len(chunks) - 1: chunk = chunk + ']'
                try: merged.extend(json.loads(chunk))
                except Exception: pass
            if merged:
                return merged
        raise ValueError(f"Failed to parse Gemini response as JSON\nRaw:\n{raw[:500]}")
    if isinstance(parsed, dict):
        for v in parsed.values():
            if isinstance(v, list):
                return v
        raise ValueError(f"Unexpected JSON object: {list(parsed.keys())}")
    return parsed
