#!/usr/bin/env python3
"""Export Aura palette variables or check representative contrast pairs."""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / "references" / "palette.json"
HEX = re.compile(r"#[0-9a-fA-F]{6}")
ROLE = re.compile(r"[a-z][a-z0-9-]*")
PAIRS = (
    ("foreground", "background", 4.5),
    ("foreground", "window", 4.5),
    ("muted", "surface", 4.5),
    ("foreground", "selection", 4.5),
    ("mint", "background", 4.5),
    ("accent", "window", 3.0),
)


def load_palette(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    colors = data.get("colors") if isinstance(data, dict) else None
    if not isinstance(colors, dict) or not colors or any(
        not ROLE.fullmatch(role) or role.startswith("ansi-") or not isinstance(color, str) or not HEX.fullmatch(color)
        for role, color in colors.items()
    ):
        raise ValueError("colors must map lowercase role names outside ansi-* to six-digit hex values")
    ansi = data.get("ansi", [])
    if "ansi" in data:
        if not isinstance(ansi, list) or len(ansi) != 16 or any(
            not isinstance(color, str) or not HEX.fullmatch(color) for color in ansi
        ):
            raise ValueError("ansi must contain 16 six-digit hex values in terminal index order")
    return colors, ansi


def css(colors, ansi):
    lines = [":root {", "  color-scheme: dark;"]
    lines.extend(f"  --aura-{role}: {color};" for role, color in colors.items())
    lines.extend(f"  --aura-ansi-{index}: {color};" for index, color in enumerate(ansi))
    lines.append("}")
    return "\n".join(lines)


def luminance(color):
    def linear(value):
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    rgb = [linear(int(color[index:index + 2], 16) / 255) for index in (1, 3, 5)]
    return sum(channel * weight for channel, weight in zip(rgb, (0.2126, 0.7152, 0.0722)))


def contrast(colors, pairs):
    report = []
    for foreground, background, threshold in pairs:
        low, high = sorted((luminance(colors[foreground]), luminance(colors[background])))
        ratio = (high + 0.05) / (low + 0.05)
        report.append({"foreground": foreground, "background": background, "ratio": round(ratio, 3),
                       "minimum": threshold, "passes": ratio >= threshold})
    return {"ok": all(item["passes"] for item in report), "pairs": report}


def parse_pair(value):
    try:
        foreground, background, minimum = value.split(":")
        threshold = float(minimum)
        if ROLE.fullmatch(foreground) and ROLE.fullmatch(background) and 1 <= threshold <= 21:
            return foreground, background, threshold
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("use foreground:background:minimum with a ratio between 1 and 21")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("format", choices=("css", "contrast"))
    parser.add_argument("--palette", type=Path, default=DEFAULT)
    parser.add_argument("--pair", type=parse_pair, action="append", metavar="FOREGROUND:BACKGROUND:MINIMUM",
                        help="replace the default checks with one or more explicit pairs")
    args = parser.parse_args()
    if args.pair and args.format != "contrast":
        parser.error("--pair requires contrast output")
    try:
        colors, ansi = load_palette(args.palette.expanduser())
        if args.format == "css":
            print(css(colors, ansi))
            return 0
        result = contrast(colors, args.pair or PAIRS)
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"{parser.prog}: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
