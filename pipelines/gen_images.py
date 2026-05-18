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
    "Bold flat vector illustration in a premium business publication "
    "style. Strict palette ONLY: deep navy #03112A, mustard gold #FBB03B, "
    "bright sky blue #2A98D9, off-white #F5F2EC. SOLID DEEP NAVY "
    "background filling the entire image — NO cream, NO white background, "
    "NO paper texture. Bold geometric shapes, large flat color fills, "
    "thick confident lines, generous negative space. NO text, NO letters, "
    "NO numbers, NO faces, NO watermarks, NO logos. Style: Mailchimp / "
    "Stripe illustration system — graphic, modern, instantly readable at "
    "small sizes."
)

IMAGES = {
    "page2-concept": (
        "Bold flat illustration on solid deep navy #03112A background. "
        "Centered: a single off-white #F5F2EC rectangular sheet of paper "
        "tilted at 8 degrees, divided into 6 labeled blocks suggesting a "
        "one-page business summary — block outlines visible but no real "
        "text. A bright gold #FBB03B circle (representing focus / a stamp) "
        "overlaps the top-right corner of the paper. A small bright blue "
        "#2A98D9 square sits on the lower-left corner of the paper as a "
        "highlighted section. Generous navy negative space around the "
        "paper. " + STYLE_ANCHOR
    ),
    "page2-funnel": (
        "Bold flat illustration on solid deep navy #03112A background. "
        "An inverted funnel made of three stacked horizontal bars in "
        "off-white, narrowing toward the bottom — top bar widest, bottom "
        "bar narrowest. The bottom bar is bright gold #FBB03B. Suggests "
        "qualification / filtering of investors. A tiny bright blue circle "
        "sits inside the gold bar. Centered square composition. " + STYLE_ANCHOR
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
