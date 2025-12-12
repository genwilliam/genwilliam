import os
import time
from pathlib import Path
from typing import Iterable

import cairosvg
import requests


OUTPUT_DIR = Path(
    os.environ.get("STATS_OUTPUT_DIR", Path(__file__).resolve().parent.parent / "dist")
)


def fetch_svg(url: str, retries: int = 5, delay: float = 2.5) -> bytes:
    """Download an SVG document with basic retry to handle transient 5xx."""
    headers = {"User-Agent": "genwilliam-stats-bot/1.0"}
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=30, headers=headers)
            resp.raise_for_status()
            return resp.content
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response else "unknown"
            if attempt == retries or status < 500:
                raise
            wait = delay * attempt
            print(f"[WARN] {status} on {url}, retry {attempt}/{retries} after {wait}s")
            time.sleep(wait)
    raise RuntimeError("Unreachable fetch_svg loop")


def svg_to_png(svg_bytes: bytes, output_path: Path) -> None:
    """Convert SVG bytes to a PNG file at output_path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(bytestring=svg_bytes, write_to=str(output_path))


def build_targets(username: str, theme: str, trophy_theme: str) -> Iterable[dict]:
    base_stats = "https://github-readme-stats.vercel.app"
    base_trophy = "https://github-profile-trophy.vercel.app"
    return [
        {
            "name": "github-stats.png",
            "url": f"{base_stats}/api?username={username}&show_icons=true&theme={theme}",
        },
        {
            "name": "top-langs.png",
            "url": f"{base_stats}/api/top-langs/?username={username}"
            f"&layout=compact&theme={theme}",
        },
        {
            "name": "trophy.png",
            "url": f"{base_trophy}/?username={username}&theme={trophy_theme}",
        },
    ]


def main() -> None:
    username = os.environ.get("STATS_USERNAME", "genwilliam")
    theme = os.environ.get("STATS_THEME", "gruvbox")
    trophy_theme = os.environ.get("TROPHY_THEME", theme)

    print(f"Output dir: {OUTPUT_DIR}")
    for target in build_targets(username, theme, trophy_theme):
        name, url = target["name"], target["url"]
        print(f"Fetching {name} from {url}")
        svg_bytes = fetch_svg(url)
        out_path = OUTPUT_DIR / name
        svg_to_png(svg_bytes, out_path)
        print(f"Saved {name} to {out_path}")


if __name__ == "__main__":
    main()
