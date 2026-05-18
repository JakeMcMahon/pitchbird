#!/usr/bin/env python3
"""Pitchbird lead-magnet PDF generator - v2, brand-corrected.

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

ICON_DIR = pathlib.Path("/root/pitchbird/lm-images/icons")


def icon_svg(name):
    """Read a Phosphor duotone SVG, return its raw markup with class injected."""
    txt = (ICON_DIR / f"{name}.svg").read_text()
    return txt.replace("<svg ", '<svg class="phx" ', 1)


META = {
    "one-pager": {
        "slug": "one-pager",
        "title": "The Power of the One Pager",
        "title_split": ("The Power of", "the One Pager"),
        "subtitle": "Capturing your startup in a single, investor-ready snapshot",
        "author": "Magdalena Reith · Founder, Pitchbird",
        "cover_lede": "Investors decide whether to take your call in less than 15 seconds. The one-pager is the document that has to survive that test.",
        "cover_body": [
            "A pitch deck wins the room. The one-pager wins the chance to be in the room. It travels in inboxes, sits on phone screens, and gets forwarded between partners - usually without you in the conversation.",
            "Drawing on Pitchbird's work with thousands of founders, this guide distils the eight non-negotiables every one-pager needs, the four upgrades that turn competent into memorable, and the design principles that respect how investors actually read.",
            "In the following pages, you'll learn:",
        ],
        "cover_bullets": [
            "The 8 elements every one-pager must have",
            "The 4 high-leverage additions to consider",
            "How investors scan - and what to put where their eyes go",
            "When the one-pager helps and when it limits you",
        ],
        "cover_quote": "Well-designed one-pagers turn cold inboxes into conversations that change everything.",
        "stat": "32%",
        "stat_caption": "of decision-makers drop off after 15 seconds of reading a one-pager.",
        "stat_source": "Storydoc, 2024",
        "must_haves": [
            ("Company name & logo", "Identity is the anchor. Investors know who they're dealing with before they read a single word.", "identification-card"),
            ("Contact information", "The most-skipped basic. If they can't reach you in one click, the document did nothing.", "phone"),
            ("Company profile", "A short, informative introduction - what you are, who you serve, why you exist.", "info"),
            ("Business idea", "Describe the core concept in one tight sentence. No jargon, no hedging.", "lightbulb"),
            ("Unique selling proposition", "What makes this venture distinct from the next ten emails in the inbox.", "medal"),
            ("Roadmap & timeline", "Graphically show where the business is going and when. Visual beats prose here.", "chart-line-up"),
            ("Investment ask", "The amount needed, the structure (one-time or tranches), and the deadline. Specific.", "currency-circle-dollar"),
            ("Investment highlights", "The three or four reasons this allocation pays back. Punchy, not vague.", "sparkle"),
        ],
        "page2_body": [
            "A pitch deck wins the room. The one-pager wins the chance to be in the room. It travels in inboxes, sits on phone screens, and gets forwarded between partners - usually without you in the conversation.",
            "That means every element has to do double duty: <strong>introduce, intrigue, and stand on its own.</strong> VCs process pitch documents as self-contained assets. Partners share them with colleagues who may evaluate them without you present. (PitchGrade / DocSend, 2024)",
            "Funding Blueprint (2026) found that a well-structured one-pager reduces decision friction by approximately <strong>47%</strong> compared to a full pitch deck - while maintaining narrative control. That's the edge in cold outreach.",
        ],
        "do_dont_pairs": [
            ("Dense, unbroken paragraphs that force the investor to find the headline", "One dominant headline - 14pt or larger - visible without scrolling or rotating"),
            ("Revenue model buried below line 8 - 71% of readers never reach it. (River Editor, 2026)", "Revenue model in the top-half of the page, on the natural Z-scan path"),
            ("900+ words crammed onto a single page", "400-500 words with white space. (Storydoc, 2024)"),
            ("No funding ask, or vague 'seeking strategic partners' language", "Specific ask: amount, instrument (SAFE / equity), and close date"),
            ("Team section missing - or 'bios available on request'", "Founder names, roles, one credibility signal each"),
            ("Three fonts, five brand colours, a stock-photo background", "One primary font, two colours, one well-chosen image"),
            ("Contact info on a second page, or missing entirely", "Email, phone, LinkedIn in the bottom-right - every time"),
            ("Runs to 1.5 or 2 pages - investor stops at the scroll", "Hard stop at one page. If it doesn't fit, cut - don't extend."),
        ],
        "do_dont_note": "The one-pager must be designed for rapid comprehension without verbal explanation. Partners share it with colleagues who may evaluate it without you present. (PitchGrade / DocSend Data, 2024)",
        "examples": [
            ("Airbnb (2008)", "The original lean pitch", "peach", "Airbnb began as a simple one-pager built on WordPress before it raised a single dollar. It named the problem (no affordable short-term accommodation), the model (peer-to-peer room rental), and the founders. No deck. No presentation. One page.", "The idea earned the meeting. The one-pager was the proof it could be communicated clearly.", "Free Startup Funding, 2024"),
            ("Warm-intro advantage", "Structure over luck", "blue", "DocSend data shows warm introductions convert at <strong>40-50%</strong> versus <strong>3-5%</strong> for cold decks. A well-crafted one-pager sent to a mutual contact converts cold outreach into a warm intro - before the deck ever opens.", "Use the one-pager as the ask for an introduction, not as a substitute for one.", "PitchGrade / DocSend, 2024"),
            ("Traction-first sequencing", "Faster closes by 6.4 weeks", "green", "Funding Blueprint's analysis found that companies leading with traction metrics - not vision statements - close funding rounds <strong>6.4 weeks faster</strong>. The first thing the investor reads sets the frame for everything that follows.", "Lead with your best proof point. Vision supports traction. Not the other way around.", "Funding Blueprint, 2026"),
        ],
        "examples_framework": "What all strong one-pagers share: the problem is named in one line, the ask is on the page, the team is visible, and it fits on a single sheet without shrinking the font below 10pt.",
        "word_economy_intro": "The 400-500 word limit is not a stylistic preference. It is the threshold above which investors stop reading. Storydoc's benchmark across thousands of one-pagers is unambiguous: above 500 words, the document looks unedited - and the reader skips to the exit. The discipline of cutting is the work.",
        "word_economy": [
            ("Start with a word count", "pencil-simple-line", "Paste your draft into any word processor. If it reads over 500 words, you are not done yet. Count before you edit - not after.", "Our proprietary, AI-powered platform leverages cutting-edge machine learning algorithms to deliver personalised, data-driven insights that help enterprise customers optimise their operational workflows and significantly reduce costs.", "Our AI platform cuts enterprise operating costs by 30% in under 90 days."),
            ("Kill the adjectives first", "warning-octagon", "Ask every adjective and adverb: does this add data, or does it add enthusiasm? Enthusiasm is free; data is not. Every 'innovative', 'revolutionary', 'world-class' costs you credibility, not goodwill.", "Our highly experienced, passionate team of world-class experts has developed a truly innovative solution.", "Our team has built and exited two SaaS companies. The solution is in pilot with three enterprise clients."),
            ("One sentence per idea", "book-open-text", "A sentence with three clauses is three sentences that haven't been separated yet. If a sentence runs past 20 words, break it. Read it aloud - if you run out of breath, it's too long.", "We are targeting the rapidly growing SME market segment in the DACH region, which represents an addressable market of over €4 billion annually and has historically been underserved by existing SaaS providers.", "Target: SMEs in DACH. Addressable market: €4bn. Underserved by every existing SaaS provider."),
            ("Replace paragraphs with bullets", "chart-bar-horizontal", "Three consecutive sentences listing related things are a bullet list in disguise. Bullets scan faster, skip slower, and - critically - take up less vertical space on the page.", "The funding will be used to expand our sales team, accelerate product development, and build out our customer success function to support expected growth.", "Use of funds: sales (40%) · product (35%) · customer success (25%)"),
            ("The five-word test", "lightning", "Can you summarise the business in five words? If not, the headline is doing too much. The headline's job is to make the investor read the next line - not explain everything.", "Building the future of sustainable urban mobility for the next generation of city commuters.", "EV scooter rentals for cities."),
        ],
        "word_economy_closing": "Cutting is not about losing content. It is about finding the 50 words that carry the other 450. When you have cut everything that doesn't earn its place, what remains is the argument.",
        "first_60_intro": "Investors don't read a one-pager. They scan it - in a Z-shape, top-left to bottom-right - and decide in the first 15 seconds whether to keep going. 32% drop off before that window closes. (Storydoc, 2024) Understanding their path is the single most actionable thing you can do.",
        "first_60_sequence": [
            ("0-5 sec", "Header: logo, company name, tagline.", "Do I recognise this space? Is this category interesting to me?", "Identity and category signal. The tagline must name the category and the outcome - not a slogan. If the investor can't place the business in five seconds, the rest is irrelevant."),
            ("5-15 sec", "Headline + USP - the sentence that earns the next 45 seconds.", "Is this a big enough problem? Is this approach credible?", "Lead with the outcome, not the mechanism. 'We help enterprise HR teams cut onboarding by half' beats 'We are an AI-powered HR automation platform.'"),
            ("15-30 sec", "Traction and team - the proof this is real.", "Is there evidence this works? Can I trust who is building it?", "Investors spend an average of 62 seconds on team in pitch decks. (PitchGrade / DocSend, 2024) In a one-pager that scrutiny compresses into a few lines. One credibility signal per founder. One traction proof with a number."),
            ("30-60 sec", "Investment ask and contact.", "What exactly do they need? How do I respond?", "Companies leading with traction close 6.4 weeks faster than those leading with vision. (Funding Blueprint, 2026) Make the ask specific: amount, instrument, close date. Then make response trivial - email, phone, LinkedIn, bottom-right."),
        ],
        "first_60_rule": "<strong>The 8-line rule.</strong> If your revenue model is not visible in the first eight lines of the document, 71% of readers never see it. (River Editor, 2026) That is not a layout preference - it is a structural requirement. Count the lines in your draft. The problem, the model, and the traction must all land above that threshold.",
        "pressure_test_intro": "You do not need analytics software to know whether a one-pager works. You need five disciplined tests - each surfaces a different failure mode. They take less than a week. They will save you from sending something that quietly fails and never tells you why.",
        "pressure_tests": [
            ("Read it aloud", "megaphone-simple", "Print the document or open it on a screen, and read every word out loud at normal speaking pace - without pausing to correct yourself mid-sentence.", "Read straight through without hesitation. Pace feels like a confident conversation.", "You stumble, slow down, or have to re-read a sentence. Every stumble is a sentence that is too dense or too long."),
            ("Three advisors, separately", "user-focus", "Send to three people who understand your space but are not inside your company. Same brief: 'Read this cold. Tell me what's unclear, what's missing.' Never as a group.", "Each person flags something different - minor, specific, fixable.", "Two or more flag the same thing. That is not preference. It's a broken element. Fix it."),
            ("The 5-second test, with 5 founders", "timer", "Send to five founders - peers who do not know your pitch. Ask: 'After five seconds, what does this company do?' Collect their exact words.", "Four of five describe the business accurately in one sentence.", "Fewer than three get it right, or descriptions vary wildly. The headline isn't doing its job."),
            ("Print it", "device-mobile", "Print the one-pager at 100% scale on A4 or letter. Look at it from arm's length before reading a word.", "Hierarchy is visible. Headline stands out. Clear white space. Looks like a professional document.", "Looks grey, dense, or cramped. Font below 10pt. No clear visual anchor. Fails on paper = fails on screen."),
            ("The 8-must-haves checklist", "check-circle", "Open page 03 of this guide. Walk through all eight must-haves - name, contact, profile, business idea, USP, roadmap, ask, highlights. Mark each on your draft.", "All eight are present. Each is visible without hunting for it.", "One or more missing, vague, or buried. An incomplete one-pager is a disqualifier - not a work in progress."),
        ],
        "pressure_test_closing": "The one-pager doesn't fail at the send. It fails at the desk, before the investor ever sees it. These five tests catch what founder-proximity blinds you to.",
        "about_paragraphs": [
            "<strong>Magdalena Reith</strong> is the founder of Pitchbird, an agency specialising in pitch deck design and startup consulting. Since founding Pitchbird in 2015, Magdalena has helped <strong>over 10,000 startups</strong> across a variety of industries tell their stories and secure funding.",
            "With a background in global companies spanning business development, investor relations, and design, Magdalena brings a multidisciplinary perspective to her work with founders. Her expertise includes <strong>crafting compelling investor documents, delivering impactful corporate presentations, and providing personalised pitch coaching</strong> to help startups refine their messaging.",
            "In addition to running Pitchbird, <strong>Magdalena is a frequent speaker and pitch coach for startup programs including Burda Bootcamp and Startup SAFARI</strong>. She has hosted Pitch Masterclasses at Startup SAFARI events, helping founders at all levels shine on stage.",
            "When she's not working with startups, you can find Magdalena enjoying the vibrant scene in Munich and connecting with fellow entrepreneurs.",
            "Connect with her on LinkedIn or learn more about Pitchbird's services at pitchbird.de.",
        ],
        "failures": [
            ("Runs to more than one page", "The investor stops at the scroll. Immediate disqualifier.", "Hard-cut at one page. If it doesn't fit, the message isn't tight enough yet.", "Storydoc, 2024"),
            ("Revenue model buried below line 8", "71% of readers never reach it. They assume you're pre-revenue or hiding something.", "Place the revenue model in the top half of the page, on the Z-scan path.", "River Editor, 2026"),
            ("No funding ask - or a vague one", "'Seeking strategic investment' is not an ask. Missing status is an immediate disqualifier.", "State the amount, instrument (SAFE / equity), and close date. Specific numbers signal preparation.", "Storydoc, 2024"),
            ("Team section missing or deferred", "Investors spend more time on team than any other section - 1 minute 2 seconds on average. No team = no trust.", "Name the founders, their roles, one credibility signal each. It belongs on the page.", "PitchGrade / DocSend, 2024"),
            ("Too many words, too little white space", "The ideal is 400-500 words. Above that, the document looks unedited and the reader skips to the exit.", "Cut to 500 words. Use white space as structure, not decoration.", "Storydoc, 2024"),
            ("Contact information missing or buried", "Founders spend weeks on design and forget to include a working email address. Without it, the document did nothing.", "Email, phone, LinkedIn. Bottom-right. Every time, without exception.", "Chapter 7"),
        ],
        "nice_callouts": [
            ("Problem", "peach", "target", "Frame the pain in market terms before you frame yourself.", "Investors connect with the problem first. Make them feel it before you sell the cure."),
            ("Solution", "blue", "lightbulb-filament", "Show how your business removes that pain. Two lines, max.", "Lead with the outcome - not the mechanism. Save the how for the deck."),
            ("Traction", "green", "trend-up", "Prove customers want it. Revenue, signups, LOIs - whichever you have.", "Proof beats promise. Companies leading with traction close 6.4 weeks faster. (Funding Blueprint, 2026)"),
            ("Market", "lavender", "globe-hemisphere-east", "Who you sell to, and the competitive landscape they live in.", "Investors want a beachhead, not 'everyone'. Show the wedge first."),
        ],
        "design_principles": [
            ("Content is king", "Clarity first. Strong narrative - problem, solution, impact. Hierarchy via headings, sub-heads, and bullets that guide the eye."),
            ("Visually appealing", "Clean composition, generous white space, strategic visuals over walls of text. Colour evokes brand, not chaos."),
            ("Remember your audience", "Investors scan, not read. Lead with what helps their decision. Professional, confident tone throughout."),
            ("Call to action", "End with one specific ask. 'Schedule a 20-minute call.' Not 'we'd love to chat sometime.'"),
        ],
        "anatomy_zones": [
            ("Header", "top", "Logo + company name. Often the only thing the partner remembers ten minutes later - make it work.", "1"),
            ("Headline + USP", "top", "One sentence that earns the next 14 seconds of attention. Lead with the outcome, not the mechanism.", "2"),
            ("Problem", "mid-l", "Pain in the customer's words. Numbers if you have them, story if you don't.", "3"),
            ("Solution + visual", "mid-r", "How you remove the pain - paired with a mock-up, screenshot or icon. Visual carries weight here.", "4"),
            ("Traction", "low-l", "Proof. Revenue, signups, LOIs, pilots. One number beats a paragraph of optimism.", "5"),
            ("Market + roadmap", "low-r", "Beachhead first, then the trajectory. 6/12/24-month milestones in a single timeline.", "6"),
            ("Investment ask", "foot-l", "The amount, the structure, the deadline. Specific. No 'flexible'.", "7"),
            ("Contact", "foot-r", "Name, email, phone, LinkedIn. The most-skipped detail. Don't skip it.", "8"),
        ],
        "quotes": [
            ("You can't connect the dots looking forward; you can only connect them looking backwards. So you have to trust that the dots will somehow connect in your future.", "Steve Jobs", "Founder, Apple", "big"),
            ("Chase the vision, not the money - the money will end up following you.", "Tony Hsieh", "Founder, Zappos", "small"),
            ("The best investment you can make is in your own knowledge.", "Warren Buffett", "Berkshire Hathaway", "small"),
            ("My biggest motivation? Just to keep challenging myself.", "Richard Branson", "Founder, Virgin Group", "small"),
            ("Success is the journey where you reach and exist in places you never thought of before.", "Jayshree Chhajjer", "Founder, Maitree Utsav", "small"),
        ],
        "analytics": [
            ("Click-through rate", "peach", "cursor-click", "The percentage of recipients who clicked your CTA. The cleanest signal that the one-pager earned a next step.", "Track per source - what works in DMs may flop in cold email."),
            ("Time on page", "blue", "timer", "How long readers actually spend with it. Under 20 seconds = re-write. Over 90 = lower the density.", "Pair with scroll depth before drawing conclusions."),
            ("Scroll depth", "green", "arrow-line-down", "How far down they read. Cliffs in the curve show where attention drops - fix that section first.", "Bottom-third drop-off is normal. Top-third drop-off is a red flag."),
            ("Conversion rate", "lavender", "check-circle", "The percentage who took the requested action - booked, replied, downloaded. The number you optimise everything else for.", "If conv-rate is fine but absolute numbers are tiny, the gap is reach, not the page."),
            ("A/B testing", "peach", "flask", "Run two versions in parallel. One change per test (headline, hero image, CTA copy). Decide on ≥30 events per arm.", "Smaller decks need ranking judgements, not statistical significance."),
        ],
        "optimization": [
            ("Headline & hook", "rocket-launch", "Test 3-5 versions. The best one outperforms the average by 2-3x - and you won't pick it intuitively."),
            ("Visual hierarchy", "chart-bar-horizontal", "Move the most-skimmed elements to the top-left and bottom-right - that's where eyes actually land."),
            ("Content priority", "pencil-simple-line", "Reorder by what the data says - not by what feels logical to the founder. Engagement signals beat outline-logic."),
            ("CTA testing", "cursor-click", "Position, colour, copy. 'Book a 15-min call' converts higher than 'Get in touch' on every cohort we've measured."),
            ("Personalisation", "user-focus", "Swap the lede paragraph per investor persona. The rest stays. Drives 30-60% lifts on warm sends."),
            ("Mobile optimisation", "device-mobile", "Most first reads happen on a phone. If the headline wraps to four lines on mobile, the document is broken."),
            ("Channel integration", "megaphone-simple", "The one-pager and the email + DM and the deck all use the same headline, the same numbers, the same proof points. Consistency compounds."),
            ("Feedback loop", "arrows-clockwise", "Ship, measure, edit, re-ship - weekly. The one-pager you send in month three should be unrecognisable from month one."),
        ],
        "reading": [
            ("The One Page Proposal", "Patrick G. Riley", "The original framework. Forces you to defend every line on the page."),
            ("Made to Stick", "Chip & Dan Heath", "Why some ideas survive. Six principles - apply all of them to your one-pager."),
            ("Business Model Generation", "Osterwalder & Pigneur", "The Business Model Canvas - a different one-pager that pairs well with the investor version."),
            ("The Lean Startup", "Eric Ries", "Validate before you polish. Your one-pager evolves with the business - let it."),
            ("The One Page Marketing Plan", "Allan Dib", "Marketing-focused, but the brevity discipline transfers directly to investor docs."),
            ("Storyworthy", "Matthew Dicks", "The 'homework for life' principle - find the moment in your founder story that actually lands."),
        ],
        "advantages": [
            "Respects the investor's time - and signals you respect it too.",
            "Forces sharper thinking. If it doesn't fit on a page, the idea isn't focused yet.",
            "Travels well - easy to forward, print, remember.",
        ],
        "limitations": [
            "Brevity is unforgiving. Every missing detail is a potential rejection.",
            "Hard to write alone - outside eyes catch what founder-bias hides.",
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


def callout_card(theme, label, icon_name, headline, body):
    """Pain-Point/Solutions style card. theme in: peach, blue, green, lavender."""
    return f"""
<div class="callout callout-{theme}">
  <div class="callout-head-row">
    <div class="callout-pill"><span class="callout-pill-label">{label}</span></div>
    <div class="callout-icon">{icon_svg(icon_name)}</div>
  </div>
  <div class="callout-headline">{headline}</div>
  <div class="callout-body">{body}</div>
</div>"""


# ---------- page HTML ----------

def html(meta):
    img_path = lambda name: f"file://{IMG / (name + '.png')}"

    must_have_items = "".join(
        f"""<div class="mh-row">
              <div class="mh-icon">{icon_svg(icon)}</div>
              <div class="mh-num">{str(i+1).zfill(2)}</div>
              <div class="mh-body">
                <div class="mh-title">{title}</div>
                <div class="mh-desc">{desc}</div>
              </div>
            </div>"""
        for i, (title, desc, icon) in enumerate(meta["must_haves"])
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

    # Anatomy zones (page 5)
    anatomy_map_html = "".join(
        f'<div class="az {zone}"><span class="az-num">{num}</span><span class="az-label">{label}</span></div>'
        for label, zone, _desc, num in meta["anatomy_zones"]
    )
    anatomy_list_html = "".join(
        f'<div class="anatomy-li"><div class="anatomy-li-num">{num}</div>'
        f'<div><div class="anatomy-li-label">{label}</div>'
        f'<div class="anatomy-li-desc">{desc}</div></div></div>'
        for label, _zone, desc, num in meta["anatomy_zones"]
    )

    # Page 2 body (with citations)
    page2_body_html = "".join(f"<p>{p}</p>" for p in meta.get("page2_body", []))

    # Do/Don't pairs (page 6)
    dodont_html = "".join(
        f'<div class="dodont-row"><div class="c-dont">{dont}</div><div class="c-do">{do}</div></div>'
        for dont, do in meta["do_dont_pairs"]
    )

    # Examples — split across two pages: first 2 on page A, last 1 + framework on page B
    def _ex_card(name, label, theme, body, take, source):
        return (
            f'<div class="ex-card ex-card-{theme}">'
            f'<div><div class="ex-label">{label}</div>'
            f'<div class="ex-name">{name}</div>'
            f'<div class="ex-source">{source}</div></div>'
            f'<div><div class="ex-body">{body}</div>'
            f'<div class="ex-take">{take}</div></div>'
            f'</div>'
        )
    examples_a_html = "".join(_ex_card(*e) for e in meta["examples"][:2])
    examples_b_html = "".join(_ex_card(*e) for e in meta["examples"][2:])

    # Analytics callouts (page 8) - reuse callout_card with extra icons
    analytics_html = "".join(
        callout_card(theme, label, icon, headline, body)
        for label, theme, icon, headline, body in meta["analytics"]
    )

    # Optimization rows (page 8 second section)
    opt_html = "".join(
        f'<div class="opt-row"><div class="opt-icon">{icon_svg(icon)}</div>'
        f'<div><div class="opt-body-label">{label}</div>'
        f'<div class="opt-body-desc">{desc}</div></div></div>'
        for label, icon, desc in meta["optimization"][:4]
    )

    # Word economy (new page)
    we_html = "".join(
        f'<div class="we-block"><div class="we-icon">{icon_svg(icon)}</div>'
        f'<div><div class="we-label">{label}</div>'
        f'<div class="we-rule">{rule}</div>'
        f'<div class="we-example">'
        f'<div class="we-example-bloated">{bloated}</div>'
        f'<div class="we-example-tight">{tight}</div>'
        f'</div></div></div>'
        for label, icon, rule, bloated, tight in meta["word_economy"]
    )

    # First 60 seconds — split rows 1-2 on page A, rows 3-4 + 8-line-rule on page B
    def _t60_row(window, what, q, guidance):
        return (
            f'<div class="t60-row">'
            f'<div class="t60-window">{window}</div>'
            f'<div><div class="t60-what-label">They look at</div>'
            f'<div class="t60-what">{what}</div>'
            f'<div class="t60-guidance">{guidance}</div></div>'
            f'<div><div class="t60-q-label">Their question</div>'
            f'<div class="t60-q">&ldquo;{q}&rdquo;</div></div>'
            f'</div>'
        )
    t60_a_html = "".join(_t60_row(*r) for r in meta["first_60_sequence"][:2])
    t60_b_html = "".join(_t60_row(*r) for r in meta["first_60_sequence"][2:])

    # Pressure test
    pt_html = "".join(
        f'<div class="pt-row">'
        f'<div class="pt-icon">{icon_svg(icon)}</div>'
        f'<div><div class="pt-name">{name}</div>'
        f'<div class="pt-how">{how}</div></div>'
        f'<div class="pt-signals">'
        f'<div class="pt-pass">{pass_signal}</div>'
        f'<div class="pt-fail">{fail_signal}</div>'
        f'</div></div>'
        for name, icon, how, pass_signal, fail_signal in meta["pressure_tests"]
    )

    # About paragraphs
    about_html = "".join(f"<p>{p}</p>" for p in meta["about_paragraphs"])

    # Failures (page 9)
    failures_html = "".join(
        f'<div class="fail-row">'
        f'<div class="fail-mode">{mode}</div>'
        f'<div class="fail-detail">{detail}<span class="fail-source">{source}</span></div>'
        f'<div class="fail-fix"><span class="fail-fix-label">Fix</span>{fix}</div>'
        f'</div>'
        for mode, detail, fix, source in meta["failures"]
    )

    arrow = page_arrow()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{meta['title']} - Pitchbird</title>
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
  background: var(--navy);
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
  break-after: page;
  background: var(--paper);
}}
.page:last-child {{ page-break-after: auto; break-after: auto; }}
/* Page-break safety: never split these atomic chunks across pages */
.mh-row, .nice-card, .principle, .pr, .callout, .qcard, .opt-row,
.dodont-row, .ex-card, .fail-row, .we-block, .t60-row, .pt-row,
.findus-row, .stat-card, .pullquote, .cta-bar, .ex-framework,
.opt-capstone, .pt-closing, .t60-rule {{
  page-break-inside: avoid;
  break-inside: avoid;
}}

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

/* ===== COVER v2 (type-led, Figma-matching) ===== */
.cover-v2-body {{ padding: 14mm 18mm 6mm; }}
.cover-eyebrow {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 9.5pt;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 8mm;
}}
.cover-h1 {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 44pt;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin-bottom: 10mm;
}}
.cover-h1 .g {{ color: var(--gold); }}
.cover-h1 .n {{ color: var(--ink); }}
.cover-lede {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 13pt;
  line-height: 1.4;
  color: var(--ink);
  letter-spacing: -0.015em;
  margin-bottom: 6mm;
}}
.cover-p {{
  font-family: Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.55;
  color: var(--ink-2);
  margin-bottom: 4mm;
}}
.cover-bullets {{
  list-style: none;
  padding: 0;
  margin: 2mm 0 6mm;
}}
.cover-bullets li {{
  font-family: Arial, sans-serif;
  font-weight: 700;
  font-size: 11pt;
  line-height: 1.55;
  color: var(--ink);
  padding-left: 7mm;
  position: relative;
  margin-bottom: 1.5mm;
}}
.cover-bullets li::before {{
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 2.1mm; height: 2.1mm;
  background: var(--gold);
  border-radius: 50%;
}}
.cover-sign {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 11pt;
  color: var(--ink);
  margin-top: 4mm;
}}
.cover-quote-band {{
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 70mm;
  background: var(--navy);
  padding: 14mm 18mm 12mm;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}}
.cover-quote-inner {{
  position: relative;
  max-width: 130mm;
  padding-left: 14mm;
}}
.cover-quote-mark {{
  position: absolute;
  top: -10mm; left: 0;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 80pt;
  color: var(--gold);
  line-height: 1;
}}
.cover-quote-text {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 18pt;
  line-height: 1.3;
  color: var(--paper);
  letter-spacing: -0.02em;
  margin: 0;
}}
.cover-quote-arrow {{
  align-self: flex-end;
}}
.cover-quote-arrow svg circle {{ fill: var(--gold); }}

/* ===== COVER (old, kept for fallback) ===== */
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
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 88mm;
  overflow: hidden;
}}
.illus-navy {{ background: var(--navy); }}
.illus img {{ width: 100%; height: 100%; object-fit: cover; }}
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
.mh-icon {{
  width: 10mm; height: 10mm;
  flex-shrink: 0;
  background: var(--navy);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.mh-icon svg {{ width: 5.5mm; height: 5.5mm; color: var(--gold); }}
.mh-num {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 18pt;
  color: var(--gold);
  line-height: 1;
  min-width: 9mm;
  letter-spacing: -0.02em;
  align-self: center;
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
.callout-icon {{ width: 9mm; height: 9mm; display: inline-flex; align-items: center; }}
.callout-icon svg {{ width: 9mm; height: 9mm; }}
.callout-peach    .callout-icon svg {{ color: #C77A0A; }}
.callout-blue     .callout-icon svg {{ color: #1B6FA8; }}
.callout-green    .callout-icon svg {{ color: #1A7240; }}
.callout-lavender .callout-icon svg {{ color: #5B408C; }}

/* ===== Anatomy map (page 5) ===== */
.anatomy {{
  margin-top: 4mm;
  display: grid;
  grid-template-columns: 0.8fr 1.05fr;
  gap: 8mm;
  align-items: start;
}}
.anatomy-map {{
  background: #F4F1EA;
  border-radius: 4mm;
  padding: 5mm;
  display: grid;
  grid-template-rows: auto 1fr 1fr auto;
  grid-template-columns: 1fr 1fr;
  gap: 3mm;
  aspect-ratio: 0.78;
  position: relative;
}}
.az {{
  background: #fff;
  border: 1.4pt solid var(--line);
  border-radius: 2.5mm;
  padding: 3mm 3.5mm;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  min-height: 16mm;
}}
.az-num {{
  position: absolute;
  top: 2mm; right: 3mm;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 10pt;
  color: var(--gold);
}}
.az-label {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 9pt;
  color: var(--ink);
  letter-spacing: -0.005em;
}}
.az.top {{ grid-column: 1 / -1; }}
.az.foot-l {{ grid-column: 1; }}
.az.foot-r {{ grid-column: 2; }}
.anatomy-list {{ display: flex; flex-direction: column; gap: 3mm; }}
.anatomy-li {{
  display: flex;
  gap: 4mm;
  padding-top: 2.5mm;
  border-top: 1pt solid var(--line);
}}
.anatomy-li:first-child {{ border-top: none; padding-top: 0; }}
.anatomy-li-num {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 13pt;
  color: var(--gold);
  min-width: 7mm;
  line-height: 1;
}}
.anatomy-li-label {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 10.5pt;
  margin-bottom: 0.5mm;
  letter-spacing: -0.005em;
}}
.anatomy-li-desc {{
  font-family: Arial, sans-serif;
  font-size: 9pt;
  line-height: 1.45;
  color: var(--ink-2);
}}

/* ===== Quotes spread (page 6) ===== */
.quote-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto auto;
  gap: 4mm;
  margin-top: 4mm;
}}
.qcard {{
  background: #F4F1EA;
  border-radius: 4mm;
  padding: 7mm 7mm 7mm 7mm;
  position: relative;
}}
.qcard-mark {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 36pt;
  color: var(--gold);
  line-height: 0.8;
  margin-bottom: 2mm;
}}
.qcard-text {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 11pt;
  line-height: 1.35;
  color: var(--ink);
  letter-spacing: -0.015em;
  margin-bottom: 4mm;
}}
.qcard-attr {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 9pt;
  color: var(--ink);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}}
.qcard-role {{
  font-family: Arial, sans-serif;
  font-size: 8.5pt;
  color: var(--muted);
  margin-top: 0.5mm;
}}
.qcard.big {{
  grid-column: 1 / -1;
  background: var(--navy);
  color: var(--paper);
}}
.qcard.big .qcard-text {{ color: var(--paper); font-size: 16pt; line-height: 1.3; }}
.qcard.big .qcard-attr {{ color: var(--gold); }}
.qcard.big .qcard-role {{ color: rgba(255,255,255,0.55); }}

/* ===== Optimization grid (page 8) ===== */
.opt-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4mm;
  margin-top: 5mm;
}}
.opt-row {{
  display: flex;
  gap: 4mm;
  padding: 4mm 0;
  border-top: 1.4pt solid var(--line);
}}
.opt-icon {{
  width: 9mm; height: 9mm;
  flex-shrink: 0;
  background: #FDF1DA;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.opt-icon svg {{ width: 5mm; height: 5mm; color: #C77A0A; }}
.opt-body-label {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 11pt;
  margin-bottom: 1mm;
  letter-spacing: -0.005em;
}}
.opt-body-desc {{
  font-family: Arial, sans-serif;
  font-size: 9.5pt;
  line-height: 1.5;
  color: var(--ink-2);
}}

/* ===== Do / Don't table (page 6) ===== */
.dodont {{
  margin-top: 4mm;
  border-radius: 4mm;
  overflow: hidden;
  border: 1.4pt solid var(--line);
}}
.dodont-head {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: var(--navy);
  color: var(--paper);
}}
.dodont-head > div {{
  padding: 3mm 6mm;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 10pt;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}}
.dodont-head .h-dont {{ color: #F5896A; }}
.dodont-head .h-do {{ color: var(--gold); border-left: 1pt solid rgba(255,255,255,0.15); }}
.dodont-row {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-top: 1pt solid var(--line);
}}
.dodont-row:first-of-type {{ border-top: none; }}
.dodont-row > div {{
  padding: 3.5mm 6mm;
  font-family: Arial, sans-serif;
  font-size: 9.5pt;
  line-height: 1.5;
  color: var(--ink-2);
  position: relative;
}}
.dodont-row .c-dont {{
  background: #FBEFEB;
}}
.dodont-row .c-do {{
  background: #FDF6E6;
  border-left: 1pt solid var(--line);
}}
.dodont-row .c-dont::before {{
  content: "\\00d7";
  position: absolute;
  left: 2.5mm; top: 3.6mm;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  color: #C45641;
  font-size: 10pt;
  line-height: 1;
}}
.dodont-row .c-do::before {{
  content: "\\2713";
  position: absolute;
  left: 2.5mm; top: 3.6mm;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  color: #1A7240;
  font-size: 10pt;
  line-height: 1;
}}
.dodont-row .c-dont,
.dodont-row .c-do {{
  padding-left: 6mm;
}}
.dodont-note {{
  margin-top: 5mm;
  font-family: Arial, sans-serif;
  font-style: italic;
  font-size: 9.5pt;
  color: var(--muted);
}}

/* ===== Examples (page 7) ===== */
.examples {{
  display: grid;
  grid-template-columns: 1fr;
  gap: 4mm;
  margin-top: 5mm;
}}
.ex-card {{
  display: grid;
  grid-template-columns: 50mm 1fr;
  gap: 5mm;
  padding: 5mm 6mm;
  border-radius: 4mm;
  align-items: start;
}}
.ex-card-peach {{ background: var(--c-peach-bg); }}
.ex-card-blue {{ background: var(--c-blue-bg); }}
.ex-card-green {{ background: var(--c-green-bg); }}
.ex-name {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 13pt;
  letter-spacing: -0.015em;
  margin-bottom: 1mm;
}}
.ex-label {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 8.5pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink);
  opacity: 0.7;
}}
.ex-body {{
  font-family: Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.5;
  color: var(--ink);
  margin-bottom: 2.5mm;
}}
.ex-take {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 9.5pt;
  line-height: 1.45;
  color: var(--ink);
  border-top: 1pt solid rgba(0,0,0,0.12);
  padding-top: 2.5mm;
}}
.ex-source {{
  font-family: Arial, sans-serif;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--ink);
  opacity: 0.55;
  margin-top: 1.5mm;
}}
.ex-framework {{
  margin-top: 5mm;
  background: var(--navy);
  color: var(--paper);
  padding: 6mm 8mm;
  border-radius: 4mm;
  font-family: Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.5;
}}
.ex-framework strong {{ color: var(--gold); }}

/* ===== Failure modes (page 9) ===== */
.failures {{
  margin-top: 4mm;
}}
.fail-row {{
  display: grid;
  grid-template-columns: 38mm 1fr 60mm;
  gap: 6mm;
  padding: 3.5mm 0;
  border-top: 1.4pt solid var(--line);
  align-items: start;
}}
.fail-row:first-of-type {{ border-top: 1.4pt solid var(--ink); }}
.fail-mode {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 11pt;
  color: var(--ink);
  letter-spacing: -0.01em;
}}
.fail-detail {{
  font-family: Arial, sans-serif;
  font-size: 9.5pt;
  line-height: 1.5;
  color: var(--ink-2);
}}
.fail-source {{
  display: block;
  margin-top: 1.5mm;
  font-family: Arial, sans-serif;
  font-size: 7.5pt;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
}}
.fail-fix {{
  background: #FDF6E6;
  border-left: 3pt solid var(--gold);
  padding: 3mm 4mm;
  border-radius: 0 2mm 2mm 0;
  font-family: Arial, sans-serif;
  font-size: 9pt;
  line-height: 1.45;
  color: var(--ink);
}}
.fail-fix-label {{
  display: block;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 8pt;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #B58510;
  margin-bottom: 1mm;
}}

/* ===== Visual cover (page 0) ===== */
.vcover {{
  background: var(--navy);
  height: 297mm;
  position: relative;
  overflow: hidden;
}}
.vcover-tri-tl {{
  position: absolute;
  top: 0; left: 0;
  width: 0; height: 0;
  border-style: solid;
  border-width: 130mm 0 0 95mm;
  border-color: var(--gold) transparent transparent transparent;
  z-index: 1;
}}
.vcover-tri-br {{
  position: absolute;
  bottom: 0; right: 0;
  width: 0; height: 0;
  border-style: solid;
  border-width: 0 58mm 46mm 0;
  border-color: transparent var(--gold) transparent transparent;
  z-index: 1;
}}
.vcover-band {{
  position: absolute;
  top: 0; left: 0; right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14mm 22mm 0;
  z-index: 3;
}}
.vcover-band img {{ height: 17mm; }}
.vcover-band .url {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 10pt;
  color: var(--paper);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}}
.vcover-hero-wrap {{
  position: absolute;
  top: 64mm;
  left: 50%;
  transform: translateX(-50%);
  width: 130mm;
  height: 100mm;
  z-index: 2;
}}
.vcover-hero-wrap img {{
  width: 100%; height: 100%; object-fit: cover;
  border-radius: 4mm;
}}
.vcover-title {{
  position: absolute;
  bottom: 38mm;
  left: 22mm;
  right: 22mm;
  z-index: 3;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 44pt;
  line-height: 1.04;
  color: var(--paper);
  letter-spacing: -0.03em;
  max-width: 150mm;
}}
.vcover-title .g {{ color: var(--gold); }}
.vcover-tag {{
  position: absolute;
  bottom: 24mm;
  left: 22mm;
  z-index: 3;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 10pt;
  letter-spacing: 0.22em;
  color: var(--paper);
  text-transform: uppercase;
}}

/* ===== About author page ===== */
.about-h1 {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 42pt;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin-bottom: 8mm;
}}
.about-h1 .black {{ color: var(--ink); }}
.about-h1 .gold {{ color: var(--gold); }}
.about-body p {{
  font-family: Arial, sans-serif;
  font-size: 10.5pt;
  line-height: 1.5;
  color: var(--ink-2);
  margin-bottom: 3mm;
  max-width: 158mm;
}}
.about-body strong {{ color: var(--ink); font-weight: 700; }}
.about-portrait-row {{
  display: flex;
  align-items: center;
  gap: 6mm;
  margin-top: 6mm;
}}
.about-portrait {{
  width: 30mm;
  height: 30mm;
  border-radius: 50%;
  background: #F4F1EA;
  overflow: hidden;
  flex-shrink: 0;
}}
.about-portrait img {{ width: 100%; height: 100%; object-fit: cover; }}
.about-linkedin {{
  display: flex;
  align-items: center;
  gap: 3mm;
  font-family: Arial, sans-serif;
  font-size: 11pt;
  color: var(--ink);
  text-decoration: underline;
}}
.about-linkedin .li-icon {{
  width: 8mm; height: 8mm;
  background: #0A66C2;
  border-radius: 1.5mm;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-family: Arial, sans-serif;
  font-weight: 900;
  font-size: 9pt;
}}

/* ===== Find us / contact CTA (last page) ===== */
.findus {{
  background: var(--navy);
  height: 297mm;
  color: var(--paper);
  position: relative;
  overflow: hidden;
}}
.findus-tri {{ display: none; }}
.findus-accent {{
  position: absolute;
  top: 22mm; right: 22mm;
  width: 14mm; height: 14mm;
  background: var(--gold);
  border-radius: 50%;
  z-index: 1;
}}
.findus-band {{
  position: absolute;
  top: 0; left: 0; right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14mm 22mm 0;
  z-index: 3;
}}
.findus-band img {{ height: 17mm; }}
.findus-band .url {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 10pt;
  color: var(--paper);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}}
.findus-inner {{
  position: relative;
  padding: 42mm 22mm 38mm;
  z-index: 2;
}}
.findus-eyebrow {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 11pt;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 6mm;
}}
.findus-h1 {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 40pt;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin-bottom: 8mm;
  max-width: 160mm;
}}
.findus-h1 .gold {{ color: var(--gold); }}
.findus-lede {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 12pt;
  line-height: 1.4;
  color: rgba(255,255,255,0.78);
  max-width: 140mm;
  margin-bottom: 10mm;
  letter-spacing: -0.015em;
}}
.findus-rows {{ display: flex; flex-direction: column; gap: 0; max-width: 160mm; }}
.findus-row {{
  display: grid;
  grid-template-columns: 32mm 1fr;
  gap: 6mm;
  align-items: center;
  padding: 4mm 0;
  border-top: 1pt solid rgba(255,255,255,0.18);
}}
.findus-row:first-of-type {{ border-top: 1pt solid rgba(255,255,255,0.30); }}
.findus-row-label {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 8.5pt;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold);
}}
.findus-row-value, .findus-row-value a {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 12.5pt;
  color: var(--paper);
  letter-spacing: -0.005em;
  text-decoration: none;
}}
.findus-cta, .findus-cta:link, .findus-cta:visited {{
  margin-top: 10mm;
  display: inline-block;
  background: var(--gold);
  color: var(--navy);
  padding: 4mm 8mm;
  border-radius: 2mm;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 11pt;
  letter-spacing: -0.01em;
  text-decoration: none;
}}

/* ===== Word economy page ===== */
.we-grid {{ display: flex; flex-direction: column; gap: 1.8mm; margin-top: 3mm; }}
.we-block {{
  background: #F4F1EA;
  border-radius: 3mm;
  padding: 2.5mm 5mm;
  display: grid;
  grid-template-columns: 9mm 1fr;
  gap: 4mm;
  align-items: start;
}}
.we-icon {{
  width: 10mm; height: 10mm;
  background: var(--navy);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 0.5mm;
}}
.we-icon svg {{ width: 5.5mm; height: 5.5mm; color: var(--gold); }}
.we-label {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 10.5pt;
  letter-spacing: -0.015em;
  margin-bottom: 0.5mm;
}}
.we-rule {{
  font-family: Arial, sans-serif;
  font-size: 8.8pt;
  line-height: 1.4;
  color: var(--ink-2);
  margin-bottom: 1.5mm;
}}
.we-example {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3mm;
  margin-top: 1mm;
}}
.we-example-bloated, .we-example-tight {{
  padding: 1.8mm 2.5mm 1.8mm 6mm;
  border-radius: 2mm;
  font-family: Arial, sans-serif;
  font-size: 7.8pt;
  line-height: 1.35;
  position: relative;
}}
.we-example-bloated {{ background: #FBEFEB; color: #4A1E14; }}
.we-example-tight {{ background: #FDF6E6; color: var(--ink); }}
.we-example-bloated::before {{
  content: "\\00d7";
  position: absolute;
  left: 2mm; top: 2mm;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 9pt;
  color: #C45641;
  line-height: 1;
}}
.we-example-tight::before {{
  content: "\\2713";
  position: absolute;
  left: 2mm; top: 2mm;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 9pt;
  color: #1A7240;
  line-height: 1;
}}
.we-closing {{
  margin-top: 5mm;
  font-family: Arial, sans-serif;
  font-style: italic;
  font-size: 10pt;
  color: var(--muted);
}}

/* ===== First 60 seconds page ===== */
.t60-grid {{ display: flex; flex-direction: column; gap: 0; margin-top: 4mm; }}
.t60-row {{
  display: grid;
  grid-template-columns: 26mm 1fr 1fr;
  gap: 5mm;
  padding: 3mm 0;
  border-top: 1.4pt solid var(--line);
  align-items: start;
}}
.t60-row:first-of-type {{ border-top: 1.4pt solid var(--ink); }}
.t60-window {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 15pt;
  color: var(--gold);
  letter-spacing: -0.02em;
  line-height: 1.05;
}}
.t60-what-label, .t60-q-label {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 8pt;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink);
  margin-bottom: 1.5mm;
}}
.t60-what {{
  font-family: Arial, sans-serif;
  font-size: 9pt;
  line-height: 1.4;
  color: var(--ink-2);
}}
.t60-guidance {{
  font-family: Arial, sans-serif;
  font-size: 8.5pt;
  line-height: 1.4;
  color: var(--ink-2);
  margin-top: 1.5mm;
}}
.t60-q {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-style: italic;
  font-size: 10pt;
  line-height: 1.4;
  color: var(--ink);
}}
.t60-rule {{
  margin-top: 4mm;
  background: var(--navy);
  color: var(--paper);
  border-radius: 4mm;
  padding: 5mm 7mm;
  font-family: Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.45;
}}
.t60-rule strong {{ color: var(--gold); }}

/* ===== Pressure test page ===== */
.pt-grid {{ display: flex; flex-direction: column; gap: 3mm; margin-top: 4mm; }}
.pt-row {{
  display: grid;
  grid-template-columns: 10mm 50mm 1fr;
  gap: 4mm;
  padding: 4mm 5mm;
  background: #F4F1EA;
  border-radius: 3mm;
  align-items: start;
}}
.pt-icon {{
  width: 10mm; height: 10mm;
  background: var(--gold);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 0.5mm;
}}
.pt-icon svg {{ width: 5.5mm; height: 5.5mm; color: var(--navy); }}
.pt-name {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 11pt;
  letter-spacing: -0.015em;
  margin-bottom: 1mm;
}}
.pt-how {{
  font-family: Arial, sans-serif;
  font-size: 9pt;
  line-height: 1.4;
  color: var(--ink-2);
}}
.pt-signals {{
  display: flex;
  flex-direction: column;
  gap: 1.5mm;
  font-family: Arial, sans-serif;
  font-size: 8.5pt;
}}
.pt-pass, .pt-fail {{
  padding-left: 6mm;
  position: relative;
  line-height: 1.4;
}}
.pt-pass {{ color: #0E5731; }}
.pt-fail {{ color: #8C3C2A; }}
.pt-pass::before {{
  content: "✓";
  position: absolute;
  left: 1mm; top: 0;
  font-weight: 900;
  color: #1A7240;
}}
.pt-fail::before {{
  content: "✗";
  position: absolute;
  left: 1mm; top: 0;
  font-weight: 900;
  color: #C45641;
}}
.pt-closing {{
  margin-top: 4mm;
  background: var(--navy);
  color: var(--paper);
  border-radius: 4mm;
  padding: 6mm 8mm 6mm 18mm;
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 13pt;
  line-height: 1.4;
  letter-spacing: -0.018em;
  position: relative;
}}
.pt-closing::before {{
  content: "\\201C";
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 48pt;
  color: var(--gold);
  position: absolute;
  top: -1mm; left: 5mm;
  line-height: 1;
}}

/* ===== Optimisation capstone band (page 9) ===== */
.opt-capstone {{
  margin-top: 10mm;
  background: var(--navy);
  color: var(--paper);
  border-radius: 4mm;
  padding: 8mm 10mm;
  display: grid;
  grid-template-columns: 45mm 1fr;
  gap: 8mm;
  align-items: center;
}}
.opt-capstone-img {{
  background: rgba(255,255,255,0.04);
  border-radius: 3mm;
  padding: 4mm;
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 1;
}}
.opt-capstone-img img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 2mm; }}
.opt-capstone-eyebrow {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 800;
  font-size: 9pt;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 3mm;
}}
.opt-capstone-text {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 13pt;
  line-height: 1.4;
  color: var(--paper);
  letter-spacing: -0.015em;
}}

/* ===== Z-scan overlay on anatomy map ===== */
.zscan-overlay {{
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 2;
}}

/* ===== Reading grid (page 9) ===== */
.read-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4mm;
  margin-top: 5mm;
}}
.book {{
  display: flex;
  gap: 4mm;
  align-items: flex-start;
  padding: 4mm 5mm;
  background: #F4F1EA;
  border-radius: 3mm;
  border-left: 3pt solid var(--gold);
}}
.book-mark {{ flex-shrink: 0; }}
.book-mark svg {{ width: 7mm; height: 7mm; color: var(--ink); }}
.book-title {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 900;
  font-size: 11pt;
  letter-spacing: -0.01em;
  margin-bottom: 0.5mm;
}}
.book-author {{
  font-family: 'Mulish', Arial, sans-serif;
  font-weight: 700;
  font-size: 8.5pt;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 2mm;
}}
.book-take {{
  font-family: Arial, sans-serif;
  font-size: 9pt;
  line-height: 1.45;
  color: var(--ink-2);
}}
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

<!-- ============= PAGE 0 - VISUAL COVER ============= -->
<div class="page vcover">
  <div class="vcover-tri-br"></div>
  <div class="vcover-band">
    <img src="{LOGO}" alt="Pitchbird">
    <div class="url">www.pitchbird.de</div>
  </div>
  <div class="vcover-hero-wrap">
    <img src="{img_path('visual-cover-hero')}" alt="">
  </div>
  <div class="vcover-tag">Pitchbird · Founder Guide</div>
  <div class="vcover-title">
    <span>The Power of </span><span class="g">the One Pager</span>
  </div>
</div>

<!-- ============= PAGE 1 - COVER (type-led, Figma-matching) ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body cover-v2-body">
    <div class="cover-eyebrow">Pitchbird · Founder Guide · Chapter 7</div>
    <h1 class="cover-h1">
      <span class="g">{meta['title_split'][0]}</span> <span class="n">{meta['title_split'][1]}</span>
    </h1>
    <p class="cover-lede">{meta['cover_lede']}</p>
    {''.join(f'<p class="cover-p">{p}</p>' for p in meta['cover_body'])}
    <ul class="cover-bullets">
      {''.join(f'<li>{b}</li>' for b in meta['cover_bullets'])}
    </ul>
    <p class="cover-sign">{meta['author']}</p>
  </div>
  <div class="cover-quote-band">
    <div class="cover-quote-inner">
      <div class="cover-quote-mark">&ldquo;</div>
      <p class="cover-quote-text">{meta['cover_quote']}</p>
    </div>
    <div class="cover-quote-arrow">{arrow}</div>
  </div>
</div>

<!-- ============= PAGE 2 - WHY IT MATTERS ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('01:', 'Why it matters')}
    <h2>One sheet of paper.<br>One decision.</h2>
    <p class="lede">The one-pager is the door, not the room. Done well, it earns you the meeting. Done badly, it earns you silence - and you'll never know which line lost you the deal.</p>
    <div class="two-col">
      <div>
        {page2_body_html}
        <div class="stat-card">
          <div class="stat-num">{meta['stat']}</div>
          <div class="stat-text">{meta['stat_caption']} The first impression is the only impression.</div>
          <div class="stat-source">Source · {meta['stat_source']}</div>
        </div>
      </div>
      <div>
        <div class="illus illus-navy"><img src="{img_path('page2-zscan')}" alt=""></div>
        <div class="illus-cap">Investors don't read - they scan a Z. The page has to deliver on that path or it doesn't deliver at all.</div>
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

<!-- ============= PAGE 3 - THE 8 MUST-HAVES ============= -->
<div class="page">
  {header('www.pitchbird.de')}
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

<!-- ============= PAGE 4 - NICE TO HAVES + PRINCIPLES ============= -->
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

<!-- ============= PAGE 5 - ANATOMY MAP ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('04:', 'Anatomy')}
    <h2>Where everything goes on the page</h2>
    <p style="max-width:150mm;">Investors don't read a one-pager - they scan it in a Z-shape, top-left to bottom-right. The eight elements earn their spot only when they sit where eyes already land.</p>
    <div class="anatomy">
      <div class="anatomy-map">{anatomy_map_html}</div>
      <div class="anatomy-list">{anatomy_list_html}</div>
    </div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">05</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 6 - DO / DON'T ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('05:', 'Design in practice')}
    <h2>What separates a readable one-pager from a rejected one</h2>
    <p style="max-width:155mm;">The difference is rarely the idea - it's the execution of the page itself. Eight calls investors make in the first scan.</p>
    <div class="dodont">
      <div class="dodont-head">
        <div class="h-dont">Don't</div>
        <div class="h-do">Do</div>
      </div>
      {dodont_html}
    </div>
    <p class="dodont-note">{meta['do_dont_note']}</p>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">06</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 7A - EXAMPLES (1-2 of 3) ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('06:', 'Examples')}
    <h2>What strong one-pagers look like</h2>
    <p style="max-width:155mm;">Three patterns we see in the one-pagers that earn meetings - backed by published investor-engagement data.</p>
    <div class="examples">{examples_a_html}</div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">07</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 7B - EXAMPLES (3 of 3 + framework) ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('06:', 'Examples cont.')}
    <h2>And one more pattern</h2>
    <p style="max-width:155mm;">The third - and most consequential - pattern: the order in which information lands.</p>
    <div class="examples">{examples_b_html}</div>
    <div class="ex-framework">{meta['examples_framework']}</div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">08</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 9 - WORD ECONOMY ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('07:', 'Word economy')}
    <h2>Cut to 500 words. Then cut again.</h2>
    <p style="max-width:160mm;">The 400-500 word limit is the threshold above which investors stop reading. (Storydoc, 2024) The discipline of cutting is the work - and here is how to do it.</p>
    <div class="we-grid">{we_html}</div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">09</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 10A - FIRST 60 SECONDS (0-15) ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('08:', 'First 60 seconds')}
    <h2>What they read,<br>in what order.</h2>
    <p style="max-width:160mm;">{meta['first_60_intro']}</p>
    <div class="t60-grid">{t60_a_html}</div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">10</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 10B - FIRST 60 SECONDS (15-60) + 8-LINE RULE ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('08:', 'First 60 seconds cont.')}
    <h2>The decision window</h2>
    <p style="max-width:160mm;">By second 15, the partner has decided whether to keep reading. The next 45 seconds decide whether to reply.</p>
    <div class="t60-grid">{t60_b_html}</div>
    <div class="t60-rule">{meta['first_60_rule']}</div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">11</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 11 - PRESSURE-TEST ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('09:', 'Pressure-test')}
    <h2>Five tests before<br>you hit send.</h2>
    <p style="max-width:160mm;">{meta['pressure_test_intro']}</p>
    <div class="pt-grid">{pt_html}</div>
    <div class="pt-closing">{meta['pressure_test_closing']}</div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">12</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 12 - FAILURE MODES ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    {kicker('10:', 'Failure modes')}
    <h2>Why investors stop reading - and where</h2>
    <p style="max-width:155mm;">Each failure below maps to a specific drop-off point in investor attention. Know them before you send.</p>
    <div class="failures">{failures_html}</div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">13</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 10 - CLOSE + CTA ============= -->
<div class="page close">
  <div class="cover-band">
    <img src="{LOGO}" alt="Pitchbird">
    <div class="hdr-url">www.pitchbird.de</div>
  </div>
  <div class="body" style="padding-top:34mm;">
    {kicker('11:', 'Trade-offs')}
    <h2>What it gives you<br>- and what it can't</h2>
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
        <a class="cta-meta-action" href="mailto:office@pitchbird.de" style="color:var(--navy);text-decoration:none;">office@pitchbird.de</a>
        <div class="cta-meta-sub"><a href="tel:+4916097026216" style="color:rgba(3,17,42,0.7);text-decoration:none;">+49 (0) 160 97026216</a> · <a href="https://pitchbird.de" style="color:rgba(3,17,42,0.7);text-decoration:none;">pitchbird.de</a></div>
      </div>
    </div>
  </div>
  <div class="foot foot-dark">
    <span>Pitchbird · Founder Guide</span>
    <div class="foot-right">
      <span class="page-num">14</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 14 - ABOUT THE AUTHOR ============= -->
<div class="page">
  {header('www.pitchbird.de')}
  <div class="body">
    <div class="about-h1">
      <span class="black">About the</span> <span class="gold">Author</span>
    </div>
    <div class="about-body">{about_html}</div>
    <div class="about-portrait-row">
      <div class="about-portrait"><img src="{img_path('magdalena-portrait')}" alt="Magdalena Reith"></div>
      <a class="about-linkedin" href="https://www.linkedin.com/in/magdalena-reith-370108a1/">
        <span class="li-icon">in</span>
        <span>Connect with Magdalena</span>
      </a>
    </div>
  </div>
  <div class="foot">
    <span>The Power of the One Pager</span>
    <div class="foot-right">
      <span class="page-num">15</span>
      <span class="foot-arrow">{arrow}</span>
    </div>
  </div>
</div>

<!-- ============= PAGE 15 - FIND US ============= -->
<div class="page findus">
  <div class="findus-accent"></div>
  <div class="findus-band">
    <img src="{LOGO}" alt="Pitchbird">
    <a class="url" href="https://pitchbird.de">www.pitchbird.de</a>
  </div>
  <div class="findus-inner">
    <div class="findus-eyebrow">Find us</div>
    <div class="findus-h1">Let's make your one-pager <span class="gold">land.</span></div>
    <div class="findus-lede">Pitchbird helps founders craft pitch documents that earn the meeting. From a single one-pager review to a full investor-document overhaul - we're a message away.</div>
    <div class="findus-rows">
      <div class="findus-row">
        <div class="findus-row-label">Website</div>
        <div class="findus-row-value"><a href="https://pitchbird.de">pitchbird.de</a></div>
      </div>
      <div class="findus-row">
        <div class="findus-row-label">Email</div>
        <div class="findus-row-value"><a href="mailto:office@pitchbird.de">office@pitchbird.de</a></div>
      </div>
      <div class="findus-row">
        <div class="findus-row-label">Phone</div>
        <div class="findus-row-value"><a href="tel:+4916097026216">+49 (0) 160 97026216</a></div>
      </div>
      <div class="findus-row">
        <div class="findus-row-label">LinkedIn</div>
        <div class="findus-row-value"><a href="https://www.linkedin.com/in/magdalena-reith-370108a1/">linkedin.com/in/magdalena-reith-370108a1</a></div>
      </div>
    </div>
    <a class="findus-cta" href="mailto:office@pitchbird.de?subject=One-pager review request">Book a one-pager review &rarr;</a>
  </div>
  <div class="foot foot-dark">
    <span>Pitchbird · Founder Guide</span>
    <div class="foot-right">
      <span class="page-num">16</span>
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
        await page.pdf(path='{pdf_path.resolve()}',
                       width='210mm', height='297mm',
                       print_background=True, prefer_css_page_size=True,
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
