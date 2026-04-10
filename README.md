# ResonanceHistory

🌐 **Live Demo:** [Map](https://threebodyrabbit.github.io/ResonanceHistory/) · [Transitions](https://threebodyrabbit.github.io/ResonanceHistory/world_transitions.html) · [Compare](https://threebodyrabbit.github.io/ResonanceHistory/world_compare.html)

History doesn't just happen linearly. It echoes. This is an AI powered interactive map that shows you how history repeats itself across countries and time.

![World map timeline](asset/sc-1.png)
![Event card with resonance](asset/sc-2.png)
![Resonance echo detail](asset/sc-3.png)

![ResonanceHistory](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

## What It Does

700+ historically accurate events across 64 regions and countries, from 600 BCE to 2026. Covers wars, collapses, revolutions, technology breakthroughs, diplomatic events, economic crises and booms, reforms, pandemics, natural disasters, independence movements, civil wars, colonization, cultural peaks, discoveries, and migrations — 16 event categories in total.

Three linked interactive pages:

**Map** — world map with timeline playback. Pulsing dots mark events with resonance connections. Click one to see its structural echo in another civilization. Switch between English and Chinese (简体中文).

**Transitions** — Markov transition graph and heatmap showing how event types follow each other across civilizations. Country-specific event paths for China, USA, UK, Germany, Japan, France, Russia, India. Top transitions with real historical examples.

**Compare** — side-by-side structural alignment of civilization pairs (Rome vs USA, Rome vs Han Dynasty, etc.). Backtest accuracy of transition predictions per country. Multi-factor forecast of what comes next based on each country's recent event pattern.

Fully self-contained HTML output, no server required.

## Try It Without Running

A pre-generated visualization is included in `docs/index.html`:

```bash
open docs/index.html
```

## Setup

Requires Python 3.10+ and a [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key).

```bash
git clone https://github.com/threebodyrabbit/ResonanceHistory.git
cd ResonanceHistory

python3 -m venv .venv
source .venv/bin/activate
pip install -e .

export GEMINI_API_KEY=your_key_here
```

## Run

Generate all three pages (map, transitions, compare):

```bash
python -m resonancehistory --all-regions --output world.html --transitions --open
```

Or target specific regions:

```bash
python -m resonancehistory \
  --region "Roman Empire" --era "500 BCE - 476 CE" \
  --region "Han Dynasty"  --era "206 BCE - 220 CE" \
  --output comparison.html --open
```

| Flag | Default | Description |
|------|---------|-------------|
| `--all-regions` | | Generate all 64 built-in regions |
| `--region` / `--era` | | Custom region + era pair, repeatable |
| `--output` | `output.html` | Output file path |
| `--transitions` | off | Also generate transitions and compare pages |
| `--open` | off | Open in browser after generation |

## How It Works

The LLM agent (Gemini 2.5 Flash) generates events for each region sequentially with automatic retry and caching. Results are stored in `~/.cache/resonancehistory/` so repeat runs are instant.

Events include bilingual content (English + Chinese), Wikipedia links, geographic coordinates, and resonance connections with structural explanations.

The transition analysis builds a Markov chain over 16 event categories, computes transition probabilities, and uses a sliding window of recent events with exponential weighting for multi-factor predictions.

## Python API

```python
from resonancehistory.agent.historian import Historian
from resonancehistory.render.visualizer import Visualizer

historian = Historian()
events = historian.generate_batch([
    ("Roman Empire", "500 BCE - 476 CE", 16),
    ("Han Dynasty",  "206 BCE - 220 CE", 12),
])

Visualizer().render(events, output_path="output.html")
```

## Contributing

Open an issue or pull request.

## License

MIT
