#!/usr/bin/env python3
"""Redraw SFAM Figure 4.4 as vector, plus one worksheet per business domain.

The raster in assets/arch/sfam.jpg is a photograph of a printed figure: fine at
thumbnail size, soft on a projector, and impossible to edit. This regenerates the
same figure as SVG from the model's own axes, so the drawing cannot drift from the
tower it depicts, and adds a fill-in worksheet for each of the three business
domains the value chain is being built around.

    python3 tools/draw_sfam.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
M = json.loads((ROOT / "data" / "architecture-model.json").read_text(encoding="utf-8"))
SF = next(t for t in M["towers"] if t["id"] == "SFAM")

# axes straight out of the model, so the picture and the tower cannot disagree
DOMAINS = [i[1] for i in SF["xAxis"]["items"]]          # 5, upstream -> downstream
ZONES   = [i[1] for i in SF["yAxis"]["items"]]          # 6, listed top-down
ZONES_UP = list(reversed(ZONES))                        # figure draws them bottom-up
LAYERS  = [(l[0], l[1]) for l in SF["layers"]]          # 6, BUS..AST
LAYERS_UP = list(reversed(LAYERS))                      # figure stacks Asset at the bottom

ND, NZ, NL = len(DOMAINS), len(ZONES), len(LAYERS)

# isometric basis
DXX, DXY = 78.0, 19.5      # one step along Domains: right and slightly down
ZXX, ZXY = 63.0, -25.5     # one step along Zones: right and up
GAP = 84                   # vertical distance between layer planes
OX, OY = 250.0, 690.0      # (domain 0, zone 0) corner of the bottom plane

SKIN = {  # layer code -> (stroke, fill, fill-opacity) matching the printed figure
    "BUS": ("#d9534f", "#f2a9a4", .42),
    "FUN": ("#e0a33a", "#f7dda8", .40),
    "INF": ("#4da97c", "#a9dabd", .38),
    "COM": ("#2f9e9e", "#a0d7d5", .38),
    "ITG": ("#4a90c2", "#a9cee5", .38),
    "AST": ("#9aa0a6", "#e6e8ea", .55),
}
def P(d, z, layer):
    return (OX + d * DXX + z * ZXX, OY + d * DXY + z * ZXY - layer * GAP)

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def plane(code, li):
    """One interoperability layer: its ND x NZ grid, drawn as an isometric parallelogram."""
    st, fl, fo = SKIN[code]
    o = []
    c = [P(0, 0, li), P(ND, 0, li), P(ND, NZ, li), P(0, NZ, li)]
    o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in c)}" '
             f'fill="{fl}" fill-opacity="{fo}" stroke="{st}" stroke-width="1.5"/>')
    for d in range(1, ND):                      # grid lines along the zone direction
        a, b = P(d, 0, li), P(d, NZ, li)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                 f'stroke="{st}" stroke-width=".7" stroke-opacity=".85"/>')
    for z in range(1, NZ):                      # grid lines along the domain direction
        a, b = P(0, z, li), P(ND, z, li)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                 f'stroke="{st}" stroke-width=".7" stroke-opacity=".85"/>')
    return "\n".join(o)

def cell_centre(d, z, li):
    (x1, y1), (x2, y2) = P(d, z, li), P(d + 1, z + 1, li)
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def chip(d, z, li, w, colour):
    """A device/asset chip lying flat on a plane, drawn as a small iso parallelogram."""
    cx, cy = cell_centre(d, z, li)
    hx, hy = DXX * w / 2, DXY * w / 2
    zx, zy = ZXX * .16, ZXY * .16
    pts = [(cx - hx - zx, cy - hy - zy), (cx + hx - zx, cy + hy - zy),
           (cx + hx + zx, cy + hy + zy), (cx - hx + zx, cy - hy + zy)]
    return (f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" '
            f'fill="{colour}" stroke="#ffffff" stroke-width=".6"/>')

def riser(d, z, lo, hi):
    """The red vertical connector the printed figure runs between asset and integration."""
    a, b = cell_centre(d, z, lo), cell_centre(d, z, hi)
    return (f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
            f'stroke="#c0392b" stroke-width="1.5" stroke-opacity=".85"/>')

def arrow(x1, y1, x2, y2, w=1.6):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1a1a1a" '
            f'stroke-width="{w}" marker-start="url(#ms)" marker-end="url(#me)"/>')

DEFS = '''<defs>
  <marker id="me" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,1 L9,5 L0,9 z" fill="#1a1a1a"/></marker>
  <marker id="ms" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M9,1 L0,5 L9,9 z" fill="#1a1a1a"/></marker>
</defs>'''
FONT = ("font-family=\"Charter, 'Bitstream Charter', 'Sitka Text', Cambria, "
        "'Noto Serif', 'Times New Roman', serif\"")
SANS = "font-family=\"'Helvetica Neue', Helvetica, Arial, 'Noto Sans Thai', sans-serif\""


def figure():
    W, H = 1220, 980
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         DEFS, f'<rect width="{W}" height="{H}" fill="#ffffff"/>']

    for li, (code, name) in enumerate(LAYERS_UP):          # bottom (Asset) upward
        o.append(plane(code, li))
        if code == "AST":                                   # stylised farm assets
            for d in range(ND):
                for z in range(1, NZ, 2):
                    o.append(chip(d, z, li, .26, "#f0a848"))
        if code == "ITG":                                   # the coloured device bars
            bars = ["#5fae6a", "#4a86c8", "#8f6fc0", "#3fa9a2"]
            for d in range(ND):
                for z in range(1, NZ, 2):
                    o.append(chip(d, z, li, .58, bars[(d + z) % len(bars)]))

    ai = [c for c, _ in LAYERS_UP].index("AST")
    ii = [c for c, _ in LAYERS_UP].index("ITG")
    for d in range(ND):                                     # risers, asset -> integration
        for z in range(1, NZ, 2):
            o.append(riser(d, z, ai, ii))

    # layer names down the left, each on its own plane's height
    for li, (code, name) in enumerate(LAYERS_UP):
        _, y = P(0, NZ * .42, li)
        o.append(f'<text x="212" y="{y:.1f}" text-anchor="end" {FONT} font-size="15" '
                 f'fill="#1a1a1a">{esc(name)} Layer</text>')

    # Domains: labels stepped along the front edge, then one arrow beneath
    for d, dn in enumerate(DOMAINS):
        x, y = P(d, 0, 0)
        tx, ty = x + 4, y + 34
        o.append(f'<text x="{tx:.1f}" y="{ty:.1f}" {FONT} font-size="11.5" fill="#1a1a1a" '
                 f'transform="rotate(14 {tx:.1f} {ty:.1f})">{esc(dn)}</text>')
        tick = P(d, 0, 0)
        o.append(f'<line x1="{tick[0]:.1f}" y1="{tick[1] + 6:.1f}" x2="{tick[0] - 4:.1f}" '
                 f'y2="{tick[1] + 18:.1f}" stroke="#1a1a1a" stroke-width=".9"/>')
    a, b = P(0, 0, 0), P(ND, 0, 0)
    o.append(arrow(a[0] - 26, a[1] + 66, b[0] - 6, b[1] + 66))
    mx, my = (a[0] + b[0]) / 2 - 16, (a[1] + b[1]) / 2 + 88
    o.append(f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" {FONT} font-size="16" '
             f'fill="#1a1a1a">Domains</text>')

    # Zones: labels stepped up the right edge, then one arrow outside them
    for z, zn in enumerate(ZONES_UP):
        x, y = P(ND, z + .35, 0)
        tx, ty = x + 22, y + 26
        w = zn.split(" ", 1) if " " in zn else [zn, ""]
        o.append(f'<text x="{tx:.1f}" y="{ty:.1f}" {FONT} font-size="11" fill="#1a1a1a" '
                 f'transform="rotate(-22 {tx:.1f} {ty:.1f})">{esc(w[0])}'
                 f'<tspan x="{tx:.1f}" dy="12.5">{esc(w[1])}</tspan></text>')
    a, b = P(ND, 0, 0), P(ND, NZ, 0)
    o.append(arrow(a[0] + 96, a[1] + 96, b[0] + 96, b[1] + 96))
    mx, my = (a[0] + b[0]) / 2 + 128, (a[1] + b[1]) / 2 + 104
    o.append(f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" {FONT} font-size="16" '
             f'fill="#1a1a1a" transform="rotate(-22 {mx:.1f} {my:.1f})">Zones</text>')

    o.append(f'<text x="{W/2}" y="{H - 26}" text-anchor="middle" {FONT} font-size="17" fill="#1a1a1a">'
             f'<tspan font-weight="700">Figure 4.4:</tspan> The Smart Farming Architecture Model '
             f'with interoperability layers</text>')
    o.append("</svg>")
    return "\n".join(o)


# ---- one fill-in worksheet per business domain -----------------------------
BIZ = [
    {"n": 1, "cols": ["Cultivation area"], "title": "Cultivation Area",
     "sub": "Land Development", "accent": "#4da97c"},
    {"n": 2, "cols": ["Livestock"], "title": "Livestock",
     "sub": "Bamboo Plant Development", "accent": "#e0a33a"},
    {"n": 3, "cols": ["Processing", "Distribution"], "title": "Process &amp; Distribution",
     "sub": "Products", "accent": "#4a90c2"},
]

def worksheet(b):
    W, H = 1180, 800
    idx = [DOMAINS.index(c) for c in b["cols"]]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         DEFS, f'<rect width="{W}" height="{H}" fill="#ffffff"/>']

    o.append(f'<rect x="0" y="0" width="{W}" height="6" fill="{b["accent"]}"/>')
    o.append(f'<text x="44" y="62" {SANS} font-size="26" font-weight="700" fill="#14212a">'
             f'Domain {b["n"]} · {b["title"]}</text>')
    o.append(f'<text x="44" y="90" {SANS} font-size="15" fill="{b["accent"]}" font-weight="600">'
             f'{esc(b["sub"])}</text>')
    o.append(f'<text x="44" y="114" {SANS} font-size="11.5" fill="#7c8c97">'
             f'SFAM · {" + ".join(esc(c) for c in b["cols"])} · '
             f'{NL} interoperability layers x {NZ} zones = {NL*NZ*len(idx)} cells</text>')

    # locator: the five domains as a strip, with this one filled. A miniature of the
    # isometric model was unreadable at this size — which column is highlighted is the
    # only thing the reader needs here.
    lx, ly, bw, bh = 44, 152, 206, 34
    o.append(f'<text x="{lx}" y="{ly - 12}" {SANS} font-size="10.5" font-weight="600" '
             f'fill="#7c8c97" letter-spacing="1.4">THIS DOMAIN IN THE SFAM VALUE CHAIN</text>')
    for d, dn in enumerate(DOMAINS):
        x = lx + d * (bw + 8)
        on = dn in b["cols"]
        fill = b["accent"] if on else "#f4f7f8"
        txt = "#ffffff" if on else "#7c8c97"
        o.append(f'<rect x="{x}" y="{ly}" width="{bw}" height="{bh}" rx="5" fill="{fill}" '
                 f'stroke="{b["accent"] if on else "#c7d0d6"}" stroke-width="{2 if on else 1}"/>')
        o.append(f'<text x="{x + bw/2:.0f}" y="{ly + 22}" text-anchor="middle" {SANS} '
                 f'font-size="12" font-weight="{700 if on else 400}" fill="{txt}">{esc(dn)}</text>')
        if d < ND - 1:
            o.append(f'<text x="{x + bw + 4:.0f}" y="{ly + 22}" text-anchor="middle" {SANS} '
                     f'font-size="12" fill="#c7d0d6">›</text>')

    # the worksheet grid: layers down, zones across, blank cells to write in
    gx, gy, cw, ch = 44, 238, 160, 82
    o.append(f'<text x="{gx}" y="{gy - 14}" {SANS} font-size="10.5" font-weight="600" '
             f'fill="#7c8c97" letter-spacing="1.4">ZONES →</text>')
    for z, zn in enumerate(ZONES_UP):
        x = gx + 150 + z * cw
        o.append(f'<text x="{x + cw/2:.0f}" y="{gy + 14}" text-anchor="middle" {SANS} '
                 f'font-size="10.5" font-weight="600" fill="#14212a">{esc(zn)}</text>')
    for li, (code, name) in enumerate(LAYERS):          # Business at the top, as printed
        y = gy + 30 + li * ch
        st, fl, _ = SKIN[code]
        o.append(f'<rect x="{gx}" y="{y}" width="146" height="{ch - 6}" rx="4" fill="{fl}" '
                 f'fill-opacity=".45" stroke="{st}" stroke-width="1"/>')
        o.append(f'<text x="{gx + 12}" y="{y + 30}" {SANS} font-size="13" font-weight="700" '
                 f'fill="#14212a">{esc(name)}</text>')
        o.append(f'<text x="{gx + 12}" y="{y + 48}" {SANS} font-size="10" fill="#5f7078">'
                 f'{esc(code)} Layer</text>')
        for z in range(NZ):
            x = gx + 150 + z * cw
            o.append(f'<rect x="{x}" y="{y}" width="{cw - 6}" height="{ch - 6}" rx="4" '
                     f'fill="#ffffff" stroke="#c7d0d6" stroke-width="1"/>')
    o.append(f'<text x="{gx}" y="{gy + 30 + NL*ch + 22}" {SANS} font-size="11" fill="#7c8c97">'
             f'Write the value, actor and asset for this domain into each cell. '
             f'A cell left empty is a gap, not a mistake.</text>')
    o.append("</svg>")
    return "\n".join(o)


(OUT / "sfam-figure-4-4.svg").write_text(figure(), encoding="utf-8")
print(f"  sfam-figure-4-4.svg          {len(figure()):>6} bytes")
for b in BIZ:
    p = OUT / f"sfam-domain-{b['n']}.svg"
    p.write_text(worksheet(b), encoding="utf-8")
    print(f"  sfam-domain-{b['n']}.svg   {p.stat().st_size:>6} bytes  {b['title']} — {b['sub']}")
print(f"\naxes taken from the model: {ND} domains x {NZ} zones x {NL} layers = {SF['cubes']} cubes")
