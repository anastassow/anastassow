#!/usr/bin/env python3
"""The profile's cards as HTML, rendered to PNG by render_cards.js (Playwright)."""
import os
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards")
os.makedirs(HERE, exist_ok=True)

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700&family=JetBrains+Mono:wght@400;500;700&display=block" rel="stylesheet">
<style>
html,body{margin:0;background:transparent}
.card{position:relative;box-sizing:border-box;background:#0d1412;border:1.5px solid #202f2b;border-radius:18px;overflow:hidden;font-family:Archivo,sans-serif;color:#f3f5f4}
.k{font-family:"JetBrains Mono",monospace;font-size:21px;letter-spacing:.08em;color:#3eb189;text-transform:uppercase}
.t{font-weight:700;font-size:50px;margin-top:8px;letter-spacing:-.5px}
.d{font-size:26px;line-height:1.38;color:#d0d6d4;margin-top:12px}
.f{position:absolute;left:34px;bottom:26px;font-family:"JetBrains Mono",monospace;font-size:20px;color:#99a4a1}
.dot{display:inline-block;width:11px;height:11px;border-radius:50%;background:#3eb189;margin-right:8px;vertical-align:middle}
</style>"""

def page(name, w, h, inner):
    open(os.path.join(HERE, name + ".html"), "w").write(
        f'<!doctype html><html><head><meta charset="utf-8">{CSS}</head><body>'
        f'<div class="card" id="c" style="width:{w}px;height:{h}px">{inner}</div></body></html>')

def project(name, kicker, title, desc, foot, art):
    page(name, 800, 400, f'''
<div style="position:absolute;left:34px;top:30px;width:500px">
  <div class="k">{kicker}</div><div class="t">{title}</div><div class="d">{desc}</div></div>
<div class="f">{foot}</div>
<div style="position:absolute;right:24px;top:50%;transform:translateY(-50%) scale(.82);transform-origin:right center">{art}</div>''')

# --- small drawings ---------------------------------------------------------
def pages_art():
    import random
    r = random.Random(3); cells = []
    for i in range(12):
        x, y = (i % 4) * 58, (i // 4) * 58
        hl = i == 5
        kind = "u" if r.random() < .6 or hl else "c"
        inner = ""
        if kind == "u":
            g = 3 if r.random() < .5 or hl else 5
            s = 44 / g
            for a in range(g):
                for b in range(g):
                    col = "#3eb189" if hl and a == 0 and b == 0 else ("#99a4a1" if (a * g + b) % 5 != 3 else "#4a5955")
                    inner += f'<rect x="{6+b*s+1:.1f}" y="{6+a*s+1:.1f}" width="{s-2:.1f}" height="{s-2:.1f}" rx="1" fill="{col}"/>'
            stroke = "#3eb189" if hl else "#354540"
            cells.append(f'<g transform="translate({x},{y})"><rect width="50" height="50" rx="5" fill="#13241f" stroke="{stroke}" stroke-width="{2 if hl else 1.2}"/>{inner}</g>')
        else:
            cells.append(f'<g transform="translate({x},{y})"><rect width="50" height="50" rx="5" fill="none" stroke="#354540" stroke-dasharray="4 4"/></g>')
    return f'<svg width="226" height="168" viewBox="0 0 226 168">{"".join(cells)}</svg>'

def net_art():
    cols = [4, 6, 6, 3]; xs = [10, 80, 150, 220]; nodes = []
    for ci, n in enumerate(cols):
        top = 84 - (n - 1) * 15
        nodes.append([(xs[ci], top + j * 30) for j in range(n)])
    lines = ""
    for a, b in zip(nodes, nodes[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                lines += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#354540" stroke-width="1"/>'
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="{"#3eb189" if ci == 3 and j == 1 else "#13241f"}" stroke="{"#3eb189" if ci == 3 and j == 1 else "#99a4a1"}" stroke-width="1.6"/>'
                   for ci, col in enumerate(nodes) for j, (x, y) in enumerate(col))
    return f'<svg width="232" height="172" viewBox="0 0 232 172">{lines}{dots}</svg>'

def doc_art():
    rows = [(0, 150), (20, 110), (20, 160), (0, 90), (0, 170), (20, 120), (40, 100), (20, 140)]
    out = ""
    for i, (ind, w) in enumerate(rows):
        y = i * 20
        col = "#3eb189" if i in (1, 5) else "#4a5955"
        out += f'<rect x="{30+ind}" y="{y}" width="{w}" height="9" rx="4" fill="{col}"/>'
        out += f'<text x="0" y="{y+9}" font-family="JetBrains Mono" font-size="11" fill="#697772">{i+1:02d}</text>'
    return f'<svg width="232" height="160" viewBox="0 0 232 160">{out}</svg>'

def tree_art():
    pts = {"r": (110, 14), "a": (50, 74), "b": (170, 74), "c": (20, 134), "d": (80, 134), "e": (140, 134), "f": (200, 134)}
    edges = [("r", "a"), ("r", "b"), ("a", "c"), ("a", "d"), ("b", "e"), ("b", "f")]
    out = "".join(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" stroke="#354540" stroke-width="1.6"/>' for a, b in edges)
    for k, (x, y) in pts.items():
        hl = k == "r"
        out += f'<rect x="{x-22}" y="{y-12}" width="44" height="24" rx="6" fill="{"#0f2a22" if hl else "#13241f"}" stroke="{"#3eb189" if hl else "#99a4a1"}" stroke-width="1.4"/>'
    return f'<svg width="222" height="150" viewBox="0 0 222 150">{out}</svg>'

# --- cards ------------------------------------------------------------------
project("quicx", "Task queue engine · C", "Quicx",
        "My own task queue, with my own memory allocator and protocol. When memory is full, it keeps the most valuable work.",
        '<span class="dot"></span>research on ML for Systems', pages_art())
project("sandokan", "CPU training library · C++", "Sandokan",
        "Neural network training on the CPU, tuned for speed. No Python and no GPU needed.",
        "on-device learning", net_art())
project("zdoc", "Documentation engine", "ZDoc",
        "An optimized documentation generator for mainframe and modern code, built at the IBM summer practice.",
        "PL/X · assembler · C/C++ · Java", doc_art())
project("more", "Also", "Compilers and robotics",
        "A compiler for a C-style language, and autonomous robots with on-board vision and machine learning.",
        "lexers · parsers · computer vision", tree_art())

cols = [("01", "Optimization", "Making systems faster and leaner, down to what the processor and the cache are doing."),
        ("02", "Systems for ML", "Training and running models where memory and compute are tight, without a GPU."),
        ("03", "ML for Systems", "Systems software that learns from its own behaviour what to keep and what to drop.")]
inner = '<div style="position:absolute;left:40px;top:30px" class="k">What I do</div>'
for i, (n, t, d) in enumerate(cols):
    x = 40 + i * 515
    inner += f'''<div style="position:absolute;left:{x}px;top:76px;width:460px">
      <div style="font-family:'JetBrains Mono',monospace;font-size:21px;color:#697772">{n}</div>
      <div class="t" style="font-size:44px;margin-top:6px">{t}</div>
      <div class="d" style="font-size:27px">{d}</div></div>'''
    if i:
        inner += f'<div style="position:absolute;left:{x-28}px;top:84px;width:1.5px;height:250px;background:#202f2b"></div>'
page("focus", 1600, 370, inner)

symbol = ('<svg width="130" height="130" viewBox="0 0 100 100"><rect x="0" y="0" width="75" height="25" fill="#f1f4f3"/>'
          '<rect x="25" y="37.5" width="75" height="25" fill="#3eb189"/><rect x="0" y="75" width="75" height="25" fill="#f1f4f3"/></svg>')
page("ssb", 1600, 300, f'''
<div style="position:absolute;left:52px;top:50%;transform:translateY(-50%)">{symbol}</div>
<div style="position:absolute;left:220px;top:50%;transform:translateY(-50%)">
  <div class="k">Founder</div>
  <div class="t" style="font-size:58px">System Society Bulgaria</div>
  <div class="d" style="font-size:30px">Everything runs on systems. AI, quantum, and business are all built on them.</div>
</div>''')
print("ok")
