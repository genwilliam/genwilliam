import os
from pathlib import Path

import cairosvg
import requests


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def fetch_svg(url: str) -> bytes:
    """Download an SVG document."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.content


def svg_to_png(svg_bytes: bytes, output_path: Path) -> None:
    """Convert SVG bytes to a PNG file at output_path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(bytestring=svg_bytes, write_to=str(output_path))


def main() -> None:
    username = os.environ.get("STATS_USERNAME", "genwilliam")
    theme = os.environ.get("STATS_THEME", "gruvbox")
    trophy_theme = os.environ.get("TROPHY_THEME", theme)

    targets = [
        {
            "name": "github-stats.png",
            "url": f"https://github-readme-stats.vercel.app/api"
            f"?username={username}&show_icons=true&theme={theme}",
        },
        {
            "name": "top-langs.png",
            "url": f"https://github-readme-stats.vercel.app/api/top-langs/"
            f"?username={username}&layout=compact&theme={theme}",
        },
        {
            "name": "trophy.png",
            "url": f"https://github-profile-trophy.vercel.app/"
            f"?username={username}&theme={trophy_theme}",
        },
    ]

    for target in targets:
        name, url = target["name"], target["url"]
        print(f"Fetching {name} from {url}")
        svg_bytes = fetch_svg(url)
        svg_to_png(svg_bytes, ASSETS_DIR / name)
        print(f"Saved {name} to {ASSETS_DIR / name}")


if __name__ == "__main__":
    main()
