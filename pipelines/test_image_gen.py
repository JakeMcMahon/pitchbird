#!/usr/bin/env python3
"""Test OpenRouter image gen for Pitchbird lead magnets."""
import os, sys, json, base64, pathlib, urllib.request

API_KEY = os.environ["OPENROUTER_API_KEY"]
OUT = pathlib.Path("/root/pitchbird/lm-test-images")
OUT.mkdir(parents=True, exist_ok=True)

STYLE = (
    "Editorial flat vector illustration in the style of a premium investor "
    "guide. Restricted palette: deep navy #0F1B3D, mustard gold #F4B82E, "
    "warm salmon #F5896A, cream off-white #F8F6F1. Soft paper-grain texture. "
    "Geometric paper-cut layered shapes, clean lines, generous negative "
    "space, no text, no faces, no watermarks. High-end editorial magazine "
    "aesthetic, Pentagram / It's Nice That feel."
)

TESTS = [
    {
        "name": "one-pager-hero",
        "size": "1024x1536",
        "prompt": (
            "Hero illustration for a startup pitch one-pager guide. "
            "Single sheet of paper floating at slight 3D angle, divided into "
            "8 labeled rectangular sections suggesting a one-page business "
            "summary. A magnifying glass in mustard gold hovers over one "
            "section. Small dotted connection lines. Deep navy background "
            "with subtle gold triangular accent in upper-right corner bleeding "
            "off the edge. Generous bottom negative space for headline overlay. "
            + STYLE
        ),
    },
    {
        "name": "must-haves-checklist",
        "size": "1024x1024",
        "prompt": (
            "Conceptual illustration of 'investor first impression': a tall "
            "stack of paper documents in cream and off-white, with one "
            "highlighted document in mustard gold rising to the top, "
            "glowing softly. Small salmon-colored checkmarks float around "
            "the gold document. Deep navy backdrop. Composition centered, "
            "square, suitable for a chapter-section header. "
            + STYLE
        ),
    },
]

def gen(test):
    print(f"Generating {test['name']}...", flush=True)
    body = {
        "model": "openai/gpt-5-image",
        "messages": [{"role": "user", "content": test["prompt"]}],
        "modalities": ["image", "text"],
        "extra_body": {"size": test["size"]},
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
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read())
    (OUT / f"{test['name']}.response.json").write_text(json.dumps(data, indent=2)[:5000])
    # Try multiple shapes for image output
    msg = data["choices"][0]["message"]
    images = msg.get("images") or []
    if not images and isinstance(msg.get("content"), list):
        images = [c for c in msg["content"] if c.get("type") == "image_url"]
    saved = []
    for i, img in enumerate(images):
        url = img.get("image_url", {}).get("url") if isinstance(img.get("image_url"), dict) else img.get("image_url")
        if not url:
            url = img.get("url")
        if url and url.startswith("data:"):
            b64 = url.split(",", 1)[1]
            path = OUT / f"{test['name']}-{i}.png"
            path.write_bytes(base64.b64decode(b64))
            saved.append(str(path))
        elif url:
            path = OUT / f"{test['name']}-{i}.png"
            urllib.request.urlretrieve(url, path)
            saved.append(str(path))
    print(f"  saved: {saved or 'NONE — see response.json'}")
    return saved

if __name__ == "__main__":
    for t in TESTS:
        try:
            gen(t)
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback; traceback.print_exc()
