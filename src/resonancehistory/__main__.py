import argparse
from resonancehistory.agent.historian import Historian
from resonancehistory.agent.portraits import enrich_event_images
from resonancehistory.render.visualizer import Visualizer
from resonancehistory.data.regions import MAJOR_REGIONS


def main():
    parser = argparse.ArgumentParser(description="ResonanceHistory — generate a historical visualization.")
    parser.add_argument("--region", action="append",
                        help="Region to include (repeatable). Omit to use --all-regions.")
    parser.add_argument("--era", action="append",
                        help="Era per region in matching order.")
    parser.add_argument("--all-regions", action="store_true",
                        help="Generate events for all major world regions.")
    parser.add_argument("--count", type=int, default=8,
                        help="Events per region (default: 8; use fewer when running all regions)")
    parser.add_argument("--output", default="output.html", help="Output HTML file path")
    parser.add_argument("--open", action="store_true", help="Open the output in the browser after generation")
    args = parser.parse_args()

    if args.all_regions:
        requests = [(r, e, c) for r, e, _, c in MAJOR_REGIONS]
        total = sum(c for _, _, _, c in MAJOR_REGIONS)
        print(f"Generating {len(requests)} regions ({total} total events)...")
    elif args.region and args.era:
        if len(args.region) != len(args.era):
            parser.error("--region and --era must be provided in matching pairs")
        requests = [(r, e, args.count) for r, e in zip(args.region, args.era)]
    else:
        parser.error("Provide --all-regions, or one or more --region/--era pairs")

    historian = Historian()
    events = historian.generate_batch(requests)
    print(f"Generated {len(events)} events total.")

    enrich_event_images(events)

    visualizer = Visualizer()
    visualizer.render(events, output_path=args.output)
    print(f"Visualization saved to {args.output}")
    if args.open:
        import webbrowser, pathlib
        webbrowser.open(pathlib.Path(args.output).resolve().as_uri())


if __name__ == "__main__":
    main()
