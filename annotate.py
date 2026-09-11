#!/usr/bin/env python3
"""Annotate the product page screenshot with the three matchable fields.

Crops to the info column, dims everything that is not a target, then draws
accent boxes and numbered badges. The explanation lives in the HTML caption
so the text stays selectable and on-brand.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

SRC = Path('shots/product-page.png')
OUT = Path('shots/product-page-annotated.png')

ACC = (255, 146, 71)
INK = (10, 11, 12)

im = Image.open(SRC).convert('RGB')
W, H = im.size

# crop away the empty lower-left and the big product photo, keep the info column
crop = im.crop((740, 0, W, 560))
cw, ch = crop.size
scale = 2
crop = crop.resize((cw * scale, ch * scale), Image.LANCZOS)
cw, ch = crop.size

# targets in ORIGINAL page coords -> shifted by the crop, then scaled
targets = [
    ('1', (762, 55, 1500, 125)),     # product name
    ('2', (880, 155, 1100, 222)),    # price
    ('3', (1300, 480, 1565, 530)),   # model number
]

# dim the whole frame, then punch the targets back to full brightness
dim = Image.eval(crop, lambda p: int(p * 0.42))
for _, (x0, y0, x1, y1) in targets:
    box = ((x0 - 740) * scale, y0 * scale, (x1 - 740) * scale, y1 * scale)
    dim.paste(crop.crop(box), (box[0], box[1]))
canvas = dim

d = ImageDraw.Draw(canvas)


def font(sz):
    for p in ('C:/Windows/Fonts/segoeuib.ttf', 'C:/Windows/Fonts/arialbd.ttf'):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()


f_badge = font(30)

for label, (x0, y0, x1, y1) in targets:
    bx0, by0 = (x0 - 740) * scale, y0 * scale
    bx1, by1 = (x1 - 740) * scale, y1 * scale
    d.rounded_rectangle([bx0 - 6, by0 - 6, bx1 + 6, by1 + 6], radius=10,
                        outline=ACC, width=4)
    # numbered badge on the top-left corner of the box
    r = 22
    cx, cy = bx0 - 6, by0 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACC)
    tb = d.textbbox((0, 0), label, font=f_badge)
    d.text((cx - (tb[2] - tb[0]) / 2, cy - (tb[3] - tb[1]) / 2 - 4),
           label, font=f_badge, fill=INK)

# thin border so it reads as a framed object on the dark page
d.rectangle([0, 0, cw - 1, ch - 1], outline=(60, 60, 64), width=2)

canvas.save(OUT, optimize=True)
print('%s  %s  %.0f KB' % (OUT, canvas.size, OUT.stat().st_size / 1024))
