#!/usr/bin/env python3
"""Pitchbird lead-magnet PDF generator — v2, brand-corrected.

Brand spec (from Figma file APBB7O5bxfboLWeg2FbXgY):
  - Navy #03112A, Gold #FBB03B
  - Headlines: Product Sans (Google-internal) → Mulish 700 as web sub
  - Body: Arial Regular/Bold (universal)
  - Header band: 155px navy, actual Pitchbird logo left, URL right
  - Callout cards: pastel panels + script-pill label + emoji + bold heading
  - Page-nav: dot-matrix chevron, bottom-right
"""
import argparse, subprocess, pathlib

ROOT = pathlib.Path("/root/pitchbird/lm")
IMG = pathlib.Path("/root/pitchbird/lm-images/one-pager")

META = {
    "one-pager": {
        "slug": "one-pager",
        "title": "The Power of the One Pager",
        "subtitle": "Capturing your startup in a single, investor-ready snapshot",
        "author": "Magdalena Reith · Founder, Pitchbird",
        "stat": "32%",
        "stat_caption": "of decision-makers drop off after 15 seconds of reading a one-pager.",
        "stat_source": "Storydoc, 2024",
        "must_haves": [
            ("Company name & logo", "Identity is the anchor. Investors know who they're dealing with before they read a single word."),
            ("Contact information", "The most-skipped basic. If they can't reach you in one click, the document did nothing."),
            ("Company profile", "A short, informative introduction — what you are, who you serve, why you exist."),
            ("Business idea", "Describe the core concept in one tight sentence. No jargon, no hedging."),
            ("Unique selling proposition", "What makes this venture distinct from the next ten emails in the inbox."),
            ("Roadmap & timeline", "Graphically show where the business is going and when. Visual beats prose here."),
            ("Investment ask", "The amount needed, the structure (one-time or tranches), and the deadline. Specific."),
            ("Investment highlights", "The three or four reasons this allocation pays back. Punchy, not vague."),
        ],
        "nice_callouts": [
            ("Problem", "peach", "🎯", "Frame the pain in market terms before you frame yourself.", "Investors connect with the problem first. Make them feel it before you sell the cure."),
            ("Solution", "blue", "💊", "Show how your business removes that pain. Two lines, max.", "Lead with the outcome — not the mechanism. Save the how for the deck."),
            ("Traction", "green", "📈", "Prove customers want it. Revenue, signups, LOIs — whichever you have.", "Proof beats promise. One data point trumps a paragraph of optimism."),
            ("Market", "lavender", "🌍", "Who you sell to, and the competitive landscape they live in.", "Investors want a beachhead, not 'everyone'. Show the wedge first."),
        ],
        "design_principles": [
            ("Content is king", "Clarity first. Strong narrative — problem, solution, impact. Hierarchy via headings, sub-heads, and bullets that guide the eye."),
            ("Visually appealing", "Clean composition, generous white space, strategic visuals over walls of text. Colour evokes brand, not chaos."),
            ("Remember your audience", "Investors scan, not read. Lead with what helps their decision. Professional, confident tone throughout."),
            ("Call to action", "End with one specific ask. 'Schedule a 20-minute call.' Not 'we'd love to chat sometime.'"),
        ],
        "advantages": [
            "Respects the investor's time — and signals you respect it too.",
            "Forces sharper thinking. If it doesn't fit on a page, the idea isn't focused yet.",
            "Travels well — easy to forward, print, remember.",
        ],
        "limitations": [
            "Brevity is unforgiving. Every missing detail is a potential rejection.",
            "Hard to write alone — outside eyes catch what founder-bias hides.",
            "Not a substitute for the full deck. It is the door, not the room.",
        ],
    },
}


# ---------- shared building blocks ----------

LOGO = f"file://{IMG / 'pitchbird-logo.png'}"


def header(url):
    return f"""
<div class="hdr">
  <img class="hdr-logo" src="{LOGO}" alt="Pitchbird">
  <div class="hdr-url">{url}</div>
</div>"""


# small dot-matrix right-chevron made from a 6x9 grid of dots
def page_arrow():
    rows = [
        "100000000",
        "110000000",
        "111000000",
        "111100000",
        "111110000",
        "111100000",
        "111000000",
        "110000000",
        "100000000",
    ]
    dots = []
    cell = 4
    for ry, r in enumerate(rows):
        for rx, c in enumerate(r):
            if c == "1":
                dots.append(
                    f'<circle cx="{rx*cell+2}" cy="{ry*cell+2}" r="1.4" fill="#03112A"/>'
                )
    svg = (
        f'<svg width="36" height="36" viewBox="0 0 {9*cell} {9*cell}" '
        f'xmlns="http://www.w3.org/2000/svg">{"".join(dots)}</svg>'
    )
    return svg


def kicker(num, label):
    """Gold 'Slide X:' style heading kicker."""
    return f'<div class="kicker"><span class="kicker-num">{num}</span><span class="kicker-label">{label}</span></div>'


def callout_card(theme, label, emoji, headline, body):
    """Pain-Point/Solutions style card. theme in: peach, blue, green, lavender."""
    return f"""
<div class="callout callout-{theme}">
  <div class="callout-head-row">
    <div class="callout-pill"><span class="callout-pill-label">{label}</span></div>
    <div class="callout-emoji">{emoji}</div>
  </div>
  <div class="callout-headline">{headline}</div>
  <div class="callout-body">{body}</div>
</div>"""


# ---------- page HTML ----------

def html(meta):
    img_path = lambda name: f"file://{IMG / (name + '.png')}"

    must_have_items = "".join(
        f"""<div class="mh-row">
              <div class="mh-num">{str(i+1).zfill(2)}</div>
              <div class="mh-body">
                <div class="mh-title">{title}</div>
                <div class="mh-desc">{desc}</div>
              </div>
            </div>"""
        for i, (title, desc) in enumerate(meta["must_haves"])
    )

    callouts = "".join(
        callout_card(theme, label, emoji, headline, body)
        for label, theme, emoji, headline, body in meta["nice_callouts"]
    )

    principles = "".join(
        f"""<div class="pr">
              <div class="pr-dot"></div>
              <div>
                <div class="pr-title">{title}</div>
                <div class="pr-desc">{desc}</div>
              </div>
            </div>"""
        for title, desc in meta["design_principles"]
    )

    adv = "".join(f"<li>{x}</li>" for x in meta["advantages"])
    lim = "".join(f"<li>{x}</li>" for x in meta["limitations"])

    arrow = page_arrow()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{meta['title']} — Pitchbird</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mulish:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root {{
  --navy: #03112A;
  --gold: #FBB03B;
  --paper: #FFFFFF;
  --ink: #03112A;
  --ink-2: #1F2742;
  --muted: #5B6377;
  --line: rgba(3,17,42,0.10);

  --c-peach-bg:   #FCEFDC;
  --c-peach-pill: #FBB03B;
  --c-peach-ink:  #2B1A02;

  --c-blue-bg:    #DDF1FB;
  --c-blue-pill:  #2A98D9;
  --c-blue-ink:   #08243A;

  --c-green-bg:   #DEF4E4;
  --c-green-pill: #25A05A;
  --c-green-ink:  #0C2818;

  --c-lavender-bg:   #EAE3F7;
  --c-lavender-pill: #8166C9;
  --c-lavender-ink:  #1F1438;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
@page {{ size: A4 portrait; margin: 0; }}
html, body {{
  font-family: Arial, 'Mulish', sans-serif;
  color: var(--ink);
  background: var(--paper);
  font-size: 11pt;
  line-height: 1.45;
  letter-spacing: -0.01em;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}}
strong, b {{ font-weight: 700; color: var(--ink); }}

.page {{
  width: 210mm;
  height: 297mm;
  position: relative;
  overflow: hidden;
  page-break-after: always;
  background: var(--paper);
}}
.page:last-child {{ page-break-after: auto; }}

/* ===== Header band ===== */
.hdr {{
  height: 22mm;
  background: var(--navy);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 18mm;
}}
.hdr-logo {{ height: 14mm; width: auto; }}
.hdr-url {{
  font-family: Arial, sans-serif;
  font-size: 10pt;
  color: rgba(255,255,255,0.85);
  letter-spacing: 0.01em;
}}
.hdr-divider {{
  height: 0.7mm;
  background: var(--gold);
  width: 100%;
}}

/* ===== Body ===== */
.body {{ padding: 14mm 18mm 12mm; }}

.kicker {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 22pt;
  letter-spacing: -0.02em;
  margin-bottom: 6mm;
  line-height: 1.1;
}}
.kicker-num {{ color: var(--gold); }}
.kicker-label {{ color: var(--ink); margin-left: 0.2em; }}

h2 {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 30pt;
  line-height: 1.12;
  color: var(--ink);
  letter-spacing: -0.025em;
  margin-bottom: 5mm;
}}
h3 {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 17pt;
  line-height: 1.2;
  color: var(--ink);
  letter-spacing: -0.02em;
  margin-bottom: 3mm;
}}
p {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.55; color: var(--ink-2); }}

/* ===== Footer w/ page arrow + page number ===== */
.foot {{
  position: absolute;
  bottom: 10mm;
  left: 18mm;
  right: 18mm;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: Arial, sans-serif;
  font-size: 9pt;
  color: rgba(3,17,42,0.5);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}}
.foot-right {{ display: flex; align-items: center; gap: 4mm; }}
.page-num {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 14pt;
  color: var(--ink);
  letter-spacing: 0;
}}
.foot-arrow svg {{ display: block; }}

/* ===== COVER ===== */
.cover {{
  background: var(--navy);
  color: var(--paper);
  height: 297mm;
  position: relative;
  overflow: hidden;
}}
.cover-band {{
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 22mm;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 18mm;
  z-index: 3;
}}
.cover-band img {{ height: 14mm; }}
.cover-band .hdr-url {{ color: rgba(255,255,255,0.85); }}

.cover-gold-tri {{
  position: absolute;
  top: 0; right: 0;
  width: 0; height: 0;
  border-style: solid;
  border-width: 0 95mm 95mm 0;
  border-color: transparent var(--gold) transparent transparent;
}}
.cover-gold-corner {{
  position: absolute;
  bottom: 0; left: 0;
  width: 0; height: 0;
  border-style: solid;
  border-width: 0 0 75mm 65mm;
  border-color: transparent transparent var(--gold) transparent;
}}

.cover-mark {{
  position: absolute;
  top: 105mm;
  right: 22mm;
  width: 78mm;
  height: 78mm;
}}
.cover-mark .ring-1 {{
  position: absolute; inset: 0;
  border-radius: 50%;
  background: var(--gold);
}}
.cover-mark .ring-2 {{
  position: absolute; inset: 14mm;
  border-radius: 50%;
  background: #2A98D9;
}}
.cover-mark .ring-3 {{
  position: absolute; inset: 26mm;
  border-radius: 50%;
  background: var(--navy);
  border: 2px solid rgba(255,255,255,0.05);
}}

.cover-inner {{
  position: absolute;
  inset: 0;
  padding: 40mm 22mm 32mm;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  z-index: 2;
}}
.cover-tag {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 11pt;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 10mm;
}}
.cover-title {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 58pt;
  line-height: 1.02;
  color: var(--paper);
  letter-spacing: -0.035em;
  max-width: 160mm;
  margin-bottom: 8mm;
}}
.cover-sub {{
  font-family: Arial, sans-serif;
  font-size: 14pt;
  line-height: 1.5;
  color: rgba(255,255,255,0.78);
  max-width: 130mm;
  margin-bottom: 14mm;
}}
.cover-author {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 10pt;
  letter-spacing: 0.18em;
  color: rgba(255,255,255,0.65);
  text-transform: uppercase;
}}

/* ===== LEDE ===== */
.lede {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 14pt;
  line-height: 1.4;
  color: var(--ink);
  margin-bottom: 7mm;
  letter-spacing: -0.015em;
}}

/* ===== STAT CARD ===== */
.stat-card {{
  background: #F8F1E0;
  padding: 8mm 10mm;
  border-radius: 4mm;
  margin-top: 4mm;
}}
.stat-num {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 58pt;
  line-height: 1;
  color: var(--navy);
  letter-spacing: -0.04em;
  margin-bottom: 3mm;
}}
.stat-text {{
  font-family: Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.45;
  color: var(--ink);
}}
.stat-source {{
  font-family: Arial, sans-serif;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
  margin-top: 3mm;
}}

/* ===== TWO COL ===== */
.two-col {{ display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 12mm; }}
.illus {{
  background: #F8F1E0;
  border-radius: 4mm;
  padding: 8mm;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 88mm;
}}
.illus img {{ max-width: 100%; max-height: 100%; }}
.illus-cap {{
  font-family: Arial, sans-serif;
  font-style: italic;
  color: var(--muted);
  font-size: 10pt;
  margin-top: 4mm;
}}

/* ===== Must-have grid ===== */
.mh-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4mm 8mm;
  margin-top: 4mm;
}}
.mh-row {{
  display: flex;
  gap: 4mm;
  padding: 4mm 0;
  border-top: 1.4pt solid var(--line);
}}
.mh-num {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 26pt;
  color: var(--gold);
  line-height: 1;
  min-width: 16mm;
  letter-spacing: -0.02em;
}}
.mh-title {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 11.5pt;
  margin-bottom: 1mm;
  color: var(--ink);
  letter-spacing: -0.01em;
}}
.mh-desc {{
  font-family: Arial, sans-serif;
  font-size: 9.7pt;
  line-height: 1.45;
  color: var(--ink-2);
}}

/* ===== Callout cards ===== */
.callouts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-top: 4mm; margin-bottom: 6mm; }}
.callout {{
  border-radius: 3mm;
  padding: 5mm 6mm 5mm 6mm;
  position: relative;
}}
.callout-head-row {{
  display: flex;
  align-items: center;
  gap: 3mm;
  margin-bottom: 3mm;
}}
.callout-pill {{
  display: inline-block;
  padding: 1.2mm 3mm;
  border-radius: 2mm;
  transform: rotate(-2deg);
}}
.callout-pill-label {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 9pt;
  font-style: italic;
  letter-spacing: -0.01em;
}}
.callout-emoji {{ font-size: 13pt; }}
.callout-headline {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 11pt;
  line-height: 1.2;
  margin-bottom: 2mm;
  letter-spacing: -0.015em;
}}
.callout-body {{
  font-family: Arial, sans-serif;
  font-size: 9pt;
  line-height: 1.4;
  color: var(--ink-2);
}}

.callout-peach    {{ background: var(--c-peach-bg); }}
.callout-peach .callout-pill {{ background: var(--c-peach-pill); }}
.callout-peach .callout-pill-label {{ color: var(--c-peach-ink); }}

.callout-blue     {{ background: var(--c-blue-bg); }}
.callout-blue .callout-pill {{ background: var(--c-blue-pill); }}
.callout-blue .callout-pill-label {{ color: #fff; }}

.callout-green    {{ background: var(--c-green-bg); }}
.callout-green .callout-pill {{ background: var(--c-green-pill); }}
.callout-green .callout-pill-label {{ color: #fff; }}

.callout-lavender {{ background: var(--c-lavender-bg); }}
.callout-lavender .callout-pill {{ background: var(--c-lavender-pill); }}
.callout-lavender .callout-pill-label {{ color: #fff; }}

/* ===== Principles ===== */
.principles {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 8mm; margin-top: 4mm; }}
.pr {{
  display: flex; gap: 4mm; align-items: flex-start;
  padding-top: 4mm;
  border-top: 1.4pt solid var(--line);
}}
.pr-dot {{
  width: 5mm; height: 5mm;
  background: var(--gold);
  border-radius: 50%;
  margin-top: 1.5mm;
  flex-shrink: 0;
}}
.pr-title {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 11pt;
  letter-spacing: -0.01em;
  margin-bottom: 1mm;
}}
.pr-desc {{
  font-family: Arial, sans-serif;
  font-size: 9.5pt;
  line-height: 1.5;
  color: var(--ink-2);
}}

/* ===== Close ===== */
.close {{ background: var(--navy); color: var(--paper); height: 297mm; position: relative; overflow: hidden; }}
.close .body {{ color: var(--paper); }}
.close h2 {{ color: var(--paper); }}
.close p {{ color: rgba(255,255,255,0.78); }}
.close strong {{ color: var(--paper); }}
.close .kicker-label {{ color: var(--paper); }}
.adv-lim {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10mm; margin-top: 6mm; }}
.adv-lim h3 {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 10pt;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  margin-bottom: 5mm;
}}
.adv-lim .adv h3 {{ color: var(--gold); }}
.adv-lim .lim h3 {{ color: #F5896A; }}
.adv-lim ul {{ list-style: none; padding: 0; }}
.adv-lim li {{
  font-family: Arial, sans-serif;
  font-size: 10.5pt;
  line-height: 1.5;
  color: rgba(255,255,255,0.82);
  padding: 3mm 0;
  border-top: 1pt solid rgba(255,255,255,0.15);
}}
.adv-lim li:first-child {{ border-top: none; }}

.pullquote {{
  position: relative;
  background: #0A1B3A;
  border-radius: 4mm;
  padding: 9mm 12mm 9mm 18mm;
  margin: 9mm 0 9mm;
}}
.pullquote::before {{
  content: '\\201C';
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 70pt;
  color: var(--gold);
  position: absolute;
  top: -4mm; left: 6mm;
  line-height: 1;
}}
.pullquote p {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 16pt;
  line-height: 1.35;
  color: var(--paper);
  letter-spacing: -0.02em;
}}

.cta-bar {{
  background: var(--gold);
  color: var(--navy);
  padding: 9mm 12mm;
  border-radius: 4mm;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8mm;
  margin-top: 4mm;
}}
.cta-bar h3 {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 20pt;
  color: var(--navy);
  letter-spacing: -0.025em;
  max-width: 100mm;
  margin: 0;
}}
.cta-meta-action {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 11pt;
  color: var(--navy);
}}
.cta-meta-sub {{
  font-family: Arial, sans-serif;
  font-size: 9.5pt;
  color: rgba(3,17,42,0.7);
  margin-top: 1mm;
}}
.foot-dark {{ color: rgba(255,255,255,0.55); }}
.foot-dark .page-num {{ color: var(--paper); }}
.foot-dark .foot-arrow circle {{ fill: #FBB03B; }}
</style>
</head>
<body>

<!-- ============= PAGE 1 — COVER ============= -->
<div class="page cover">
  <div class="cover-gold-tri"></div>
  <div class="cover-gold-corner"></div>
  <div class="cover-mark">
    <div class="ring-1"></div>
    <div class="ring-2"></div>
    <div class="ring-3"></div>
  </div>
  <div class="cover-band">
    <img src="{LOGO}" alt="Pitchbird">
    <div class="hdr-url">www.pitchbird.de</div>
  </div>
  <div class="cover-inner">
    <div>
      <div class="cover-tag">Pitchbird · Founder Guide</div>
      <div class="cover-title">{meta['title']}</div>
      <div class="cover-sub">{meta['subtitle']}</div>
      <div class="cover-author">By {meta['author']}</div>
    </div>
  </div>
</div>

<!-- ============= PAGE 2 — WHY IT MATTERS ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('01:', 'Why it matters')}
    <h2>One sheet of paper.<br>One decision.</h2>
    <p class="lede">The one-pager is the door, not the room. Done well, it earns you the meeting. Done badly, it earns you silence — and you'll never know which line lost you the deal.</p>
    <div class="two-col">
      <div>
        <p>A pitch deck wins the room. The one-pager wins the chance to be in the room. It travels in inboxes, sits on phone screens, and gets forwarded between partners — usually without you in the conversation.</p>
        <p style="margin-top:3mm;">That means every element has to do double duty: <strong>introduce, intrigue, and stand on its own.</strong></p>
        <div class="stat-card">
          <div class="stat-num">{meta['stat']}</div>
          <div class="stat-text">{meta['stat_caption']} The first impression is the only impression.</div>
          <div class="stat-source">Source · {meta['stat_source']}</div>
        </div>
      </div>
      <div>
        <div class="illus"><img src="{img_path('concept-magnifier')}" alt=""></div>
        <div class="illus-cap">Treat the one-pager as the most-circulated document you will ever make. Because it is.</div>
      </div>
    </div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">02</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 3 — THE 8 MUST-HAVES ============= -->
<div class="page">
  {header('www.magdalenareith.com')}
  <div class="body">
    {kicker('02:', 'The framework')}
    <h2>The eight non-negotiables</h2>
    <p style="max-width:150mm;margin-bottom:2mm;">If a one-pager misses any of these, it is incomplete. Treat this as the checklist before you send anything.</p>
    <div class="mh-grid">
      {must_have_items}
    </div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">03</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 4 — NICE TO HAVES + PRINCIPLES ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('03:', 'Beyond the basics')}
    <h2>Add these if you have the space</h2>
    <p style="max-width:150mm;">The four below are the most common upgrades. Together, they turn a competent one-pager into a memorable one.</p>
    <div class="callouts">
      {callouts}
    </div>
    {kicker('04:', 'Design principles')}
    <h3 style="margin-bottom:2mm;">How investors actually read it</h3>
    <div class="principles">
      {principles}
    </div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">04</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 5 — CLOSE + CTA ============= -->
<div class="page close">
  <div class="cover-band">
    <img src="{LOGO}" alt="Pitchbird">
    <div class="hdr-url">www.pitchbird.de</div>
  </div>
  <div class="body" style="padding-top:34mm;">
    {kicker('05:', 'Trade-offs')}
    <h2>What it gives you<br>— and what it can't</h2>
    <div class="adv-lim">
      <div class="adv">
        <h3>Strengths</h3>
        <ul>{adv}</ul>
      </div>
      <div class="lim">
        <h3>Limitations</h3>
        <ul>{lim}</ul>
      </div>
    </div>
    <div class="pullquote">
      <p>The one-pager is brutal in the right way. If your business doesn't fit on the page, the business isn't sharp yet.</p>
    </div>
    <div class="cta-bar">
      <h3>Want a Pitchbird review of your one-pager?</h3>
      <div>
        <div class="cta-meta-action">office@pitchbird.de</div>
        <div class="cta-meta-sub">+49 (0) 160 97026216 · pitchbird.de</div>
      </div>
    </div>
  </div>
  <div class="foot foot-dark">
    <span>Pitchbird · Founder Guide</span>
    <div class="foot-right">
      <span class="page-num">05</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

</body>
</html>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slug", default="one-pager")
    args = p.parse_args()
    meta = META[args.slug]

    outdir = ROOT / meta["slug"]
    outdir.mkdir(parents=True, exist_ok=True)
    html_path = outdir / f"{meta['slug']}-lead-magnet.html"
    pdf_path = outdir / f"{meta['slug']}-lead-magnet.pdf"

    html_path.write_text(html(meta))
    print(f"HTML: {html_path}")

    code = f"""
import asyncio
from playwright.async_api import async_playwright
async def go():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page()
        await page.goto('file://{html_path.resolve()}', wait_until='networkidle')
        await page.pdf(path='{pdf_path.resolve()}', format='A4',
                       print_background=True,
                       margin={{'top':'0','bottom':'0','left':'0','right':'0'}})
        await b.close()
asyncio.run(go())
"""
    r = subprocess.run(["python3", "-c", code], capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        print("PDF ERROR:", r.stderr)
        return
    print(f"PDF:  {pdf_path}")


if __name__ == "__main__":
    main()
