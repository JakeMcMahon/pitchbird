#!/usr/bin/env python3
"""Generate Pitchbird lead-magnet images via OpenRouter (openai/gpt-5-image).

Composite trick: GPT-5-image often ignores 'navy background' — we generate
illustrations on a cream/transparent feel and place them on navy via CSS.
"""
import os, sys, json, base64, pathlib, urllib.request, argparse

API_KEY = os.environ["OPENROUTER_API_KEY"]
OUT = pathlib.Path("/root/pitchbird/lm-images/one-pager")
OUT.mkdir(parents=True, exist_ok=True)

STYLE_ANCHOR = (
    "Editorial flat vector illustration for a premium investor guide. "
    "Restricted palette ONLY: deep navy #0F1B3D, mustard gold #F4B82E, "
    "warm salmon #F5896A, cream #F8F6F1, off-white. Soft paper-grain "
    "texture. Geometric paper-cut layered shapes, clean confident lines, "
    "generous negative space. NO text, NO letters, NO numbers, NO faces, "
    "NO watermarks, NO logos. Pentagram / It's Nice That editorial feel. "
    "Cream off-white background, no harsh white."
)

IMAGES = {
    "cover-hero": (
        "Hero composition for a book chapter cover about 'the one pager' for "
        "startup founders. Centered: a single sheet of paper tilted at a 12 "
        "degree angle, slightly overlapping a smaller folded paper behind it. "
        "Mustard gold geometric triangle bleeding from the upper-right corner. "
        "A small salmon dot in the lower-left as visual rhythm. Composition "
        "leaves the lower third empty for headline overlay. " + STYLE_ANCHOR
    ),
    "design-principles": (
        "Illustration of layout and hierarchy: three abstract document panels "
        "arranged in a staggered diagonal cascade, each panel showing simple "
        "horizontal line patterns suggesting paragraphs and one gold "
        "rectangle suggesting a highlighted block. A salmon arrow flows "
        "between them suggesting visual flow. Centered square composition. "
        + STYLE_ANCHOR
    ),
    "cta-consultation": (
        "Two minimalist coffee cups on saucers facing each other across a "
        "subtle cream tabletop, suggesting a founder-investor conversation. "
        "Soft gold steam curls rise from one cup. A tiny salmon notepad sits "
        "to the side. Generous negative space. " + STYLE_ANCHOR
    ),
}

def gen(name, prompt):
    print(f"→ {name}", flush=True)
    body = {
        "model": "openai/gpt-5-image",
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://pitchbird.de",
            "X-Title": "Pitchbird Lead Magnet",
        },
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        data = json.loads(r.read())
    msg = data["choices"][0]["message"]
    images = msg.get("images") or []
    if not images:
        print(f"  NO IMAGE — finish={data['choices'][0].get('finish_reason')}")
        return None
    img = images[0]
    url = (img.get("image_url") or {}).get("url") if isinstance(img.get("image_url"), dict) else img.get("image_url")
    if url and url.startswith("data:"):
        path = OUT / f"{name}.png"
        path.write_bytes(base64.b64decode(url.split(",", 1)[1]))
        print(f"  saved {path}")
        return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="*", help="generate only these keys")
    args = parser.parse_args()
    for name, prompt in IMAGES.items():
        if args.only and name not in args.only:
            continue
        try:
            gen(name, prompt)
        except Exception as e:
            print(f"  ERROR {name}: {e}")
