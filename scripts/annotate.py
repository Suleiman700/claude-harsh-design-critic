#!/usr/bin/env python3
"""Draw numbered issue markers and measurement lines on a COPY of a screenshot.

Usage:
  python annotate.py <image> <spec.json> <out.png>

spec.json:
{
  "issues": [
    {"n": "DT-018", "box": [x1, y1, x2, y2]},          # red badge with the task id (or a number)
    {"n": "DT-005", "box": [x1, y1, x2, y2], "shape": "circle"},
    {"n": "DT-005", "box": [x1, y1, x2, y2], "badge": false}   # same issue elsewhere: thin box, no label
  ],
  "measures": [
    {"line": [x1, y1, x2, y2], "text": "72px"}          # cyan measurement line
  ]
}
The original image is never modified.
"""
import json
import sys

from PIL import Image, ImageDraw, ImageFont

RED = (235, 30, 45, 255)
CYAN = (0, 220, 255, 255)
WHITE = (255, 255, 255, 255)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def font(size):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def badge(draw, x, y, n, scale):
    """Red badge with the issue label. Short labels get a circle, task ids ("DT-018") a pill."""
    t = str(n)
    f = font(int(16 * scale))
    w = draw.textlength(t, font=f)
    r = int(14 * scale)
    half = max(r, w / 2 + 8 * scale)
    draw.rounded_rectangle([x - half, y - r, x + half, y + r], radius=r, fill=RED,
                           outline=WHITE, width=max(2, int(2 * scale)))
    draw.text((x - w / 2, y - 10 * scale), t, font=f, fill=WHITE)
    return half


def main():
    src, spec_path, out = sys.argv[1:4]
    im = Image.open(src).convert("RGBA")
    spec = json.load(open(spec_path))
    scale = max(1.0, min(im.size) / 500)
    lw = max(3, int(3 * scale))
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    for m in spec.get("measures", []):
        x1, y1, x2, y2 = m["line"]
        d.line([x1, y1, x2, y2], fill=CYAN, width=max(2, int(2 * scale)))
        # end ticks
        if abs(x2 - x1) < abs(y2 - y1):  # vertical line -> horizontal ticks
            for yy in (y1, y2):
                d.line([x1 - 8 * scale, yy, x1 + 8 * scale, yy], fill=CYAN, width=2)
        else:
            for xx in (x1, x2):
                d.line([xx, y1 - 8 * scale, xx, y1 + 8 * scale], fill=CYAN, width=2)
        f = font(int(14 * scale))
        tw = d.textlength(m["text"], font=f)
        tx, ty = (x1 + x2) / 2 + 6 * scale, (y1 + y2) / 2 - 8 * scale
        if abs(x2 - x1) >= abs(y2 - y1):  # horizontal line: label centered above it
            tx, ty = (x1 + x2) / 2 - tw / 2, min(y1, y2) - 24 * scale
        tx = min(max(4, tx), im.size[0] - tw - 6)  # keep labels inside the image
        if tx < max(x1, x2) and abs(x2 - x1) < abs(y2 - y1) and tx + tw > im.size[0] - 6:
            tx = min(x1, x2) - tw - 10 * scale
        ty = min(max(4, ty), im.size[1] - 22 * scale)
        d.rectangle([tx - 3, ty - 2, tx + tw + 3, ty + 18 * scale], fill=(0, 0, 0, 200))
        d.text((tx, ty), m["text"], font=f, fill=CYAN)

    placed = []
    r = 16 * scale
    for it in spec.get("issues", []):
        x1, y1, x2, y2 = it["box"]
        w = lw if it.get("badge", True) else max(2, lw // 2)  # secondary boxes: thinner, no label
        if it.get("shape") == "circle":
            d.ellipse([x1, y1, x2, y2], outline=RED, width=w)
        else:
            d.rectangle([x1, y1, x2, y2], outline=RED, width=w)
    fb = font(int(16 * scale))
    for it in [i for i in spec.get("issues", []) if i.get("badge", True)]:  # badges last, never overlapping
        x1, y1, x2, y2 = it["box"]
        half = max(r, d.textlength(str(it["n"]), font=fb) / 2 + 8 * scale)
        W, H = im.size
        clamp = lambda x, y: (min(max(x, half), W - half), min(max(y, r), H - r))
        # Stay attached to the box: try its corners and edges, then just above/below them.
        cands = [(x1 + half - r, y1), (x2 - half + r, y1), (x1 + half - r, y2), (x2 - half + r, y2),
                 ((x1 + x2) / 2, y1), ((x1 + x2) / 2, y2),
                 (x1 + half - r, y1 - 2.2 * r), (x2 - half + r, y1 - 2.2 * r),
                 (x1 + half - r, y2 + 2.2 * r), (x2 - half + r, y2 + 2.2 * r),
                 (x1 - half - 4, (y1 + y2) / 2), (x2 + half + 4, (y1 + y2) / 2)]
        free = lambda bx, by: all(abs(bx - p[0]) >= half + p[2] + 4 or abs(by - p[1]) >= 2.1 * r for p in placed)
        bx, by = clamp(*cands[0])
        for c in cands:
            cx, cy = clamp(*c)
            if free(cx, cy):
                bx, by = cx, cy
                break
        placed.append((bx, by, half))
        badge(d, bx, by, it["n"], scale)

    Image.alpha_composite(im, overlay).convert("RGB").save(out)
    print(out)


if __name__ == "__main__":
    main()
