#!/usr/bin/env python3
"""
ZIRTUNO Liquid Contributions & Systems Architecture Organ
Generates the authentic, fully-animated liquid SVG for Pedro Mautone.
Strictly follows Zirtuno's R5 'One Continuous Liquid' design system.
"""

import json
import math
import os
import sys
import datetime
import urllib.request
import subprocess
from pathlib import Path

def load_stats():
    cache_path = Path(r"C:\Users\pedro\.gemini\antigravity\brain\59c11caf-5a39-4a7d-8fde-539ec21d1553\scratch\pedro_stats.json")
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "repos": 2,
        "stars": 1,
        "commits": 243,
        "followers": 1,
        "bytes": 67406,
        "languages": [("Python", 52336), ("C++", 15070)],
        "monthly": [{"month": m, "value": v} for m, v in zip(range(1, 13), [0, 1, 0, 0, 0, 0, 0, 44, 41, 26, 32, 102])],
        "built": datetime.date.today().strftime("%d %b %Y").upper()
    }

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_wave(width, height, baseline, amplitude, frequency, phase=0):
    """Generate seamless repeating SVG wave path for infinite CSS translation (period = width)"""
    points = []
    total_w = width * 2
    steps = 80
    dx = total_w / steps
    for i in range(steps + 1):
        x = i * dx
        y = baseline + amplitude * math.sin((x / width) * 2 * math.pi * frequency + phase)
        points.append((x, y))
    
    d = [f"M 0 {height}"]
    d.append(f"L {points[0][0]:.2f} {points[0][1]:.2f}")
    for p in points[1:]:
        d.append(f"L {p[0]:.2f} {p[1]:.2f}")
    d.append(f"L {total_w:.2f} {height}")
    d.append("Z")
    return " ".join(d)

def render_liquid(stats, theme="dark"):
    W, H = 940, 600
    
    if theme == "dark":
        bg0 = "#050709"
        bg1 = "#090D12"
        cyan = "#00E3FE"
        cyan_glow = "#4DECFF"
        cyan_deep = "#008B9E"
        cyan_dark = "#002933"
        paper = "#F2F0EB"
        paper_muted = "#9BA3AF"
        paper_sub = "#5E6875"
        glass_fill = "rgba(10, 14, 20, 0.78)"
        glass_border = "rgba(0, 227, 254, 0.20)"
        glass_border_hi = "rgba(0, 227, 254, 0.45)"
        datum_color = "rgba(0, 227, 254, 0.30)"
    else:
        bg0 = "#F4F7F8"
        bg1 = "#EBF2F5"
        cyan = "#009BB0"
        cyan_glow = "#00B6CC"
        cyan_deep = "#006C7A"
        cyan_dark = "#C2E8EF"
        paper = "#08161A"
        paper_muted = "#344D55"
        paper_sub = "#6B8891"
        glass_fill = "rgba(255, 255, 255, 0.88)"
        glass_border = "rgba(0, 155, 176, 0.25)"
        glass_border_hi = "rgba(0, 155, 176, 0.60)"
        datum_color = "rgba(0, 155, 176, 0.35)"

    total_contribs = sum(m["value"] for m in stats["monthly"])
    lifetime_commits = stats["commits"]
    
    # 3 Continuous flowing wave paths
    wave_base = 356
    w_path1 = generate_wave(W, H, baseline=wave_base, amplitude=14, frequency=1.5, phase=0)
    w_path2 = generate_wave(W, H, baseline=wave_base + 8, amplitude=11, frequency=2.2, phase=math.pi / 3)
    w_path3 = generate_wave(W, H, baseline=wave_base + 15, amplitude=7, frequency=3.0, phase=math.pi / 2)

    # Months mapping & contribution tide heights
    month_names = ["OCT", "NOV", "DEC", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP"]
    m_vals = [m["value"] for m in stats["monthly"]]
    max_val = max(m_vals) or 1

    # Liquid droplets positioned over contribution hot spots
    # (cx, cy, r, anim_class, delay)
    droplets = [
        (800, 310, 19, "moteFloat1", "0s"),    # Peak over Sep (102 contribs!)
        (760, 332, 13, "moteFloat2", "1.1s"),
        (840, 338, 14, "moteFloat3", "2.2s"),
        (680, 345, 12, "moteFloat1", "3.0s"),  # Over Aug (32)
        (620, 348, 11, "moteFloat2", "0.7s"),  # Over Jul (26)
        (560, 340, 14, "moteFloat3", "1.8s"),  # Over Jun (41)
        (500, 342, 13, "moteFloat1", "2.5s"),  # Over May (44)
        (400, 362, 8,  "moteFloat2", "3.2s"),
        (230, 364, 7,  "moteFloat3", "1.4s"),
    ]

    o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Pedro Mautone — ZIRTUNO Liquid Contributions &amp; Systems Architecture">
<defs>
  <!-- Background radial depth -->
  <radialGradient id="abyssGrad" cx="50%" cy="25%" r="80%">
    <stop offset="0%" stop-color="{bg1}"/>
    <stop offset="65%" stop-color="{bg0}"/>
    <stop offset="100%" stop-color="#020304"/>
  </radialGradient>

  <!-- Liquid wave layer 1 (deepest current) -->
  <linearGradient id="liquidGrad1" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{cyan}" stop-opacity="0.35"/>
    <stop offset="40%" stop-color="{cyan_deep}" stop-opacity="0.65"/>
    <stop offset="100%" stop-color="{cyan_dark}" stop-opacity="0.95"/>
  </linearGradient>

  <!-- Liquid wave layer 2 (mid stream) -->
  <linearGradient id="liquidGrad2" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{cyan_glow}" stop-opacity="0.55"/>
    <stop offset="35%" stop-color="{cyan}" stop-opacity="0.80"/>
    <stop offset="100%" stop-color="{cyan_deep}" stop-opacity="0.98"/>
  </linearGradient>

  <!-- Liquid wave layer 3 (surface crest with bright luminous meniscus) -->
  <linearGradient id="liquidGrad3" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.75"/>
    <stop offset="12%" stop-color="{cyan_glow}" stop-opacity="0.88"/>
    <stop offset="55%" stop-color="{cyan}" stop-opacity="0.96"/>
    <stop offset="100%" stop-color="{cyan_deep}" stop-opacity="1"/>
  </linearGradient>

  <!-- Caustic Bloom / Radiant Glow -->
  <radialGradient id="causticGlow" cx="78%" cy="60%" r="45%">
    <stop offset="0%" stop-color="{cyan_glow}" stop-opacity="0.30"/>
    <stop offset="45%" stop-color="{cyan}" stop-opacity="0.10"/>
    <stop offset="100%" stop-color="{cyan}" stop-opacity="0"/>
  </radialGradient>

  <!-- Droplet Radial Shimmer -->
  <radialGradient id="dropletShimmer" cx="35%" cy="30%" r="70%">
    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
    <stop offset="35%" stop-color="{cyan_glow}" stop-opacity="0.85"/>
    <stop offset="85%" stop-color="{cyan}" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="{cyan_deep}" stop-opacity="1"/>
  </radialGradient>

  <!-- Organic Metaball Fluid Filter -->
  <filter id="metaballFilter" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur in="SourceGraphic" stdDeviation="7" result="blur" />
    <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 22 -7" result="goo" />
    <feBlend in="SourceGraphic" in2="goo" />
  </filter>

  <!-- Atmospheric Glow Filter -->
  <filter id="fluidBloom" x="-25%" y="-25%" width="150%" height="150%">
    <feGaussianBlur stdDeviation="3.5" result="bloom"/>
    <feMerge>
      <feMergeNode in="bloom"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>

  <!-- Clip boundary -->
  <clipPath id="stageClip">
    <rect x="0" y="0" width="{W}" height="{H}" rx="16"/>
  </clipPath>
</defs>''']

    o.append('<g clip-path="url(#stageClip)">')
    
    # 1. Base void & caustic glow
    o.append(f'<rect width="{W}" height="{H}" fill="url(#abyssGrad)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#causticGlow)"/>')

    # Subtle ambient atmospheric particles
    o.append(f'<circle cx="180" cy="130" r="1.4" fill="{cyan}" opacity="0.35" class="particleDrift1"/>')
    o.append(f'<circle cx="460" cy="85"  r="2.0" fill="{cyan_glow}" opacity="0.50" class="particleDrift2"/>')
    o.append(f'<circle cx="780" cy="115" r="1.6" fill="{cyan}" opacity="0.45" class="particleDrift3"/>')
    o.append(f'<circle cx="890" cy="205" r="2.2" fill="{cyan_glow}" opacity="0.35" class="particleDrift1"/>')

    # =========================================================================
    # 2. CONTINUOUS LIQUID BODY (Undulating waves + contribution metaballs)
    # =========================================================================
    o.append('<g class="liquidOrgan">')
    
    # Wave 1 (Deepest, slowest current)
    o.append(f'<path d="{w_path1}" fill="url(#liquidGrad1)" class="waveMove1"/>')
    
    # Wave 2 (Middle current)
    o.append(f'<path d="{w_path2}" fill="url(#liquidGrad2)" class="waveMove2"/>')
    
    # Metaball Droplets Group (Morphing & fusing with the wave crests)
    o.append('<g filter="url(#metaballFilter)">')
    for cx, cy, r, acls, dly in droplets:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#dropletShimmer)" class="{acls}" style="animation-delay:{dly};"/>')
    o.append('</g>')

    # Wave 3 (Forefront liquid crest with bright luminous meniscus)
    o.append(f'<path d="{w_path3}" fill="url(#liquidGrad3)" class="waveMove3"/>')

    o.append('</g>') # End liquidOrgan

    # =========================================================================
    # 3. CONTRIBUTION TIMELINE RESTING ON THE FLUID WATERLINE
    # =========================================================================
    o.append(f'<g transform="translate(0, {wave_base + 32})">')
    
    # Horizontal glass datum line
    o.append(f'<line x1="44" y1="0" x2="{W - 44}" y2="0" stroke="{datum_color}" stroke-width="1.2" stroke-dasharray="4 6"/>')
    
    step_m = (W - 128) / 11
    for mi in range(12):
        mx = 64 + mi * step_m
        val = m_vals[mi]
        m_name = month_names[mi]
        
        h_ratio = val / max_val
        beacon_h = max(h_ratio * 48, 4)
        
        if val > 0:
            # Pulsing beacon line rising from the liquid
            o.append(f'<line x1="{mx:.1f}" y1="0" x2="{mx:.1f}" y2="{-beacon_h:.1f}" stroke="{cyan_glow}" stroke-width="2" stroke-linecap="round" class="beaconLine"/>')
            o.append(f'<circle cx="{mx:.1f}" cy="{-beacon_h:.1f}" r="3.5" fill="#FFFFFF" filter="url(#fluidBloom)"/>')
            o.append(f'<text x="{mx:.1f}" y="{-beacon_h - 9:.1f}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10.5" font-weight="700" fill="{paper}" text-anchor="middle">{val}</text>')
        else:
            o.append(f'<circle cx="{mx:.1f}" cy="0" r="2" fill="{cyan}" opacity="0.3"/>')
            
        o.append(f'<text x="{mx:.1f}" y="18" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, monospace" font-size="9" font-weight="600" fill="{paper_muted}" text-anchor="middle" letter-spacing="1">{m_name}</text>')

    o.append('</g>')

    # =========================================================================
    # 4. BRAND HEADER & STAGE IDENTITY
    # =========================================================================
    o.append('<g transform="translate(44, 38)">')
    
    # ZIRTUNO AUTHENTIC VECTOR LOGO MARK (S-curved fluid droplet / infinity)
    o.append('<g transform="translate(0, 0) scale(0.0106)" fill="#00E3FE" filter="url(#fluidBloom)">')
    o.append('<path d="M3001.12,3538.79 C3011.52,3602.99 3013.09,3665.3 2995.72,3726.82 C2984.39,3766.97 2967.22,3804.76 2938.56,3835.53 C2877.17,3901.46 2801.66,3924.54 2713.46,3905.9 C2668.3,3896.36 2630.61,3873.61 2598.94,3840.57 C2581.73,3822.61 2568.32,3801.55 2557.96,3779.31 C2540.75,3742.36 2529.15,3703.77 2528.63,3662.1 C2527.96,3608.75 2541.02,3559.32 2565.72,3512.51 C2583.5,3478.8 2605.66,3448.02 2628.13,3417.34 C2658.57,3375.79 2685.32,3332.1 2697.18,3281.07 C2708.19,3233.75 2706.38,3187.09 2687.94,3141.78 C2668.52,3094.05 2639.08,3053.52 2600.1,3019.62 C2555.77,2981.06 2504.75,2954.07 2451.11,2931.5 C2382.08,2902.46 2310.43,2882.05 2236.66,2869.55 C2182.63,2860.39 2128.06,2856.96 2073.3,2860.62 C2022.28,2864.02 1973.31,2875.79 1927.72,2899.76 C1888.31,2920.49 1857.61,2950.42 1835.68,2988.96 C1807.61,3038.3 1801.63,3090.83 1817.1,3145.3 C1826.04,3176.77 1839.28,3206.16 1858.22,3233.53 C1880.35,3265.52 1906.07,3294.13 1931.81,3322.96 C1949.99,3343.32 1967.87,3364.03 1984.69,3385.52 C2005.89,3412.59 2021.05,3443.11 2027.71,3476.96 C2043.75,3558.45 2005.33,3640.8 1925.71,3675.74 C1895.52,3688.99 1864.02,3695.66 1830.72,3696.23 C1761.2,3697.4 1696.09,3680.12 1633.76,3651.25 C1571.08,3622.23 1514.13,3584.03 1462.76,3537.87 C1424.98,3503.92 1391.25,3466.21 1362.17,3424.41 C1304.36,3341.31 1265.36,3250.01 1243.24,3151.43 C1226.94,3078.8 1221.92,3005.11 1224.48,2930.88 C1227.11,2854.79 1237.33,2779.62 1252.91,2705.11 C1265.6,2644.44 1281.05,2584.49 1299.63,2525.39 C1312.21,2485.4 1325.96,2445.75 1340.01,2406.24 C1369.96,2322.03 1406.28,2240.58 1447.69,2161.39 C1476.5,2106.29 1510.46,2054.64 1550.5,2006.98 C1600.44,1947.51 1659.08,1898.99 1729.03,1864.84 C1780.84,1839.55 1835.17,1822.53 1892.63,1815.17 C1933.9,1809.88 1975.25,1809.23 2016.34,1813.06 C2074.24,1818.46 2130.34,1832.64 2184.5,1854.5 C2287.61,1896.1 2375.67,1959.21 2452.22,2039.23 C2493.25,2082.13 2532.46,2126.63 2569.98,2172.6 C2616.76,2229.9 2662.5,2288.06 2709.76,2344.97 C2753.61,2397.77 2797.91,2450.3 2848.65,2496.84 C2875.68,2521.63 2903.29,2545.8 2934.08,2565.9 C2968.21,2588.2 3003.83,2607.68 3043.63,2618 C3082.85,2628.17 3122.44,2631.75 3162.08,2620.28 C3228.91,2600.93 3272.24,2557.13 3291.79,2490.92 C3311.45,2424.32 3307.07,2357.94 3285.72,2292.22 C3275.55,2260.91 3259.76,2232.36 3243.4,2204.19 C3216.72,2158.28 3181.9,2118.76 3142.79,2083.17 C3095.26,2039.92 3042.56,2003.89 2985.94,1973.44 C2931.23,1944.03 2874.25,1919.94 2815.64,1899.74 C2747.68,1876.31 2679.3,1854.08 2611.34,1830.62 C2548.9,1809.07 2487.9,1784.07 2432.56,1747.27 C2385.45,1715.94 2345.32,1677.74 2314.41,1629.74 C2289.54,1591.12 2271.3,1550.07 2262.38,1505.18 C2249.42,1439.98 2250.47,1375 2272.77,1311.87 C2303.61,1224.53 2357.39,1153.94 2432.62,1099.72 C2489.69,1058.59 2553.51,1032.85 2621.31,1015.92 C2659,1006.51 2697.46,1002.87 2736.03,1000.53 C2770.84,998.42 2805.17,1004.21 2839.34,1009.87 C2918.44,1022.96 2991.79,1051.71 3061.13,1091.62 C3162.21,1149.8 3244.88,1227.72 3312.05,1322.69 C3351.48,1378.42 3384.55,1437.66 3409.77,1501.01 C3433.68,1561.06 3453.5,1622.58 3467.68,1685.69 C3480.52,1742.84 3492.03,1800.3 3503.68,1857.72 C3523.97,1957.73 3550.35,2055.92 3588.03,2150.97 C3615.79,2221.03 3648.17,2288.87 3682.7,2355.76 C3708.68,2406.06 3734.02,2456.66 3755.86,2508.95 C3782.21,2572.04 3800.55,2637.31 3806.71,2705.46 C3812.1,2764.93 3809.71,2824.39 3791.54,2881.67 C3761.88,2975.17 3707.97,3050.38 3621.44,3100.3 C3558.66,3136.52 3491.38,3154.06 3419.11,3153.11 C3385.77,3152.67 3352.51,3151.45 3319.85,3143.59 C3242.36,3124.93 3171.88,3091.31 3107.79,3044.2 C3055.03,3005.41 3006.87,2961.47 2961.82,2913.9 C2889.18,2837.17 2826.11,2753.05 2767.02,2665.74 C2756.19,2649.75 2744.36,2634.42 2733.85,2618.22 C2701.59,2568.48 2669.78,2518.45 2637.74,2468.58 C2630.53,2457.37 2623.23,2446.22 2615.71,2435.23 C2579.59,2382.45 2544.62,2328.83 2506.86,2277.26 C2468.94,2225.48 2425.31,2178.64 2372.04,2141.83 C2362.74,2135.41 2353.13,2129.28 2343.13,2124.04 C2302.85,2102.91 2261.05,2085.65 2215.9,2078.15 C2160.8,2068.99 2105.64,2068.37 2051.16,2081.98 C2001.24,2094.44 1956.66,2117.54 1918.51,2152.64 C1875.6,2192.13 1853.94,2241.67 1849.38,2298.95 C1847.46,2322.98 1851.61,2346.71 1858.58,2369.91 C1871.54,2413.05 1895.78,2449.38 1926.33,2481.69 C1964.18,2521.73 2008.37,2553.6 2056.24,2580.65 C2112.55,2612.47 2171.28,2639.29 2229.99,2666.25 C2293.51,2695.43 2357.8,2722.98 2420.01,2755 C2528.26,2810.71 2625.31,2881.43 2708.03,2970.94 C2755.62,3022.43 2797.25,3078.71 2835.53,3137.43 C2866.48,3184.91 2894.78,3233.91 2918.87,3285.27 C2950.64,3352.99 2975.52,3423.16 2993.24,3495.83 C2996.54,3509.38 2998.33,3523.31 3001.12,3538.79 Z M2226.65,2242.32 C2301.1,2206.22 2370.92,2224.53 2421.76,2272.34 C2462.36,2320.25 2479.61,2373.56 2459.21,2435.44 C2438.12,2499.4 2392.24,2536.45 2327.64,2546.74 C2239.94,2560.7 2170.17,2504.01 2148.04,2435.46 C2124.56,2362.74 2151.82,2288.66 2216.72,2248.07 C2219.54,2246.31 2222.49,2244.75 2226.65,2242.32 Z"/>')
    o.append('</g>')

    # Studio Title & Monogram
    o.append(f'<text x="44" y="22" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="14" font-weight="800" fill="{paper}" letter-spacing="2">ZIRTUNO</text>')
    o.append(f'<text x="136" y="22" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, monospace" font-size="10" font-weight="600" fill="{cyan}" letter-spacing="1.5">STUDIO // SYSTEMS ARCHITECTURE</text>')

    # Live Systems Status Beacon
    o.append(f'<g transform="translate({W - 88 - 260}, 10)">')
    o.append(f'<circle cx="0" cy="11" r="4.5" fill="{cyan}" class="beaconPulse"/>')
    o.append(f'<text x="14" y="15" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, monospace" font-size="10" font-weight="600" fill="{cyan_glow}" letter-spacing="1.2">SYSTEMS ACTIVE // NODE: LATAM-01</text>')
    o.append('</g>')

    o.append('</g>') # End Header

    # =========================================================================
    # 5. HERO IDENTITY & DISPLAY COPY
    # =========================================================================
    o.append('<g transform="translate(44, 98)">')
    o.append(f'<text x="0" y="38" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="34" font-weight="800" fill="{paper}" letter-spacing="1.5">PEDRO MAUTONE</text>')
    o.append(f'<text x="0" y="66" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="14.5" font-weight="600" fill="{cyan}" letter-spacing="1.2">Co-Founder &amp; Systems Architect at Zirtuno</text>')
    o.append(f'<text x="0" y="90" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12" fill="{paper_muted}">High-concurrency distributed backends · Edge computer vision telemetry · Low-level protocol dissection</text>')
    o.append('</g>')

    # =========================================================================
    # 6. SUSPENDED GLASS TELEMETRY CAPSULES
    # =========================================================================
    pills = [
        ("LIFETIME COMMITS", f"{lifetime_commits}", f"{paper}"),
        ("ANNUAL VELOCITY", f"{total_contribs} contribs", f"{cyan}"),
        ("ACTIVE REPOSITORIES", f"{stats['repos']:02d} systems", f"{paper}"),
        ("PRIMARY STACK", "77.6% Py · 22.4% C++", f"{cyan_glow}"),
    ]
    
    pill_w = (W - 88 - 3 * 12) / 4
    for pi, (plabel, pval, pcol) in enumerate(pills):
        px = 44 + pi * (pill_w + 12)
        py = 216
        o.append(f'<g transform="translate({px:.1f}, {py})" class="glassCapsule">')
        o.append(f'<rect width="{pill_w:.1f}" height="52" rx="10" fill="{glass_fill}" stroke="{glass_border}" stroke-width="1.2"/>')
        o.append(f'<text x="14" y="20" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, monospace" font-size="9" font-weight="700" fill="{paper_sub}" letter-spacing="1.2">{esc(plabel)}</text>')
        o.append(f'<text x="14" y="40" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="14" font-weight="700" fill="{pcol}">{esc(pval)}</text>')
        o.append('</g>')

    # =========================================================================
    # 7. ARCHITECTURAL PILLARS (Suspended in the lower fluid substrate)
    # =========================================================================
    pillars = [
        ("EDGE TELEMETRY & CV", "ESP32-CAM · FreeRTOS · YOLOv8", "Sub-100ms spatial vehicle tracking & occupancy stream"),
        ("ENTERPRISE DATA BUS", "FastAPI · Redis · PostgreSQL · ERP", "Bi-directional ERP/CRM sync engine with transactional outbox"),
        ("LOW-LEVEL & PROTOCOLS", "C / C++ · Linux / POSIX · GDB", "Binary reverse engineering & hardware socket interop"),
    ]
    
    card_w = (W - 88 - 2 * 14) / 3
    for ci, (ctitle, cstack, cdesc) in enumerate(pillars):
        cx = 44 + ci * (card_w + 14)
        cy = 452
        o.append(f'<g transform="translate({cx:.1f}, {cy})" class="pillarCard">')
        o.append(f'<rect width="{card_w:.1f}" height="82" rx="10" fill="{glass_fill}" stroke="{glass_border}" stroke-width="1.2"/>')
        o.append(f'<circle cx="16" cy="23" r="3.2" fill="{cyan}"/>')
        o.append(f'<text x="26" y="26" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700" fill="{paper}">{esc(ctitle)}</text>')
        o.append(f'<text x="16" y="46" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, monospace" font-size="9.5" font-weight="600" fill="{cyan_glow}">{esc(cstack)}</text>')
        o.append(f'<text x="16" y="64" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10" fill="{paper_muted}">{esc(cdesc)}</text>')
        o.append('</g>')

    # Footer datum
    o.append(f'<text x="44" y="568" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, monospace" font-size="9" fill="{paper_sub}" letter-spacing="1.2">ZIRTUNO R5 // ONE CONTINUOUS LIQUID ENGINE</text>')
    o.append(f'<text x="{W - 44}" y="568" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, monospace" font-size="9" fill="{paper_sub}" letter-spacing="1.2" text-anchor="end">TELEMETRY SYNCED {esc(stats["built"])}</text>')

    # Border perimeter
    o.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{glass_border}" stroke-width="1"/>')
    o.append('</g>') # End stageClip

    # =========================================================================
    # 8. PURE CSS CONTINUOUS FLUID ANIMATIONS (60 FPS Infinite Loops)
    # =========================================================================
    css = f'''
    /* Continuous infinite wave translation */
    .waveMove1 {{
        animation: waveShift1 16s linear infinite;
    }}
    .waveMove2 {{
        animation: waveShift2 11s linear infinite;
    }}
    .waveMove3 {{
        animation: waveShift3 7.5s linear infinite;
    }}

    @keyframes waveShift1 {{
        0%   {{ transform: translateX(0px); }}
        100% {{ transform: translateX(-{W}px); }}
    }}
    @keyframes waveShift2 {{
        0%   {{ transform: translateX(-{W}px); }}
        100% {{ transform: translateX(0px); }}
    }}
    @keyframes waveShift3 {{
        0%   {{ transform: translateX(0px); }}
        100% {{ transform: translateX(-{W}px); }}
    }}

    /* Droplet bobbing and coalescing with fill-box transform-origin */
    .moteFloat1 {{
        transform-box: fill-box;
        transform-origin: center;
        animation: floatMote1 4.8s ease-in-out infinite;
    }}
    .moteFloat2 {{
        transform-box: fill-box;
        transform-origin: center;
        animation: floatMote2 3.9s ease-in-out infinite;
    }}
    .moteFloat3 {{
        transform-box: fill-box;
        transform-origin: center;
        animation: floatMote3 5.4s ease-in-out infinite;
    }}

    @keyframes floatMote1 {{
        0%, 100% {{ transform: translateY(0px) scale(1); }}
        50%      {{ transform: translateY(-15px) scale(1.15); }}
    }}
    @keyframes floatMote2 {{
        0%, 100% {{ transform: translateY(0px) scale(1); }}
        50%      {{ transform: translateY(12px) scale(0.90); }}
    }}
    @keyframes floatMote3 {{
        0%, 100% {{ transform: translateY(0px) scale(1); }}
        50%      {{ transform: translateY(-9px) scale(1.10); }}
    }}

    /* High atmosphere ambient drifting particles */
    .particleDrift1 {{
        transform-box: fill-box;
        transform-origin: center;
        animation: driftParticle1 7s ease-in-out infinite;
    }}
    .particleDrift2 {{
        transform-box: fill-box;
        transform-origin: center;
        animation: driftParticle2 10s ease-in-out infinite;
    }}
    .particleDrift3 {{
        transform-box: fill-box;
        transform-origin: center;
        animation: driftParticle3 8.5s ease-in-out infinite;
    }}

    @keyframes driftParticle1 {{
        0%, 100% {{ transform: translate(0px, 0px); opacity: 0.35; }}
        50%      {{ transform: translate(14px, -8px); opacity: 0.75; }}
    }}
    @keyframes driftParticle2 {{
        0%, 100% {{ transform: translate(0px, 0px); opacity: 0.50; }}
        50%      {{ transform: translate(-12px, 9px); opacity: 0.85; }}
    }}
    @keyframes driftParticle3 {{
        0%, 100% {{ transform: translate(0px, 0px); opacity: 0.45; }}
        50%      {{ transform: translate(9px, 7px); opacity: 0.80; }}
    }}

    /* Telemetry Beacon Pulse */
    .beaconPulse {{
        transform-box: fill-box;
        transform-origin: center;
        animation: pulseBeacon 2.2s ease-in-out infinite;
    }}
    @keyframes pulseBeacon {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50%      {{ opacity: 0.35; transform: scale(0.75); }}
    }}

    .beaconLine {{
        animation: pulseLine 2.5s ease-in-out infinite;
    }}
    @keyframes pulseLine {{
        0%, 100% {{ opacity: 1; }}
        50%      {{ opacity: 0.5; }}
    }}

    /* Accessibility reduced motion fallback */
    @media (prefers-reduced-motion: reduce) {{
        .waveMove1, .waveMove2, .waveMove3, .moteFloat1, .moteFloat2, .moteFloat3,
        .particleDrift1, .particleDrift2, .particleDrift3, .beaconPulse, .beaconLine {{
            animation: none !important;
        }}
    }}
    '''

    o.append(f'<style>{css}</style>')
    o.append('</svg>')
    return "\n".join(o)

def main():
    repo_dir = Path(__file__).resolve().parent
    assets_dir = repo_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    stats = load_stats()
    
    for theme in ("dark", "light"):
        svg_code = render_liquid(stats, theme)
        
        # New Zirtuno Liquid assets
        p1 = assets_dir / f"zirtuno-liquid-{theme}.svg"
        p1.write_text(svg_code, encoding="utf-8")
        print(f"Generated {p1.name} ({p1.stat().st_size / 1024:.1f} KB)")
        
        # Legacy/Compatibility filenames
        p2 = assets_dir / f"console-{theme}.svg"
        p2.write_text(svg_code, encoding="utf-8")
        print(f"Updated compatibility asset {p2.name}")

if __name__ == "__main__":
    main()
