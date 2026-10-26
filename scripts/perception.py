#!/usr/bin/env python3
"""Perception and colorblind tests in one contact sheet.

Usage:
  python perception.py <image> <out.png>

Panels: original, blur (squint test), grayscale, deuteranopia, protanopia, tritanopia.
- Blur: is the hierarchy still obvious? The primary action should still be the
  first thing you see.
- Grayscale: do states, pieces and currencies still differ without color?
- Colorblind: do any two game pieces / states collapse into the same color?
Colorblind matrices: Machado et al. 2009 (severity 1.0), applied in linear RGB.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

CVD = {
    "Deuteranopia": np.array([[0.367322, 0.860646, -0.227968],
                              [0.280085, 0.672501, 0.047413],
                              [-0.011820, 0.042940, 0.968881]]),
    "Protanopia": np.array([[0.152286, 1.052583, -0.204868],
                            [0.114503, 0.786281, 0.099216],
                            [-0.003882, -0.048116, 1.051998]]),
    "Tritanopia": np.array([[1.255528, -0.076749, -0.178779],
                            [-0.078411, 0.930809, 0.147602],
                            [0.004733, 0.691367, 0.303900]]),
}


def to_lin(a):
    a = a / 255.0
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def to_srgb(a):
    a = np.clip(a, 0, 1)
    return (np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055) * 255).astype(np.uint8)


def simulate(im, m):
    lin = to_lin(np.asarray(im).astype(float))
    return Image.fromarray(to_srgb(lin @ m.T))


def main():
    src, out = sys.argv[1:3]
    im = Image.open(src).convert("RGB")
    if max(im.size) > 700:
        im.thumbnail((700, 700))
    blur_r = max(4, min(im.size) // 60)
    panels = [
        ("Original", im),
        ("Blur / squint", im.filter(ImageFilter.GaussianBlur(blur_r))),
        ("Grayscale", im.convert("L").convert("RGB")),
    ] + [(name, simulate(im, m)) for name, m in CVD.items()]

    w, h = im.size
    pad, head = 10, 30
    sheet = Image.new("RGB", (3 * w + 4 * pad, 2 * (h + head) + 3 * pad), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.load_default(18)
    except TypeError:
        f = ImageFont.load_default()
    for i, (name, p) in enumerate(panels):
        x = pad + (i % 3) * (w + pad)
        y = pad + (i // 3) * (h + head + pad)
        d.text((x, y + 4), name, fill="white", font=f)
        sheet.paste(p, (x, y + head))
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
