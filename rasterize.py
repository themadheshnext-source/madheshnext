from playwright.sync_api import sync_playwright
import os
L = os.path.abspath("assets/logo")
jobs = [
    # (svg, out, width, height, bg)
    ("madheshnext-logo.svg", "madheshnext-logo.png", 800, None, "transparent"),
    ("madheshnext-logo-reversed.svg", "madheshnext-logo-reversed.png", 800, None, "transparent"),
    ("madheshnext-logo-bilingual.svg", "madheshnext-logo-bilingual.png", 800, None, "transparent"),
    ("madheshnext-mark.svg", "apple-touch-icon.png", 180, 180, "#121212"),
    ("madheshnext-mark.svg", "favicon-32.png", 32, 32, "#121212"),
    ("madheshnext-mark.svg", "favicon-16.png", 16, 16, "#121212"),
]
with sync_playwright() as p:
    b = p.chromium.launch()
    for svg, out, w, h, bg in jobs:
        src = open(os.path.join(L, svg), encoding="utf-8").read()
        # native aspect
        import re
        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', src)
        vw, vh = float(vb.group(1)), float(vb.group(2))
        H = h or round(w * vh / vw)
        pg = b.new_page(viewport={"width": w, "height": H}, device_scale_factor=1)
        pg.set_content(f'<body style="margin:0;background:{bg}">'
                       f'<img src="data:image/svg+xml;utf8,{src.replace("#","%23")}" '
                       f'style="width:{w}px;height:{H}px;display:block">')
        pg.wait_for_timeout(250)
        pg.screenshot(path=os.path.join(L, out), omit_background=(bg == "transparent"))
        pg.close()
        print("  ", out, f"{w}x{H}")
    # OG image 1200x630, NYT-style
    og = open(os.path.join(L, "madheshnext-lockup.svg"), encoding="utf-8").read().replace("#", "%23")
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(f'''<body style="margin:0;background:#fff;font-family:Georgia,serif">
      <div style="padding:70px 80px;height:630px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between">
        <img src="data:image/svg+xml;utf8,{og}" style="height:190px;width:auto">
        <div>
          <div style="border-top:3px solid #121212;padding-top:22px;font-size:40px;line-height:1.25;color:#121212;max-width:20ch">The conversation Madhesh must have now is about its economy.</div>
          <div style="margin-top:24px;font-family:-apple-system,Helvetica,sans-serif;font-size:15px;letter-spacing:.13em;text-transform:uppercase;color:#666">8 Districts · 136 Local Governments · madheshnext.org</div>
        </div>
      </div></body>''')
    pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(L, "og-image.png"))
    print("   og-image.png 1200x630")
    b.close()
