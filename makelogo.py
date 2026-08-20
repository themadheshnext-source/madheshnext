# -*- coding: utf-8 -*-
"""Madhesh Next logo suite.

A single-line wordmark set in Inter ExtraBold, navy, with the "x" of "Next"
split into two diagonal bars — the rising bar in teal, forming the chevron.

All type is converted to outlines, so the SVGs render identically everywhere
with no font to install. The teal bar is produced by clipping a rotated band
to the actual "x" glyph outline, so it follows the letterform exactly rather
than being drawn by hand.

Run:  python3 makelogo.py
"""
import math
import os

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "logo")
os.makedirs(OUT, exist_ok=True)

INTER = os.path.join(ROOT, "node_modules/@fontsource/inter/files/inter-latin-800-normal.woff")
DEVA = os.path.join(ROOT, "node_modules/@fontsource/noto-sans-devanagari/files/"
                          "noto-sans-devanagari-devanagari-700-normal.woff")

# ---------------------------------------------------------------- brand colour
NAVY = "#1B3160"     # wordmark
TEAL = "#14A79E"     # the chevron bar in the x
WHITE = "#ffffff"
INK = "#121212"      # newsprint single-colour variant


class Typeset:
    """Minimal typesetter that returns SVG path data and glyph positions."""

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
        os2 = self.f["OS/2"]
        self.cap = getattr(os2, "sCapHeight", int(0.727 * self.upm)) / self.upm
        self.xh = getattr(os2, "sxHeight", int(0.546 * self.upm)) / self.upm

    def _name(self, ch):
        return self.cmap.get(ord(ch))

    def layout(self, text, size, x=0.0, y=0.0, tracking=0.0):
        """Return (list of glyph dicts, total advance).

        Each glyph dict: {char, d (svg path), x0, adv, xmin, xmax}
        """
        scale = size / self.upm
        pen_x = 0.0
        prev = None
        out = []
        for ch in text:
            g = self._name(ch)
            if g is None:
                continue
            if prev is not None:
                pen_x += self.kern.get((prev, g), 0)
            gx = x + pen_x * scale
            tr = Transform(scale, 0, 0, -scale, gx, y)
            pen = SVGPathPen(self.gs)
            self.gs[g].draw(TransformPen(pen, tr))
            adv = self.hmtx[g][0] * scale
            # tight bounds of this glyph in user units
            try:
                gl = self.f["glyf"][g] if "glyf" in self.f else None
                if gl is not None and gl.numberOfContours:
                    xmin = gx + gl.xMin * scale
                    xmax = gx + gl.xMax * scale
                else:
                    xmin, xmax = gx, gx + adv
            except Exception:
                xmin, xmax = gx, gx + adv
            out.append({"char": ch, "d": pen.getCommands(), "x0": gx,
                        "adv": adv, "xmin": xmin, "xmax": xmax})
            pen_x += self.hmtx[g][0] + tracking * self.upm
            prev = g
        return out, pen_x * scale

    def path(self, text, size, x=0.0, y=0.0, tracking=0.0):
        glyphs, adv = self.layout(text, size, x, y, tracking)
        return " ".join(g["d"] for g in glyphs if g["d"]), adv

    def width(self, text, size, tracking=0.0):
        return self.path(text, size, tracking=tracking)[1]


inter = Typeset(INTER)
deva = Typeset(DEVA)

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
       'width="{w:.0f}" height="{h:.0f}" fill="none" role="img" aria-label="{label}">'
       '<title>{label}</title>{defs}{body}</svg>')


def write(name, w, h, body, defs="", label="Madhesh Next"):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(SVG.format(w=w, h=h, body=body, defs=defs, label=label))
    return name


def _band(xa, ya, xb, yb, half, extend):
    """Polygon points for a thick band along the segment (xa,ya)-(xb,yb)."""
    dx, dy = xb - xa, yb - ya
    ln = math.hypot(dx, dy) or 1.0
    ux, uy = dx / ln, dy / ln          # along
    px, py = -uy, ux                   # perpendicular
    ax, ay = xa - ux * extend, ya - uy * extend
    bx, by = xb + ux * extend, yb + uy * extend
    pts = [(ax + px * half, ay + py * half), (bx + px * half, by + py * half),
           (bx - px * half, by - py * half), (ax - px * half, ay - py * half)]
    return " ".join("%.2f,%.2f" % p for p in pts)


def wordmark(text_colour=NAVY, accent=TEAL, name="madheshnext-logo.svg",
             size=100.0, tracking=-0.012, rising=True, uid="x"):
    """Single-line 'Madhesh Next' with a two-tone x.

    rising=True  -> the bottom-left→top-right bar is the accent colour.
    rising=False -> the top-left→bottom-right bar is the accent colour.
    """
    S = size
    asc = inter.cap * S            # cap height above baseline
    desc = 0.06 * S                # tiny optical margin (no descenders in mark)
    baseline = asc

    glyphs, total = inter.layout("Madhesh Next", S, x=0.0, y=baseline,
                                 tracking=tracking)

    # the "x" is the second-to-last glyph of "Next"
    xg = None
    for g in reversed(glyphs):
        if g["char"] == "x":
            xg = g
            break

    navy_d = " ".join(g["d"] for g in glyphs if g["d"])

    defs = ""
    accent_shape = ""
    if xg is not None and accent:
        xtop = baseline - inter.xh * S
        xbot = baseline
        xa, xb = xg["xmin"], xg["xmax"]
        if rising:
            p1, p2 = (xa, xbot), (xb, xtop)
        else:
            p1, p2 = (xa, xtop), (xb, xbot)
        half = 0.115 * S
        pts = _band(p1[0], p1[1], p2[0], p2[1], half, extend=0.25 * S)
        defs = ('<defs><clipPath id="mnx-%s"><path d="%s"/></clipPath></defs>'
                % (uid, xg["d"]))
        accent_shape = ('<g clip-path="url(#mnx-%s)">'
                        '<polygon points="%s" fill="%s"/></g>' % (uid, pts, accent))

    body = ('<path d="%s" fill="%s"/>%s' % (navy_d, text_colour, accent_shape))
    return write(name, total, asc + desc, body, defs=defs)


def stacked(text_colour=NAVY, accent=TEAL, name="madheshnext-logo-stacked.svg",
            size=100.0, tracking=-0.012, uid="s"):
    """Two-line lockup: Madhesh / Next, left aligned, two-tone x."""
    S = size
    asc = inter.cap * S
    lead = 1.02 * S
    g1, w1 = inter.layout("Madhesh", S, x=0.0, y=asc, tracking=tracking)
    g2, w2 = inter.layout("Next", S, x=0.0, y=asc + lead, tracking=tracking)
    width = max(w1, w2)

    xg = next((g for g in g2 if g["char"] == "x"), None)
    d = " ".join(g["d"] for g in (g1 + g2) if g["d"])

    defs = accent_shape = ""
    if xg is not None:
        base = asc + lead
        pts = _band(xg["xmin"], base, xg["xmax"], base - inter.xh * S,
                    0.115 * S, extend=0.25 * S)
        defs = ('<defs><clipPath id="mnx-%s"><path d="%s"/></clipPath></defs>'
                % (uid, xg["d"]))
        accent_shape = ('<g clip-path="url(#mnx-%s)"><polygon points="%s" fill="%s"/></g>'
                        % (uid, pts, accent))

    body = '<path d="%s" fill="%s"/>%s' % (d, text_colour, accent_shape)
    return write(name, width, asc + lead + 0.06 * S, body, defs=defs)


def bilingual(name="madheshnext-logo-bilingual.svg", size=100.0, uid="b"):
    """Wordmark with मधेश नेक्स्ट set beneath a hairline."""
    S = size
    tracking = -0.012
    asc = inter.cap * S
    glyphs, total = inter.layout("Madhesh Next", S, x=0.0, y=asc, tracking=tracking)
    xg = next((g for g in reversed(glyphs) if g["char"] == "x"), None)
    d = " ".join(g["d"] for g in glyphs if g["d"])

    rule_y = asc + 0.22 * S
    ns = 0.285 * S
    dn, _ = deva.path("मधेश नेक्स्ट", ns, x=0.0, y=rule_y + 0.40 * S)
    h = rule_y + 0.58 * S

    defs = accent_shape = ""
    if xg is not None:
        pts = _band(xg["xmin"], asc, xg["xmax"], asc - inter.xh * S,
                    0.115 * S, extend=0.25 * S)
        defs = ('<defs><clipPath id="mnx-%s"><path d="%s"/></clipPath></defs>'
                % (uid, xg["d"]))
        accent_shape = ('<g clip-path="url(#mnx-%s)"><polygon points="%s" fill="%s"/></g>'
                        % (uid, pts, TEAL))

    body = ('<path d="%s" fill="%s"/>%s'
            '<rect x="0" y="%.2f" width="%.2f" height="2" fill="%s"/>'
            '<path d="%s" fill="%s"/>'
            % (d, NAVY, accent_shape, rule_y, total, NAVY, dn, NAVY))
    return write(name, total, h, body, defs=defs)


def mark(name="madheshnext-mark.svg", bg=NAVY, bar=WHITE, accent=TEAL,
         size=100.0, uid="m"):
    """Square app mark: the two-tone X, centred in a solid tile."""
    BOX = 100.0
    S = size * 1.30
    glyphs, adv = inter.layout("x", S, x=0.0, y=0.0)
    g = glyphs[0]
    gw = g["xmax"] - g["xmin"]
    gh = inter.xh * S
    # centre the glyph in the box
    ox = (BOX - gw) / 2 - g["xmin"]
    oy = (BOX + gh) / 2
    glyphs, _ = inter.layout("x", S, x=ox, y=oy)
    g = glyphs[0]

    pts = _band(g["xmin"], oy, g["xmax"], oy - gh, 0.115 * S, extend=0.3 * S)
    defs = ('<defs><clipPath id="mnx-%s"><path d="%s"/></clipPath></defs>'
            % (uid, g["d"]))
    body = ('<rect width="100" height="100" fill="%s"/>'
            '<path d="%s" fill="%s"/>'
            '<g clip-path="url(#mnx-%s)"><polygon points="%s" fill="%s"/></g>'
            % (bg, g["d"], bar, uid, pts, accent))
    return write(name, BOX, BOX, body, defs=defs)


if __name__ == "__main__":
    made = [
        # primary — navy wordmark, teal rising bar
        wordmark(NAVY, TEAL, "madheshnext-logo.svg", uid="p"),
        # reversed for dark backgrounds
        wordmark(WHITE, TEAL, "madheshnext-logo-reversed.svg", uid="r"),
        # single-colour fallbacks
        wordmark(NAVY, None, "madheshnext-logo-navy-solid.svg", uid="n"),
        wordmark(INK, None, "madheshnext-logo-black.svg", uid="k"),
        wordmark(WHITE, None, "madheshnext-logo-white.svg", uid="w"),
        # alternate x split, for comparison
        wordmark(NAVY, TEAL, "madheshnext-logo-alt.svg", rising=False, uid="a"),
        # lockups
        stacked(NAVY, TEAL, "madheshnext-logo-stacked.svg", uid="s"),
        stacked(WHITE, TEAL, "madheshnext-logo-stacked-reversed.svg", uid="sr"),
        bilingual(),
        # marks
        mark("madheshnext-mark.svg", bg=NAVY, bar=WHITE, accent=TEAL, uid="m1"),
        mark("favicon.svg", bg=NAVY, bar=WHITE, accent=TEAL, uid="m2"),
        mark("madheshnext-mark-light.svg", bg="#ffffff", bar=NAVY, accent=TEAL, uid="m3"),
    ]
    for m in made:
        print("  ", m)
