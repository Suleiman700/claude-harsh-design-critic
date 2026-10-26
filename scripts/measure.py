#!/usr/bin/env python3
"""Pixel measurement helpers so reviews report numbers, not impressions.

Commands:
  python measure.py blobs <image> --color "#5BC83A" [--tol 40] [--region x1,y1,x2,y2] [--min 200]
      Bounding boxes of connected regions close to a color (e.g. all green buttons,
      all currency pills). Use it to compare sibling heights and positions.

  python measure.py fg <image> --region x1,y1,x2,y2 [--bg auto|#RRGGBB] [--tol 30]
      Bounding box of the content inside a container (pixels that differ from the
      container background). Prints content center vs region center offset:
      the number that proves "the price is not centered in the button".

  python measure.py contrast "#FFFFFF" "#2F6BD8"
      WCAG contrast ratio between two colors.

  python measure.py pick <image> x,y
      Hex color at a pixel.
"""
import argparse
import json

import numpy as np
from PIL import Image
from scipy import ndimage


def hex2rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)


def load(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(float)


def crop(a, region):
    if not region:
        return a, 0, 0
    x1, y1, x2, y2 = [int(v) for v in region.split(",")]
    return a[y1:y2, x1:x2], x1, y1


def cmd_blobs(o):
    a, ox, oy = crop(load(o.image), o.region)
    mask = np.sqrt(((a - hex2rgb(o.color)) ** 2).sum(-1)) < o.tol
    lab, n = ndimage.label(mask)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        area = int((lab[sl] == i).sum())
        if area < o.min:
            continue
        y, x = sl
        out.append({"x1": x.start + ox, "y1": y.start + oy, "x2": x.stop + ox, "y2": y.stop + oy,
                    "w": x.stop - x.start, "h": y.stop - y.start,
                    "cx": (x.start + x.stop) / 2 + ox, "cy": (y.start + y.stop) / 2 + oy, "area": area})
    out.sort(key=lambda b: (b["y1"] // 20, b["x1"]))
    print(json.dumps(out, indent=1))


def cmd_fg(o):
    a, ox, oy = crop(load(o.image), o.region)
    if o.bg == "auto":
        edge = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
        vals, counts = np.unique((edge // 8).astype(int), axis=0, return_counts=True)
        bg = vals[counts.argmax()] * 8 + 4
    else:
        bg = hex2rgb(o.bg)
    mask = np.sqrt(((a - bg) ** 2).sum(-1)) > o.tol
    mask = ndimage.binary_opening(mask, iterations=1)
    ys, xs = np.where(mask)
    if not len(xs):
        print(json.dumps({"error": "no content found"}))
        return
    h, w = a.shape[:2]
    c = {"content": [int(xs.min()) + ox, int(ys.min()) + oy, int(xs.max()) + ox, int(ys.max()) + oy],
         "content_center": [float((xs.min() + xs.max()) / 2 + ox), float((ys.min() + ys.max()) / 2 + oy)],
         "region_center": [ox + w / 2, oy + h / 2]}
    c["offset_px"] = [round(c["content_center"][0] - c["region_center"][0], 1),
                      round(c["content_center"][1] - c["region_center"][1], 1)]
    c["bg"] = "#%02X%02X%02X" % tuple(int(v) for v in bg)
    print(json.dumps(c, indent=1))


def lum(rgb):
    c = rgb / 255
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def cmd_contrast(o):
    l1, l2 = sorted([lum(hex2rgb(o.c1)), lum(hex2rgb(o.c2))], reverse=True)
    r = (l1 + 0.05) / (l2 + 0.05)
    print(json.dumps({"ratio": round(float(r), 2), "AA_text": bool(r >= 4.5), "AA_large": bool(r >= 3)}))


def cmd_pick(o):
    a = load(o.image)
    x, y = [int(v) for v in o.xy.split(",")]
    print("#%02X%02X%02X" % tuple(int(v) for v in a[y, x]))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("blobs"); b.add_argument("image"); b.add_argument("--color", required=True)
    b.add_argument("--tol", type=float, default=40); b.add_argument("--region"); b.add_argument("--min", type=int, default=200)
    f = sp.add_parser("fg"); f.add_argument("image"); f.add_argument("--region", required=True)
    f.add_argument("--bg", default="auto"); f.add_argument("--tol", type=float, default=30)
    c = sp.add_parser("contrast"); c.add_argument("c1"); c.add_argument("c2")
    p = sp.add_parser("pick"); p.add_argument("image"); p.add_argument("xy")
    o = ap.parse_args()
    {"blobs": cmd_blobs, "fg": cmd_fg, "contrast": cmd_contrast, "pick": cmd_pick}[o.cmd](o)


if __name__ == "__main__":
    main()
