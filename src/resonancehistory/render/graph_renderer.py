import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from resonancehistory.analysis.transitions import compute, CATEGORIES
from resonancehistory.data.schema import HistoricalEvent

TEMPLATE_DIR = Path(__file__).parent.parent.parent.parent / "templates"


def render_transitions(events: list[HistoricalEvent], output_path: str = "transitions.html"):
    matrix = compute(events)

    regions = set(e.region for e in events)

    # Country paths for major countries
    COUNTRY_REGIONS = {
        "China":   ["Ancient China", "Imperial China Early", "Tang & Song Dynasties", "Ming & Qing Dynasties", "Modern China"],
        "USA":     ["United States History"],
        "UK":      ["British History"],
        "Germany": ["German History"],
        "Japan":   ["Feudal Japan", "Modern Japan"],
        "France":  ["French History"],
        "Russia":  ["Russian History"],
        "India":   ["Classical India", "Medieval India", "Mughal Empire", "Modern India"],
    }
    country_paths = {}
    for country, region_names in COUNTRY_REGIONS.items():
        evs = [e for e in events if e.region in region_names]
        evs.sort(key=lambda e: e.year)
        country_paths[country] = [
            {"year": e.year, "category": e.category,
             "title": e.title, "title_zh": e.title_zh or e.title_local or e.title}
            for e in evs
        ]

    data = {
        "categories": CATEGORIES,
        "counts":  {k: dict(v) for k, v in matrix.counts.items()},
        "probs":   matrix.probs,
        "top_transitions": [
            {
                "from": t[0], "to": t[1], "prob": t[2], "count": t[3],
                "example": t[4] if t[4] else None
            }
            for t in matrix.top_transitions
        ],
        "country_paths": country_paths,
        "stats": {
            "total_events":      matrix.total_events,
            "total_transitions": matrix.total_transitions,
            "total_regions":     len(regions),
        },
    }

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("transitions.html")
    html = template.render(data_json=json.dumps(data))
    Path(output_path).write_text(html, encoding="utf-8")
    print(f"Transition graph saved to {output_path}")
