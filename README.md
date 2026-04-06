# ResonanceHistory

History doesn't just happen linearly — it echoes. The same dynamics repeat across civilizations that had no contact with each other: imperial overreach leading to currency debasement and peasant revolt, plague reshaping labor markets and triggering cultural renaissances, ideological ruptures following economic collapse. ResonanceHistory makes these patterns visible.

An open source, AI-powered interactive map that surfaces the hidden structural patterns history keeps repeating — across civilizations, centuries apart.

![World map timeline](asset/sc-1.png)
![Event card with resonance](asset/sc-2.png)
![Resonance echo detail](asset/sc-3.png)

![ResonanceHistory](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

## What It Does

- Generates 400+ historically accurate events across 50+ regions (600 BCE – 2024)
- Covers dynasty changes, wars, pandemics, famines, natural disasters, economic crises, and cultural peaks
- Renders an interactive world map with timeline playback — watch history unfold
- Identifies deep structural echoes between events: not "both were revolutions" but *why* the same economic spiral, plague dynamic, or ideological rupture played out identically in civilizations that never met
- Bilingual display for East Asian events (Chinese, Japanese, Korean)
- Fully self-contained HTML output — no server required

## Setup

**Requirements:** Python 3.10+, a [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key)

```bash
git clone https://github.com/yourusername/ResonanceHistory.git
cd ResonanceHistory

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install
pip install -e .

# Set your Gemini API key
export GEMINI_API_KEY=your_key_here
```

## Run

Generate the full world visualization and open it in your browser:

```bash
python -m resonancehistory --all-regions --output world.html --open
```

Or target specific regions:

```bash
python -m resonancehistory \
  --region "Roman Empire" --era "500 BCE - 476 CE" \
  --region "Han Dynasty"  --era "206 BCE - 220 CE" \
  --output comparison.html --open
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--all-regions` | — | Generate all 50+ built-in regions |
| `--region` / `--era` | — | Custom region + era pair (repeatable) |
| `--output` | `output.html` | Output file path |
| `--open` | off | Auto-open in browser after generation |

## How It Works

1. The LLM agent generates events for each region in parallel (batched async Gemini calls)
2. Events are cached locally in `~/.cache/resonancehistory/` — repeat runs are instant
3. The visualizer renders a self-contained HTML file using Leaflet.js
4. Click any pulsing dot (events with resonance connections) to see its structural echo in another civilization, with an analytical explanation of the repeating pattern

## Python API

```python
from resonancehistory.agent.historian import Historian
from resonancehistory.render.visualizer import Visualizer

historian = Historian()  # uses gemini-2.5-flash by default
events = historian.generate_batch([
    ("Roman Empire", "500 BCE - 476 CE", 16),
    ("Han Dynasty",  "206 BCE - 220 CE", 12),
])

Visualizer().render(events, output_path="output.html")
```

## Contributing

Contributions welcome — open an issue or pull request.

## License

MIT
