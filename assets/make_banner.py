#!/usr/bin/env python3
"""
The profile banner: the layout and memory-page grid of the Quicx README
banner, in the colours of System Society Bulgaria (night ground, Displaced
Green). Draws with Quicx's diagram code:

    python3 assets/make_banner.py ~/Desktop/Quicx-adaptive/docs/report/scripts
    rsvg-convert -z 2 assets/banner-dark.svg -o assets/banner-dark.png   (and light)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.expanduser(sys.argv[1]))
from make_diagrams import Canvas, DARK, LIGHT  # noqa: E402

NIGHT = dict(DARK, bg="#0d1412", panel="#101f1b", panel2="#13241f", well="#06120f", line="#202f2b",
             strong="#354540", text="#f3f5f4", body="#d0d6d4", muted="#99a4a1", dim="#697772",
             accent="#3eb189", accent_text="#3eb189", accent_soft="#0f2a22", warm="#354540",
             block="#99a4a1", block2="#4a5955", badge="#0d1412")
PAPER = dict(LIGHT, bg="#ffffff", panel="#f8fbfa", panel2="#e3e7e6", line="#d0d6d4", strong="#99a4a1",
             text="#121a18", body="#202f2b", muted="#4a5955", dim="#697772",
             accent="#0a7a5a", accent_text="#0a7a5a", accent_soft="#d6f8e9", warm="#d0d6d4",
             block="#697772", block2="#99a4a1")


def banner(pal):
    c = Canvas(pal, 1600, 420)
    c.text(82, 124, "Hi, I'm", size=24, mono=True, color="accent_text")
    c.text(80, 192, "Dimitar Anastasov", size=66, weight=700, color="text")
    c.text(80, 256, "Systems programmer: optimization, Systems for ML and ML for Systems.", size=26, color="body")
    c.text(80, 300, "Final-year student at TUES. Founder of System Society Bulgaria.", size=22, color="muted")

    # memory pages, as in the Quicx diagrams: in use (finer grid = smaller blocks), warm, cold
    kinds = ["u6", "u6", "u3", "u6", "hl", "w", "u6", "u3",
             "u3", "w", "u6", "u6", "u3", "c", "u6", "w",
             "u6", "u3", "c", "u6", "c", "c", "w", "c",
             "c", "u6", "c", "c", "c", "c", "c", "c"]
    s, g, x0, y0 = 46, 10, 1080, 96
    for i, k in enumerate(kinds):
        x, y = x0 + (i % 8) * (s + g), y0 + (i // 8) * (s + g)
        if k.startswith("u"):
            c.page(x, y, s, "used", grid=int(k[1]))
        elif k == "hl":
            c.page(x, y, s, "used", grid=3, hl=True)
        elif k == "w":
            c.page(x, y, s, "warm")
        else:
            c.page(x, y, s, "cold")
    return c


for name, pal in (("dark", NIGHT), ("light", PAPER)):
    svg = banner(pal).svg("Dimitar Anastasov", "Systems programming, ML for Systems and Systems for ML")
    open(os.path.join(HERE, f"banner-{name}.svg"), "w").write(svg)
print("ok")
