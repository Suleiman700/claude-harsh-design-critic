#!/usr/bin/env python3
"""Extract the dominant colors of a screenshot (k-means) and render a swatch strip.

Usage:
  python palette.py <image> [--k 10] [--out swatches.png]

Prints JSON: [{"hex": "#2F6BD8", "share": 0.31}, ...] sorted by share.
"""
import argparse
import json

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def kmeans(px, k, iters=20, seed=0):
    rng = np.random.default_rng(seed)
    centers = px[rng.choice(len(px), k, replace=False)].astype(float)
    for _ in range(iters):
        d = ((px[:, None, :] - centers[None]) ** 2).sum(-1)
        lab = d.argmin(1)
        for i in range(k):
            m = px[lab == i]
            if len(m):
                centers[i] = m.mean(0)
    return centers, lab


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--out")
    a = ap.parse_args()

    im = Image.open(a.image).convert("RGB")
    im.thumbnail((300, 300))
    px = np.asarray(im).reshape(-1, 3).astype(float)
    centers, lab = kmeans(px, a.k)
    counts = np.bincount(lab, minlength=a.k) / len(lab)
    order = np.argsort(-counts)
    result = [
        {"hex": "#%02X%02X%02X" % tuple(int(v) for v in centers[i]), "share": round(float(counts[i]), 3)}
        for i in order if counts[i] > 0.005
    ]
    print(json.dumps(result, indent=1))

    if a.out:
        w, h = 120, 90
        strip = Image.new("RGB", (w * len(result), h + 26), "white")
        d = ImageDraw.Draw(strip)
        try:
            f = ImageFont.load_default(14)
        except TypeError:
            f = ImageFont.load_default()
        for i, c in enumerate(result):
            d.rectangle([i * w, 0, (i + 1) * w - 2, h], fill=c["hex"])
            d.text((i * w + 6, h + 5), f'{c["hex"]} {int(c["share"] * 100)}%', fill="black", font=f)
        strip.save(a.out)


if __name__ == "__main__":
    main()
