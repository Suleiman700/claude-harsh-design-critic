#!/usr/bin/env python3
"""One cropped, annotated screenshot per issue, named after its task id.

Usage:
  python issue_shots.py <spec.json> <out_dir>

spec.json:
{
  "source": "docs/game-prompts/design-review/screenshots/screens/review-01_shop.png",
  "issues": [
    {"id": "DT-001", "slug": "shop-price-overlay", "title": "Price centered in stray overlay",
     "severity": "CRITICAL", "box": [700, 372, 828, 522],
     "extra_boxes": [[700, 625, 828, 820]],                 # optional: same issue elsewhere
     "measures": [{"line": [624, 560, 858, 560], "text": "btn 741 / price 769"}],   # optional
     "pad": 120}                                             # optional context around the boxes
  ]
}
Writes <out_dir>/<id>_<slug>.png, e.g. DT-001_shop-price-overlay.png, and prints a markdown
link line per file to paste into DESIGN_TASKS.md / the review. The source is never modified.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

RED, CYAN = (235, 30, 45), (0, 200, 240)
SEV_COLORS = {"CRITICAL": (235, 30, 45), "MAJOR": (245, 140, 30), "MINOR": (230, 190, 40), "NITPICK": (150, 150, 160)}


def font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "C:/Windows/Fonts/arialbd.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def main():
    spec_path, out_dir = sys.argv[1:3]
    spec = json.load(open(spec_path))
    src = Image.open(spec["source"]).convert("RGB")
    W, H = src.size
    os.makedirs(out_dir, exist_ok=True)
    for it in spec["issues"]:
        boxes = [it["box"]] + it.get("extra_boxes", [])
        pts = [b for b in boxes] + [m["line"] for m in it.get("measures", [])]
        pad = it.get("pad", 100)
        x1 = max(0, min(p[0] for p in pts) - pad); y1 = max(0, min(p[1] for p in pts) - pad)
        x2 = min(W, max(p[2] for p in pts) + pad); y2 = min(H, max(p[3] for p in pts) + pad)
        cw = x2 - x1
        lw = max(3, cw // 160)
        f = font(max(14, min(24, cw // 36)))
        measures = it.get("measures", [])
        # Labels live in a dark strip under the image, so they never cover what they measure.
        strip = (f.size + 18) if measures else 0
        img = Image.new("RGB", (cw, (y2 - y1) + strip), (22, 22, 26))
        img.paste(src.crop((x1, y1, x2, y2)), (0, 0))
        d = ImageDraw.Draw(img)
        sh = lambda p: [p[0] - x1, p[1] - y1, p[2] - x1, p[3] - y1]
        for b in boxes:
            d.rectangle(sh(b), outline=RED, width=lw)
        ch = y2 - y1
        for m in measures:
            lx1, ly1, lx2, ly2 = sh(m["line"])
            d.line([lx1, ly1, lx2, ly2], fill=CYAN, width=max(2, lw - 1))
            mx = (lx1 + lx2) / 2
            # dotted leader from the line down into the label strip
            for yy in range(int(max(ly1, ly2)) + 4, ch + 6, 8):
                d.line([mx, yy, mx, yy + 3], fill=CYAN, width=2)
            tw = d.textlength(m["text"], font=f)
            tx = min(max(4, mx - tw / 2), cw - tw - 4)
            ty = ch + 8
            d.text((tx, ty), m["text"], font=f, fill=CYAN)
        crop = img
        if crop.width < 640:  # small crops are hard to read and the title won't fit; upscale for viewing
            s = 640 / crop.width
            crop = crop.resize((int(crop.width * s), int(crop.height * s)), Image.LANCZOS)
        # banner with id, severity and title
        bf = font(20)
        label = f'{it["id"]} · {it.get("severity", "")} · {it.get("title", "")}'.replace(" ·  · ", " · ")
        bh = 40
        out = Image.new("RGB", (crop.width, crop.height + bh), (22, 22, 26))
        out.paste(crop, (0, bh))
        od = ImageDraw.Draw(out)
        od.rectangle([0, 0, 8, bh], fill=SEV_COLORS.get(it.get("severity", ""), RED))
        while od.textlength(label, font=bf) > crop.width - 24 and len(label) > 10:
            label = label[:-2]
        od.text((16, 9), label, font=bf, fill="white")
        name = f'{it["id"]}_{it["slug"]}.png'
        out.save(os.path.join(out_dir, name))
        print(f'[{it["id"]}](screenshots/issues/{name})')


if __name__ == "__main__":
    main()
