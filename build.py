# -*- coding: utf-8 -*-
"""Static site generator for madheshnext.org. Run: python3 build.py"""
import os, shutil
from data import PROVINCE, DISTRICTS, TYPE_LABEL, CONVENERS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")

NAV = [
    ("index.html", "Home", "गृहपृष्ठ"),
    ("manifesto.html", "The Argument", "मूल विमर्श"),
    ("vision.html", "Vision", "दृष्टिकोण"),
    ("modules.html", "Modules", "मोड्युल"),
    ("districts.html", "Districts", "जिल्ला"),
    ("conveners.html", "Conveners", "संयोजक"),
    ("media.html", "Media", "मिडिया"),
    ("join.html", "Join", "सहभागी"),
]


def t(en, ne):
    """Inline bilingual span."""
    return ('<span class="t" data-en="%s" data-ne="%s">%s</span>'
            % (en.replace('"', '&quot;'), ne.replace('"', '&quot;'), en))


def blocks(en_html, ne_html):
    """Block-level bilingual pair."""
    return ('<div data-lang="en" lang="en">%s</div>\n'
            '<div data-lang="ne" lang="ne" hidden>%s</div>' % (en_html, ne_html))


def layout(title_en, title_ne, body, base="", desc_en="", active=""):
    links = "".join(
        '<a href="%s%s">%s</a>' % (base, href, t(en, ne)) for href, en, ne in NAV
    )
    foot_links = "".join(
        '<a href="%s%s">%s</a>' % (base, href, t(en, ne)) for href, en, ne in NAV[1:]
    )
    dist_links = "".join(
        '<a href="%sdistricts/%s.html">%s</a>' % (base, d["slug"], t(d["en"], d["ne"]))
        for d in DISTRICTS
    )
    return """<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Madhesh Next</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} — Madhesh Next">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Madhesh Next">
<meta property="og:image" content="https://madheshnext.org/assets/logo/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{base}assets/logo/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{base}assets/logo/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{base}assets/logo/apple-touch-icon.png">
<link rel="stylesheet" href="{base}assets/style.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <nav class="nav">
      <a class="brand" href="{base}index.html" aria-label="Madhesh Next — home">
        <img class="brand__logo" src="{base}assets/logo/madheshnext-logo.svg" alt="Madhesh Next" width="118" height="34">
      </a>
      <button class="navtoggle" aria-expanded="false" aria-label="Menu">☰</button>
      <div class="nav__links">
        {links}
        <div class="langswitch" role="group" aria-label="Language">
          <button data-set="en" class="is-on">EN</button>
          <button data-set="ne">ने</button>
        </div>
      </div>
    </nav>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img class="footer__logo" src="{base}assets/logo/madheshnext-logo.svg" alt="Madhesh Next" width="152" height="44">
        <p style="max-width:34ch;margin-bottom:14px">{tagline}</p>
        <p style="font-size:.92rem"><a href="mailto:hello@madheshnext.org" style="display:inline">hello@madheshnext.org</a></p>
      </div>
      <div><h4>{h_pages}</h4>{foot_links}</div>
      <div><h4>{h_districts}</h4>{dist_links}</div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Madhesh Next · madheshnext.org</span>
      <span>{nonpartisan}</span>
    </div>
  </div>
</footer>

<script src="{base}assets/site.js"></script>
</body>
</html>
""".format(
        title=title_en, desc=desc_en or "A citizen-led, non-partisan campaign to bring the economy into everyday public conversation in Madhesh.",
        base=base, body="@@BODY@@", links=links, foot_links=foot_links, dist_links=dist_links,
        tagline=t("A citizen-led, non-partisan effort to move public discourse from politics to economy.",
                  "सार्वजनिक विमर्शलाई राजनीतिबाट अर्थतन्त्रतर्फ लैजाने नागरिक नेतृत्वको गैर-दलीय प्रयास।"),
        h_pages=t("Pages", "पृष्ठहरू"), h_districts=t("Districts", "जिल्लाहरू"),
        nonpartisan=t("Non-partisan · Citizen-led", "गैर-दलीय · नागरिक नेतृत्वमा"),
    ).replace("<main>\n@@BODY@@\n</main>", "<main>\n" + body + "\n</main>")


# ----------------------------------------------------------------- components
_DEV = {"0": "\u0966", "1": "\u0967", "2": "\u0968", "3": "\u0969", "4": "\u096a",
        "5": "\u096b", "6": "\u096c", "7": "\u096d", "8": "\u096e", "9": "\u096f"}


def nep(s):
    """Western digits -> Devanagari digits."""
    return "".join(_DEV.get(ch, ch) for ch in str(s))


def stat(n, label_en, label_ne):
    return stat_x(str(n), nep(n), label_en, label_ne)


def stat_x(n_en, n_ne, label_en, label_ne):
    return '<div class="stat"><div class="stat__n">%s</div><div class="stat__l">%s</div></div>' % (
        t(n_en, n_ne), t(label_en, label_ne))


def totals():
    c = {"METRO": 0, "SUB": 0, "MUN": 0, "RM": 0}
    for d in DISTRICTS:
        for _, _, ty in d["lgs"]:
            c[ty] += 1
    return c


def lg_table(rows, show_district=True):
    """rows: list of (district_dict, name_en, name_ne, type)"""
    head = "<tr><th>%s</th>%s<th>%s</th></tr>" % (
        t("Local level", "स्थानीय तह"),
        ("<th>%s</th>" % t("District", "जिल्ला")) if show_district else "",
        t("Type", "प्रकार"),
    )
    body = []
    for d, en, ne, ty in rows:
        lab_en, lab_ne, cls = TYPE_LABEL[ty]
        body.append(
            '<tr data-type="%s" data-district="%s" data-search="%s">'
            '<td><div class="lgname">%s</div><div class="lgne">%s</div></td>'
            '%s'
            '<td><span class="pill %s">%s</span></td>'
            '</tr>' % (
                ty, d["slug"],
                "%s %s %s %s %s" % (en, ne, d["en"], d["ne"], lab_en),
                en, ne,
                ('<td>%s</td>' % t(d["en"], d["ne"])) if show_district else "",
                cls, t(lab_en, lab_ne),
            ))
    return ('<div class="table-scroll"><table class="lgs"><thead>%s</thead>'
            '<tbody>%s</tbody></table></div>' % (head, "".join(body)))


# ----------------------------------------------------------------------- pages
def page_home():
    c = totals()
    hero = """
<section class="hero">
  <div class="wrap">
    <p class="hero__years">{years}</p>
    <h1>{h1}</h1>
    <p class="hero__lede">{lede}</p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="join.html">{cta1}</a>
      <a class="btn btn--ghost" href="manifesto.html">{cta2}</a>
      <a class="btn btn--ghost" href="districts.html">{cta3}</a>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="stats">
      {stats}
    </div>
  </div>
</section>
""".format(
        years=t("Madhesh 2030 · 2040 · 2050", "मधेश २०३० · २०४० · २०५०"),
        h1=t("The conversation Madhesh must have now is about its economy.",
             "मधेशले अब गर्नैपर्ने बहस भनेको उसको अर्थतन्त्रको हो।"),
        lede=t("Madhesh Next is a citizen-led, non-partisan campaign to make economic possibility a subject of everyday public conversation — in all 8 districts and 136 local governments.",
               "मधेश नेक्स्ट एक नागरिक नेतृत्वको गैर-दलीय अभियान हो, जसले आर्थिक सम्भावनालाई दैनिक सार्वजनिक बहसको विषय बनाउँछ — सबै ८ जिल्ला र १३६ स्थानीय तहमा।"),
        cta1=t("Join the campaign", "अभियानमा सहभागी हुनुहोस्"),
        cta2=t("Read the argument", "मूल विमर्श पढ्नुहोस्"),
        cta3=t("Explore districts", "जिल्लाहरू हेर्नुहोस्"),
        stats="".join([
            stat_x("6.11M", "६१.१ लाख", "Population", "जनसंख्या"),
            stat("9,661", "km² area", "वर्ग कि.मी."),
            stat("8", "Districts", "जिल्ला"),
            stat("136", "Local governments", "स्थानीय तह"),
            stat("633", "People per km²", "प्रति वर्ग कि.मी."),
        ]),
    )

    shift = """
<section class="section section--paper2">
  <div class="wrap">
    <div class="grid grid--2" style="gap:56px;align-items:start">
      <div>
        <p class="eyebrow">{eb}</p>
        <h2>{h2}</h2>
        {p}
        <p><a class="btn btn--line" href="manifesto.html">{cta}</a></p>
      </div>
      <div class="callout">
        <p class="eyebrow" style="margin-bottom:.7em">{qeb}</p>
        {ql}
      </div>
    </div>
  </div>
</section>
""".format(
        eb=t("From political discourse to economic possibility", "राजनीतिक विमर्शबाट आर्थिक सम्भावनातर्फ"),
        h2=t("Madhesh has never been short of political conversation.",
             "मधेशमा राजनीतिक बहसको कहिल्यै कमी भएन।"),
        p=blocks(
            "<p>For decades, questions of identity, representation, inclusion, citizenship, federalism and political power have occupied the centre of public life. That conversation remains important and should stay vibrant.</p>"
            "<p>And yet there is another conversation Madhesh must turn to now. Where will its young people find meaningful work? What can municipalities do to encourage enterprise? What can Madhesh produce competitively for the national market and for the markets across the border?</p>"
            "<p><strong>That is the gap Madhesh Next seeks to address.</strong></p>",
            "<p>दशकौंदेखि पहिचान, प्रतिनिधित्व, समावेशिता, नागरिकता, संघीयता र राजनीतिक शक्तिका प्रश्नहरू सार्वजनिक जीवनको केन्द्रमा रहे। त्यो बहस महत्त्वपूर्ण छ र जीवन्त रहनुपर्छ।</p>"
            "<p>तर अब मधेशले अर्को बहसतर्फ फर्कनुपर्छ। हाम्रा युवाले अर्थपूर्ण काम कहाँ पाउँछन्? नगरपालिकाले उद्यम प्रवर्धन गर्न के गर्न सक्छन्? मधेशले राष्ट्रिय बजार र सीमापारिको बजारका लागि के प्रतिस्पर्धी रूपमा उत्पादन गर्न सक्छ?</p>"
            "<p><strong>यही खाडल पूर्ति गर्न मधेश नेक्स्ट अघि सरेको हो।</strong></p>"),
        cta=t("Read the full argument", "पूरा विमर्श पढ्नुहोस्"),
        qeb=t("The questions we want asked", "हामी सोधिनुपर्छ भन्ने प्रश्नहरू"),
        ql='<ul class="qlist">' + "".join(
            "<li>%s</li>" % t(a, b) for a, b in [
                ("What can our municipality do to create jobs?", "हाम्रो नगरपालिकाले रोजगारी सिर्जना गर्न के गर्न सक्छ?"),
                ("What local businesses could grow here?", "यहाँ कुन स्थानीय व्यवसाय हुर्कन सक्छन्?"),
                ("What skills do our local industries need?", "हाम्रा स्थानीय उद्योगलाई कस्तो सीप चाहिन्छ?"),
                ("What could Madhesh produce for the Indian market?", "मधेशले भारतीय बजारका लागि के उत्पादन गर्न सक्छ?"),
                ("How many jobs were created here last year?", "गत वर्ष यहाँ कति रोजगारी सिर्जना भयो?"),
            ]) + "</ul>",
    )

    pillars = """
<section class="section">
  <div class="wrap">
    <p class="eyebrow">{eb}</p>
    <h2>{h2}</h2>
    <p class="lede">{lede}</p>
    <div class="grid grid--4" style="margin-top:34px">{cards}</div>
    <p style="margin-top:28px"><a class="btn btn--line" href="modules.html">{cta}</a></p>
  </div>
</section>
""".format(
        eb=t("How the campaign is built", "अभियानको संरचना"),
        h2=t("Four modules", "चार मोड्युल"),
        lede=t("Everything Madhesh Next does fits into one of four modules. Each district chapter runs the same four — so work is comparable, repeatable and easy to join.",
               "मधेश नेक्स्टका सबै काम चार मोड्युलमध्ये कुनै एकमा पर्छन्। हरेक जिल्ला च्याप्टरले यिनै चार चलाउँछ — जसले काम तुलनायोग्य, दोहोर्‍याउन मिल्ने र सहभागी हुन सजिलो बनाउँछ।"),
        cards="".join(
            '<a class="card" href="modules.html#%s"><span class="card__num">%s</span><h3>%s</h3><p>%s</p></a>' % (
                sl, num, t(en, ne), t(de, dn))
            for sl, num, en, ne, de, dn in MODULES_SHORT),
        cta=t("See how the modules work", "मोड्युल कसरी चल्छन् हेर्नुहोस्"),
    )

    dgrid = """
<section class="section section--paper2">
  <div class="wrap">
    <p class="eyebrow">{eb}</p>
    <h2>{h2}</h2>
    <p class="lede">{lede}</p>
    <div class="dgrid" style="margin-top:32px">{cards}</div>
    <p style="margin-top:30px"><a class="btn btn--dark" href="districts.html">{cta}</a></p>
  </div>
</section>
""".format(
        eb=t("Where the work happens", "काम कहाँ हुन्छ"),
        h2=t("8 districts · 136 local governments", "८ जिल्ला · १३६ स्थानीय तह"),
        lede=t("The 2015 Constitution made municipalities powerful institutions. Madhesh Next treats every one of them as an economic actor — with its own page, its own questions and its own numbers.",
               "२०७२ को संविधानले नगरपालिकालाई शक्तिशाली संस्था बनायो। मधेश नेक्स्टले हरेकलाई आर्थिक कर्ताका रूपमा हेर्छ — आफ्नै पृष्ठ, आफ्नै प्रश्न र आफ्नै तथ्याङ्कसहित।"),
        cards="".join(dcard(d, base="") for d in DISTRICTS),
        cta=t("All districts & local levels", "सबै जिल्ला र स्थानीय तह"),
    )

    people = """
<section class="section">
  <div class="wrap">
    <p class="eyebrow">{eb}</p>
    <h2>{h2}</h2>
    <div class="people" style="margin-top:30px">{cards}</div>
    <p style="margin-top:28px"><a class="btn btn--line" href="conveners.html">{cta}</a></p>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap narrow center">
    <h2 style="margin-bottom:.5em">{ch}</h2>
    <p class="lede" style="color:#d6d6d6;margin:0 auto 28px">{cl}</p>
    <a class="btn btn--primary" href="join.html">{cc}</a>
  </div>
</section>
""".format(
        eb=t("Campaign conveners", "अभियान संयोजक"),
        h2=t("Five conveners, one question", "पाँच संयोजक, एउटै प्रश्न"),
        cards="".join(person_card(p, short=True) for p in CONVENERS),
        cta=t("Meet the conveners", "संयोजकहरूलाई चिन्नुहोस्"),
        ch=t("Before governments change, the conversation must change.",
             "सरकार फेरिनुअघि, बहस फेरिनुपर्छ।"),
        cl=t("Start a chapter in your municipality, contribute data, write, or simply ask your representative one economic question this month.",
             "आफ्नो नगरपालिकामा च्याप्टर सुरु गर्नुहोस्, तथ्याङ्क दिनुहोस्, लेख्नुहोस्, वा यो महिना आफ्नो जनप्रतिनिधिलाई एउटा आर्थिक प्रश्न सोध्नुहोस्।"),
        cc=t("Join Madhesh Next", "मधेश नेक्स्टमा सहभागी हुनुहोस्"),
    )

    return layout("Home", "गृहपृष्ठ", hero + shift + pillars + dgrid + people,
                  desc_en="Madhesh Next — a citizen-led, non-partisan campaign to move public discourse in Madhesh from politics to economy. 8 districts, 136 local governments.")


MODULES_SHORT = [
    ("project", "01", "Project", "परियोजना",
     "Time-bound interventions with a defined outcome and an end date.",
     "निश्चित परिणाम र अन्त्य मिति भएका समयबद्ध हस्तक्षेप।"),
    ("program", "02", "Program", "कार्यक्रम",
     "Continuing streams of work that run across years and districts.",
     "वर्षौं र जिल्लाभर निरन्तर चल्ने कामका धाराहरू।"),
    ("poll", "03", "Poll", "जनमत",
     "The listening module — surveys, town halls and citizen questions.",
     "सुन्ने मोड्युल — सर्वेक्षण, नागरिक भेला र नागरिक प्रश्न।"),
    ("publication", "04", "Publication", "प्रकाशन",
     "The knowledge module — data, briefs, reporting and the manual.",
     "ज्ञान मोड्युल — तथ्याङ्क, संक्षिप्त अध्ययन, रिपोर्टिङ र म्यानुअल।"),
]


def dcard(d, base=""):
    c = {"METRO": 0, "SUB": 0, "MUN": 0, "RM": 0}
    for _, _, ty in d["lgs"]:
        c[ty] += 1
    urban = c["METRO"] + c["SUB"] + c["MUN"]
    return """
<a class="dcard" href="{base}districts/{slug}.html">
  <p class="dcard__name">{nm}</p>
  <p class="dcard__ne">{nm2}</p>
  <div class="dcard__row"><span>{l_hq}</span><span>{hq}</span></div>
  <div class="dcard__row"><span>{l_pop}</span><span>{pop}</span></div>
  <div class="dcard__row"><span>{l_lg}</span><span>{lg}</span></div>
  <div class="dcard__row"><span>{l_lit}</span><span>{lit}</span></div>
</a>""".format(
        base=base, slug=d["slug"],
        nm=t(d["en"], d["ne"]), nm2=t(d["ne"], d["en"]),
        l_hq=t("Headquarters", "सदरमुकाम"), hq=t(d["hq_en"], d["hq_ne"]),
        l_pop=t("Population", "जनसंख्या"),
        pop=t("{:,}".format(d["pop"]), nep("{:,}".format(d["pop"]))),
        l_lg=t("Local levels", "स्थानीय तह"),
        lg=t("%d (%d urban · %d rural)" % (len(d["lgs"]), urban, c["RM"]),
             nep("%d" % len(d["lgs"])) + " (" + nep(urban) + " सहरी · " + nep(c["RM"]) + " गाउँ)"),
        l_lit=t("Literacy", "साक्षरता"), lit=t(d["lit"], nep(d["lit"])),
    )


def person_card(p, short=False):
    initials = "".join(w[0] for w in p["name_en"].split()[:2])
    bio = "" if short else '<p class="card__meta" style="justify-content:center;display:block;margin-top:12px">%s</p>' % t(p["bio_en"], p["bio_ne"])
    return """
<div class="person">
  <div class="person__avatar" aria-hidden="true">{ini}</div>
  <p class="person__name">{name}</p>
  <p class="person__ne" lang="ne">{ne}</p>
  <p class="person__role" style="margin-top:8px">{role}</p>
  {bio}
</div>""".format(ini=initials, name=p["name_en"], ne=p["name_ne"],
                 role=t("Campaign Convener", "अभियान संयोजक"), bio=bio)


# --------------------------------------------------------------- manifesto
MANIFESTO = [
    # (heading_en, heading_ne, [ (en_html, ne_html), ... ])
    (None, None, [
        ("<p class='lede'>Madhesh has never been short of political conversation. For decades, questions of identity, representation, inclusion, citizenship, federalism, rights and political power have occupied the centre of public life. The political movements of Madhesh fundamentally changed Nepal's democratic discourse and forced the country to confront questions that had remained unresolved for generations.</p>"
         "<p>That conversation remains important. It should remain vibrant, democratic and progressive.</p>"
         "<p>And yet there is another conversation that Madhesh must turn its attention to now.</p>"
         "<blockquote>The conversation about its economy.</blockquote>"
         "<p>What kind of economy can Madhesh build? Where will its young people find meaningful work? What small enterprises and big businesses can emerge here? What can municipalities do to encourage enterprise? What skills should schools and colleges develop? What can Madhesh produce competitively for the national market and for the markets across the border? How can existing entrepreneurs grow and budding entrepreneurs survive and sustain? How can institutions like CDO offices, security forces, customs and traffic administrators become facilitators of economic activity rather than obstacles?</p>"
         "<p>These questions are rarely part of everyday public discourse in Madhesh. Economic policy is discussed, of course. But much of that discussion takes place among industrialists, large business interests, ministers, bureaucrats, economists and development professionals. Vendors and small and medium enterprises — the biggest job and value creators — are seldom heard. It seldom becomes a popular, all-sided conversation including young people, citizens, political workers, local elected representatives, students, journalists and communities.</p>"
         "<p><strong>That is the gap Madhesh Next seeks to address.</strong> It is a citizen-led, non-partisan effort to bring the economy into the everyday political and social conversation of Madhesh.</p>",
         "<p class='lede'>मधेशमा राजनीतिक बहसको कहिल्यै कमी भएन। दशकौंदेखि पहिचान, प्रतिनिधित्व, समावेशिता, नागरिकता, संघीयता, अधिकार र राजनीतिक शक्तिका प्रश्नहरू सार्वजनिक जीवनको केन्द्रमा रहे। मधेशका राजनीतिक आन्दोलनले नेपालको लोकतान्त्रिक विमर्शलाई आधारभूत रूपमै बदले र पुस्तौंदेखि अनुत्तरित रहेका प्रश्नहरूसँग देशलाई जुध्न बाध्य बनाए।</p>"
         "<p>त्यो बहस महत्त्वपूर्ण छ। यो जीवन्त, लोकतान्त्रिक र प्रगतिशील रहनुपर्छ।</p>"
         "<p>तर अब मधेशले ध्यान दिनुपर्ने अर्को बहस पनि छ।</p>"
         "<blockquote>त्यो हो — उसको अर्थतन्त्रको बहस।</blockquote>"
         "<p>मधेशले कस्तो अर्थतन्त्र बनाउन सक्छ? यहाँका युवाले अर्थपूर्ण काम कहाँ पाउँछन्? यहाँ कस्ता साना उद्यम र ठूला व्यवसाय जन्मन सक्छन्? नगरपालिकाले उद्यम प्रवर्धन गर्न के गर्न सक्छन्? विद्यालय र क्याम्पसले कस्तो सीप विकास गर्नुपर्छ? मधेशले राष्ट्रिय बजार र सीमापारिको बजारका लागि के प्रतिस्पर्धी रूपमा उत्पादन गर्न सक्छ? विद्यमान उद्यमी कसरी बढ्न सक्छन् र नयाँ उद्यमी कसरी टिक्न सक्छन्? प्रजिअ कार्यालय, सुरक्षा निकाय, भन्सार र ट्राफिक प्रशासनजस्ता संस्था अवरोध होइन, आर्थिक गतिविधिका सहजकर्ता कसरी बन्न सक्छन्?</p>"
         "<p>यी प्रश्नहरू मधेशको दैनिक सार्वजनिक विमर्शमा विरलै पर्छन्। आर्थिक नीतिको बहस हुन्छ, तर त्यो प्रायः उद्योगपति, ठूला व्यावसायिक स्वार्थ, मन्त्री, कर्मचारी, अर्थशास्त्री र विकास पेसाकर्मीबीच मात्र सीमित हुन्छ। सबैभन्दा बढी रोजगारी र मूल्य सिर्जना गर्ने साना व्यापारी र लघु–मझौला उद्यमको आवाज विरलै सुनिन्छ।</p>"
         "<p><strong>यही खाडल पूर्ति गर्न मधेश नेक्स्ट अघि सरेको हो।</strong> यो अर्थतन्त्रलाई मधेशको दैनिक राजनीतिक र सामाजिक बहसमा ल्याउने नागरिक नेतृत्वको गैर-दलीय प्रयास हो।</p>"),
    ]),
    ("Joblessness and middle-class poverty", "बेरोजगारी र मध्यमवर्गीय गरिबी", [
        ("<p>The absence of this conversation is not merely intellectual. It has very real consequences.</p>"
         "<p>Madhesh has a large young population, enormous agricultural potential, important cities and trading centres, a long tradition of commerce, and immediate geographical access to the Indian market. Yet for many young Madheshis, the most visible economic pathway remains migration. Young people who are educated, hardworking and ambitious often find themselves asking not how to build something here, but where they should go to find work.</p>"
         "<p>Madhesh continues to face abject poverty. But alongside this familiar poverty, another phenomenon deserves greater recognition: <strong>middle-class poverty</strong>. Families may educate their children, maintain respectable homes and aspire to a better life, yet struggle to generate sufficient income from local economic activity. Young people may have degrees but no productive employment. Small entrepreneurs may have ideas but no ecosystem in which those ideas can grow.</p>"
         "<p>Even something as ordinary as a clean, affordable tea or coffee shop can serve as a useful proxy. Such establishments are now a familiar part of urban life in Kathmandu, Pokhara, Butwal and Bharatpur. Their presence reflects more than changing tastes — it indicates purchasing power, urban footfall, disposable income, employment and supply chains. Their relative scarcity in many parts of Madhesh is therefore worth asking about.</p>"
         "<p>The point is not a decent restaurant. The point is what the restaurant represents.</p>",
         "<p>यो बहसको अभाव केवल बौद्धिक कुरा होइन। यसका ठोस परिणाम छन्।</p>"
         "<p>मधेशसँग ठूलो युवा जनसंख्या, विशाल कृषि सम्भावना, महत्त्वपूर्ण सहर र व्यापारिक केन्द्र, लामो व्यापारिक परम्परा र भारतीय बजारसम्मको तत्काल भौगोलिक पहुँच छ। तर धेरै युवा मधेशीका लागि सबैभन्दा देखिने आर्थिक बाटो अझै पनि बसाइँसराइ नै हो। शिक्षित, मेहनती र महत्त्वाकांक्षी युवाहरू 'यहाँ के बनाउने' होइन, 'काम खोज्न कहाँ जाने' भन्ने प्रश्न सोध्न बाध्य छन्।</p>"
         "<p>मधेशमा चरम गरिबी अझै छ। तर यससँगै अर्को परिघटनालाई पनि चिन्न जरुरी छ — <strong>मध्यमवर्गीय गरिबी</strong>। परिवारले छोराछोरी पढाउँछन्, इज्जतिलो घर राख्छन्, राम्रो जीवनको आकांक्षा गर्छन्, तर स्थानीय आर्थिक गतिविधिबाट पर्याप्त आम्दानी गर्न संघर्ष गर्छन्। युवासँग डिग्री छ तर उत्पादनशील रोजगारी छैन। साना उद्यमीसँग विचार छ तर त्यो हुर्कने पारिस्थितिकी छैन।</p>"
         "<p>एउटा सफा र सुलभ चिया वा कफी पसलजस्तो सामान्य कुरा पनि राम्रो सूचक हुन सक्छ। काठमाडौं, पोखरा, बुटवल र भरतपुरमा यस्ता ठाउँ सहरी जीवनको सामान्य हिस्सा बनिसके। तिनको उपस्थिति स्वाद परिवर्तन मात्र होइन — क्रयशक्ति, सहरी आवागमन, खर्च गर्न सकिने आम्दानी, रोजगारी र आपूर्ति शृंखलाको संकेत हो। मधेशका धेरै भागमा तिनको सापेक्षिक अभाव त्यसैले प्रश्न गर्न लायक छ।</p>"
         "<p>कुरा राम्रो रेस्टुरेन्टको होइन। कुरा त्यो रेस्टुरेन्टले के प्रतिनिधित्व गर्छ भन्ने हो।</p>"),
    ]),
    ("Madhesh has economic advantages. What is missing is economic ambition.",
     "मधेशसँग आर्थिक सुविधा छ। नभएको आर्थिक महत्त्वाकांक्षा हो।", [
        ("<p>Madhesh possesses many of the conditions normally associated with economic opportunity. Fertile land and significant agricultural potential. Major cities and towns. An established trading culture. Transport corridors connecting it to the rest of Nepal and to India. A large labour force and a growing consumer population. Most importantly, it sits immediately next to one of the world's largest and fastest-growing markets.</p>"
         "<p>Yet these advantages have not been converted into a broad-based economic transformation. Agriculture remains predominantly an activity rather than a modern economic ecosystem. Industry exists, but concentrated around a limited number of locations and sectors. Trade is vibrant, but the conversation often stops at trade itself rather than asking what Madhesh can produce, process and export. Cities are growing, but urbanisation has not automatically created productive local economies.</p>"
         "<p>The problem is not simply a shortage of resources. It is partly a shortage of <strong>economic ambition</strong> — the collective confidence to ask what Madhesh could produce, build, sell and become if its institutions were organised around economic opportunity.</p>",
         "<p>आर्थिक अवसरसँग सामान्यतः जोडिने धेरै अवस्था मधेशसँग छन्। उर्वर भूमि र ठूलो कृषि सम्भावना। ठूला सहर र बजार। स्थापित व्यापारिक संस्कृति। नेपालको बाँकी भाग र भारतसँग जोड्ने यातायात कोरिडोर। ठूलो श्रमशक्ति र बढ्दो उपभोक्ता जनसंख्या। सबैभन्दा महत्त्वपूर्ण — यो विश्वकै ठूलो र द्रुत बढ्दो बजारको ठीक छेउमा छ।</p>"
         "<p>तर यी सुविधाहरू व्यापक आर्थिक रूपान्तरणमा परिणत भएका छैनन्। कृषि आधुनिक आर्थिक पारिस्थितिकी नभई एउटा गतिविधि मात्र रहेको छ। उद्योग छ, तर सीमित स्थान र क्षेत्रमा केन्द्रित। व्यापार जीवन्त छ, तर बहस व्यापारमै रोकिन्छ — मधेशले के उत्पादन, प्रशोधन र निर्यात गर्न सक्छ भन्ने प्रश्नसम्म पुग्दैन। सहर बढिरहेका छन्, तर सहरीकरणले आफैँ उत्पादनशील स्थानीय अर्थतन्त्र बनाएको छैन।</p>"
         "<p>समस्या स्रोतको अभाव मात्र होइन। यो आंशिक रूपमा <strong>आर्थिक महत्त्वाकांक्षाको अभाव</strong> हो — संस्थाहरू आर्थिक अवसरका वरिपरि संगठित भए मधेशले के उत्पादन गर्न, बनाउन, बेच्न र बन्न सक्छ भनी सोध्ने सामूहिक आत्मविश्वासको अभाव।</p>"),
    ]),
    ("From “What will government give us?” to “What can we build here?”",
     "“सरकारले के दिन्छ?” बाट “हामी यहाँ के बनाउन सक्छौं?” सम्म", [
        ("<p>One of the most important changes Madhesh needs is a change in the questions citizens ask. Political discourse often revolves around what the federal government should provide: roads, bridges, irrigation, budgets, appointments, programmes. These things matter. But Madhesh Next wants to add another set of questions.</p>"
         "<ul>"
         "<li>What can our municipality do to create jobs?</li>"
         "<li>What local businesses could grow here?</li>"
         "<li>What would make an entrepreneur establish a business in this town rather than somewhere else?</li>"
         "<li>What skills do our local industries need?</li>"
         "<li>What can our colleges teach that connects directly with the economy around them?</li>"
         "<li>How can local government make it easier — not harder — to start and operate a legitimate business?</li>"
         "<li>What products could Madhesh sell to the rest of Nepal? What could it produce for the Indian market?</li>"
         "</ul>"
         "<p>These are economic questions, but they are also democratic questions. Citizens should be able to ask their mayors, ward chairs, provincial ministers and parliamentarians not only what they will demand from Kathmandu, but what economic transformation they intend to deliver locally.</p>",
         "<p>मधेशलाई चाहिने सबैभन्दा महत्त्वपूर्ण परिवर्तनमध्ये एक हो — नागरिकले सोध्ने प्रश्नमै परिवर्तन। राजनीतिक बहस प्रायः संघीय सरकारले के दिनुपर्छ भन्ने वरिपरि घुम्छ: सडक, पुल, सिँचाइ, बजेट, नियुक्ति, कार्यक्रम। यी महत्त्वपूर्ण छन्। तर मधेश नेक्स्ट अर्को शृंखलाका प्रश्न थप्न चाहन्छ।</p>"
         "<ul>"
         "<li>हाम्रो नगरपालिकाले रोजगारी सिर्जना गर्न के गर्न सक्छ?</li>"
         "<li>यहाँ कुन स्थानीय व्यवसाय हुर्कन सक्छन्?</li>"
         "<li>उद्यमीले अन्यत्र होइन, यही सहरमा व्यवसाय खोल्न किन चाहून्?</li>"
         "<li>हाम्रा स्थानीय उद्योगलाई कस्तो सीप चाहिन्छ?</li>"
         "<li>हाम्रा क्याम्पसले वरिपरिको अर्थतन्त्रसँग सीधै जोडिने के पढाउन सक्छन्?</li>"
         "<li>स्थानीय सरकारले वैध व्यवसाय खोल्न र चलाउन कसरी सजिलो बनाउन सक्छ?</li>"
         "<li>मधेशले नेपालको बाँकी भागलाई के बेच्न सक्छ? भारतीय बजारका लागि के उत्पादन गर्न सक्छ?</li>"
         "</ul>"
         "<p>यी आर्थिक प्रश्न हुन्, तर लोकतान्त्रिक प्रश्न पनि हुन्। नागरिकले मेयर, वडाध्यक्ष, प्रदेश मन्त्री र सांसदलाई काठमाडौंसँग के माग्ने भन्ने मात्र होइन, स्थानीय रूपमा कस्तो आर्थिक रूपान्तरण दिने भन्ने पनि सोध्न सक्नुपर्छ।</p>"),
    ]),
    ("Municipalities should become primary economic actors",
     "नगरपालिका प्रमुख आर्थिक कर्ता बन्नुपर्छ", [
        ("<p>The 2015 Constitution gave the nation an important institutional advantage: local government. Municipalities and rural municipalities have become powerful institutions in the federal structure. Yet their economic role is still insufficiently developed.</p>"
         "<p>A municipality should not think of itself merely as an administrator of roads, waste, buildings, permits and social programmes. It can become a platform for local economic development. It can identify local economic strengths, make business registration easier, improve markets and commercial spaces, work with banks and cooperatives, identify skills that local businesses require, help entrepreneurs navigate government, and actively promote local products.</p>"
         "<p>And, critically, it can begin to measure itself by economic outcomes:</p>"
         "<ul><li>How many new businesses were established?</li><li>How many survived?</li><li>How many jobs were created?</li><li>How much local economic activity was generated?</li><li>How much additional tax revenue came from a growing local economy?</li></ul>"
         "<p>These questions should become part of local political discourse.</p>",
         "<p>२०७२ को संविधानले देशलाई एउटा महत्त्वपूर्ण संस्थागत सुविधा दियो: स्थानीय सरकार। नगरपालिका र गाउँपालिका संघीय संरचनाका शक्तिशाली संस्था बने। तर तिनको आर्थिक भूमिका अझै पर्याप्त विकसित छैन।</p>"
         "<p>नगरपालिकाले आफूलाई सडक, फोहोर, भवन, अनुमतिपत्र र सामाजिक कार्यक्रमको प्रशासक मात्र ठान्नु हुँदैन। यो स्थानीय आर्थिक विकासको मञ्च बन्न सक्छ। यसले स्थानीय आर्थिक शक्ति पहिचान गर्न, व्यवसाय दर्ता सजिलो बनाउन, बजार र व्यापारिक स्थल सुधार्न, बैंक र सहकारीसँग काम गर्न, स्थानीय उद्योगलाई चाहिने सीप पहिचान गर्न, उद्यमीलाई सरकारी प्रक्रियामा सघाउन र स्थानीय उत्पादनको सक्रिय प्रवर्धन गर्न सक्छ।</p>"
         "<p>र सबैभन्दा महत्त्वपूर्ण — यसले आफूलाई आर्थिक नतिजाबाट नाप्न थाल्न सक्छ:</p>"
         "<ul><li>कति नयाँ व्यवसाय दर्ता भए?</li><li>कति टिके?</li><li>कति रोजगारी सिर्जना भयो?</li><li>कति स्थानीय आर्थिक गतिविधि बढ्यो?</li><li>बढ्दो स्थानीय अर्थतन्त्रबाट कति थप राजस्व आयो?</li></ul>"
         "<p>यी प्रश्न स्थानीय राजनीतिक बहसको हिस्सा बन्नुपर्छ।</p>"),
    ]),
    ("The missing bridge between education and the local economy",
     "शिक्षा र स्थानीय अर्थतन्त्रबीचको हराएको पुल", [
        ("<p>Too often, education and the economy operate as separate worlds. A college may be surrounded by agriculture, manufacturing, trading, logistics or emerging service businesses, while its curriculum remains largely disconnected from these realities.</p>"
         "<p>Agricultural areas can develop expertise in agribusiness, food processing, agricultural technology and supply chains. Industrial towns can connect education with manufacturing, engineering and technical skills. Trading centres can develop expertise in logistics, commerce, finance, languages and cross-border business. Growing cities can develop skills in hospitality, retail, digital services, design and entrepreneurship.</p>"
         "<p>The objective is not simply to make young people employable. <strong>It is also to make them capable of creating employment.</strong></p>",
         "<p>प्रायः शिक्षा र अर्थतन्त्र छुट्टाछुट्टै संसारजस्तै चल्छन्। क्याम्पसको वरिपरि कृषि, उत्पादन, व्यापार, लजिस्टिक वा उदीयमान सेवा व्यवसाय हुन्छन्, तर पाठ्यक्रम ती यथार्थसँग जोडिँदैन।</p>"
         "<p>कृषि क्षेत्रले कृषि–व्यवसाय, खाद्य प्रशोधन, कृषि प्रविधि र आपूर्ति शृंखलामा विशेषज्ञता विकास गर्न सक्छ। औद्योगिक सहरले शिक्षालाई उत्पादन, इन्जिनियरिङ र प्राविधिक सीपसँग जोड्न सक्छ। व्यापारिक केन्द्रले लजिस्टिक, वाणिज्य, वित्त, भाषा र सीमापार व्यापारमा दक्षता बनाउन सक्छ। बढ्दो सहरले आतिथ्य, खुद्रा, डिजिटल सेवा, डिजाइन र उद्यमशीलताको सीप विकास गर्न सक्छ।</p>"
         "<p>उद्देश्य युवालाई रोजगारयोग्य बनाउनु मात्र होइन। <strong>तिनलाई रोजगारी सिर्जना गर्न सक्ने बनाउनु पनि हो।</strong></p>"),
    ]),
    ("Madhesh's entrepreneurs need an ecosystem",
     "मधेशका उद्यमीलाई पारिस्थितिकी चाहिन्छ", [
        ("<p>Madheshis have demonstrated entrepreneurial energy for generations. But individual enterprise cannot substitute for an ecosystem.</p>"
         "<p>A young entrepreneur needs access to finance, knowledge, mentors, technology, markets, skilled workers, reliable infrastructure and predictable administration. They also need a social environment that respects entrepreneurship.</p>"
         "<blockquote>A person who creates twenty jobs should be celebrated as much as a person who occupies an important political position.</blockquote>"
         "<p>In a country where opportunities are limited and young people are leaving in such large numbers, job creators are among the most important nation-builders. Madhesh Next wants to bring this idea into the mainstream public conversation.</p>",
         "<p>मधेशीहरूले पुस्तौंदेखि उद्यमशील ऊर्जा देखाएका छन्। तर व्यक्तिगत उद्यमले पारिस्थितिकीको विकल्प दिन सक्दैन।</p>"
         "<p>युवा उद्यमीलाई वित्त, ज्ञान, मार्गदर्शक, प्रविधि, बजार, दक्ष कामदार, भरपर्दो पूर्वाधार र पूर्वानुमानयोग्य प्रशासनको पहुँच चाहिन्छ। उद्यमशीलतालाई सम्मान गर्ने सामाजिक वातावरण पनि चाहिन्छ।</p>"
         "<blockquote>बीस जनालाई रोजगारी दिने व्यक्तिलाई महत्त्वपूर्ण राजनीतिक पद ओगट्ने व्यक्ति जत्तिकै सम्मान गरिनुपर्छ।</blockquote>"
         "<p>अवसर सीमित भएको र युवा ठूलो संख्यामा बाहिरिइरहेको देशमा रोजगारी सिर्जना गर्नेहरू सबैभन्दा महत्त्वपूर्ण राष्ट्रनिर्माता हुन्। मधेश नेक्स्ट यो विचारलाई मूलधारको सार्वजनिक बहसमा ल्याउन चाहन्छ।</p>"),
    ]),
    ("Roads for what?", "सडक — केका लागि?", [
        ("<p>Nepal has made substantial investments in connecting Madhesh with Kathmandu, the hills and the rest of the country. These investments are important. The question Madhesh Next wants to ask is not whether the roads were necessary. It is:</p>"
         "<blockquote>Roads for what?</blockquote>"
         "<p>Are the roads primarily routes for people to travel from Madhesh to Kathmandu? Are they mainly corridors through which goods imported from India reach the hills? Or can they become economic arteries in <em>both</em> directions? Can agricultural and industrial products from Madhesh travel north? Can products from the hills and mountains travel south through Madhesh? Can Madhesh become a place where products from across Nepal are aggregated, processed, packaged, marketed and taken to nearby Indian markets?</p>"
         "<p>The objective is not simply connectivity. It is <strong>economic connectivity</strong>.</p>",
         "<p>मधेशलाई काठमाडौं, पहाड र देशको बाँकी भागसँग जोड्न नेपालले ठूलो लगानी गरेको छ। यी लगानी महत्त्वपूर्ण छन्। मधेश नेक्स्टको प्रश्न सडक चाहिन्थ्यो कि थिएन भन्ने होइन। प्रश्न हो:</p>"
         "<blockquote>सडक — केका लागि?</blockquote>"
         "<p>के यी सडक मधेशबाट काठमाडौं जाने बाटो मात्र हुन्? के यी भारतबाट आयातित सामान पहाडसम्म पुर्‍याउने कोरिडोर मात्र हुन्? कि यी <em>दुवै</em> दिशामा आर्थिक धमनी बन्न सक्छन्? मधेशका कृषि र औद्योगिक उत्पादन उत्तर जान सक्छन्? पहाड–हिमालका उत्पादन मधेश हुँदै दक्षिण जान सक्छन्? नेपालभरका उत्पादन मधेशमा जम्मा गरी प्रशोधन, प्याकेजिङ र बजारीकरण गरेर नजिकको भारतीय बजारमा पुर्‍याउन सकिन्छ?</p>"
         "<p>उद्देश्य केवल जोडाइ होइन। <strong>आर्थिक जोडाइ</strong> हो।</p>"),
    ]),
    ("Madhesh can connect Nepal's products to India's consumers",
     "मधेशले नेपालका उत्पादनलाई भारतीय उपभोक्तासँग जोड्न सक्छ", [
        ("<p>The same logic applies to tourism. Nepal has extraordinary tourism assets. Yet much of the effort to sell Nepal has traditionally been directed towards international tourists. There is another enormous market much closer to home: India's growing middle class. Madhesh sits next to that market.</p>"
         "<p>Why should a family in Bihar or Uttar Pradesh not be encouraged to spend a long weekend in Pokhara, visit Chitwan, travel to Kathmandu or explore Lumbini? And who is better positioned to understand, communicate with and sell to these neighbouring markets than people living in Madhesh?</p>"
         "<p>The same principle can apply to agriculture, food products, manufacturing, logistics, hospitality, education, healthcare and services. Madhesh's future prosperity does not have to come only from what happens inside Madhesh. <strong>It can also come from what Madhesh enables for Nepal.</strong></p>",
         "<p>यही तर्क पर्यटनमा पनि लागू हुन्छ। नेपालसँग असाधारण पर्यटन सम्पदा छ। तर नेपाल बेच्ने प्रयास परम्परागत रूपमा अन्तर्राष्ट्रिय पर्यटकतिर केन्द्रित रह्यो। घरनजिकै अर्को विशाल बजार छ: भारतको बढ्दो मध्यम वर्ग। मधेश त्यही बजारको छेउमा छ।</p>"
         "<p>बिहार वा उत्तर प्रदेशको परिवारलाई पोखरामा लामो सप्ताहन्त बिताउन, चितवन घुम्न, काठमाडौं जान वा लुम्बिनी हेर्न किन प्रोत्साहित नगर्ने? र यी छिमेकी बजार बुझ्न, संवाद गर्न र बेच्न मधेशमा बस्नेभन्दा उपयुक्त को हुन सक्छ?</p>"
         "<p>यही सिद्धान्त कृषि, खाद्य उत्पादन, उत्पादनमूलक उद्योग, लजिस्टिक, आतिथ्य, शिक्षा, स्वास्थ्य र सेवामा लागू हुन्छ। मधेशको भावी समृद्धि मधेशभित्र हुने कुराबाट मात्र आउनुपर्दैन। <strong>मधेशले नेपालका लागि के सम्भव बनाउँछ, त्यसबाट पनि आउन सक्छ।</strong></p>"),
    ]),
    ("A citizen effort, and nothing else", "नागरिक प्रयास — अरू केही होइन", [
        ("<p>Madhesh Next is not partisan activism. It is deliberately non-partisan. Its purpose is to create a citizen conversation around economic opportunity.</p>"
         "<p>We envisage young people forming local, non-partisan groups to discuss their area's economic potential. We want journalists to report not only on political events but also on enterprises being created, jobs being generated, businesses being constrained and opportunities being missed. We want elected representatives and political workers to make local economic development part of their agenda. We want colleges to engage with local economies. We want entrepreneurs to speak about what works and what does not. We want public institutions to understand that facilitating legitimate economic activity is an important part of public service.</p>"
         "<p>And we want citizens to begin asking their representatives a very simple question:</p>"
         "<blockquote>What are you doing to make it easier for people here to create jobs?</blockquote>"
         "<p>The answers should be visible, measurable and subject to public scrutiny.</p>",
         "<p>मधेश नेक्स्ट दलीय सक्रियता होइन। यो सचेत रूपमा गैर-दलीय हो। यसको उद्देश्य आर्थिक अवसरका वरिपरि नागरिक बहस सिर्जना गर्नु हो।</p>"
         "<p>हामी युवाहरूले आफ्नो क्षेत्रको आर्थिक सम्भावनाबारे छलफल गर्न स्थानीय, गैर-दलीय समूह बनाऊन् भन्ने कल्पना गर्छौं। पत्रकारहरूले राजनीतिक घटना मात्र होइन, खुल्दै गरेका उद्यम, सिर्जना भएका रोजगारी, अवरुद्ध व्यवसाय र गुमेका अवसरबारे पनि लेखून्। जनप्रतिनिधि र राजनीतिक कार्यकर्ताले स्थानीय आर्थिक विकासलाई आफ्नो एजेन्डा बनाऊन्। क्याम्पसहरू स्थानीय अर्थतन्त्रसँग जोडिऊन्। उद्यमीहरूले के काम गर्छ र के गर्दैन भनी बोलून्। सार्वजनिक संस्थाहरूले वैध आर्थिक गतिविधिलाई सहज बनाउनु सार्वजनिक सेवाकै महत्त्वपूर्ण अंग हो भन्ने बुझून्।</p>"
         "<p>र नागरिकहरूले आफ्ना प्रतिनिधिलाई एउटा सरल प्रश्न सोध्न थालून्:</p>"
         "<blockquote>यहाँका मानिसले रोजगारी सिर्जना गर्न सजिलो होस् भनेर तपाईं के गर्दै हुनुहुन्छ?</blockquote>"
         "<p>उत्तरहरू देखिने, नापिने र सार्वजनिक छानबिनयोग्य हुनुपर्छ।</p>"),
    ]),
    ("Why Madhesh Next matters to Nepal", "मधेश नेक्स्ट नेपालका लागि किन महत्त्वपूर्ण छ", [
        ("<p>Nepal cannot build a prosperous economy if one of its most strategically located and densely populated regions remains primarily a political constituency rather than an economic engine.</p>"
         "<p>The mountains and hills have products, resources and tourism destinations. Madhesh has agriculture, industry, cities, people, transport corridors and access to the Indian market. These should not be separate economic stories. They should become parts of one economic story of Nepal.</p>"
         "<p>The roads already provide much of the physical connection. The next task is to create the economic connections. And that begins not necessarily with another government programme or another change of government. <strong>It begins with changing the conversation.</strong></p>"
         "<p>To make economic possibility a subject of everyday public conversation in Madhesh. To make job creation a political expectation. To make entrepreneurship a form of citizenship. To make local government an enabler of enterprise. And ultimately, to make better use of Madhesh — not only for Madhesh, but for a more prosperous Nepal.</p>"
         "<p class='muted' style='font-family:var(--sans);font-size:.9rem;margin-top:2.5em'>Founding note by Prashant Singh, Campaign Convener.</p>",
         "<p>आफ्नो सबैभन्दा रणनीतिक अवस्थित र घना बसोबास भएको क्षेत्र आर्थिक इन्जिन नभई मुख्यतः राजनीतिक निर्वाचन क्षेत्र मात्र रहिरह्यो भने नेपालले समृद्ध अर्थतन्त्र बनाउन सक्दैन।</p>"
         "<p>पहाड–हिमालसँग उत्पादन, स्रोत र पर्यटकीय गन्तव्य छन्। मधेशसँग कृषि, उद्योग, सहर, जनशक्ति, यातायात कोरिडोर र भारतीय बजारको पहुँच छ। यी छुट्टाछुट्टै आर्थिक कथा हुनु हुँदैन। यी नेपालको एउटै आर्थिक कथाका हिस्सा बन्नुपर्छ।</p>"
         "<p>सडकले भौतिक जोडाइ धेरै हदसम्म दिइसक्यो। अबको काम आर्थिक जोडाइ बनाउनु हो। र त्यो अर्को सरकारी कार्यक्रम वा अर्को सत्ता परिवर्तनबाट सुरु हुँदैन। <strong>त्यो बहस बदल्नबाट सुरु हुन्छ।</strong></p>"
         "<p>आर्थिक सम्भावनालाई मधेशको दैनिक सार्वजनिक बहसको विषय बनाउने। रोजगारी सिर्जनालाई राजनीतिक अपेक्षा बनाउने। उद्यमशीलतालाई नागरिकताको रूप बनाउने। स्थानीय सरकारलाई उद्यमको सहजकर्ता बनाउने। र अन्ततः मधेशको राम्रो उपयोग गर्ने — मधेशका लागि मात्र होइन, अझ समृद्ध नेपालका लागि।</p>"
         "<p class='muted' style='font-family:var(--sans);font-size:.9rem;margin-top:2.5em'>संस्थापक दस्तावेज: प्रशान्त सिंह, अभियान संयोजक।</p>"),
    ]),
]


def page_manifesto():
    parts = ["""
<section class="section section--tight" style="background:var(--paper-2);border-bottom:1px solid var(--line)">
  <div class="wrap narrow">
    <p class="eyebrow">%s</p>
    <h1 style="margin-bottom:.3em">%s</h1>
    <p class="lede">%s</p>
  </div>
</section>
<section class="section">
  <div class="wrap"><div class="prose" style="margin:0 auto">
""" % (t("The founding argument", "स्थापना विमर्श"),
       t("Public discourse must shift to economy", "सार्वजनिक विमर्श अर्थतन्त्रतर्फ सर्नुपर्छ"),
       t("From political discourse to economic possibility — the founding note of Madhesh Next.",
         "राजनीतिक विमर्शबाट आर्थिक सम्भावनासम्म — मधेश नेक्स्टको स्थापना दस्तावेज।"))]

    for h_en, h_ne, paras in MANIFESTO:
        if h_en:
            parts.append("<h2>%s</h2>" % t(h_en, h_ne))
        for en, ne in paras:
            parts.append(blocks(en, ne))

    parts.append("""
  </div></div>
</section>
<section class="section section--dark">
  <div class="wrap narrow center">
    <h2>%s</h2>
    <div class="hero__actions" style="justify-content:center">
      <a class="btn btn--primary" href="join.html">%s</a>
      <a class="btn btn--ghost" href="modules.html">%s</a>
    </div>
  </div>
</section>
""" % (t("Change the conversation where you live.", "आफू बस्ने ठाउँमै बहस बदल्नुहोस्।"),
       t("Join the campaign", "अभियानमा सहभागी हुनुहोस्"),
       t("See the modules", "मोड्युल हेर्नुहोस्")))

    return layout("The Argument", "मूल विमर्श", "".join(parts),
                  desc_en="Public discourse in Madhesh must shift to economy — the founding argument of Madhesh Next by Prashant Singh.")


# ------------------------------------------------------------------- vision
VISION = [
    ("2030", "Foundations", "जग",
     "Chapters in all 8 districts. A public baseline: what each of the 136 local governments actually produces, employs and taxes. A Madhesh Next manual any citizen can pick up and run with. First cohort of municipal economic scorecards published.",
     "सबै ८ जिल्लामा च्याप्टर। सार्वजनिक आधाररेखा: १३६ स्थानीय तहमध्ये प्रत्येकले वास्तवमा के उत्पादन गर्छ, कति रोजगारी दिन्छ र कति कर उठाउँछ। कुनै पनि नागरिकले उठाएर चलाउन सक्ने मधेश नेक्स्ट म्यानुअल। नगरपालिका आर्थिक स्कोरकार्डको पहिलो शृंखला प्रकाशित।",
     ["8 district chapters active", "136 local-level economic profiles", "Annual Madhesh Economic Review", "Citizen question campaign in every municipality"],
     ["८ जिल्ला च्याप्टर सक्रिय", "१३६ स्थानीय तह आर्थिक प्रोफाइल", "वार्षिक मधेश आर्थिक समीक्षा", "हरेक नगरपालिकामा नागरिक प्रश्न अभियान"]),
    ("2040", "Transformation", "रूपान्तरण",
     "Madhesh as a processing and logistics region, not only a transit corridor. Agro-processing clusters around Sarlahi and Siraha, an industrial belt from Simara to Birgunj, and colleges whose curricula are written with local industry in the room.",
     "मधेश केवल पारवहन कोरिडोर होइन, प्रशोधन र लजिस्टिक क्षेत्रका रूपमा। सर्लाही र सिराहावरिपरि कृषि–प्रशोधन क्लस्टर, सिमरादेखि वीरगन्जसम्म औद्योगिक पेटी, र स्थानीय उद्योगसँगै लेखिएका क्याम्पस पाठ्यक्रम।",
     ["Products from all 7 provinces aggregated in Madhesh for Indian markets", "Every municipality reports jobs created annually", "Skills pipelines tied to local industry", "Measurable fall in distress migration"],
     ["सातै प्रदेशका उत्पादन भारतीय बजारका लागि मधेशमा एकत्रित", "हरेक नगरपालिकाले वार्षिक रोजगारी विवरण सार्वजनिक गर्ने", "स्थानीय उद्योगसँग जोडिएको सीप प्रणाली", "बाध्यकारी बसाइँसराइमा नापिने कमी"]),
    ("2050", "Maturity", "परिपक्वता",
     "A self-sustaining regional economy where a young Madheshi's default question is what to build here, not where to go. A broad middle class, an entrepreneurial ecosystem that no longer depends on individual heroism, and local governments judged by economic outcomes.",
     "आत्मनिर्भर क्षेत्रीय अर्थतन्त्र, जहाँ युवा मधेशीको पहिलो प्रश्न 'कहाँ जाने' होइन 'यहाँ के बनाउने' हुन्छ। व्यापक मध्यम वर्ग, व्यक्तिगत वीरतामा निर्भर नरहने उद्यमशील पारिस्थितिकी, र आर्थिक नतिजाबाट मूल्याङ्कन हुने स्थानीय सरकार।",
     ["Madhesh a net creator of jobs, not an exporter of labour", "Entrepreneurship treated as a form of citizenship", "One economic story of Nepal, not two"],
     ["मधेश श्रम निर्यातक होइन, रोजगारी सिर्जक", "उद्यमशीलता नागरिकताको रूपमा", "नेपालको एउटै आर्थिक कथा, दुई होइन"]),
]


def page_vision():
    items = []
    for year, tag_en, tag_ne, body_en, body_ne, li_en, li_ne in VISION:
        lis = "".join("<li>%s</li>" % t(a, b) for a, b in zip(li_en, li_ne))
        items.append("""
<div class="tl__item">
  <div class="tl__year">%s</div>
  <div class="tl__tag">%s</div>
  <p class="lede" style="max-width:70ch">%s</p>
  <ul class="qlist" style="max-width:70ch">%s</ul>
</div>""" % (year, t(tag_en, tag_ne), t(body_en, body_ne), lis))

    body = """
<section class="section section--tight" style="background:var(--paper-2);border-bottom:1px solid var(--line)">
  <div class="wrap narrow">
    <p class="eyebrow">{eb}</p>
    <h1 style="margin-bottom:.3em">{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="tl" style="max-width:860px">{items}</div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap narrow">
    <h2>{h2}</h2>
    {p}
  </div>
</section>
""".format(
        eb=t("Madhesh 2030 · 2040 · 2050", "मधेश २०३० · २०४० · २०५०"),
        h1=t("Three horizons", "तीन क्षितिज"),
        lede=t("A campaign that only reacts to the present cannot change it. Madhesh Next works to three horizons — each with things you can count.",
               "वर्तमानमा प्रतिक्रिया मात्र दिने अभियानले त्यसलाई बदल्न सक्दैन। मधेश नेक्स्ट तीन क्षितिजमा काम गर्छ — हरेकमा गन्न सकिने कुरा।"),
        items="".join(items),
        h2=t("Why fixed dates matter", "निश्चित मिति किन महत्त्वपूर्ण छ"),
        p=blocks(
            "<p>Development conversations in Nepal are usually open-ended. Nothing is ever due. A campaign with dates can be held to account — by its own conveners, by journalists, and by the citizens it claims to speak for.</p>"
            "<p>Every target above is designed to be checkable. If Madhesh Next has not published 136 local-level economic profiles by 2030, that is a visible failure, and it should be treated as one.</p>",
            "<p>नेपालमा विकासका बहस प्रायः खुला–अन्त्य हुन्छन्। कुनै कुरा कहिल्यै 'बुझाउनुपर्ने' हुँदैन। मिति भएको अभियानलाई जवाफदेही बनाउन सकिन्छ — आफ्नै संयोजक, पत्रकार र जसका लागि बोल्ने दाबी गरिन्छ ती नागरिकद्वारा।</p>"
            "<p>माथिका हरेक लक्ष्य जाँच्न सकिने गरी बनाइएका छन्। २०३० सम्ममा मधेश नेक्स्टले १३६ स्थानीय तहको आर्थिक प्रोफाइल प्रकाशित गरेन भने त्यो देखिने असफलता हो, र त्यसलाई त्यसै रूपमा लिइनुपर्छ।</p>"),
    )
    return layout("Vision", "दृष्टिकोण", body,
                  desc_en="Madhesh Next works to three horizons — 2030 Foundations, 2040 Transformation, 2050 Maturity.")


# ------------------------------------------------------------------ modules
MODULES_FULL = [
    ("project", "01", "Project", "परियोजना",
     "Time-bound interventions with a defined outcome",
     "निश्चित परिणाम भएका समयबद्ध हस्तक्षेप",
     "A Project has a start, an end and something you can point at when it is over. It is how a chapter turns an idea into evidence.",
     "परियोजनाको सुरु हुन्छ, अन्त्य हुन्छ, र सकिएपछि देखाउन सकिने केही हुन्छ। यसैगरी च्याप्टरले विचारलाई प्रमाणमा बदल्छ।",
     [("Municipal Business Registration Audit", "नगर व्यवसाय दर्ता अडिट", "Time how long it actually takes to register a business in your municipality, publish the number, and compare across the district."),
      ("One Product, One Palika", "एक पालिका, एक उत्पादन", "Identify and document one product each local level could produce competitively, with costs, buyers and constraints."),
      ("Campus–Industry Mapping", "क्याम्पस–उद्योग नक्साङ्कन", "Map what local employers need against what the nearest campus teaches, and publish the gap."),
      ("Border Market Study", "सीमा बजार अध्ययन", "Document what the nearest Indian market buys, at what price, and what Madhesh could supply.")]),
    ("program", "02", "Program", "कार्यक्रम",
     "Continuing streams of work that run across years",
     "वर्षौं चल्ने निरन्तर कामका धारा",
     "A Program does not end. It is the standing infrastructure of the campaign — the things that must happen every year in every district for the conversation to hold.",
     "कार्यक्रम सकिँदैन। यो अभियानको स्थायी पूर्वाधार हो — बहस टिकाउन हरेक वर्ष हरेक जिल्लामा हुनैपर्ने कामहरू।",
     [("District Chapters", "जिल्ला च्याप्टर", "A non-partisan citizen group in each of the 8 districts, meeting monthly, open to anyone."),
      ("Young Entrepreneurs Circle", "युवा उद्यमी वृत्त", "Peer support, mentors and finance navigation for people actually trying to start something."),
      ("Ask Your Mayor", "मेयरलाई सोध्नुहोस्", "A standing civic practice: one economic question, asked publicly, answered publicly, every quarter."),
      ("Economic Journalism Fellowship", "आर्थिक पत्रकारिता फेलोसिप", "Support for local journalists to report on enterprise, jobs and constraints — not only politics.")]),
    ("poll", "03", "Poll", "जनमत",
     "The listening module",
     "सुन्ने मोड्युल",
     "Poll is how the campaign avoids becoming another set of opinions from the capital. It asks, records and publishes what people in Madhesh actually say about their own economy.",
     "राजधानीबाट आउने अर्को मत बन्नबाट अभियानलाई जोगाउने काम जनमत मोड्युलले गर्छ। यसले मधेशका मानिसले आफ्नै अर्थतन्त्रबारे के भन्छन् भन्ने सोध्छ, अभिलेख राख्छ र प्रकाशित गर्छ।",
     [("Youth Work & Migration Survey", "युवा रोजगारी र बसाइँसराइ सर्वेक्षण", "Why people leave, what would make them stay, district by district."),
      ("Small Business Constraints Poll", "साना व्यवसाय अवरोध सर्वेक्षण", "What actually stops a shop, workshop or farm from growing — asked of the owners."),
      ("Town Halls", "नागरिक भेला", "Open public meetings in each municipality where economic questions are put to those in office."),
      ("Citizen Question Bank", "नागरिक प्रश्न बैंक", "A public, growing list of the economic questions citizens want answered.")]),
    ("publication", "04", "Publication", "प्रकाशन",
     "The knowledge module",
     "ज्ञान मोड्युल",
     "Publication is what survives the campaign. Data, briefs and a manual that anyone — including people who disagree with us — can use.",
     "अभियानपछि पनि बाँकी रहने कुरा प्रकाशन हो। तथ्याङ्क, संक्षिप्त अध्ययन र म्यानुअल — जो कोहीले, हामीसँग असहमत हुनेले पनि, प्रयोग गर्न सक्ने।",
     [("136 Local Level Profiles", "१३६ स्थानीय तह प्रोफाइल", "One economic profile per local government: what it produces, employs, taxes and lacks."),
      ("Madhesh Economic Review", "मधेश आर्थिक समीक्षा", "An annual, plain-language account of how the province's economy actually moved."),
      ("The Manual", "म्यानुअल", "How to start a chapter, run a town hall and audit your own municipality — free to copy."),
      ("Municipal Economic Scorecard", "नगरपालिका आर्थिक स्कोरकार्ड", "Businesses registered, survived, jobs created, revenue growth — comparable across all 136.")]),
]


def page_modules():
    secs = []
    for slug, num, en, ne, sub_en, sub_ne, body_en, body_ne, items in MODULES_FULL:
        cards = "".join(
            '<div class="card"><h4>%s</h4><p style="margin-top:8px">%s</p></div>'
            % (t(a, b), c) for a, b, c in items)
        secs.append("""
<section class="section{alt}" id="{slug}">
  <div class="wrap">
    <p class="eyebrow">{eb}</p>
    <h2 style="margin-bottom:.2em">{name}</h2>
    <p class="lede" style="font-size:1.05rem;margin-bottom:1em">{sub}</p>
    <p class="lede">{body}</p>
    <div class="grid grid--2" style="margin-top:30px">{cards}</div>
  </div>
</section>""".format(
            alt=" section--paper2" if num in ("02", "04") else "",
            slug=slug, eb="Module " + num, name=t(en, ne),
            sub=t(sub_en, sub_ne), body=t(body_en, body_ne), cards=cards))

    head = """
<section class="section section--tight" style="background:var(--ink);color:#f2f2f2">
  <div class="wrap narrow">
    <p class="eyebrow">{eb}</p>
    <h1 style="color:#fff;margin-bottom:.3em">{h1}</h1>
    <p class="lede" style="color:#d6d6d6">{lede}</p>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="grid grid--4">{nav}</div>
  </div>
</section>
""".format(
        eb=t("How the campaign is organised", "अभियानको संगठन"),
        h1=t("Four modules", "चार मोड्युल"),
        lede=t("Madhesh Next is deliberately modular. A chapter in Rautahat and a chapter in Saptari run the same four modules, so work is comparable, repeatable and easy for a newcomer to join at any point.",
               "मधेश नेक्स्ट सचेत रूपमा मोड्युलर छ। रौतहटको च्याप्टर र सप्तरीको च्याप्टरले उही चार मोड्युल चलाउँछन् — जसले काम तुलनायोग्य, दोहोर्‍याउन मिल्ने र नयाँ मानिसलाई जुनसुकै बेला जोडिन सजिलो बनाउँछ।"),
        nav="".join(
            '<a class="card" href="#%s"><span class="card__num">%s</span><h3>%s</h3><p>%s</p></a>'
            % (s, n, t(e, ne), t(se, sne))
            for s, n, e, ne, se, sne, _, _, _ in MODULES_FULL),
    )

    tail = """
<section class="section section--dark">
  <div class="wrap narrow">
    <h2>{h}</h2>
    <p class="lede" style="color:#d6d6d6">{p}</p>
    <div class="hero__actions"><a class="btn btn--primary" href="join.html">{c}</a></div>
  </div>
</section>""".format(
        h=t("Every module runs in every district", "हरेक मोड्युल हरेक जिल्लामा चल्छ"),
        p=t("A chapter does not need permission to start. Pick a module, pick your municipality, and begin with one question.",
            "च्याप्टर सुरु गर्न अनुमति चाहिँदैन। एउटा मोड्युल छान्नुहोस्, आफ्नो पालिका छान्नुहोस्, र एउटा प्रश्नबाट सुरु गर्नुहोस्।"),
        c=t("Start a chapter", "च्याप्टर सुरु गर्नुहोस्"))

    return layout("Modules", "मोड्युल", head + "".join(secs) + tail,
                  desc_en="Madhesh Next runs on four modules: Project, Program, Poll and Publication.")


# ---------------------------------------------------------------- districts
def page_districts():
    c = totals()
    rows = []
    for d in DISTRICTS:
        for en, ne, ty in d["lgs"]:
            rows.append((d, en, ne, ty))

    type_opts = "".join(
        '<option value="%s">%s</option>' % (k, TYPE_LABEL[k][0]) for k in ("METRO", "SUB", "MUN", "RM"))
    dist_opts = "".join('<option value="%s">%s</option>' % (d["slug"], d["en"]) for d in DISTRICTS)

    body = """
<section class="section section--tight" style="background:var(--paper-2);border-bottom:1px solid var(--line)">
  <div class="wrap">
    <p class="eyebrow">{eb}</p>
    <h1 style="margin-bottom:.3em">{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="stats">{stats}</div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <h2>{h2a}</h2>
    <div class="dgrid" style="margin-top:24px">{cards}</div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <h2>{h2b}</h2>
    <p class="lede" style="margin-bottom:26px">{ledeb}</p>
    <div class="toolbar">
      <input type="search" data-filter-input placeholder="Search name / नाम खोज्नुहोस्" aria-label="Search local levels">
      <select data-filter-district aria-label="Filter by district"><option value="">{all_d}</option>{dist_opts}</select>
      <select data-filter-type aria-label="Filter by type"><option value="">{all_t}</option>{type_opts}</select>
      <span class="count" data-filter-count></span>
    </div>
    {table}
  </div>
</section>
""".format(
        eb=t("Where the work happens", "काम कहाँ हुन्छ"),
        h1=t("8 districts, 136 local governments", "८ जिल्ला, १३६ स्थानीय तह"),
        lede=t("Madhesh Province is Nepal's smallest province by area and its most densely populated. Every local government here is an economic actor — this is the full list.",
               "मधेश प्रदेश क्षेत्रफलमा नेपालको सबैभन्दा सानो र जनघनत्वमा सबैभन्दा बढी छ। यहाँको हरेक स्थानीय तह एउटा आर्थिक कर्ता हो — यो पूरा सूची हो।"),
        stats="".join([
            stat(str(c["METRO"]), "Metropolitan city", "महानगरपालिका"),
            stat(str(c["SUB"]), "Sub-metropolitan cities", "उपमहानगरपालिका"),
            stat(str(c["MUN"]), "Municipalities", "नगरपालिका"),
            stat(str(c["RM"]), "Rural municipalities", "गाउँपालिका"),
        ]),
        h2a=t("The eight districts", "आठ जिल्ला"),
        cards="".join(dcard(d, base="") for d in DISTRICTS),
        h2b=t("All 136 local levels", "सबै १३६ स्थानीय तह"),
        ledeb=t("Search by name in English or Nepali, or filter by district and type.",
                "अंग्रेजी वा नेपालीमा नाम खोज्नुहोस्, वा जिल्ला र प्रकारअनुसार छान्नुहोस्।"),
        all_d="All districts", all_t="All types",
        dist_opts=dist_opts, type_opts=type_opts,
        table=lg_table(rows, show_district=True),
    )
    return layout("Districts", "जिल्ला", body,
                  desc_en="All 8 districts and 136 local governments of Madhesh Province — searchable in English and Nepali.")


def page_district(d):
    c = {"METRO": 0, "SUB": 0, "MUN": 0, "RM": 0}
    for _, _, ty in d["lgs"]:
        c[ty] += 1
    rows = [(d, en, ne, ty) for en, ne, ty in d["lgs"]]
    idx = [x["slug"] for x in DISTRICTS].index(d["slug"])
    prev_d = DISTRICTS[idx - 1] if idx > 0 else DISTRICTS[-1]
    next_d = DISTRICTS[idx + 1] if idx < len(DISTRICTS) - 1 else DISTRICTS[0]

    body = """
<section class="section section--tight" style="background:var(--ink);color:#f2f2f2">
  <div class="wrap">
    <p class="breadcrumb" style="color:#9b9b9b"><a href="../index.html" style="color:#9b9b9b">{c_home}</a> · <a href="../districts.html" style="color:#9b9b9b">{c_dist}</a></p>
    <p class="eyebrow">{prov}</p>
    <h1 style="color:#fff;margin-bottom:.12em">{en}</h1>
    <p style="font-size:1.4rem;color:#d6d6d6;margin-bottom:1em">{ne}</p>
    <p class="lede" style="color:#d6d6d6">{note}</p>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="stats">{stats}</div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <h2>{h2}</h2>
    <p class="lede" style="margin-bottom:24px">{lede}</p>
    <div class="toolbar">
      <input type="search" data-filter-input placeholder="Search name / नाम खोज्नुहोस्" aria-label="Search local levels">
      <select data-filter-type aria-label="Filter by type"><option value="">All types</option>{type_opts}</select>
      <span class="count" data-filter-count></span>
    </div>
    {table}
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <h2>{h3}</h2>
    <p class="lede">{l3}</p>
    <ul class="qlist" style="max-width:70ch">{qs}</ul>
    <div class="hero__actions">
      <a class="btn btn--dark" href="../join.html">{cta}</a>
      <a class="btn btn--line" href="../modules.html">{cta2}</a>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap" style="display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap">
    <a class="btn btn--line" href="{prev}.html">← {prev_n}</a>
    <a class="btn btn--line" href="{next}.html">{next_n} →</a>
  </div>
</section>
""".format(
        c_home=t("Home", "गृहपृष्ठ"), c_dist=t("Districts", "जिल्ला"),
        prov=t("Madhesh Province", "मधेश प्रदेश"),
        en=t(d["en"], d["ne"]), ne=t(d["ne"], d["en"]), note=t(d["note_en"], d["note_ne"]),
        stats="".join([
            stat("{:,}".format(d["pop"]), "Population (2021)", "जनसंख्या (२०२१)"),
            stat("{:,}".format(d["area"]), "km² area", "वर्ग कि.मी."),
            stat(str(len(d["lgs"])), "Local levels", "स्थानीय तह"),
            stat(d["lit"], "Literacy rate", "साक्षरता दर"),
            stat(str(round(d["pop"] / d["area"])), "People per km²", "प्रति वर्ग कि.मी."),
        ]),
        h2=t("Local governments of %s" % d["en"], "%s का स्थानीय तह" % d["ne"]),
        lede=t("%d local levels — %d municipal and %d rural. Headquarters: %s."
               % (len(d["lgs"]), c["METRO"] + c["SUB"] + c["MUN"], c["RM"], d["hq_en"]),
               "%d स्थानीय तह — %d सहरी र %d गाउँपालिका। सदरमुकाम: %s।"
               % (len(d["lgs"]), c["METRO"] + c["SUB"] + c["MUN"], c["RM"], d["hq_ne"])),
        type_opts="".join('<option value="%s">%s</option>' % (k, TYPE_LABEL[k][0])
                          for k in ("METRO", "SUB", "MUN", "RM") if c[k]),
        table=lg_table(rows, show_district=False),
        h3=t("Questions for %s" % d["en"], "%s का लागि प्रश्नहरू" % d["ne"]),
        l3=t("Every district chapter starts here. These are the questions a Madhesh Next chapter puts to local government, and publishes the answers to.",
             "हरेक जिल्ला च्याप्टर यहीँबाट सुरु हुन्छ। मधेश नेक्स्ट च्याप्टरले स्थानीय सरकारलाई सोध्ने र उत्तर सार्वजनिक गर्ने प्रश्नहरू यी हुन्।"),
        qs="".join("<li>%s</li>" % t(a, b) for a, b in [
            ("How many new businesses registered in each of our %d local levels last year — and how many survived?" % len(d["lgs"]),
             "गत वर्ष हाम्रा %d स्थानीय तहमध्ये प्रत्येकमा कति नयाँ व्यवसाय दर्ता भए — र कति टिके?" % len(d["lgs"])),
            ("What does %s produce that it could sell competitively across the border?" % d["en"],
             "%s ले सीमापारि प्रतिस्पर्धी रूपमा बेच्न सक्ने के उत्पादन गर्छ?" % d["ne"]),
            ("How long does it take to register a business in %s, in days?" % d["hq_en"],
             "%s मा व्यवसाय दर्ता गर्न कति दिन लाग्छ?" % d["hq_ne"]),
            ("What do our campuses teach, and what do our employers actually need?",
             "हाम्रा क्याम्पसले के पढाउँछन्, र हाम्रा रोजगारदातालाई वास्तवमा के चाहिन्छ?"),
            ("How many young people left this district last year, and what would have made them stay?",
             "गत वर्ष यो जिल्लाबाट कति युवा बाहिरिए, र के भएको भए तिनी रहन्थे?"),
        ]),
        cta=t("Start the %s chapter" % d["en"], "%s च्याप्टर सुरु गर्नुहोस्" % d["ne"]),
        cta2=t("See the modules", "मोड्युल हेर्नुहोस्"),
        prev=prev_d["slug"], prev_n=prev_d["en"], next=next_d["slug"], next_n=next_d["en"],
    )
    return layout(d["en"], d["ne"], body, base="../",
                  desc_en="%s district, Madhesh Province — %s local governments, population %s. Part of the Madhesh Next campaign."
                          % (d["en"], len(d["lgs"]), "{:,}".format(d["pop"])))


# ---------------------------------------------------------------- conveners
def page_conveners():
    body = """
<section class="section section--tight" style="background:var(--paper-2);border-bottom:1px solid var(--line)">
  <div class="wrap narrow">
    <p class="eyebrow">{eb}</p>
    <h1 style="margin-bottom:.3em">{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="people">{cards}</div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap narrow">
    <h2>{h2}</h2>
    {p}
  </div>
</section>

<section class="section section--dark">
  <div class="wrap narrow center">
    <h2>{h3}</h2>
    <p class="lede" style="color:#d6d6d6;margin:0 auto 26px">{p3}</p>
    <a class="btn btn--primary" href="join.html">{c3}</a>
  </div>
</section>
""".format(
        eb=t("Campaign conveners", "अभियान संयोजक"),
        h1=t("Who convenes Madhesh Next", "मधेश नेक्स्टका संयोजक"),
        lede=t("Conveners do not lead the campaign — they convene it. Their job is to keep it non-partisan, keep it open, and make sure every district can run without waiting for anyone.",
               "संयोजकहरूले अभियानको नेतृत्व गर्दैनन् — तिनले यसलाई जुटाउँछन्। तिनको काम यसलाई गैर-दलीय र खुला राख्नु, र हरेक जिल्लाले कसैको प्रतीक्षा नगरी चल्न सक्ने बनाउनु हो।"),
        cards="".join(person_card(p) for p in CONVENERS),
        h2=t("What a convener does — and does not do", "संयोजकले के गर्छन् — र के गर्दैनन्"),
        p=blocks(
            "<ul class='qlist'>"
            "<li><strong>Does:</strong> convene meetings, hold the campaign to its non-partisan commitment, help district chapters start, and answer for what has and has not been delivered.</li>"
            "<li><strong>Does not:</strong> speak for any political party, endorse candidates, control what a district chapter decides to work on, or own the campaign's material — everything Madhesh Next publishes is free to copy.</li>"
            "</ul>"
            "<p>Conveners are accountable to the same question the campaign asks of everyone else: what did you actually make easier this year?</p>",
            "<ul class='qlist'>"
            "<li><strong>गर्छन्:</strong> बैठक जुटाउने, अभियानलाई गैर-दलीय प्रतिबद्धतामा राख्ने, जिल्ला च्याप्टर सुरु गर्न सघाउने, र के भयो–के भएन भन्नेमा जवाफ दिने।</li>"
            "<li><strong>गर्दैनन्:</strong> कुनै दलका तर्फबाट बोल्ने, उम्मेदवारलाई समर्थन गर्ने, जिल्ला च्याप्टरले के काम गर्ने भन्ने नियन्त्रण गर्ने, वा अभियानको सामग्रीमाथि स्वामित्व जनाउने — मधेश नेक्स्टले प्रकाशित गर्ने सबै सामग्री स्वतन्त्र रूपमा प्रतिलिपि गर्न पाइन्छ।</li>"
            "</ul>"
            "<p>संयोजकहरू पनि अभियानले अरूलाई सोध्ने त्यही प्रश्नप्रति उत्तरदायी छन्: तपाईंले यो वर्ष वास्तवमा के सजिलो बनाउनुभयो?</p>"),
        h3=t("District conveners wanted", "जिल्ला संयोजक चाहिएको छ"),
        p3=t("Each of the 8 districts needs its own convener, and each of the 136 local levels needs at least one person willing to ask one question.",
             "८ मध्ये हरेक जिल्लालाई आफ्नै संयोजक चाहिन्छ, र १३६ स्थानीय तहमध्ये हरेकलाई एउटा प्रश्न सोध्न तयार कम्तीमा एक व्यक्ति चाहिन्छ।"),
        c3=t("Volunteer as a convener", "संयोजकका रूपमा स्वयंसेवा गर्नुहोस्"),
    )
    return layout("Conveners", "संयोजक", body,
                  desc_en="Campaign conveners of Madhesh Next: Prashant Singh, Anil Mahaseth, Sanjog Dev, Ajay Pandey and Bala Krishna.")


# -------------------------------------------------------------------- media
def page_media():
    posts = [
        ("Founding note", "स्थापना दस्तावेज",
         "Public discourse must shift to economy", "सार्वजनिक विमर्श अर्थतन्त्रतर्फ सर्नुपर्छ",
         "The full argument behind Madhesh Next — why identity politics and economic ambition are not competing agendas.",
         "मधेश नेक्स्टको पूरा तर्क — पहिचानको राजनीति र आर्थिक महत्त्वाकांक्षा किन प्रतिस्पर्धी एजेन्डा होइनन्।",
         "manifesto.html", "Prashant Singh"),
        ("Explainer", "व्याख्या",
         "Middle-class poverty, and why a tea shop is a statistic", "मध्यमवर्गीय गरिबी, र चिया पसल किन तथ्याङ्क हो",
         "What the scarcity of ordinary urban businesses tells us about purchasing power in Madhesh's towns.",
         "मधेशका सहरमा सामान्य सहरी व्यवसायको अभावले क्रयशक्तिबारे के भन्छ।",
         "manifesto.html#", ""),
        ("Data", "तथ्याङ्क",
         "All 136 local governments of Madhesh, in one place", "मधेशका सबै १३६ स्थानीय तह, एकै ठाउँमा",
         "A searchable reference of every metropolitan city, sub-metropolitan city, municipality and rural municipality in the province.",
         "प्रदेशका हरेक महानगर, उपमहानगर, नगरपालिका र गाउँपालिकाको खोजयोग्य सन्दर्भ।",
         "districts.html", ""),
        ("Framework", "ढाँचा",
         "Roads for what? Economic connectivity vs. connectivity", "सडक केका लागि? जोडाइ बनाम आर्थिक जोडाइ",
         "Nepal built the roads. The next question is which direction the goods travel — and who processes them.",
         "नेपालले सडक बनायो। अबको प्रश्न हो — सामान कुन दिशामा जान्छ, र प्रशोधन कसले गर्छ।",
         "manifesto.html#", ""),
    ]
    cards = "".join("""
<a class="card" href="{link}">
  <span class="card__num">{tag}</span>
  <h3>{title}</h3>
  <p>{blurb}</p>
  <div class="card__meta"><span>{author}</span></div>
</a>""".format(link=link, tag=t(tag_en, tag_ne), title=t(ti_en, ti_ne),
               blurb=t(b_en, b_ne), author=author or t("Madhesh Next", "मधेश नेक्स्ट"))
        for tag_en, tag_ne, ti_en, ti_ne, b_en, b_ne, link, author in posts)

    body = """
<section class="section section--tight" style="background:var(--paper-2);border-bottom:1px solid var(--line)">
  <div class="wrap narrow">
    <p class="eyebrow">{eb}</p>
    <h1 style="margin-bottom:.3em">{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid--2">{cards}</div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="grid grid--2" style="gap:48px">
      <div>
        <h2>{h2}</h2>
        {p}
      </div>
      <div class="callout">
        <h4 style="margin-bottom:10px">{h3}</h4>
        <p style="font-size:.95rem">{p3}</p>
        <p style="font-size:.95rem;margin-bottom:0"><a href="mailto:press@madheshnext.org">press@madheshnext.org</a></p>
      </div>
    </div>
  </div>
</section>
""".format(
        eb=t("Media & publications", "मिडिया र प्रकाशन"),
        h1=t("What we publish", "हामी के प्रकाशित गर्छौं"),
        lede=t("Everything Madhesh Next publishes is free to copy, translate, reprint and argue with. Attribution is welcome but not required.",
               "मधेश नेक्स्टले प्रकाशित गर्ने सबै सामग्री प्रतिलिपि, अनुवाद, पुनर्मुद्रण र खण्डन गर्न स्वतन्त्र छ। स्रोत उल्लेख स्वागतयोग्य छ तर अनिवार्य होइन।"),
        cards=cards,
        h2=t("For journalists", "पत्रकारका लागि"),
        p=blocks(
            "<p>Madhesh Next exists partly because economic reporting in Madhesh is thin. If you write about enterprise, jobs, municipal budgets or migration in any of the 8 districts, our data is yours to use.</p>"
            "<p>We can provide: local-level economic profiles, contacts in district chapters, survey microdata where consent allows, and background briefings on request. We do not pay for coverage and we do not ask for approval over what you write.</p>",
            "<p>मधेश नेक्स्ट आंशिक रूपमा यसैले छ कि मधेशमा आर्थिक रिपोर्टिङ पातलो छ। तपाईं ८ मध्ये कुनै पनि जिल्लामा उद्यम, रोजगारी, नगर बजेट वा बसाइँसराइबारे लेख्नुहुन्छ भने हाम्रो तथ्याङ्क तपाईंको हो।</p>"
            "<p>हामी दिन सक्छौं: स्थानीय तह आर्थिक प्रोफाइल, जिल्ला च्याप्टरका सम्पर्क, सहमति भएसम्म सर्वेक्षणको सूक्ष्म तथ्याङ्क, र अनुरोधमा पृष्ठभूमि ब्रिफिङ। हामी समाचारका लागि भुक्तानी गर्दैनौं र तपाईंले के लेख्ने भन्नेमा स्वीकृति माग्दैनौं।</p>"),
        h3=t("Press enquiries", "प्रेस जिज्ञासा"),
        p3=t("Interviews with conveners, district data requests and event information.",
             "संयोजकसँग अन्तर्वार्ता, जिल्ला तथ्याङ्क अनुरोध र कार्यक्रम जानकारी।"),
    )
    return layout("Media", "मिडिया", body,
                  desc_en="Publications, data and press resources from the Madhesh Next campaign.")


# --------------------------------------------------------------------- join
def page_join():
    dist_opts = "".join('<option value="%s">%s</option>' % (d["en"], d["en"]) for d in DISTRICTS)
    ways = [
        ("Start a district or palika chapter", "जिल्ला वा पालिका च्याप्टर सुरु गर्नुहोस्",
         "Gather five non-partisan people in your municipality. Pick one module. Meet monthly. We will send you the manual."),
        ("Contribute data", "तथ्याङ्क दिनुहोस्",
         "Business registration numbers, budget documents, price lists, employer needs — anything that makes a local economy legible."),
        ("Write or report", "लेख्नुहोस् वा रिपोर्ट गर्नुहोस्",
         "Local journalists, students and researchers documenting enterprise and jobs in any of the 8 districts."),
        ("Ask one question", "एउटा प्रश्न सोध्नुहोस्",
         "The smallest useful contribution: put one economic question to your mayor or ward chair this month, publicly."),
    ]
    body = """
<section class="section section--tight" style="background:var(--ink);color:#f2f2f2">
  <div class="wrap narrow">
    <p class="eyebrow">{eb}</p>
    <h1 style="color:#fff;margin-bottom:.3em">{h1}</h1>
    <p class="lede" style="color:#d6d6d6">{lede}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>{h2}</h2>
    <div class="grid grid--2" style="margin-top:26px">{ways}</div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="grid grid--2" style="gap:52px;align-items:start">
      <div>
        <h2>{h3}</h2>
        <p class="lede">{p3}</p>
        <form class="form" data-demo-form>
          <div class="field"><label>{f_name}</label><input type="text" name="name" required></div>
          <div class="field"><label>{f_email}</label><input type="email" name="email" required></div>
          <div class="field"><label>{f_dist}</label>
            <select name="district"><option value="">—</option>{dist_opts}</select></div>
          <div class="field"><label>{f_pal}</label><input type="text" name="palika" placeholder="e.g. Lalbandi Municipality"></div>
          <div class="field"><label>{f_how}</label>
            <select name="how">
              <option>{o1}</option><option>{o2}</option><option>{o3}</option><option>{o4}</option>
            </select></div>
          <div class="field"><label>{f_msg}</label><textarea name="message" placeholder="{ph}"></textarea></div>
          <div><button class="btn btn--dark" type="submit">{submit}</button></div>
          <p class="note" data-form-msg hidden></p>
          <p class="note">{note}</p>
        </form>
      </div>
      <div>
        <div class="callout" style="margin-bottom:22px">
          <h4 style="margin-bottom:10px">{c1h}</h4>
          <p style="font-size:.95rem;margin-bottom:0">{c1p}</p>
        </div>
        <div class="card">
          <h4 style="margin-bottom:12px">{c2h}</h4>
          <p style="font-size:.95rem"><a href="mailto:hello@madheshnext.org">hello@madheshnext.org</a><br>
          <a href="mailto:press@madheshnext.org">press@madheshnext.org</a></p>
          <p style="font-size:.95rem;margin-bottom:0" class="muted">{c2p}</p>
        </div>
      </div>
    </div>
  </div>
</section>
""".format(
        eb=t("Join the campaign", "अभियानमा सहभागी हुनुहोस्"),
        h1=t("You do not need permission to start.", "सुरु गर्न अनुमति चाहिँदैन।"),
        lede=t("Madhesh Next has no membership fee, no party affiliation and no central approval. If you live in Madhesh — or care about it — there is a way in.",
               "मधेश नेक्स्टमा सदस्यता शुल्क छैन, दलीय आबद्धता छैन, केन्द्रीय स्वीकृति चाहिँदैन। तपाईं मधेशमा बस्नुहुन्छ — वा मधेशको वास्ता गर्नुहुन्छ — भने जोडिने बाटो छ।"),
        h2=t("Four ways to take part", "सहभागी हुने चार बाटा"),
        ways="".join(
            '<div class="card"><span class="card__num">%02d</span><h3>%s</h3><p>%s</p></div>' % (i + 1, t(a, b), c)
            for i, (a, b, c) in enumerate(ways)),
        h3=t("Get in touch", "सम्पर्क गर्नुहोस्"),
        p3=t("Tell us where you are and what you want to work on. A convener will get back to you.",
             "तपाईं कहाँ हुनुहुन्छ र के काम गर्न चाहनुहुन्छ भन्नुहोस्। संयोजकले सम्पर्क गर्नेछन्।"),
        f_name=t("Name", "नाम"), f_email=t("Email", "इमेल"),
        f_dist=t("District", "जिल्ला"), f_pal=t("Municipality / Rural municipality", "नगरपालिका / गाउँपालिका"),
        f_how=t("How do you want to take part?", "कसरी सहभागी हुन चाहनुहुन्छ?"),
        o1="Start a chapter", o2="Contribute data", o3="Write or report", o4="Something else",
        f_msg=t("Message", "सन्देश"),
        ph="What economic question would you most like answered where you live?",
        submit=t("Send", "पठाउनुहोस्"),
        note=t("This form is a demo. Connect a form endpoint (Formspree, Netlify Forms, Google Forms) before publishing.",
               "यो फारम डेमो हो। प्रकाशन गर्नुअघि फारम इन्डपोइन्ट जोड्नुहोस्।"),
        dist_opts=dist_opts,
        c1h=t("The only rule", "एउटै नियम"),
        c1p=t("Chapters are non-partisan. Members may belong to any party or none, but a chapter does not campaign for candidates, and does not use the Madhesh Next name for party work.",
              "च्याप्टर गैर-दलीय हुन्छन्। सदस्य कुनै पनि दलमा वा कुनै दलमा नरहेका हुन सक्छन्, तर च्याप्टरले उम्मेदवारका लागि प्रचार गर्दैन र दलीय कामका लागि मधेश नेक्स्टको नाम प्रयोग गर्दैन।"),
        c2h=t("Direct contact", "प्रत्यक्ष सम्पर्क"),
        c2p=t("Replies usually within a week.", "सामान्यतया एक हप्ताभित्र जवाफ।"),
    )
    return layout("Join", "सहभागी", body,
                  desc_en="Join Madhesh Next — start a chapter, contribute data, write, or ask one economic question where you live.")


# -------------------------------------------------------------------- write
def write(path, html):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))

    made = [
        write("index.html", page_home()),
        write("manifesto.html", page_manifesto()),
        write("vision.html", page_vision()),
        write("modules.html", page_modules()),
        write("districts.html", page_districts()),
        write("conveners.html", page_conveners()),
        write("media.html", page_media()),
        write("join.html", page_join()),
    ]
    for d in DISTRICTS:
        made.append(write("districts/%s.html" % d["slug"], page_district(d)))

    # sitemap + robots
    urls = "".join("<url><loc>https://madheshnext.org/%s</loc></url>" % p for p in made)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % urls)
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: https://madheshnext.org/sitemap.xml\n")
    write("CNAME", "madheshnext.org\n")

    print("Built %d pages into %s" % (len(made), OUT))
    for p in made:
        print("  ", p)


if __name__ == "__main__":
    main()
