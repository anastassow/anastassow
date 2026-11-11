#!/usr/bin/env python3
"""The profile's images, built on the System Society Bulgaria Phase III identity.

Rules taken from ~/Desktop/SSB/phase3 (Brand-Guidelines, Design-Tokens):
  - Stone and pine: Paper / Pine grounds, Stone / Pine-plane planes. Green only as
    the one displaced plane, and that plane always carries text.
  - Sofia Sans set as text (400/500), Semi Condensed 500 for labels in sentence
    case, Light 300 for numerals. No monospace labels, no centred-dot separators.
  - Strips: m = height / 8. Pages: m = short side / 25. Positions in modules.
  - A displaced plane sits depth / 3 right of the margin and bleeds off an edge.
  - One green plane on the whole README (the banner); everything else is neutral.

Text is SVG <text> placed by its baseline, as in the SSB generator; the first
glyph's side bearing is subtracted so stems, not glyph boxes, sit on the margin.

Usage:
  <python with fontTools> assets/make_profile.py OUT_DIR
  CHROME_BIN=<chrome or chrome-headless-shell> node assets/render.js OUT_DIR/*.html
  cp OUT_DIR/*.png assets/profile/
make_profile.py writes OUT_DIR/<image>-<theme>.html; render.js (playwright-core)
screenshots the SVG in each to a PNG with a transparent background.
"""
import html
import math
import os
import sys

from fontTools.ttLib import TTFont

FONTS = os.path.expanduser("~/Desktop/SSB/phase3/Source-Files/Fonts-and-Licenses/Static")
LOGO = os.path.expanduser("~/Desktop/SSB/phase3/Assets/Logo/Masters/SVG")
OUT = sys.argv[1] if len(sys.argv) > 1 else "build"
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "light": dict(bg="#F3F5F4", plane="#C3D0C9", fg="#121A18", fg2="#4C5953",
                  field="#0A7A5A", on_field="#FFFFFF", rule="#C3D0C9", logo="color"),
    "dark": dict(bg="#0E2821", plane="#1B382E", fg="#F3F5F4", fg2="#A8B7B0",
                 field="#0A7A5A", on_field="#FFFFFF", rule="#343F3A", logo="reverse"),
}

FACES = {  # (family, weight) -> file
    ("Sofia Sans", 300): "SofiaSans-Light.ttf",
    ("Sofia Sans", 400): "SofiaSans-Regular.ttf",
    ("Sofia Sans", 500): "SofiaSans-Medium.ttf",
    ("Sofia Sans Semi Condensed", 500): "SofiaSansSemiCondensed-Medium.ttf",
}
_fonts = {}


def font(fam, w):
    if (fam, w) not in _fonts:
        t = TTFont(os.path.join(FONTS, FACES[(fam, w)]))
        _fonts[(fam, w)] = (t.getBestCmap(), t["hmtx"])
    return _fonts[(fam, w)]


def track(px, scale):
    """Phase III tracking in em, from the size people actually see."""
    return -0.016 + 0.12 * math.exp(-0.12 * px * scale)


def lsb(s, size, fam, w):
    cmap, hmtx = font(fam, w)
    return hmtx[cmap[ord(s[0])]][1] * size / 1000


def width(s, size, fam, w, ls):
    cmap, hmtx = font(fam, w)
    return sum(hmtx[cmap[ord(c)]][0] for c in s) * size / 1000 + ls * size * (len(s) - 1)


CHECKS = []


def text(x, y, size, s, color, scale, w=400, fam="Sofia Sans", anchor="start", limit=None):
    ls = track(size, scale)
    if anchor == "start":
        x -= lsb(s, size, fam, w)
    if limit is not None:
        CHECKS.append((s, x + width(s, size, fam, w, ls), limit))
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{fam}" font-weight="{w}" '
            f'font-size="{size}" letter-spacing="{ls * size:.2f}" fill="{color}" '
            f'text-anchor="{anchor}" xml:space="preserve">{html.escape(s)}</text>')


def rect(x, y, w, h, color):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{color}"/>'


def logo(version, x, y, height):
    svg = open(os.path.join(LOGO, f"ssb-horizontal-{version}.svg")).read()
    body = svg[svg.index("<g"):svg.rindex("</svg>")]
    return f'<g transform="translate({x} {y}) scale({height / 100})">{body}</g>'


def page(name, theme, w, h, inner, ground=True):
    """ground=False leaves the canvas transparent (render with OMIT=1); inner draws its own ground."""
    th = THEMES[theme]
    faces = "".join(f'@font-face{{font-family:"{f}";font-weight:{wt};src:url("file://{FONTS}/{p}")}}'
                    for (f, wt), p in FACES.items())
    open(os.path.join(OUT, f"{name}-{theme}.html"), "w").write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{faces}'
        f'html,body{{margin:0}}text{{font-kerning:normal}}</style></head><body>'
        f'<svg id="c" xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f'{rect(0, 0, w, h, th["bg"]) if ground else ""}{inner}</svg></body></html>')


# --- banner: the LinkedIn composition. The statement in two lines broken by meaning;
# the second line sits on the green plane, which bleeds off the right and bottom edges.
# 1600 x 400 strip, m = 400 / 8 = 50; margins 2m at the sides, 1m at the top. Shown ~830 px.
def banner(theme):
    th, W, H, m = THEMES[theme], 1600, 400, 50
    sc, mg, cap = 830 / W, 2 * m, 0.655
    plane_top = 5 * m
    depth = H - plane_top                       # 3m
    plane_x = mg + depth / 3                    # the displacement: a third of the depth
    size = 88
    out = text(mg, m + cap * 52, 52, "Systems programmer working on optimization",
               th["fg2"], sc, 500, "Sofia Sans Semi Condensed", limit=W - mg)
    out += text(mg, 4 * m, size, "Hi, I’m Dimitar Anastasov", th["fg"], sc, limit=W - mg)
    out += rect(plane_x, plane_top, W - plane_x, depth, th["field"])
    base = plane_top + (depth - cap * size) / 2 + cap * size - 4    # caps centred, a touch high
    out += text(plane_x + 0.75 * m, base, size, "Systems for ML and ML for Systems",
                th["on_field"], sc, limit=W - mg)
    page("banner", theme, W, H, out)


# --- work tiles, after the Luma event cover without its green plane: label, title and lead
# on the ground; an anchored Stone plane carries the numeral and one fact.
# 1200 x 750 page, m = 750 / 25 = 30; margins 2m. Two tiles share a row at 50 % each, shown
# ~410 px wide; each image carries half the gutter (GUTTER px, transparent) on its inner side,
# so the pair lines up with the full-width images above and below it.
GUTTER = 12


def tile(name, theme, num, label, title, lead, fact, side):
    th, W, H, m = THEMES[theme], 1200, 750, 30
    sc, mg, cap = 410 / W, 2 * m, 0.655
    out = rect(0, 0, W, H, th["bg"])
    out += text(mg, mg + cap * 42, 42, label, th["fg2"], sc, 500, "Sofia Sans Semi Condensed")
    out += text(mg, 6 * m, 100, title, th["fg"], sc, 500, limit=W - mg)
    for i, line in enumerate(lead):
        out += text(mg, 8.6 * m + i * 60, 48, line, th["fg"], sc, limit=W - mg)
    out += rect(0, 15.5 * m, W, H - 15.5 * m, th["plane"])
    out += text(mg, H - mg, 220, num, th["fg"], sc, 300)
    out += text(W - mg, H - mg, 42, fact, th["fg2"], sc, 500, "Sofia Sans Semi Condensed", anchor="end")
    dx = GUTTER if side == "right" else 0
    page(f"work-{name}", theme, W + GUTTER, H, f'<g transform="translate({dx} 0)">{out}</g>', ground=False)


TILES = [
    ("quicx", "01", "Task queue engine in C", "Quicx",
     ["My own memory allocator and binary protocol.",
      "When memory is full, it keeps the most",
      "valuable work."],
     "36 KB on a Raspberry Pi"),
    ("sandokan", "02", "Training library in C++", "Sandokan",
     ["Neural network training on the CPU,",
      "tuned for speed. No Python and no GPU."],
     "On-device learning"),
    ("zdoc", "03", "Documentation engine", "ZDoc",
     ["Optimized documentation for mainframe",
      "and modern code, built at the IBM",
      "summer practice."],
     "PL/X, assembler, C, C++, Java"),
    ("more", "04", "Also", "Compilers and robotics",
     ["A compiler for a C-style language, and",
      "autonomous robots with on-board vision",
      "and machine learning."],
     "Lexers, parsers, computer vision"),
]


# --- System Society Bulgaria, after the Google Forms header: type only.
# 1600 x 400 strip, m = 50: logo on row 1 at 72 px, the display word on row 5, facts on row 6.6.
def ssb(theme):
    th, W, H, m = THEMES[theme], 1600, 400, 50
    sc = 830 / W
    out = logo(th["logo"], 2 * m, m, 72)
    out += text(2 * m, 5 * m, 128, "Founder", th["fg"], sc)
    out += text(2 * m, 6.6 * m, 52, "Free monthly sessions in Sofia", th["fg2"], sc)
    page("ssb", theme, W, H, out)


# --- skills and main technologies: separate facts in columns, a hairline between them
def skills(theme):
    th, W, m = THEMES[theme], 1600, 50
    sc, cap, lead = 830 / W, 0.655, 56
    rows = [
        ("Skills", ["Mathematics, machine learning, optimization,",
                    "systems programming, operating systems,",
                    "microprocessor architecture,",
                    "memory management, parallel computing"]),
        ("Main technologies", ["C and C++, x86 and ARM assembly, Bash, Python,",
                               "Linux, macOS, Raspberry Pi, Git, Docker"]),
    ]
    out, y = "", m
    for i, (label, lines) in enumerate(rows):
        if i:
            out += rect(2 * m, y, W - 4 * m, 2, th["rule"])
            y += m
        first = y + cap * 44
        out += text(2 * m, first, 38, label, th["fg2"], sc, 500, "Sofia Sans Semi Condensed")
        for j, line in enumerate(lines):
            out += text(9 * m, first + j * lead, 44, line, th["fg"], sc, limit=W - 2 * m)
        y = first + (len(lines) - 1) * lead + 0.3 * 44 + m
    page("skills", theme, W, round(y), out)


for th in THEMES:
    banner(th)
    ssb(th)
    skills(th)
    for k, (name, num, label, title, lead, fact) in enumerate(TILES):
        tile(name, th, num, label, title, lead, fact, "left" if k % 2 == 0 else "right")

bad = [(s, round(r), lim) for s, r, lim in CHECKS if r > lim]
for s, r, lim in bad:
    print(f"overflow: {s!r} ends at {r}, limit {lim}")
print("ok" if not bad else "check the lines above", OUT)
