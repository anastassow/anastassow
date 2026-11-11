#!/usr/bin/env python3
"""The profile's graphics: the System Society Bulgaria strip and the technology plates.

The README itself is Markdown. Two things are drawn here:

1. assets/profile/ssb-{light,dark}.png, the System Society Bulgaria section, in the SSB
   Phase III identity (~/Desktop/SSB/phase3): the Google Forms header composition, type
   only. Strip 1600 x 400, m = 400 / 8 = 50; the logo on row 1 at 72 px, the display word
   on row 5, one line of facts on row 6.6. Sofia Sans, Paper / Pine grounds.
2. assets/tech/*.svg, one white plate per technology with its logo in its own colours
   (SSB: white is the colour for partner plates; outside logos keep their colours).
   A Stone hairline keeps the plate visible on GitHub's white page. The plates are plain
   SVG with the type outlined, so they need no fonts where they are shown.

Usage:
  <python with fontTools> assets/make_profile.py OUT_DIR
  CHROME_BIN=<chrome or chrome-headless-shell> node assets/render.js OUT_DIR/*.html
  cp OUT_DIR/ssb-*.png assets/profile/
The plates are written straight to assets/tech/.
"""
import html
import math
import os
import re
import sys

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.expanduser("~/Desktop/SSB/phase3/Source-Files/Fonts-and-Licenses/Static")
LOGO = os.path.expanduser("~/Desktop/SSB/phase3/Assets/Logo/Masters/SVG")
ICONS = os.path.join(HERE, "icons")
TECH_OUT = os.path.join(HERE, "tech")
OUT = sys.argv[1] if len(sys.argv) > 1 else "build"
os.makedirs(OUT, exist_ok=True)
os.makedirs(TECH_OUT, exist_ok=True)

THEMES = {
    "light": dict(bg="#F3F5F4", fg="#121A18", fg2="#4C5953", logo="color"),
    "dark": dict(bg="#0E2821", fg="#F3F5F4", fg2="#A8B7B0", logo="reverse"),
}
STONE, INK, WHITE = "#C3D0C9", "#121A18", "#FFFFFF"

FACES = {("Sofia Sans", 400): "SofiaSans-Regular.ttf", ("Sofia Sans", 700): "SofiaSans-Bold.ttf"}
_fonts = {}


def font(w):
    if w not in _fonts:
        _fonts[w] = TTFont(os.path.join(FONTS, FACES[("Sofia Sans", w)]))
    return _fonts[w]


def track(px, scale):
    """Phase III tracking in em, from the size people actually see."""
    return -0.016 + 0.12 * math.exp(-0.12 * px * scale)


def text(x, y, size, s, color, scale):
    """Sofia Sans 400 placed by its baseline, the first stem on x (side bearing removed)."""
    f = font(400)
    x -= f["hmtx"][f.getBestCmap()[ord(s[0])]][1] * size / 1000
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="Sofia Sans" font-weight="400" '
            f'font-size="{size}" letter-spacing="{track(size, scale) * size:.2f}" fill="{color}" '
            f'xml:space="preserve">{html.escape(s)}</text>')


# --- 1. System Society Bulgaria, after the Google Forms header ------------------------------
def ssb(theme):
    th, W, H, m = THEMES[theme], 1600, 400, 50
    sc = 830 / W                                   # shown about 830 px wide in the README
    svg = open(os.path.join(LOGO, f"ssb-horizontal-{th['logo']}.svg")).read()
    logo = svg[svg.index("<g"):svg.rindex("</svg>")]
    faces = "".join(f'@font-face{{font-family:"{f}";font-weight:{w};src:url("file://{FONTS}/{p}")}}'
                    for (f, w), p in FACES.items())
    body = (f'<rect width="{W}" height="{H}" fill="{th["bg"]}"/>'
            f'<g transform="translate({2 * m} {m}) scale(0.72)">{logo}</g>'
            + text(2 * m, 5 * m, 128, "Founder", th["fg"], sc)
            + text(2 * m, 6.6 * m, 52, "Free monthly sessions in Sofia", th["fg2"], sc))
    open(os.path.join(OUT, f"ssb-{theme}.html"), "w").write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{faces}html,body{{margin:0}}'
        f'</style></head><body><svg id="c" xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">{body}</svg><script>document.fonts.ready.then(() => '
        f'document.body.dataset.ready = "1")</script></body></html>')


# --- 2. technology plates --------------------------------------------------------------------
P, LOGO_BOX = 96, 60                               # plate and logo box, in plate units


def plate(name, art, title):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{P}" height="{P}" viewBox="0 0 {P} {P}" '
           f'role="img" aria-label="{title}"><title>{title}</title>'
           f'<rect x="1" y="1" width="{P - 2}" height="{P - 2}" fill="{WHITE}" stroke="{STONE}" '
           f'stroke-width="2"/>{art}</svg>\n')
    open(os.path.join(TECH_OUT, name + ".svg"), "w").write(svg)


def devicon(file):
    """A Devicon logo (128 x 128 view box) nested in the centre of the plate."""
    svg = open(os.path.join(ICONS, file)).read()
    inner = svg[svg.index(">", svg.index("<svg")) + 1:svg.rindex("</svg>")]
    o = (P - LOGO_BOX) / 2
    return (f'<svg x="{o}" y="{o}" width="{LOGO_BOX}" height="{LOGO_BOX}" viewBox="0 0 128 128">'
            f'{inner}</svg>')


def fitted_path(d, colour, max_w, max_h):
    """A one-colour path scaled to fit max_w x max_h by its real bounds, centred on the plate."""
    bp = BoundsPen(None)
    parse_path(d, bp)
    x0, y0, x1, y1 = bp.bounds
    k = min(max_w / (x1 - x0), max_h / (y1 - y0))
    tx, ty = P / 2 - (x0 + x1) / 2 * k, P / 2 - (y0 + y1) / 2 * k
    return f'<path transform="translate({tx:.3f} {ty:.3f}) scale({k:.4f})" d="{d}" fill="{colour}"/>'


def outlined(word, colour, fig):
    """A word in Sofia Sans Bold as outlines, centred, with figures fig units tall."""
    f = font(700)
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    k = fig / (0.655 * upm)
    total = sum(gs[cmap[ord(c)]].width for c in word) * k
    x, base = (P - total) / 2, P / 2 + fig / 2
    pen = SVGPathPen(gs)
    for c in word:
        g = gs[cmap[ord(c)]]
        g.draw(TransformPen(pen, (k, 0, 0, -k, x, base)))
        x += g.width * k
    return f'<path d="{pen.getCommands()}" fill="{colour}"/>'


TECH = [("c", "C", "c-original.svg"), ("cpp", "C++", "cplusplus-original.svg"),
        ("x86", "x86 assembly", None), ("arm", "ARM assembly", None),
        ("bash", "Bash", "bash-original.svg"), ("python", "Python", "python-original.svg"),
        ("linux", "Linux", "linux-original.svg"), ("macos", "macOS", "apple-original.svg"),
        ("linkedin", "LinkedIn", "linkedin-original.svg")]

for name, title, file in TECH:
    if name == "x86":                              # x86 has no logo: the word, in ink
        art = outlined("x86", INK, 26)
    elif name == "arm":                            # Simple Icons wordmark in Arm's blue
        d = re.search(r' d="([^"]+)"', open(os.path.join(ICONS, "arm.svg")).read()).group(1)
        art = fitted_path(d, "#0091BD", 70, 30)
    else:
        art = devicon(file)
    plate(name, art, title)

for th in THEMES:
    ssb(th)
print(OUT, TECH_OUT)
