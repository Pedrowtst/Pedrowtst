#!/usr/bin/env python3
"""
Generates the ZIRTUNO Systems Architecture Console SVG for Pedro Mautone's GitHub Profile.

Usage:
    python generate.py --mock     # Generate with mock data (offline)
    python generate.py            # Fetch real data via GitHub CLI / ACCESS_TOKEN

Outputs:
    assets/console-dark.svg
    assets/console-light.svg
"""

import os
import sys
import json
import math
import datetime
import urllib.request
import subprocess
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

CONFIG = {
    "username": os.environ.get("GH_USERNAME", "Pedrowtst"),
    "wordmark": "PEDRO MAUTONE",
    "role": "CO-FOUNDER & SYSTEMS ARCHITECT",
    "company": "ZIRTUNO",
    "location": "CURITIBA, PR · BR",
    "status_beacon": "SYSTEMS OPERATIONAL // BUS ACTIVE",
    "directive_title": "CORE ARCHITECTURAL DIRECTIVE",
    "directive_lines": [
        "Engineering high-concurrency backends, edge computer vision",
        "telemetry, and resilient enterprise data pipelines.",
    ],
    
    "tags": [
        "DISTRIBUTED SYSTEMS",
        "REVERSE ENGINEERING",
        "EDGE TELEMETRY",
        "ERP/CRM PIPELINES",
    ],

    "nodes": [
        {
            "id": "NODE 01",
            "name": "EDGE TELEMETRY & CV",
            "stack": "ESP32-CAM · FreeRTOS · YOLOv8",
            "details": [
                "Direction-aware vehicle tracking",
                "Sub-100ms occupancy streaming",
                "Spatial computer vision on edge",
            ],
            "metric": "INFERENCE < 100ms // 60 FPS BUS",
        },
        {
            "id": "NODE 02",
            "name": "ENTERPRISE DATA BUS",
            "stack": "FastAPI · Redis · PostgreSQL · ERP",
            "details": [
                "Bi-directional ERP/CRM sync engine",
                "Transactional outbox pattern",
                "Idempotent queue processing",
            ],
            "metric": "ZERO DATA LOSS // REAL-TIME SYNC",
        },
        {
            "id": "NODE 03",
            "name": "LOW-LEVEL & PROTOCOLS",
            "stack": "C / C++ · Linux / POSIX · GDB",
            "details": [
                "Binary protocol reverse engineering",
                "Proprietary socket dissection",
                "Deterministic memory profiling",
            ],
            "metric": "DETERMINISTIC // ZERO-COPY IO",
        },
    ],
}

THEMES = {
    "dark": {
        "bg0": "#070B0E",
        "bg1": "#0D141C",
        "card_bg": "#0A1017",
        "card_bg_hover": "#0F1822",
        "chrome": "#090E14",
        "line": "#162330",
        "line_accent": "#00F5A0",
        "ink": "#EDF6F5",
        "ink2": "#8FA9AF",
        "ink3": "#4C6B73",
        "accent": "#00F5A0",       # Zirtuno Emerald
        "accent2": "#00D2FF",      # Laser Cyan
        "accent_dim": "#004733",
        "glow": 1.0,
        "grid_opacity": 0.08,
    },
    "light": {
        "bg0": "#F6F9FA",
        "bg1": "#EAF1F4",
        "card_bg": "#FFFFFF",
        "card_bg_hover": "#F0F5F7",
        "chrome": "#E4ECEF",
        "line": "#CFDDE2",
        "line_accent": "#00A86B",
        "ink": "#092226",
        "ink2": "#2B525A",
        "ink3": "#62868E",
        "accent": "#00A86B",       # Crisp Emerald
        "accent2": "#0284C7",      # Deep Cyan
        "accent_dim": "#C3EBD7",
        "glow": 0.0,
        "grid_opacity": 0.04,
    },
}

W, H = 920, 650
M = 32
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace"

# =============================================================================
# DATA FETCHING
# =============================================================================

API = "https://api.github.com/graphql"

Q_REPOS = """
query($login:String!, $after:String) {
  user(login:$login) {
    createdAt
    followers { totalCount }
    repositories(first:100, after:$after, ownerAffiliations:OWNER,
                 isFork:false, privacy:PUBLIC) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        stargazerCount
        languages(first:12, orderBy:{field:SIZE, direction:DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""

Q_CONTRIB = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

def graphql(query, variables, token):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": f"bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "pedro-systems-console-generator",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise RuntimeError(json.dumps(payload["errors"], indent=2))
    return payload["data"]

def fetch(username, token):
    repos, stars, langs, cursor = 0, 0, {}, None
    created_at, followers = None, 0
    while True:
        d = graphql(Q_REPOS, {"login": username, "after": cursor}, token)["user"]
        created_at = d["createdAt"]
        followers = d["followers"]["totalCount"]
        rr = d["repositories"]
        repos = rr["totalCount"]
        for node in rr["nodes"]:
            stars += node["stargazerCount"]
            for edge in node["languages"]["edges"]:
                nm = edge["node"]["name"]
                langs[nm] = langs.get(nm, 0) + edge["size"]
        if not rr["pageInfo"]["hasNextPage"]:
            break
        cursor = rr["pageInfo"]["endCursor"]

    now = datetime.datetime.now(datetime.timezone.utc)
    commits = 0
    year = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00")).year
    while year <= now.year:
        frm = datetime.datetime(year, 1, 1, tzinfo=datetime.timezone.utc)
        to = min(datetime.datetime(year, 12, 31, 23, 59, tzinfo=datetime.timezone.utc), now)
        c = graphql(Q_CONTRIB, {"login": username, "from": frm.isoformat(),
                                "to": to.isoformat()}, token)["user"]["contributionsCollection"]
        commits += c["totalCommitContributions"] + c["restrictedContributionsCount"]
        year += 1

    frm = now - datetime.timedelta(days=364)
    cal = graphql(Q_CONTRIB, {"login": username, "from": frm.isoformat(),
                              "to": now.isoformat()},
                  token)["user"]["contributionsCollection"]["contributionCalendar"]
    buckets = {}
    for week in cal["weeks"]:
        for day in week["contributionDays"]:
            key = day["date"][:7]
            buckets[key] = buckets.get(key, 0) + day["contributionCount"]

    keys, cur = [], datetime.date(now.year, now.month, 1)
    for _ in range(12):
        keys.append(f"{cur.year:04d}-{cur.month:02d}")
        cur = (cur.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    keys.reverse()

    return {
        "repos": repos,
        "stars": stars,
        "commits": commits,
        "followers": followers,
        "bytes": sum(langs.values()),
        "languages": sorted(langs.items(), key=lambda kv: -kv[1]),
        "monthly": [{"month": int(k[5:7]), "value": buckets.get(k, 0)} for k in keys],
        "built": now.strftime("%d %b %Y").upper(),
    }

def mock():
    today = datetime.date.today()
    months, cur = [], datetime.date(today.year, today.month, 1)
    for _ in range(12):
        months.append(cur.month)
        cur = (cur.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    months.reverse()
    vals = [0, 1, 0, 0, 0, 0, 0, 44, 41, 26, 32, 102]
    return {
        "repos": 2,
        "stars": 1,
        "commits": 243,
        "followers": 1,
        "bytes": 67406,
        "languages": [("Python", 52336), ("C++", 15070)],
        "monthly": [{"month": m, "value": v} for m, v in zip(months, vals)],
        "built": today.strftime("%d %b %Y").upper(),
    }

# =============================================================================
# SVG PRIMITIVES & RENDERING
# =============================================================================

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def fmt(n):
    return f"{n:,}".replace(",", " ")

def smooth(points, tension=0.32):
    if len(points) < 2:
        return ""
    d = [f"M{points[0][0]:.2f},{points[0][1]:.2f}"]
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 2,
              p1[1] + (p2[1] - p0[1]) * tension / 2)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 2,
              p2[1] - (p3[1] - p1[1]) * tension / 2)
        d.append(f"C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}")
    return " ".join(d)

def render(d, theme_name):
    t = THEMES[theme_name]
    accent, accent2 = t["accent"], t["accent2"]
    ink, ink2, ink3 = t["ink"], t["ink2"], t["ink3"]
    card_bg, line = t["card_bg"], t["line"]

    MONTHS = "JFMAMJJASOND"

    o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Pedro Mautone - Systems Architect Console">
<defs>
  <radialGradient id="bg" cx="0.5" cy="0.15" r="0.85">
    <stop offset="0%" stop-color="{t['bg1']}"/>
    <stop offset="100%" stop-color="{t['bg0']}"/>
  </radialGradient>
  <linearGradient id="traceGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{accent2}"/>
    <stop offset="70%" stop-color="{accent}"/>
    <stop offset="100%" stop-color="{accent}"/>
  </linearGradient>
  <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{accent}" stop-opacity="0.32"/>
    <stop offset="100%" stop-color="{accent}" stop-opacity="0.01"/>
  </linearGradient>
  <linearGradient id="badgeGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{accent}" stop-opacity="0.14"/>
    <stop offset="100%" stop-color="{accent2}" stop-opacity="0.04"/>
  </linearGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{ink3}" stroke-width="0.8" stroke-opacity="{t['grid_opacity']}"/>
  </pattern>
  <filter id="laserGlow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="consoleClip">
    <rect x="0" y="0" width="{W}" height="{H}" rx="12"/>
  </clipPath>
</defs>''']

    # Background Base + Tech Grid
    o.append('<g clip-path="url(#consoleClip)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')

    # Top Control Bar (y: 0 to 42)
    o.append(f'<rect width="{W}" height="42" fill="{t["chrome"]}"/>')
    o.append(f'<line x1="0" y1="42" x2="{W}" y2="42" stroke="{line}" stroke-width="1"/>')
    
    # Left: Window Markers + Identity Brand
    for i, col in enumerate((ink3, accent2, accent)):
        o.append(f'<circle cx="{24 + i * 16}" cy="21" r="3.8" fill="{col}" opacity="{0.6 + i*0.2:.2f}"/>')
    
    o.append(f'<text x="80" y="25" font-family="{MONO}" font-size="11" font-weight="700" fill="{accent}" letter-spacing="1.5">[ {esc(CONFIG["company"])} ]</text>')
    o.append(f'<text x="172" y="25" font-family="{MONO}" font-size="11" fill="{ink3}" letter-spacing="1.2">// SYSTEMS ARCHITECTURAL CONSOLE</text>')

    # Right: Live Beacon & Location
    beacon_label = f"● NODE: {CONFIG['location']} // {CONFIG['status_beacon']}"
    o.append(f'<text x="{W - M}" y="25" font-family="{MONO}" font-size="10.5" font-weight="600" fill="{accent}" letter-spacing="1.2" text-anchor="end">{esc(beacon_label)}</text>')

    # =========================================================================
    # IDENTITY & HERO HEADER (y: 56 to 142)
    # =========================================================================
    o.append(f'<g transform="translate({M}, 56)">')
    
    # Left Hero Header
    o.append(f'<text x="0" y="32" font-family="{MONO}" font-size="28" font-weight="800" fill="{ink}" letter-spacing="3.0">{esc(CONFIG["wordmark"])}</text>')
    o.append(f'<text x="0" y="52" font-family="{MONO}" font-size="11.5" font-weight="700" fill="{accent}" letter-spacing="2.2">{esc(CONFIG["role"])} · {esc(CONFIG["company"])}</text>')

    # Right Architecture Directive Callout
    callout_w = 360
    callout_x = W - 2 * M - callout_w
    o.append(f'<g transform="translate({callout_x:.1f}, 6)">')
    o.append(f'<rect width="{callout_w}" height="76" rx="6" fill="{card_bg}" stroke="{line}" stroke-width="1"/>')
    o.append(f'<rect width="3" height="76" rx="1.5" fill="{accent}"/>')
    o.append(f'<text x="16" y="24" font-family="{MONO}" font-size="10" font-weight="700" fill="{accent}" letter-spacing="1.8">{esc(CONFIG["directive_title"])}</text>')
    for di, line_txt in enumerate(CONFIG["directive_lines"]):
        o.append(f'<text x="16" y="{44 + di * 16}" font-family="{MONO}" font-size="10" fill="{ink2}">{esc(line_txt)}</text>')
    o.append('</g>')

    # Tags Row (fitted neatly to left of callout)
    tag_x = 0
    for tag in CONFIG["tags"]:
        tag_w = len(tag) * 5.8 + 14
        o.append(f'<rect x="{tag_x:.1f}" y="66" width="{tag_w:.1f}" height="20" rx="3" fill="url(#badgeGrad)" stroke="{line}" stroke-width="1"/>')
        o.append(f'<text x="{tag_x + 7:.1f}" y="80" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{ink2}" letter-spacing="0.8">{esc(tag)}</text>')
        tag_x += tag_w + 6

    o.append('</g>') # End Hero Header

    # Hairline divider
    o.append(f'<line x1="{M}" y1="156" x2="{W - M}" y2="156" stroke="{line}" stroke-width="1"/>')

    # =========================================================================
    # METRIC TELEMETRY TILES (y: 170 to 244)
    # =========================================================================
    card_total_w = W - 2 * M
    num_cards = 4
    gap = 12
    cw = (card_total_w - (num_cards - 1) * gap) / num_cards

    cards = [
        ("REPOSITORIES", f"{d['repos']:02d}", "OWNED ARCHITECTURES"),
        ("STARS EARNED", f"{d['stars']:02d}", "RECOGNITION METRIC"),
        ("LIFETIME COMMITS", fmt(d["commits"]), "CODE COMMITS"),
        ("CODEBASE VOLUME", f"{d['bytes']/1024:.0f} KB", "SYSTEM RUNTIMES"),
    ]

    for ci, (label, val, sub) in enumerate(cards):
        cx = M + ci * (cw + gap)
        cy = 170
        o.append(f'<g transform="translate({cx:.1f}, {cy})">')
        o.append(f'<rect width="{cw:.1f}" height="76" rx="6" fill="{card_bg}" stroke="{line}" stroke-width="1"/>')
        o.append(f'<circle cx="16" cy="18" r="2.5" fill="{accent}"/>')
        o.append(f'<text x="26" y="21" font-family="{MONO}" font-size="9" font-weight="700" fill="{ink3}" letter-spacing="1.5">{esc(label)}</text>')
        o.append(f'<text x="16" y="52" font-family="{MONO}" font-size="24" font-weight="800" fill="{ink}" letter-spacing="0.8">{esc(val)}</text>')
        o.append(f'<text x="16" y="66" font-family="{MONO}" font-size="9" fill="{ink3}" letter-spacing="1.0">{esc(sub)}</text>')
        o.append('</g>')

    # =========================================================================
    # ENGINEERING VELOCITY & RUNTIME MATRIX (y: 260 to 420)
    # =========================================================================
    spark_w = 540
    stack_w = (W - 2 * M) - spark_w - 16
    stack_x = M + spark_w + 16

    # --- Left: Engineering Velocity Sparkline ---
    o.append(f'<g transform="translate({M}, 260)">')
    o.append(f'<rect width="{spark_w}" height="152" rx="6" fill="{card_bg}" stroke="{line}" stroke-width="1"/>')
    o.append(f'<text x="18" y="24" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{accent}" letter-spacing="1.8">ENGINEERING VELOCITY // 12-MONTH TIMELINE</text>')
    
    total_contribs = sum(m["value"] for m in d["monthly"])
    pill_label = f"{fmt(total_contribs)} CONTRIBUTIONS"
    o.append(f'<rect x="{spark_w - 160}" y="11" width="144" height="20" rx="3" fill="url(#badgeGrad)" stroke="{line}" stroke-width="1"/>')
    o.append(f'<text x="{spark_w - 88}" y="24" font-family="{MONO}" font-size="9" font-weight="700" fill="{accent}" letter-spacing="1.2" text-anchor="middle">{esc(pill_label)}</text>')

    # Sparkline Drawing
    vals = [m["value"] for m in d["monthly"]] or [0]
    peak = max(vals) or 1
    n = len(vals)
    sx0, sx1 = 20, spark_w - 20
    sy0, sy1 = 44, 126

    pts = [(sx0 + (sx1 - sx0) * (i / (n - 1)),
            sy1 - (sy1 - sy0) * (0.06 + 0.94 * (v / peak)))
           for i, v in enumerate(vals)]
    path_d = smooth(pts)

    o.append(f'<path d="{path_d} L{sx1},{sy1} L{sx0},{sy1} Z" fill="url(#areaGrad)"/>')
    o.append(f'<path d="{path_d}" fill="none" stroke="url(#traceGrad)" stroke-width="2.2" stroke-linecap="round" class="traceLine" filter="url(#laserGlow)"/>')
    o.append(f'<line x1="{sx0}" y1="{sy1}" x2="{sx1}" y2="{sy1}" stroke="{line}" stroke-width="1"/>')

    for j, m in enumerate(d["monthly"]):
        mx = sx0 + (sx1 - sx0) * (j / (n - 1))
        o.append(f'<text x="{mx:.1f}" y="{sy1 + 14}" font-family="{MONO}" font-size="9" fill="{ink3}" text-anchor="middle">{MONTHS[m["month"] - 1]}</text>')

    o.append('</g>')

    # --- Right: Language Stack Telemetry ---
    o.append(f'<g transform="translate({stack_x}, 260)">')
    o.append(f'<rect width="{stack_w}" height="152" rx="6" fill="{card_bg}" stroke="{line}" stroke-width="1"/>')
    o.append(f'<text x="18" y="24" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{accent}" letter-spacing="1.8">RUNTIME BY BYTE VOLUME</text>')

    langs = d["languages"][:4]
    grand = sum(v for _, v in d["languages"]) or 1
    slices = [(nm, v / grand) for nm, v in langs]

    bar_w = stack_w - 36
    bar_y = 44
    bar_h = 10
    o.append(f'<g transform="translate(18, {bar_y})"><g class="barGrow">')
    bx = 0
    colors = [accent, accent2, "#A78BFA", "#F59E0B"]
    for j, (nm, frac) in enumerate(slices):
        seg = max(frac * (bar_w - 2 * (len(slices) - 1)), 6)
        col = colors[j % len(colors)]
        o.append(f'<rect x="{bx:.1f}" y="0" width="{seg:.1f}" height="{bar_h}" rx="2" fill="{col}"/>')
        bx += seg + 2
    o.append('</g></g>')

    # Legend Rows
    ly = 78
    for j, (nm, frac) in enumerate(slices):
        col = colors[j % len(colors)]
        o.append(f'<rect x="18" y="{ly - 8}" width="8" height="8" rx="2" fill="{col}"/>')
        o.append(f'<text x="34" y="{ly}" font-family="{MONO}" font-size="11" font-weight="600" fill="{ink}">{esc(nm)}</text>')
        o.append(f'<text x="{stack_w - 18}" y="{ly}" font-family="{MONO}" font-size="11" font-weight="700" fill="{col}" text-anchor="end">{frac * 100:.1f}%</text>')
        ly += 22

    o.append('</g>')

    # =========================================================================
    # ARCHITECTURAL NODES CLUSTER (y: 426 to 582)
    # =========================================================================
    node_w = (card_total_w - 2 * 14) / 3
    for ni, node in enumerate(CONFIG["nodes"]):
        nx = M + ni * (node_w + 14)
        ny = 426
        o.append(f'<g transform="translate({nx:.1f}, {ny})">')
        o.append(f'<rect width="{node_w:.1f}" height="154" rx="6" fill="{card_bg}" stroke="{line}" stroke-width="1"/>')
        
        # Node Header
        o.append(f'<rect width="{node_w:.1f}" height="28" rx="6" fill="{t["chrome"]}"/>')
        o.append(f'<rect y="22" width="{node_w:.1f}" height="6" fill="{t["chrome"]}"/>')
        o.append(f'<line x1="0" y1="28" x2="{node_w:.1f}" y2="28" stroke="{line}" stroke-width="1"/>')
        o.append(f'<text x="12" y="19" font-family="{MONO}" font-size="9" font-weight="700" fill="{accent}" letter-spacing="1.2">[ {esc(node["id"])} ]</text>')
        o.append(f'<text x="82" y="19" font-family="{MONO}" font-size="9.5" font-weight="700" fill="{ink}" letter-spacing="1.0">{esc(node["name"])}</text>')

        # Stack definition
        o.append(f'<text x="12" y="46" font-family="{MONO}" font-size="9.5" font-weight="600" fill="{accent2}" letter-spacing="0.8">{esc(node["stack"])}</text>')

        # Details bullet items
        dy = 66
        for det in node["details"]:
            o.append(f'<circle cx="15" cy="{dy - 3}" r="1.8" fill="{accent}"/>')
            o.append(f'<text x="24" y="{dy}" font-family="{MONO}" font-size="10.5" fill="{ink2}">{esc(det)}</text>')
            dy += 19

        # Metric Footer Pill
        o.append(f'<line x1="12" y1="126" x2="{node_w - 12:.1f}" y2="126" stroke="{line}" stroke-width="0.8"/>')
        o.append(f'<text x="12" y="141" font-family="{MONO}" font-size="9" font-weight="600" fill="{accent}" letter-spacing="1.0">{esc(node["metric"])}</text>')
        o.append('</g>')

    # =========================================================================
    # CONSOLE FOOTER STATUS BAR (y: 594 to 650)
    # =========================================================================
    o.append(f'<line x1="{M}" y1="594" x2="{W - M}" y2="594" stroke="{line}" stroke-width="1"/>')
    
    o.append(f'<circle cx="{M + 6}" cy="621" r="3.5" fill="{accent}" class="pulseDot"/>')
    o.append(f'<text x="{M + 18}" y="625" font-family="{MONO}" font-size="10.5" font-weight="600" fill="{ink2}" letter-spacing="1.2">UPTIME: CONTINUOUS // ARCHITECTING NEXT-GEN INFRASTRUCTURE @ {esc(CONFIG["company"])}</text>')
    o.append(f'<text x="{W - M}" y="625" font-family="{MONO}" font-size="10" fill="{ink3}" letter-spacing="1.5" text-anchor="end">TELEMETRY SYNCED: {esc(d["built"])} // GRAPHQL v4</text>')

    # Subtle border outline
    o.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{line}" stroke-width="1"/>')
    o.append('</g>') # End consoleClip

    # =========================================================================
    # CSS EMBEDDED STYLES & ANIMATIONS
    # =========================================================================
    css = f'''
    text {{ text-rendering: geometricPrecision; }}

    .pulseDot {{
        animation: beaconPulse 2.4s ease-in-out infinite;
    }}
    @keyframes beaconPulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.35; }}
    }}

    .traceLine {{
        stroke-dasharray: 1200;
        stroke-dashoffset: 1200;
        animation: traceDraw 3.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }}
    @keyframes traceDraw {{
        to {{ stroke-dashoffset: 0; }}
    }}

    .barGrow {{
        transform-origin: 0 0;
        animation: barSpread 2.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    @keyframes barSpread {{
        from {{ transform: scaleX(0); }}
        to {{ transform: scaleX(1); }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        .pulseDot {{ animation: none !important; opacity: 1; }}
        .traceLine {{ animation: none !important; stroke-dashoffset: 0; }}
        .barGrow {{ animation: none !important; transform: scaleX(1); }}
    }}
    '''

    o.append(f'<style>{css}</style>')
    o.append('</svg>')
    return "\n".join(o)

# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    out = Path(__file__).resolve().parent
    assets = out / "assets"
    assets.mkdir(exist_ok=True)
    cache = out / "cache" / "data.json"
    cache.parent.mkdir(parents=True, exist_ok=True)

    if "--mock" in sys.argv:
        data = mock()
    else:
        token = os.environ.get("ACCESS_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            try:
                token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
            except Exception:
                pass

        if token:
            try:
                data = fetch(CONFIG["username"], token)
                cache.write_text(json.dumps(data, indent=2))
            except Exception as e:
                print(f"GraphQL fetch failed ({e}); falling back to cache.", file=sys.stderr)
                data = json.loads(cache.read_text()) if cache.exists() else mock()
        else:
            data = json.loads(cache.read_text()) if cache.exists() else mock()

    for theme in ("dark", "light"):
        path = assets / f"console-{theme}.svg"
        path.write_text(render(data, theme), encoding="utf-8")
        print(f"Rendered {path.name} ({path.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
