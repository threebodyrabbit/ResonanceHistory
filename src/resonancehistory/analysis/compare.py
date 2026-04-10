"""
Compare two civilizations by aligning their event sequences structurally.

Finds the longest common subsequence of event categories, scores similarity,
and identifies where the two civilizations are on the same trajectory.
"""
from resonancehistory.data.schema import HistoricalEvent
from resonancehistory.analysis.transitions import CATEGORIES


def _lcs_table(a: list[str], b: list[str]) -> list[list[int]]:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def _backtrack_lcs(dp, a, b):
    i, j = len(a), len(b)
    result = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append((i - 1, j - 1, a[i - 1]))
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return list(reversed(result))


def compare_civilizations(
    events: list[HistoricalEvent],
    region_a_names: list[str],
    region_b_names: list[str],
    label_a: str,
    label_b: str,
) -> dict:
    evs_a = sorted([e for e in events if e.region in region_a_names], key=lambda e: e.year)
    evs_b = sorted([e for e in events if e.region in region_b_names], key=lambda e: e.year)

    cats_a = [e.category for e in evs_a]
    cats_b = [e.category for e in evs_b]

    dp = _lcs_table(cats_a, cats_b)
    lcs = _backtrack_lcs(dp, cats_a, cats_b)

    lcs_len = len(lcs)
    max_len = max(len(cats_a), len(cats_b), 1)
    similarity = lcs_len / max_len

    # Build aligned timeline
    aligned = []
    for idx_a, idx_b, cat in lcs:
        ea = evs_a[idx_a]
        eb = evs_b[idx_b]
        aligned.append({
            "category": cat,
            "a": {"title": ea.title, "title_zh": ea.title_zh or ea.title_local or ea.title,
                   "year": ea.year, "description": ea.description,
                   "description_zh": ea.description_zh or ea.description_local or ea.description},
            "b": {"title": eb.title, "title_zh": eb.title_zh or eb.title_local or eb.title,
                   "year": eb.year, "description": eb.description,
                   "description_zh": eb.description_zh or eb.description_local or eb.description},
        })

    # Full timelines for side-by-side
    def ev_to_dict(e):
        return {
            "title": e.title, "title_zh": e.title_zh or e.title_local or e.title,
            "year": e.year, "category": e.category,
            "description": e.description,
            "description_zh": e.description_zh or e.description_local or e.description,
        }

    return {
        "label_a": label_a,
        "label_b": label_b,
        "similarity": round(similarity, 3),
        "lcs_length": lcs_len,
        "timeline_a": [ev_to_dict(e) for e in evs_a],
        "timeline_b": [ev_to_dict(e) for e in evs_b],
        "aligned": aligned,
    }


# Pre-defined comparison pairs
COMPARISON_PAIRS = [
    {
        "label_a": "Roman Empire",
        "label_b": "United States",
        "regions_a": ["Roman Empire"],
        "regions_b": ["United States History"],
    },
    {
        "label_a": "Roman Empire",
        "label_b": "Han Dynasty",
        "regions_a": ["Roman Empire"],
        "regions_b": ["Imperial China Early"],
    },
    {
        "label_a": "British Empire",
        "label_b": "Spanish Empire",
        "regions_a": ["British History"],
        "regions_b": ["Spanish History"],
    },
    {
        "label_a": "France",
        "label_b": "China (Ming & Qing)",
        "regions_a": ["French History"],
        "regions_b": ["Ming & Qing Dynasties"],
    },
    {
        "label_a": "Ottoman Empire",
        "label_b": "Mughal Empire",
        "regions_a": ["Ottoman Empire"],
        "regions_b": ["Mughal Empire"],
    },
    {
        "label_a": "Modern Japan",
        "label_b": "Modern Germany",
        "regions_a": ["Modern Japan"],
        "regions_b": ["German History"],
    },
]
