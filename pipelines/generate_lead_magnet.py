#!/usr/bin/env python3
"""Pitchbird lead-magnet PDF generator.

Adapted from /root/productquant_dev/pipelines/lead_magnet/generate_lead_magnet.py
but rebuilt for the Magdalena Reith / Pitchbird brand:
  - Navy #0F1B3D + mustard #F4B82E + salmon #F5896A + cream #F8F6F1
  - Playfair Display headlines + Inter body
  - A4 portrait pages with header band + URL tagline alternation
  - 5 pages: cover / why / 8 must-haves / nice-to-haves + design / advantages + CTA

Usage:
    python3 generate_lead_magnet.py --slug one-pager
"""
import argparse, subprocess, json, pathlib

ROOT = pathlib.Path("/root/pitchbird/lm")
IMG_BASE = pathlib.Path("/root/pitchbird/lm-images")

META = {
    "one-pager": {
        "slug": "one-pager",
        "title": "The Power of the One Pager",
        "subtitle": "Capturing your startup in a single, investor-ready snapshot",
        "author": "Magdalena Reith — Founder, Pitchbird",
        "image_dir": "one-pager",
        "must_haves": [
            ("Company name & logo", "Identity is the anchor. Make sure investors know who they're dealing with before they read a single word."),
            ("Contact information", "The most-skipped basic. If they can't reach you in one click, the deck did nothing."),
            ("Company profile", "A short, informative introduction — what you are, who you serve, why you exist."),
            ("Business idea", "Describe the core concept in one tight sentence. No jargon, no hedging."),
            ("Unique selling proposition", "What makes this venture distinct from the next ten emails in the inbox."),
            ("Roadmap & timeline", "Graphically show where the business is going and when. Visual beats prose here."),
            ("Investment ask", "The amount needed, the structure (one-time or tranches), and the deadline. Specific."),
            ("Investment highlights", "The three or four reasons this allocation pays back. Punchy, not vague."),
        ],
        "nice_to_haves": [
            ("Problem", "The pain in market terms — frame it before you frame yourself."),
            ("Solution", "How your business removes that pain. Two lines, max."),
            ("Traction", "Proof customers want it. Revenue, signups, LOIs — whichever you have."),
            ("Target group & market", "Who you're selling to, and the competitive landscape they live in."),
        ],
        "design_principles": [
            ("Content is king", "Clarity first. Strong narrative — problem, solution, impact. Hierarchy via headings, sub-heads, and bullets that guide the eye."),
            ("Visually appealing", "Clean composition, generous white space, strategic visuals over walls of text. Colour evokes brand, not chaos."),
            ("Remember your audience", "Investors scan, not read. Lead with what helps their decision. Professional, confident tone throughout."),
            ("Call to action", "End with one specific ask. 'Schedule a 20-minute call.' Not 'we'd love to chat sometime.'"),
        ],
        "stat": "32%",
        "stat_caption": "of decision-makers drop off after 15 seconds of reading a one-pager. The first impression is the only impression.",
        "stat_source": "Storydoc, 2024",
        "advantages": [
            "Respects the investor's time — and signals you respect it too.",
            "Forces sharper thinking. If it doesn't fit on a page, the idea isn't focused yet.",
            "Travels well — easy to forward, easy to print, easy to remember.",
        ],
        "limitations": [
            "Brevity is unforgiving. Every missing detail is a potential rejection.",
            "Hard to write alone — outside eyes catch what founder-bias hides.",
            "Not a substitute for the full deck. It is the door, not the room.",
        ],
    },
}


def html(meta):
    img = lambda name: f"file:///root/pitchbird/lm-images/{meta['image_dir']}/{name}.png"
    must_have_rows = "".join(
        f"""<div class="mh-row">
              <div class="mh-num">{str(i+1).zfill(2)}</div>
              <div class="mh-body">
                <h4>{title}</h4>
                <p>{desc}</p>
              </div>
            </div>"""
        for i, (title, desc) in enumerate(meta["must_haves"])
    )
    nice_rows = "".join(
        f"""<div class="nice-card">
              <div class="nice-tag">Nice to have</div>
              <h4>{title}</h4>
              <p>{desc}</p>
            </div>"""
        for title, desc in meta["nice_to_haves"]
    )
    principles_rows = "".join(
        f"""<div class="principle">
              <div class="principle-dot"></div>
              <div>
                <h4>{title}</h4>
                <p>{desc}</p>
              </div>
            </div>"""
        for title, desc in meta["design_principles"]
    )
    adv_items = "".join(f"<li>{x}</li>" for x in meta["advantages"])
    lim_items = "".join(f"<li>{x}</li>" for x in meta["limitations"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{meta['title']} — Pitchbird</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --navy: #0F1B3D;
  --navy-2: #1A2952;
  --gold: #F4B82E;
  --gold-2: #E0A21F;
  --salmon: #F5896A;
  --cream: #F8F6F1;
  --paper: #FFFFFF;
  --ink: #0F1B3D;
  --ink-muted: #5A6178;
  --line: rgba(15,27,61,0.10);
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
@page {{
  size: A4 portrait;
  margin: 0;
}}
html, body {{
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  color: var(--ink);
  background: var(--paper);
  font-size: 11pt;
  line-height: 1.6;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}}
.page {{
  width: 210mm;
  height: 297mm;
  position: relative;
  overflow: hidden;
  page-break-after: always;
  background: var(--paper);
}}
.page:last-child {{ page-break-after: auto; }}

/* ===== HEADER BAND ===== */
.hdr {{
  height: 22mm;
  background: var(--navy);
  color: var(--cream);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 50mm 0 18mm;
}}
.hdr-logo {{
  font-family: 'Playfair Display', serif;
  font-size: 16pt;
  letter-spacing: 0.5pt;
  color: var(--cream);
}}
.hdr-logo .dot {{ color: var(--gold); }}
.hdr-url {{
  font-family: 'Inter', sans-serif;
  font-size: 9pt;
  font-weight: 400;
  letter-spacing: 0.06em;
  color: rgba(248,246,241,0.65);
  text-transform: lowercase;
}}
.gold-tri {{
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 38mm 38mm 0;
  border-color: transparent var(--gold) transparent transparent;
  z-index: 2;
}}
.gold-tri-lg {{
  border-width: 0 70mm 70mm 0;
}}

/* ===== BODY CONTAINER ===== */
.body {{
  padding: 16mm 18mm 14mm;
}}
.kicker {{
  font-family: 'Inter', sans-serif;
  font-size: 9pt;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold-2);
  margin-bottom: 6mm;
}}
h1, h2, h3 {{
  font-family: 'Playfair Display', serif;
  font-weight: 500;
  color: var(--ink);
  letter-spacing: -0.01em;
}}
h1 {{ font-size: 38pt; line-height: 1.1; }}
h2 {{ font-size: 26pt; line-height: 1.2; margin-bottom: 6mm; }}
h3 {{ font-size: 17pt; line-height: 1.3; margin-bottom: 4mm; }}
h4 {{
  font-family: 'Inter', sans-serif;
  font-size: 12pt;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 2mm;
}}
p {{ color: var(--ink-muted); font-size: 10.5pt; line-height: 1.7; }}
strong {{ color: var(--ink); font-weight: 600; }}

/* ===== FOOTER ===== */
.foot {{
  position: absolute;
  bottom: 8mm;
  left: 18mm;
  right: 18mm;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Inter', sans-serif;
  font-size: 8pt;
  color: rgba(15,27,61,0.45);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}}
.page-num {{
  font-family: 'Playfair Display', serif;
  font-size: 11pt;
  font-weight: 500;
  color: var(--ink);
  letter-spacing: 0;
}}
.foot-dark {{ color: rgba(248,246,241,0.45); }}
.foot-dark .page-num {{ color: var(--cream); }}

/* ===== COVER ===== */
.cover {{
  background: var(--navy);
  color: var(--cream);
  height: 297mm;
  position: relative;
  padding: 0;
  overflow: hidden;
}}
.cover .gold-corner-tl {{
  position: absolute; top: 0; left: 0;
  width: 0; height: 0;
  border-style: solid;
  border-width: 95mm 0 0 75mm;
  border-color: transparent transparent transparent var(--gold);
}}
.cover .gold-corner-br {{
  position: absolute; bottom: 0; right: 0;
  width: 0; height: 0;
  border-style: solid;
  border-width: 0 0 95mm 75mm;
  border-color: transparent transparent var(--gold) transparent;
}}
.cover .salmon-dot {{
  position: absolute;
  width: 28mm; height: 28mm;
  border-radius: 50%;
  background: var(--salmon);
  bottom: 110mm; left: 28mm;
  opacity: 0.95;
}}
.cover-inner {{
  position: absolute;
  inset: 0;
  padding: 38mm 22mm 26mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 2;
}}
.cover-tag {{
  font-family: 'Inter', sans-serif;
  font-size: 9pt;
  font-weight: 600;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: var(--gold);
}}
.cover-title {{
  font-family: 'Playfair Display', serif;
  font-size: 52pt;
  line-height: 1.02;
  font-weight: 500;
  color: var(--cream);
  margin-top: auto;
  margin-bottom: 6mm;
  max-width: 150mm;
}}
.cover-sub {{
  font-family: 'Inter', sans-serif;
  font-size: 13pt;
  font-weight: 300;
  line-height: 1.5;
  color: rgba(248,246,241,0.78);
  max-width: 130mm;
  margin-bottom: 18mm;
}}
.cover-author {{
  font-family: 'Inter', sans-serif;
  font-size: 10pt;
  letter-spacing: 0.08em;
  color: rgba(248,246,241,0.55);
  text-transform: uppercase;
}}
.cover-hero {{
  position: absolute;
  right: -6mm;
  top: 78mm;
  width: 110mm;
  height: 110mm;
  background: url('{img('cover-hero')}') center/contain no-repeat;
  z-index: 1;
}}

/* ===== PAGE 2 — WHY ===== */
.lede {{
  font-family: 'Playfair Display', serif;
  font-size: 15pt;
  line-height: 1.5;
  color: var(--ink);
  font-weight: 400;
  font-style: italic;
  margin-bottom: 8mm;
}}
.two-col {{
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 14mm;
  align-items: start;
  margin-top: 8mm;
}}
.two-col p {{ margin-bottom: 4mm; }}
.stat-card {{
  background: var(--cream);
  border-left: 4pt solid var(--gold);
  padding: 12mm 10mm;
  margin-top: 6mm;
}}
.stat-num {{
  font-family: 'Playfair Display', serif;
  font-size: 64pt;
  line-height: 1;
  color: var(--navy);
  font-weight: 500;
}}
.stat-caption {{
  font-family: 'Inter', sans-serif;
  font-size: 11pt;
  color: var(--ink);
  margin-top: 3mm;
  line-height: 1.5;
}}
.stat-source {{
  font-family: 'Inter', sans-serif;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--ink-muted);
  margin-top: 4mm;
}}
.illus-frame {{
  background: var(--cream);
  border-radius: 4pt;
  padding: 8mm;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 95mm;
}}
.illus-frame img {{ max-width: 100%; max-height: 100%; }}

/* ===== PAGE 3 — MUST HAVES ===== */
.mh-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5mm 7mm;
  margin-top: 6mm;
}}
.mh-row {{
  display: flex;
  gap: 4mm;
  padding: 4mm 4mm 4mm 0;
  border-top: 1pt solid var(--line);
}}
.mh-num {{
  font-family: 'Playfair Display', serif;
  font-size: 22pt;
  font-weight: 500;
  color: var(--gold-2);
  line-height: 1;
  min-width: 14mm;
}}
.mh-body h4 {{ font-size: 11pt; margin-bottom: 1mm; }}
.mh-body p {{ font-size: 9.5pt; line-height: 1.5; }}

/* ===== PAGE 4 — NICE + DESIGN ===== */
.nice-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4mm;
  margin-top: 4mm;
  margin-bottom: 10mm;
}}
.nice-card {{
  background: var(--cream);
  padding: 5mm 5mm;
  border-radius: 3pt;
  border-left: 3pt solid var(--salmon);
}}
.nice-tag {{
  font-family: 'Inter', sans-serif;
  font-size: 7.5pt;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--salmon);
  margin-bottom: 2mm;
}}
.nice-card h4 {{ font-size: 11pt; margin-bottom: 1mm; }}
.nice-card p {{ font-size: 9.5pt; line-height: 1.5; }}
.principles {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4mm 8mm;
  margin-top: 4mm;
}}
.principle {{
  display: flex;
  gap: 4mm;
  align-items: flex-start;
  padding-top: 3mm;
  border-top: 1pt solid var(--line);
}}
.principle-dot {{
  width: 6mm; height: 6mm;
  background: var(--gold);
  border-radius: 50%;
  margin-top: 1.5mm;
  flex-shrink: 0;
}}
.principle h4 {{ font-size: 11pt; }}
.principle p {{ font-size: 9.5pt; line-height: 1.5; }}

/* ===== PAGE 5 — CLOSE ===== */
.close {{
  background: var(--navy);
  color: var(--cream);
  height: 297mm;
  position: relative;
  overflow: hidden;
}}
.close .body {{ color: var(--cream); }}
.close .kicker {{ color: var(--gold); }}
.close h2 {{ color: var(--cream); }}
.close p {{ color: rgba(248,246,241,0.74); }}
.close strong {{ color: var(--cream); }}
.close .two-col {{ gap: 12mm; }}
.adv-lim {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10mm;
  margin-top: 6mm;
}}
.adv-lim h3 {{
  font-family: 'Inter', sans-serif;
  font-size: 9pt;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin-bottom: 5mm;
}}
.adv-lim .adv h3 {{ color: var(--gold); }}
.adv-lim .lim h3 {{ color: var(--salmon); }}
.adv-lim ul {{ list-style: none; padding: 0; }}
.adv-lim li {{
  font-family: 'Inter', sans-serif;
  font-size: 10.5pt;
  line-height: 1.6;
  color: rgba(248,246,241,0.82);
  padding: 3mm 0;
  border-top: 1pt solid rgba(248,246,241,0.15);
}}
.adv-lim li:first-child {{ border-top: none; }}
.pullquote {{
  background: var(--navy-2);
  border-radius: 4pt;
  padding: 10mm 12mm;
  margin: 10mm 0 8mm;
  position: relative;
}}
.pullquote::before {{
  content: '\\201C';
  font-family: 'Playfair Display', serif;
  font-size: 60pt;
  color: var(--gold);
  position: absolute;
  top: -2mm;
  left: 4mm;
  line-height: 1;
}}
.pullquote p {{
  font-family: 'Playfair Display', serif;
  font-size: 17pt;
  line-height: 1.4;
  color: var(--cream);
  font-style: italic;
  margin-left: 14mm;
}}
.cta-bar {{
  background: var(--gold);
  color: var(--navy);
  padding: 10mm 12mm;
  margin-top: 8mm;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8mm;
}}
.cta-bar h3 {{
  font-family: 'Playfair Display', serif;
  font-size: 22pt;
  color: var(--navy);
  margin: 0;
  max-width: 100mm;
}}
.cta-meta {{
  text-align: right;
}}
.cta-meta .cta-action {{
  font-family: 'Inter', sans-serif;
  font-size: 11pt;
  font-weight: 600;
  color: var(--navy);
  letter-spacing: 0.04em;
}}
.cta-meta .cta-sub {{
  font-family: 'Inter', sans-serif;
  font-size: 9pt;
  color: rgba(15,27,61,0.7);
  margin-top: 2mm;
}}
</style>
</head>
<body>

<!-- ============= PAGE 1 — COVER ============= -->
<div class="page cover">
  <div class="gold-corner-tl"></div>
  <div class="gold-corner-br"></div>
  <div class="salmon-dot"></div>
  <div class="cover-hero"></div>
  <div class="cover-inner">
    <div>
      <div class="cover-tag">Pitchbird · Founder Guide</div>
    </div>
    <div>
      <div class="cover-title">{meta['title']}</div>
      <div class="cover-sub">{meta['subtitle']}</div>
      <div class="cover-author">By {meta['author']}</div>
    </div>
  </div>
</div>

<!-- ============= PAGE 2 — WHY THE ONE PAGER ============= -->
<div class="page">
  <div class="hdr">
    <div class="hdr-logo">Pitch<span class="dot">bird</span></div>
    <div class="hdr-url">www.pitchbird.de</div>
  </div>
  <div class="gold-tri"></div>
  <div class="body">
    <div class="kicker">01 · Why it matters</div>
    <h2>One sheet of paper. One decision.</h2>
    <p class="lede">The one-pager is the door, not the room. Done well, it earns you the meeting. Done badly, it earns you silence — and you'll never know which line lost you the deal.</p>
    <div class="two-col">
      <div>
        <p>A pitch deck wins the room. The one-pager wins the chance to be in the room. It travels in inboxes, sits on phone screens, and gets forwarded between partners — usually without you in the conversation.</p>
        <p>That means every element has to do double duty: <strong>introduce, intrigue, and stand on its own.</strong> No verbal context. No follow-up slide. Just the page.</p>
        <p>Founders consistently overspend on design polish and underspend on the boring essentials — including, embarrassingly often, their own contact details.</p>
        <div class="stat-card">
          <div class="stat-num">{meta['stat']}</div>
          <div class="stat-caption">{meta['stat_caption']}</div>
          <div class="stat-source">Source · {meta['stat_source']}</div>
        </div>
      </div>
      <div>
        <div class="illus-frame">
          <img src="{img('concept-magnifier')}" alt="">
        </div>
        <p style="margin-top:6mm;font-style:italic;">Treat the one-pager as the most-circulated document you will ever make. Because it is.</p>
      </div>
    </div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <span class="page-num">02</span>
  </div>
</div>

<!-- ============= PAGE 3 — THE 8 MUST-HAVES ============= -->
<div class="page">
  <div class="hdr">
    <div class="hdr-logo">Pitch<span class="dot">bird</span></div>
    <div class="hdr-url">www.magdalenareith.com</div>
  </div>
  <div class="gold-tri"></div>
  <div class="body">
    <div class="kicker">02 · The framework</div>
    <h2>The eight non-negotiables</h2>
    <p style="max-width:140mm;margin-bottom:4mm;">If a one-pager misses any of these, it is incomplete. Treat this as the checklist before you send anything.</p>
    <div class="mh-grid">
      {must_have_rows}
    </div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <span class="page-num">03</span>
  </div>
</div>

<!-- ============= PAGE 4 — NICE TO HAVES + DESIGN ============= -->
<div class="page">
  <div class="hdr">
    <div class="hdr-logo">Pitch<span class="dot">bird</span></div>
    <div class="hdr-url">www.pitchbird.de</div>
  </div>
  <div class="gold-tri"></div>
  <div class="body">
    <div class="kicker">03 · Beyond the basics</div>
    <h2>Add these if you have the space</h2>
    <p style="max-width:140mm;">The four below are the most common upgrades. None of them earn the page on their own; together they turn a competent one-pager into a memorable one.</p>
    <div class="nice-grid">
      {nice_rows}
    </div>
    <div class="kicker" style="margin-top:6mm;">04 · Design principles</div>
    <h3>How investors actually read it</h3>
    <div class="principles">
      {principles_rows}
    </div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <span class="page-num">04</span>
  </div>
</div>

<!-- ============= PAGE 5 — ADVANTAGES / LIMITATIONS / CTA ============= -->
<div class="page close">
  <div class="hdr" style="background:transparent;">
    <div class="hdr-logo">Pitch<span class="dot">bird</span></div>
    <div class="hdr-url">www.pitchbird.de</div>
  </div>
  <div class="body">
    <div class="kicker">05 · Trade-offs</div>
    <h2>What the one-pager gives you — and what it can't</h2>
    <div class="adv-lim">
      <div class="adv">
        <h3>Strengths</h3>
        <ul>{adv_items}</ul>
      </div>
      <div class="lim">
        <h3>Limitations</h3>
        <ul>{lim_items}</ul>
      </div>
    </div>
    <div class="pullquote">
      <p>The one-pager is brutal in the right way. If your business doesn't fit on the page, the business isn't sharp yet.</p>
    </div>
    <div class="cta-bar">
      <h3>Want a Pitchbird review of your one-pager?</h3>
      <div class="cta-meta">
        <div class="cta-action">office@pitchbird.de</div>
        <div class="cta-sub">+49 (0) 160 97026216 · pitchbird.de</div>
      </div>
    </div>
  </div>
  <div class="foot foot-dark">
    <span>Pitchbird · Founder Guide</span>
    <span class="page-num">05</span>
  </div>
</div>

</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", default="one-pager")
    args = parser.parse_args()
    meta = META[args.slug]

    outdir = ROOT / meta["slug"]
    outdir.mkdir(parents=True, exist_ok=True)

    html_path = outdir / f"{meta['slug']}-lead-magnet.html"
    pdf_path = outdir / f"{meta['slug']}-lead-magnet.pdf"

    html_path.write_text(html(meta))
    print(f"HTML: {html_path}")

    # Render PDF via Playwright
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
