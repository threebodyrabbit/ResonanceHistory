"""
Backtest transition predictions and predict next event for each country.
Uses a sliding window of recent events (not just the last one) to weight predictions.
"""
from collections import defaultdict
from resonancehistory.data.schema import HistoricalEvent
from resonancehistory.analysis.transitions import compute, CATEGORIES


def _weighted_prediction(probs: dict, recent_cats: list[str], window: int = 3) -> list[tuple[str, float]]:
    """
    Combine transition probabilities from the last `window` events.
    More recent events get higher weight (exponential decay).
    """
    combined: dict[str, float] = defaultdict(float)
    total_weight = 0

    for i, cat in enumerate(recent_cats[-window:]):
        weight = 2 ** i  # exponential: most recent = highest weight
        total_weight += weight
        row = probs.get(cat, {})
        for next_cat, p in row.items():
            combined[next_cat] += p * weight

    if total_weight > 0:
        for k in combined:
            combined[k] /= total_weight

    return sorted(combined.items(), key=lambda x: -x[1])


def backtest_and_predict(events: list[HistoricalEvent], country_regions: dict[str, list[str]]) -> dict:
    matrix = compute(events)
    probs = matrix.probs

    results = {}

    for country, region_names in country_regions.items():
        evs = sorted([e for e in events if e.region in region_names], key=lambda e: e.year)
        if len(evs) < 2:
            continue

        # Backtest with multi-factor window
        correct = 0
        total = 0
        predictions_log = []
        window = 3

        for i in range(len(evs) - 1):
            actual_next = evs[i + 1].category
            if actual_next not in CATEGORIES:
                continue

            recent = [e.category for e in evs[max(0, i - window + 1):i + 1] if e.category in CATEGORIES]
            if not recent:
                continue

            preds = _weighted_prediction(probs, recent, window)
            if not preds:
                continue

            predicted = preds[0][0]
            predicted_prob = preds[0][1]
            actual_prob = dict(preds).get(actual_next, 0)
            hit = predicted == actual_next
            if hit:
                correct += 1
            total += 1

            predictions_log.append({
                "from_title": evs[i].title,
                "from_title_zh": evs[i].title_zh or evs[i].title_local or evs[i].title,
                "from_year": evs[i].year,
                "from_cat": evs[i].category,
                "context_cats": recent,
                "actual_title": evs[i + 1].title,
                "actual_title_zh": evs[i + 1].title_zh or evs[i + 1].title_local or evs[i + 1].title,
                "actual_year": evs[i + 1].year,
                "actual_cat": actual_next,
                "predicted_cat": predicted,
                "predicted_prob": round(predicted_prob, 3),
                "actual_prob": round(actual_prob, 3),
                "hit": hit,
            })

        accuracy = correct / total if total > 0 else 0

        # Predict next from latest events using window
        recent_cats = [e.category for e in evs[-window:] if e.category in CATEGORIES]
        preds = _weighted_prediction(probs, recent_cats, window)[:5]

        latest = evs[-1]

        results[country] = {
            "accuracy": round(accuracy, 3),
            "correct": correct,
            "total": total,
            "log": predictions_log[-5:],  # last 5 for display
            "latest": {
                "title": latest.title,
                "title_zh": latest.title_zh or latest.title_local or latest.title,
                "year": latest.year,
                "category": latest.category,
            },
            "context": [
                {"category": e.category, "year": e.year,
                 "title": e.title, "title_zh": e.title_zh or e.title_local or e.title}
                for e in evs[-window:]
            ],
            "next_predictions": [
                {"category": cat, "probability": round(p, 3)}
                for cat, p in preds
            ],
        }

    return results
