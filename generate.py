#!/usr/bin/env python3
"""Render the profile README artwork from the last GitHub contribution snapshot."""

import argparse
import datetime
from html import escape
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import profile_data as data

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artwork"
FRAMES = 16

PALETTES = {
    "dark": {
        "sky": "#091519", "base": "#0c191d", "text": "#f1f4f0", "sub": "#afbfbd", "accent": "#73dad1",
        "line": "#293a3c", "water-high": "#78eee1", "water-mid": "#13c6c7", "water-deep": "#078396",
        "water-low": "#154b61", "back-left": "#17474d", "back-mid": "#267e84", "back-light": "#70c8c0",
        "back-right": "#285d68", "front-left": "#158d96", "front-mid": "#106074", "front-right": "#11394d",
    },
    "light": {
        "sky": "#f4f7f4", "base": "#f8faf7", "text": "#192b2d", "sub": "#4d6666", "accent": "#087f7d",
        "line": "#c3d2cf", "water-high": "#99f6e8", "water-mid": "#4bcfc6", "water-deep": "#168fa1",
        "water-low": "#226c80", "back-left": "#a4d1c9", "back-mid": "#8ccbc3", "back-light": "#b5e8da",
        "back-right": "#78b5b3", "front-left": "#41b5b4", "front-mid": "#248997", "front-right": "#21677b",
    },
}

TYPE = """
text {font-family:Inter,'Segoe UI',Arial,sans-serif;fill:var(--text)}
.brand {font-size:13px;font-weight:650;letter-spacing:2px}
.name {font-size:71px;font-weight:600;letter-spacing:-3.3px}
.role {font-size:21px;fill:var(--sub)}
.metric {font-size:21px;font-weight:600;letter-spacing:-.5px}
.caption {font-size:12px;fill:var(--sub)}
.dates {font-size:11.5px;fill:var(--sub);font-variant-numeric:tabular-nums}
.mobile .name {font-size:41px;letter-spacing:-1.8px}
.mobile .role {font-size:16px}
.mobile .metric {font-size:21px}
.mobile .caption {font-size:12px}
.mobile .dates {font-size:11px}
"""


def text_at(x, y, content, style, anchor="start", fit=None):
    spacing = f' textLength="{fit}" lengthAdjust="spacingAndGlyphs"' if fit else ""
    return (f'<text x="{x:g}" y="{y:g}" class="{style}" text-anchor="{anchor}"{spacing}>'
            f'{escape(str(content))}</text>')


def water_height(layer, x, phase, shore, mobile):
    """Superimpose a travelling swell and a slower crest under the drops."""
    a = math.tau * x
    crest_x = .75 + .045 * math.sin(phase)
    crest = math.exp(-((x - crest_x) / .18) ** 2)
    k = .74 if mobile else 1
    surface = shore - k * (68 + 48 * crest)
    if layer == "far":
        return surface + k * (13 * math.sin(a + phase + 1) - 19 * math.cos(a * 1.5 - phase))
    if layer == "near":
        return shore - k * (22 + 12 * math.sin(a - phase + .45) + 8 * math.sin(2*a + phase))
    return surface + k * (10 * math.sin(a + phase) + 15 * math.sin(2*a - phase + .7))


def surface_path(layer, width, shore, phase, mobile):
    """Smooth quadratic spans share their knots at every phase of the loop."""
    intervals = 18
    step = (width + 40) / intervals
    points = []
    for i in range(intervals + 1):
        x = -20 + i * step
        y = water_height(layer, x / width, phase, shore, mobile)
        points.append((x, y))
    commands = [f'M{points[0][0]:g} {points[0][1]:.1f}']
    for (x, y), (end_x, end_y) in zip(points, points[1:]):
        commands.append(f'Q{x:.1f} {y:.1f} {(x+end_x)/2:.1f} {(y+end_y)/2:.1f}')
    x, y = points[-1]
    commands.append(f'L{x:.1f} {y:.1f}V{shore+14}H-20Z')
    return ''.join(commands)


def motion(name, frames):
    rules = ''.join(f'{i*100/FRAMES:g}%{{{value}}}' for i, value in enumerate(frames))
    return f'.{name}{{animation:{name} 13s linear infinite}}@keyframes {name}{{{rules}}}'


def highlight_path(width, shore, phase, mobile):
    """A tapered reflection follows the lit face of the main swell."""
    scale = .74 if mobile else 1
    upper, lower = [], []
    for i in range(19):
        u = i / 18
        x = width * (.18 + .82*u)
        envelope = math.sin(math.pi*u)**2
        depth = 8 + envelope*(8 + 6*math.sin(phase + 7*u))
        y = water_height("body", x/width, phase, shore, mobile) + depth*scale
        upper.append((x, y))
        lower.append((x, y + scale*envelope*(4.5 + 3.5*math.cos(phase - 10*u))))
    points = upper + list(reversed(lower))
    segments = [f'M{points[0][0]:.1f} {points[0][1]:.1f}']
    for (x, y), (nx, ny) in zip(points, points[1:]):
        segments.append(f'Q{x:.1f} {y:.1f} {(x+nx)/2:.1f} {(y+ny)/2:.1f}')
    return ''.join(segments) + 'Z'


def liquid(width, shore, mobile):
    # Set the final phase to exactly zero so the static frame and the seam agree.
    phases = [math.tau * i / FRAMES for i in range(FRAMES)] + [0]
    styles, paths = [], {}
    for layer in ("far", "body", "near"):
        frames = [surface_path(layer, width, shore, phase, mobile) for phase in phases]
        paths[layer] = f'class="{layer}" d="{frames[0]}"'
        styles.append(motion(layer, [f'd:path("{frame}")' for frame in frames]))
    highlights = [highlight_path(width, shore, phase, mobile) for phase in phases]
    styles.append(motion("glint", [f'd:path("{frame}")' for frame in highlights]))

    drops = []
    # Relative position, radius, travel above the crest, and time of release.
    beads = [(.72, 22, 69, .3), (.79, 9, 84, 1.4), (.86, 12, 41, 2.8), (.65, 6, 33, 3.4)]
    scale = .65 if mobile else 1
    for index, (pos, r, travel, offset) in enumerate(beads):
        transforms = []
        for phase in phases:
            lift = (1 + math.cos(phase + offset)) / 2
            dx = pos * width + 8 * scale * math.sin(phase + offset)
            dy = water_height("body", dx / width, phase, shore, mobile) + scale * (r * .75 - travel * lift)
            stretch = 1 + .17 * math.sin(phase + offset)
            transforms.append((dx, dy, stretch))
        name = f'drop{index}'
        styles.append(motion(name, [f'transform:translate({x:.1f}px,{y:.1f}px) scale({1/s:.3f},{s:.3f})'
                                    for x, y, s in transforms]))
        x, y, s = transforms[0]
        drops.append(f'<g class="{name}" transform="translate({x:.1f} {y:.1f}) scale({1/s:.3f} {s:.3f})">'
                     f'<circle r="{r*scale:g}" fill="url(#bead)"/></g>')

    return ''.join([
        f'<defs><clipPath id="sea"><rect width="{width}" height="{shore}"/></clipPath></defs>',
        '<style>@media (prefers-reduced-motion:no-preference){', *styles, '}</style>',
        '<g clip-path="url(#sea)">',
        f'<path {paths["far"]} fill="url(#back)"/>',
        '<g filter="url(#cohesion)">', *drops, f'<path {paths["body"]} fill="url(#water)"/></g>',
        f'<path class="glint" d="{highlights[0]}" fill="url(#refraction)" opacity=".82"/>',
        f'<path {paths["near"]} fill="url(#front)" stroke="url(#refraction)" stroke-width="1.1"/>',
        '</g>',
    ])


def activity(stats, width, margin, shore, mobile):
    start = datetime.date.fromisoformat(stats["from"])
    end = datetime.date.fromisoformat(stats["through"])
    date_range = f"{start:%b %Y} – {end:%d %b %Y}"
    metrics = [(f"{stats['total']:,}", "Contributions"), (f"{stats['commits']:,}", "Commits"),
               (str(stats["repos"]), "Public projects")]
    xs = (margin, 150, 272) if mobile else (margin, 224, 411)
    out = []
    for (value, caption), x in zip(metrics, xs):
        fit = (75 if mobile else 120) if len(value) > (7 if mobile else 11) else None
        out.append(text_at(x, shore + 34, value, "metric", fit=fit))
        out.append(text_at(x, shore + 53, caption, "caption"))

    bar_width = 6 if mobile else 8
    step = 11 if mobile else 16
    months = stats["monthly"]
    peak = max(1, max(m["value"] for m in months))
    x0 = margin if mobile else width - margin - (len(months)-1) * step - bar_width
    floor = shore + (93 if mobile else 35)
    out.append('<g><title>Monthly GitHub contributions</title>')
    for i, month in enumerate(months):
        value = month["value"]
        h = max(1.5, value / peak * 23)
        out.append(f'<rect x="{x0+i*step}" y="{floor-h:.1f}" width="{bar_width}" height="{h:.1f}" rx="1" '
                   f'fill="var(--accent)"><title>{month["month"]}: {value}</title></rect>')
    out.extend(['</g>', text_at(width-margin, shore + (93 if mobile else 53), date_range, "dates", "end")])
    return '\n'.join(out)


def render_liquid(stats, theme="dark", mobile=False):
    width, height, margin, shore = (400, 376, 20, 267) if mobile else (940, 384, 37, 312)
    colors = ';'.join(f'--{key}:{value}' for key, value in PALETTES[theme].items())
    mark = (ART / "zirtuno.path").read_text(encoding="utf-8").strip()
    definitions = (ART / "liquid-defs.svg").read_text(encoding="utf-8").strip()
    monthly = ", ".join(f"{m['month']} ({m['value']})" for m in stats["monthly"])
    end = stats["through"]
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'class="{"mobile" if mobile else "desktop"}" role="img" aria-labelledby="title desc">',
        '<title id="title">Pedro Mautone · Zirtuno</title>',
        f'<desc id="desc">Co-founder and systems architect. Monthly GitHub contributions through {end}: {monthly}.</desc>',
        f'<style>:root{{{colors}}}{TYPE}</style>', definitions,
        f'<defs><clipPath id="frame"><rect width="{width}" height="{height}" rx="12"/></clipPath></defs>',
        '<g clip-path="url(#frame)">',
        f'<rect width="{width}" height="{height}" fill="var(--base)"/>',
        f'<rect width="{width}" height="{shore}" fill="var(--sky)"/>', liquid(width, shore, mobile),
        f'<g transform="translate({margin} {21 if mobile else 26}) scale(.0075) translate(-1221.92 -998.42)">'
        f'<path d="{mark}" fill="var(--accent)"/></g>',
        text_at(margin+29, 38 if mobile else 43, "ZIRTUNO", "brand"),
        text_at(margin-2, 96 if mobile else 133, "Pedro Mautone", "name"),
        text_at(margin, 125 if mobile else 169, "Co-founder & Systems Architect", "role"),
        activity(stats, width, margin, shore, mobile),
        f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="12" fill="none" stroke="var(--line)" stroke-width=".8"/>',
        '</g></svg>',
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    root = ROOT
    login = os.environ.get("GH_USERNAME", "Pedrowtst")
    cache = root / "cache/data.json"
    if args.refresh:
        now = datetime.datetime.now(datetime.timezone.utc)
        response = data.graphql({"login": login, "from": data.month_window(now.date())[0] + "-01T00:00:00Z", "to": now.isoformat(timespec="seconds")})
        stats = data.aggregate(response["calendar"], login, now)
        stats.update(response["summary"])
        data.validate_cache(stats, login)
    else:
        stats = data.validate_cache(json.loads(cache.read_text(encoding="utf-8")), login)
    files = {}
    for theme in ("dark", "light"):
        for mobile in (False, True):
            suffix = theme + ("-mobile" if mobile else "")
            files[f"zirtuno-liquid-{suffix}.svg"] = render_liquid(stats, theme, mobile)
            files[f"zirtuno-liquid-{suffix}-refined.svg"] = files[f"zirtuno-liquid-{suffix}.svg"]
        files[f"console-{theme}.svg"] = files[f"zirtuno-liquid-{theme}.svg"]
    for name, svg in files.items():
        (root / "assets" / name).write_text(svg + "\n", encoding="utf-8", newline="\n")
    if args.refresh:
        cache.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Generated {len(files)} liquid assets; {stats['total']} contributions through {stats['through']}.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        print(f"Generation failed ({type(error).__name__}); no fabricated fallback data used.", file=sys.stderr)
        sys.exit(1)
