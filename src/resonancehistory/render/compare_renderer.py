import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from resonancehistory.data.schema import HistoricalEvent
from resonancehistory.analysis.compare import compare_civilizations, COMPARISON_PAIRS
from resonancehistory.analysis.predict import backtest_and_predict

TEMPLATE_DIR = Path(__file__).parent.parent.parent.parent / "templates"

COUNTRY_REGIONS = {
    "China":   ["Ancient China", "Imperial China Early", "Tang & Song Dynasties", "Ming & Qing Dynasties", "Modern China"],
    "USA":     ["United States History"],
    "UK":      ["British History"],
    "Germany": ["German History"],
    "Japan":   ["Feudal Japan", "Modern Japan"],
    "France":  ["French History"],
    "Russia":  ["Russian History"],
    "India":   ["Classical India", "Medieval India", "Mughal Empire", "Modern India"],
    "Iran":    ["Persian Empire", "Iran History"],
    "Spain":   ["Spanish History"],
}


def render_comparison(events: list[HistoricalEvent], output_path: str = "compare.html"):
    comparisons = []
    for pair in COMPARISON_PAIRS:
        result = compare_civilizations(
            events,
            pair["regions_a"], pair["regions_b"],
            pair["label_a"], pair["label_b"],
        )
        # Generate "what comes next" prediction from the alignment
        if result["aligned"]:
            last_a = result["timeline_a"][-1] if result["timeline_a"] else None
            last_b = result["timeline_b"][-1] if result["timeline_b"] else None
            # Find where B's last event aligns in A's timeline
            a_cats = [e["category"] for e in result["timeline_a"]]
            b_last_cat = last_b["category"] if last_b else None
            next_in_a = None
            if b_last_cat and b_last_cat in a_cats:
                idx = len(a_cats) - 1 - a_cats[::-1].index(b_last_cat)
                if idx + 1 < len(result["timeline_a"]):
                    next_ev = result["timeline_a"][idx + 1]
                    next_in_a = {
                        "title": next_ev["title"],
                        "title_zh": next_ev["title_zh"],
                        "year": next_ev["year"],
                        "category": next_ev["category"],
                        "description": next_ev["description"],
                        "description_zh": next_ev["description_zh"],
                    }
            result["prediction"] = next_in_a
        else:
            result["prediction"] = None
        comparisons.append(result)

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("compare.html")

    # Backtest + predict
    predictions = backtest_and_predict(events, COUNTRY_REGIONS)

    html = template.render(
        data_json=json.dumps(comparisons),
        predictions_json=json.dumps(predictions),
    )
    Path(output_path).write_text(html, encoding="utf-8")
    print(f"Comparison saved to {output_path}")
