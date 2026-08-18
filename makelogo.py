# -*- coding: utf-8 -*-
"""Regenerate the whole Madhesh Next logo suite into assets/logo/.

The mark: "Madhesh Next" in Poppins SemiBold, converted to outlines, navy #0A2C5A,
with the LEFT half of the x in "Next" filled teal #009B95 — the forward chevron.
Tagline: "Moving Forward", Poppins Medium, teal, letterspaced, right-aligned.

You almost never need to run this. Everything in assets/logo/ is final and committed.
Run it only to change the wording, the colours or the tagline:

    pip install uharfbuzz fonttools cairosvg
    mkdir -p /tmp/fonts && cd /tmp/fonts
    B=https://raw.githubusercontent.com/google/fonts/main/ofl
    curl -LO $B/poppins/Poppins-SemiBold.ttf
    curl -LO $B/poppins/Poppins-Medium.ttf
    curl -L -o NotoSansDevanagari.ttf \
      "$B/notosansdevanagari/NotoSansDevanagari%5Bwdth%2Cwght%5D.ttf"
    python3 makelogo.py

Then commit whatever changed in assets/logo/.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo")
os.makedirs(OUT, exist_ok=True)

import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

NAVY = "#0A2C5A"
TEAL = "#009B95"
WHITE = "#FFFFFF"

FONTS = {
    "poppins": "/tmp/fonts/Poppins-SemiBold.ttf",
    "poppins_med": "/tmp/fonts/Poppins-Medium.ttf",
    "deva": "/tmp/fonts/NotoSansDevanagari.ttf",
}
_cache = {}


def _load(key):
    if key not in _cache:
        path = FONTS[key]
        with open(path, "rb") as fh:
            data = fh.read()
        face = hb.Face(data)
        font = hb.Font(face)
        tt = TTFont(path)
        _cache[key] = (font, tt, face.upem)
    return _cache[key]


def shape(text, key="poppins", size=1000, tracking=0, variations=None):
    """Return (glyph_runs, advance_width) in `size` units. Origin at baseline left."""
    font, tt, upem = _load(key)
    if variations:
        font.set_variations(variations)
    font.scale = (upem, upem)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf)
    glyph_set = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    scale = size / upem
    runs, x = [], 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        pen = SVGPathPen(glyph_set)
        glyph_set[name].draw(pen)
        d = pen.getCommands()
        gx = (x + pos.x_offset) * scale
        gy = pos.y_offset * scale
        if d:
            runs.append({"d": d, "x": gx, "y": gy, "scale": scale, "name": name,
                         "adv": pos.x_advance * scale, "cluster": info.cluster})
        x += pos.x_advance + tracking / scale
    return runs, x * scale


def path_el(run, fill, clip=None, extra=""):
    tr = "translate(%.2f %.2f) scale(%.5f -%.5f)" % (run["x"], run["y"], run["scale"], run["scale"])
    c = ' clip-path="url(#%s)"' % clip if clip else ""
    return '<path transform="%s" d="%s" fill="%s"%s%s/>' % (tr, run["d"], fill, c, extra)


def wordmark(size=1000, tracking=-10, text_fill=NAVY, uid="a"):
    """Return (svg_body, width, defs) for 'Madhesh Next' with the split teal x."""
    runs, width = shape("Madhesh Next", size=size, tracking=tracking)
    # locate the final 'x' glyph (the one in "Next": index of 'x' in the string)
    xi = "Madhesh Next".index("x")
    parts, defs = [], []
    for i, r in enumerate(runs):
        if r.get("cluster") == xi:
            # crossing point = horizontal middle of the glyph ink box
            gx0 = r["x"]
            gw = r["adv"]
            mid = gx0 + gw / 2.0
            top, bot = -size * 1.2, size * 1.2
            defs.append('<clipPath id="xl%s"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/></clipPath>'
                        % (uid, gx0 - size, top, size + (mid - gx0), bot - top))
            defs.append('<clipPath id="xr%s"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/></clipPath>'
                        % (uid, mid, top, size * 2, bot - top))
            parts.append('<g clip-path="url(#xl%s)">%s</g>' % (uid, path_el(r, TEAL)))
            parts.append('<g clip-path="url(#xr%s)">%s</g>' % (uid, path_el(r, text_fill)))
        else:
            parts.append(path_el(r, text_fill))
    return "\n  ".join(parts), width, "\n  ".join(defs)


def svg(width, height, body, defs="", pad=0, bg=None):
    d = "<defs>%s</defs>" % defs if defs else ""
    b = '<rect width="%.2f" height="%.2f" fill="%s"/>' % (width, height, bg) if bg else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" '
            'width="%.2f" height="%.2f" role="img" aria-label="Madhesh Next">\n'
            '%s%s\n  %s\n</svg>\n' % (width, height, width, height, d, b, body))


from fontTools.pens.boundsPen import BoundsPen


def ink_bbox(runs, key="poppins"):
    font, tt, upem = _load(key)
    gs = tt.getGlyphSet()
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for r in runs:
        bp = BoundsPen(gs)
        gs[r["name"]].draw(bp)
        if bp.bounds is None:
            continue
        a, b, c, d = bp.bounds
        s = r["scale"]
        x0 = min(x0, r["x"] + a * s); x1 = max(x1, r["x"] + c * s)
        y0 = min(y0, r["y"] - d * s); y1 = max(y1, r["y"] - b * s)
    return x0, y0, x1, y1


# ============================ asset build =============================

S = 1000
TRACK = -12
TAGLINE = "Moving Forward"
TAGLINE_NE = "अगाडि बढ्दै"


def build_wordmark(fill, uid, pad_ratio=0.10):
    runs, adv = shape("Madhesh Next", size=S, tracking=TRACK)
    x0, y0, x1, y1 = ink_bbox(runs)
    body, _, defs = wordmark(size=S, tracking=TRACK, text_fill=fill, uid=uid)
    pad = S * pad_ratio
    w = (x1 - x0) + 2 * pad
    h = (y1 - y0) + 2 * pad
    shift = "translate(%.2f %.2f)" % (pad - x0, pad - y0)
    return '<g transform="%s">\n  %s\n  </g>' % (shift, body), w, h, defs, (x0, y0, x1, y1)


def write(name, txt):
    p = os.path.join(OUT, name)
    with open(p, "w") as fh:
        fh.write(txt)
    print(name, len(txt))


# ---------- 1. primary wordmark ----------
body, w, h, defs, bb = build_wordmark(NAVY, "p")
write("madheshnext-logo.svg", svg(w, h, body, defs))

# ---------- 2. reversed (white on dark) ----------
body, w, h, defs, bb = build_wordmark(WHITE, "r")
write("madheshnext-logo-reversed.svg", svg(w, h, body, defs))

# ---------- 3. horizontal = wordmark + rule + tagline ----------
def with_tagline(fill, tag_fill, uid, tagline=TAGLINE):
    runs, _ = shape("Madhesh Next", size=S, tracking=TRACK)
    x0, y0, x1, y1 = ink_bbox(runs)
    body, _, defs = wordmark(size=S, tracking=TRACK, text_fill=fill, uid=uid)
    tsize = S * 0.235
    truns, tadv = shape(tagline, key="poppins_med", size=tsize, tracking=tsize * 0.42)
    tx0, ty0, tx1, ty1 = ink_bbox(truns, "poppins_med")
    pad = S * 0.10
    gap = S * 0.20
    wm_w = x1 - x0
    wm_h = y1 - y0
    tag_h = ty1 - ty0
    w = wm_w + 2 * pad
    h = wm_h + gap + tag_h + 2 * pad
    tag_body = "\n    ".join(path_el(r, tag_fill) for r in truns)
    # right-align tagline under the wordmark
    tag_shift = pad + wm_w - (tx1 - tx0)
    out = ('<g transform="translate(%.2f %.2f)">\n  %s\n  </g>\n'
           '  <g transform="translate(%.2f %.2f)">\n    %s\n  </g>'
           % (pad - x0, pad - y0, body,
              tag_shift - tx0, pad + wm_h + gap - ty0, tag_body))
    return out, w, h, defs


body, w, h, defs = with_tagline(NAVY, TEAL, "h")
write("madheshnext-logo-horizontal.svg", svg(w, h, body, defs))

body, w, h, defs = with_tagline(WHITE, TEAL, "hr")
write("madheshnext-logo-tagline-reversed.svg", svg(w, h, body, defs))

# ---------- 4. bilingual: wordmark + rule + मधेश नेक्स्ट ----------
def bilingual(fill, uid):
    runs, _ = shape("Madhesh Next", size=S, tracking=TRACK)
    x0, y0, x1, y1 = ink_bbox(runs)
    body, _, defs = wordmark(size=S, tracking=TRACK, text_fill=fill, uid=uid)
    nsize = S * 0.46
    nruns, _ = shape("मधेश नेक्स्ट", key="deva", size=nsize,
                       variations={"wght": 600})
    nx0, ny0, nx1, ny1 = ink_bbox(nruns, "deva")
    pad = S * 0.10
    gap = S * 0.16
    rule_gap = S * 0.14
    wm_w, wm_h = x1 - x0, y1 - y0
    ne_h = ny1 - ny0
    w = wm_w + 2 * pad
    h = wm_h + gap + rule_gap + ne_h + 2 * pad
    ne_body = "\n    ".join(path_el(r, fill) for r in nruns)
    rule_y = pad + wm_h + gap
    out = ('<g transform="translate(%.2f %.2f)">\n  %s\n  </g>\n'
           '  <rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>\n'
           '  <g transform="translate(%.2f %.2f)">\n    %s\n  </g>'
           % (pad - x0, pad - y0, body,
              pad, rule_y, wm_w, S * 0.035, TEAL,
              pad - nx0, rule_y + rule_gap - ny0, ne_body))
    return out, w, h, defs


body, w, h, defs = bilingual(NAVY, "b")
write("madheshnext-logo-bilingual.svg", svg(w, h, body, defs))

# ---------- 5. lockup: bilingual + tagline + dates ----------
def lockup():
    runs, _ = shape("Madhesh Next", size=S, tracking=TRACK)
    x0, y0, x1, y1 = ink_bbox(runs)
    body, _, defs = wordmark(size=S, tracking=TRACK, text_fill=NAVY, uid="l")
    tsize = S * 0.235
    truns, _ = shape(TAGLINE, key="poppins_med", size=tsize, tracking=tsize * 0.42)
    tx0, ty0, tx1, ty1 = ink_bbox(truns, "poppins_med")
    dsize = S * 0.19
    druns, _ = shape("MADHESH 2030 · 2040 · 2050", key="poppins_med", size=dsize,
                       tracking=dsize * 0.30)
    dx0, dy0, dx1, dy1 = ink_bbox(druns, "poppins_med")
    pad = S * 0.12
    wm_w, wm_h = x1 - x0, y1 - y0
    y = pad + wm_h + S * 0.20
    tag_h = ty1 - ty0
    y2 = y + tag_h + S * 0.16
    h = y2 + S * 0.10 + (dy1 - dy0) + pad
    w = wm_w + 2 * pad
    tag_body = "\n    ".join(path_el(r, TEAL) for r in truns)
    date_body = "\n    ".join(path_el(r, "#5A6B82") for r in druns)
    out = ('<g transform="translate(%.2f %.2f)">\n  %s\n  </g>\n'
           '  <g transform="translate(%.2f %.2f)">\n    %s\n  </g>\n'
           '  <rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>\n'
           '  <g transform="translate(%.2f %.2f)">\n    %s\n  </g>'
           % (pad - x0, pad - y0, body,
              pad + wm_w - (tx1 - tx0) - tx0, y - ty0, tag_body,
              pad, y2 - S * 0.02, wm_w, S * 0.02, "#D8DEE7",
              pad + wm_w - (dx1 - dx0) - dx0, y2 + S * 0.10 - dy0, date_body))
    return out, w, h, defs


body, w, h, defs = lockup()
write("madheshnext-lockup.svg", svg(w, h, body, defs))


# ---------- 6. MN mark ----------
def mark(bg, fill, teal, size=512, rounded=0):
    runs, adv = shape("MN", size=size * 0.52, tracking=-size * 0.012)
    x0, y0, x1, y1 = ink_bbox(runs)
    cx = (size - (x1 - x0)) / 2 - x0
    cy = (size - (y1 - y0)) / 2 - y0
    body = "\n  ".join(path_el(r, fill) for r in runs)
    bar_h = size * 0.075
    parts = ['<rect width="%d" height="%d" fill="%s"/>' % (size, size, bg),
             '<g transform="translate(%.2f %.2f)">%s</g>' % (cx, cy - size * 0.045, body),
             '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>'
             % (size * 0.30, size * 0.755, size * 0.40, bar_h, teal)]
    return svg(size, size, "\n  ".join(parts))


write("madheshnext-mark.svg", mark(NAVY, WHITE, TEAL))
write("madheshnext-mark-light.svg", mark(WHITE, NAVY, TEAL))
write("favicon.svg", mark(NAVY, WHITE, TEAL))


# ============================== rasterise =============================

import cairosvg
def png(src,dst,w=None,h=None,bg=None):
    cairosvg.svg2png(url=os.path.join(OUT,src), write_to=os.path.join(OUT,dst),
                     output_width=w, output_height=h, background_color=bg)
    print(dst, os.path.getsize(os.path.join(OUT,dst)))

png("madheshnext-logo.svg","madheshnext-logo.png",800)
png("madheshnext-logo-reversed.svg","madheshnext-logo-reversed.png",800)
png("madheshnext-logo-bilingual.svg","madheshnext-logo-bilingual.png",800)
png("madheshnext-logo-horizontal.svg","madheshnext-logo-horizontal.png",1200)
png("favicon.svg","favicon-32.png",32,32)
png("favicon.svg","favicon-16.png",16,16)
png("favicon.svg","apple-touch-icon.png",180,180)

# og-image 1200x630, navy field, reversed wordmark + tagline
S=1000; TRACK=-12
runs,_ = shape("Madhesh Next", size=S, tracking=TRACK)
x0,y0,x1,y1 = ink_bbox(runs)
body,_,defs = wordmark(size=S, tracking=TRACK, text_fill=WHITE, uid="og")
tsize=S*0.235
truns,_ = shape("Moving Forward", key="poppins_med", size=tsize, tracking=tsize*0.42)
tx0,ty0,tx1,ty1 = ink_bbox(truns,"poppins_med")
W,H=1200,630
target_w=880.0
sc=target_w/(x1-x0)
wm_h=(y1-y0)*sc
tag_h=(ty1-ty0)*sc
gap=S*0.20*sc
total=wm_h+gap+tag_h
ox=(W-target_w)/2
oy=(H-total)/2 - 18
tag_body="\n    ".join(path_el(r, TEAL) for r in truns)
parts=[
 '<rect width="%d" height="%d" fill="%s"/>'%(W,H,NAVY),
 '<g transform="translate(%.2f %.2f) scale(%.5f)"><g transform="translate(%.2f %.2f)">%s</g></g>'
   %(ox,oy,sc,-x0,-y0,body),
 '<g transform="translate(%.2f %.2f) scale(%.5f)"><g transform="translate(%.2f %.2f)">%s</g></g>'
   %(ox+target_w-(tx1-tx0)*sc, oy+wm_h+gap, sc, -tx0, -ty0, tag_body),
 '<rect x="%.2f" y="%.2f" width="%.2f" height="6" fill="%s"/>'%(ox, H-96, 120, TEAL),
]
svg=svg(W,H,"\n  ".join(parts),defs)
open(os.path.join(OUT,"og-image.svg"),"w").write(svg)
png("og-image.svg","og-image.png",1200,630)
os.remove(os.path.join(OUT,"og-image.svg"))
