"""
Compute event category transition probabilities from historical event data.

For each region, events are sorted by year. Consecutive event pairs (A → B)
are counted as transitions. The result is a Markov-style transition matrix
showing P(next_category | current_category).
"""
from collections import defaultdict
from dataclasses import dataclass
from resonancehistory.data.schema import HistoricalEvent


CATEGORIES = [
    "war", "collapse", "revolution", "cultural_peak",
    "discovery", "migration", "pandemic", "disaster",
]


@dataclass
class TransitionMatrix:
    counts: dict[str, dict[str, int]]
    probs:  dict[str, dict[str, float]]
    top_transitions: list[tuple]   # (from, to, prob, count, example)
    total_events: int
    total_transitions: int


def compute(events: list[HistoricalEvent]) -> TransitionMatrix:
    # Group by region, sort by year
    by_region: dict[str, list[HistoricalEvent]] = defaultdict(list)
    for ev in events:
        by_region[ev.region].append(ev)

    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    # Store one example pair per (from, to)
    examples: dict[str, dict[str, tuple[str, str, int, int]]] = defaultdict(dict)

    for region, evs in by_region.items():
        sorted_evs = sorted(evs, key=lambda e: e.year)
        for i in range(len(sorted_evs) - 1):
            a = sorted_evs[i]
            b = sorted_evs[i + 1]
            if a.category in CATEGORIES and b.category in CATEGORIES:
                counts[a.category][b.category] += 1
                if b.category not in examples[a.category]:
                    examples[a.category][b.category] = {
                        "a_title": a.title, "b_title": b.title,
                        "a_title_zh": a.title_zh or a.title_local or a.title,
                        "b_title_zh": b.title_zh or b.title_local or b.title,
                        "a_year": a.year, "b_year": b.year,
                    }

    # Compute probabilities
    probs: dict[str, dict[str, float]] = {}
    for cat in CATEGORIES:
        total = sum(counts[cat].values())
        if total > 0:
            probs[cat] = {to: c / total for to, c in counts[cat].items()}
        else:
            probs[cat] = {}

    # Top transitions sorted by count, with example
    top = []
    for frm, tos in counts.items():
        for to, cnt in tos.items():
            prob = probs[frm].get(to, 0)
            ex = examples[frm].get(to)
            top.append((frm, to, prob, cnt, ex))
    top.sort(key=lambda x: x[3], reverse=True)

    total_transitions = sum(sum(v.values()) for v in counts.values())

    return TransitionMatrix(
        counts=dict(counts),
        probs=probs,
        top_transitions=top[:20],
        total_events=len(events),
        total_transitions=total_transitions,
    )
