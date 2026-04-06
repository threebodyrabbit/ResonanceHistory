import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from resonancehistory.data.schema import HistoricalEvent

TEMPLATE_DIR = Path(__file__).parent.parent.parent.parent / "templates"


class Visualizer:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

    def render(self, events: list[HistoricalEvent], output_path: str = "output.html"):
        template = self.env.get_template("visualization.html")
        # Strip large base64 image_url — images are now fetched live in the browser
        data = []
        for e in events:
            d = e.model_dump()
            d.pop('image_url', None)
            data.append(d)
        events_json = json.dumps(data, indent=2)
        html = template.render(events_json=events_json)
        Path(output_path).write_text(html, encoding="utf-8")
