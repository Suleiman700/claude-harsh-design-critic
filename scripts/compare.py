#!/usr/bin/env python3
"""Side-by-side boards: before/after proof images and competitor comparison boards.

Usage:
  python compare.py <out.png> --title "DT-007 settings button" \
      --item "Before=before.png" --item "After=after.png" [--note "pills 72px / settings 72px"]

  python compare.py board.png --title "Booster bar vs market" \
      --item "Yours=mine.png" --item "Block Blast=bb.png" --item "Royal Match=rm.png"

All images are scaled to the same height and labeled.
"""
import argparse

from PIL import Image, ImageDraw, ImageFont


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
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--item", action="append", required=True, help="Label=path")
    ap.add_argument("--title", default="")
    ap.add_argument("--note", default="")
    ap.add_argument("--height", type=int, default=520)
    a = ap.parse_args()

    items = []
    for it in a.item:
        label, path = it.split("=", 1)
        im = Image.open(path).convert("RGB")
        im = im.resize((int(im.width * a.height / im.height), a.height))
        items.append((label, im))

    pad, head, top = 16, 34, 56 if a.title else 16
    foot = 40 if a.note else 0
    W = sum(i.width for _, i in items) + pad * (len(items) + 1)
    H = top + head + a.height + pad + foot
    board = Image.new("RGB", (W, H), (22, 22, 26))
    d = ImageDraw.Draw(board)
    if a.title:
        d.text((pad, 14), a.title, fill="white", font=font(26))
    x = pad
    for label, im in items:
        color = (120, 230, 140) if label.lower() in ("after", "yours (after)") else (255, 210, 80)
        d.text((x, top + 4), label, fill=color, font=font(20))
        board.paste(im, (x, top + head))
        x += im.width + pad
    if a.note:
        d.text((pad, H - foot + 6), a.note, fill=(200, 200, 210), font=font(18))
    board.save(a.out)
    print(a.out)


if __name__ == "__main__":
    main()
