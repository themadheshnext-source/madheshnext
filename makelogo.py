# -*- coding: utf-8 -*-
"""Generate the Madhesh Next logo suite as SVG (text converted to outlines).

Structure mirrors the Saptari Next mark: a stacked two-line grotesque wordmark
with negative leading and the second line indented under the first.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "logo")
os.makedirs(OUT, exist_ok=True)

INTER = os.path.join(ROOT, "node_modules/@fontsource/inter/files/inter-latin-800-normal.woff")
DEVA = os.path.join(ROOT, "node_modules/@fontsource/noto-sans-devanagari/files/noto-sans-devanagari-devanagari-700-normal.woff")


class Typeset:
    def __init__(self, path):
        self.f = TTFont(path)
        self.upm = self.f["head"].unitsPerEm
        self.gs = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.hmtx = self.f["hmtx"]
        try:
            self.kern = self.f["kern"].kernTables[0].kernTable
        except Exception:
            self.kern = {}

    def gname(self, ch):
        return self.cmap.get(ord(ch))

    def path(self, text, size, x=0, y=0, tracking=0.0):
        """Return (svg_path_d, advance_width). y is the baseline. tracking in em."""
        scale = size / self.upm
        d = []
        pen_x = 0.0
        prev = None
        for ch in text:
            g = self.gname(ch)
            if g is None:
                continue
            if prev is not None:
                pen_x += self.kern.get((prev, g), 0)
            # y flips: font units go up, SVG goes down
            tr = Transform(scale, 0, 0, -scale, x + pen_x * scale, y)
            pen = SVGPathPen(self.gs)
            self.gs[g].draw(TransformPen(pen, tr))
            seg = pen.getCommands()
            if seg:
                d.append(seg)
            pen_x += self.hmtx[g][0] + tracking * self.upm
            prev = g
        return " ".join(d), pen_x * scale

    def width(self, text, size, tracking=0.0):
        return self.path(text, size, tracking=tracking)[1]


inter = Typeset(INTER)
deva = Typeset(DEVA)

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" '
       'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{label}">'
       '<title>{label}</title>{body}</svg>')


def write(name, w, h, body, label="Madhesh Next"):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(SVG.format(w=w, h=h, body=body, label=label))
    return name


# ---------------------------------------------------------------- 1. stacked
def stacked(color="#121212", name="madheshnext-logo.svg", pad=0.0):
    """Two lines, negative leading, line 2 right-aligned to line 1."""
    S = 100.0                 # cap size
    TRACK = -0.022            # tight, like the Saptari mark
    LEAD = 0.78 * S           # negative leading — lines nearly touch

    w1 = inter.width("Madhesh", S, TRACK)
    w2 = inter.width("Next", S, TRACK)
    width = max(w1, w2)

    asc = 0.73 * S            # cap height above baseline
    desc = 0.21 * S           # descender of 'h'/'x' below

    y1 = asc
    y2 = asc + LEAD
    h = y2 + desc

    d1, _ = inter.path("Madhesh", S, x=0, y=y1, tracking=TRACK)
    d2, _ = inter.path("Next", S, x=width - w2, y=y2, tracking=TRACK)

    body = '<g fill="%s"><path d="%s"/><path d="%s"/></g>' % (color, d1, d2)
    return write(name, width + pad * 2, h + pad * 2,
                 '<g transform="translate(%.1f,%.1f)">%s</g>' % (pad, pad, body))


# ------------------------------------------------------------- 2. horizontal
def horizontal(color="#121212", name="madheshnext-logo-horizontal.svg"):
    S = 100.0
    TRACK = -0.022
    gap = 0.24 * S
    d1, w1 = inter.path("Madhesh", S, x=0, y=0.73 * S, tracking=TRACK)
    d2, w2 = inter.path("Next", S, x=w1 + gap, y=0.73 * S, tracking=TRACK)
    width = w1 + gap + w2
    body = '<g fill="%s"><path d="%s"/><path d="%s"/></g>' % (color, d1, d2)
    return write(name, width, 0.73 * S + 0.21 * S, body)


# --------------------------------------------------------------- 3. bilingual
def bilingual(color="#121212", name="madheshnext-logo-bilingual.svg"):
    """Stacked English mark with the Nepali name set beneath a hairline rule."""
    S = 100.0
    TRACK = -0.022
    LEAD = 0.78 * S
    w1 = inter.width("Madhesh", S, TRACK)
    w2 = inter.width("Next", S, TRACK)
    width = max(w1, w2)
    asc, desc = 0.73 * S, 0.21 * S
    y1, y2 = asc, asc + LEAD

    d1, _ = inter.path("Madhesh", S, x=0, y=y1, tracking=TRACK)
    d2, _ = inter.path("Next", S, x=width - w2, y=y2, tracking=TRACK)

    rule_y = y2 + desc + 0.20 * S
    ns = 0.30 * S
    dn, wn = deva.path("मधेश नेक्स्ट", ns, x=0, y=rule_y + 0.42 * S)
    h = rule_y + 0.60 * S

    body = ('<g fill="{c}"><path d="{d1}"/><path d="{d2}"/>'
            '<rect x="0" y="{ry:.1f}" width="{w:.1f}" height="2"/>'
            '<path d="{dn}"/></g>').format(c=color, d1=d1, d2=d2, ry=rule_y, w=width, dn=dn)
    return write(name, width, h, body)


# ------------------------------------------------------------------ 4. mark
def mark(fg="#ffffff", bg="#121212", name="madheshnext-mark.svg"):
    """Square monogram: MN stacked inside a solid block. For avatars/favicons."""
    BOX = 100.0
    S = 46.0
    TRACK = -0.03
    wm = inter.width("M", S, TRACK)
    wn = inter.width("N", S, TRACK)
    width = max(wm, wn)
    lead = 0.98 * S
    top = (BOX - (0.73 * S + lead)) / 2 + 0.73 * S
    x0 = (BOX - width) / 2
    dm, _ = inter.path("M", S, x=x0, y=top, tracking=TRACK)
    dn, _ = inter.path("N", S, x=x0 + (width - wn), y=top + lead, tracking=TRACK)
    body = ('<rect width="100" height="100" fill="%s"/>'
            '<g fill="%s"><path d="%s"/><path d="%s"/></g>' % (bg, fg, dm, dn))
    return write(name, BOX, BOX, body)


def favicon(name="favicon.svg"):
    return mark(fg="#ffffff", bg="#121212", name=name)


# --------------------------------------------------------------- 5. lockups
def lockup_rule(color="#121212", name="madheshnext-lockup.svg"):
    """Wordmark with the campaign years under a hairline — masthead lockup."""
    S = 100.0
    TRACK = -0.022
    LEAD = 0.78 * S
    w1 = inter.width("Madhesh", S, TRACK)
    w2 = inter.width("Next", S, TRACK)
    width = max(w1, w2)
    asc, desc = 0.73 * S, 0.21 * S
    d1, _ = inter.path("Madhesh", S, x=0, y=asc, tracking=TRACK)
    d2, _ = inter.path("Next", S, x=width - w2, y=asc + LEAD, tracking=TRACK)
    rule_y = asc + LEAD + desc + 0.18 * S
    ys = 0.155 * S
    dy, wy = inter.path("MADHESH 2030 · 2040 · 2050", ys, x=0, y=rule_y + 0.34 * S, tracking=0.14)
    h = rule_y + 0.50 * S
    body = ('<g fill="{c}"><path d="{d1}"/><path d="{d2}"/>'
            '<rect x="0" y="{ry:.1f}" width="{w:.1f}" height="2"/>'
            '<path d="{dy}"/></g>').format(c=color, d1=d1, d2=d2, ry=rule_y,
                                           w=max(width, wy), dy=dy)
    return write(name, max(width, wy), h, body)


if __name__ == "__main__":
    made = [
        stacked("#121212", "madheshnext-logo.svg"),
        stacked("#ffffff", "madheshnext-logo-reversed.svg"),
        horizontal("#121212"),
        bilingual("#121212"),
        lockup_rule("#121212"),
        mark("#ffffff", "#121212", "madheshnext-mark.svg"),
        mark("#121212", "#ffffff", "madheshnext-mark-light.svg"),
        favicon(),
    ]
    for m in made:
        print("  ", m)
