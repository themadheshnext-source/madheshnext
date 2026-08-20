# -*- coding: utf-8 -*-
"""Rasterise the logo SVGs to PNG / favicon / OG-image. Run after makelogo.py."""
import os, re
from playwright.sync_api import sync_playwright

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo")
NAVY = "#1B3160"

JOBS = [
    ("madheshnext-logo.svg",           "madheshnext-logo.png",          1200, None, "transparent"),
    ("madheshnext-logo-reversed.svg",  "madheshnext-logo-reversed.png", 1200, None, "transparent"),
    ("madheshnext-logo-stacked.svg",   "madheshnext-logo-stacked.png",   800, None, "transparent"),
    ("madheshnext-logo-bilingual.svg", "madheshnext-logo-bilingual.png", 900, None, "transparent"),
    ("madheshnext-mark.svg",           "apple-touch-icon.png",           180,  180, NAVY),
    ("madheshnext-mark.svg",           "favicon-32.png",                  32,   32, NAVY),
    ("madheshnext-mark.svg",           "favicon-16.png",                  16,   16, NAVY),
]


def run():
    with sync_playwright() as p:
        b = p.chromium.launch()
        for svg, out, w, h, bg in JOBS:
            src = open(os.path.join(L, svg), encoding="utf-8").read()
            vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', src)
            vw, vh = float(vb.group(1)), float(vb.group(2))
            H = h or max(1, round(w * vh / vw))
            pg = b.new_page(viewport={"width": w, "height": H}, device_scale_factor=2)
            data = src.replace("#", "%23").replace('"', "'")
            pg.set_content("<body style='margin:0;background:%s'>"
                           "<img src=\"data:image/svg+xml;utf8,%s\" "
                           "style='width:%dpx;height:%dpx;display:block'>" % (bg, data, w, H))
            pg.wait_for_timeout(250)
            pg.screenshot(path=os.path.join(L, out),
                          omit_background=(bg == "transparent"))
            pg.close()
            print("  ", out, "%dx%d" % (w, H))

        # Open Graph card, 1200x630
        logo = open(os.path.join(L, "madheshnext-logo.svg"), encoding="utf-8").read()
        logo = logo.replace("#", "%23").replace('"', "'")
        pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        pg.set_content("""<body style="margin:0;background:#fff;font-family:Georgia,serif">
  <div style="padding:64px 76px;height:630px;box-sizing:border-box;display:flex;
              flex-direction:column;justify-content:space-between">
    <img src="data:image/svg+xml;utf8,%s" style="width:520px">
    <div>
      <div style="border-top:3px solid %s;padding-top:22px;font-size:41px;line-height:1.24;
                  color:#121212;max-width:20ch">The conversation Madhesh must have now is
                  about its economy.</div>
      <div style="margin-top:22px;font-family:-apple-system,Helvetica,sans-serif;font-size:15px;
                  letter-spacing:.13em;text-transform:uppercase;color:#666">8 Districts &middot;
                  136 Local Governments &middot; madheshnext.org</div>
    </div>
  </div></body>""" % (logo, NAVY))
        pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(L, "og-image.png"))
        print("   og-image.png 1200x630")
        b.close()


if __name__ == "__main__":
    run()
