#!/usr/bin/env python3
"""Make every tool logo occupy the same optical weight.

Each source PNG carries a different amount of built-in padding, so at a fixed
CSS box one mark looks tiny and the next looks huge. This trims each logo to
its actual ink, scales the longest side to a fixed fraction of the canvas, and
recentres it. Run: python normalize_logos.py
"""
from pathlib import Path
from PIL import Image

DIR = Path('logos/tools')
CANVAS = 128
FILL = 0.86          # longest side of the mark, as a fraction of the canvas


def ink_box(im):
    """Bounding box of everything that is not transparent, falling back to
    non-uniform-background for logos saved without an alpha channel."""
    a = im.getchannel('A')
    bbox = a.getbbox()
    if bbox and (bbox[2] - bbox[0]) < im.width * 0.98:
        return bbox
    # opaque image: treat the corner pixel as the background colour
    rgb = im.convert('RGB')
    bg = rgb.getpixel((0, 0))
    mask = Image.new('L', im.size, 0)
    px, mpx = rgb.load(), mask.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > 28:
                mpx[x, y] = 255
    return mask.getbbox() or bbox


for f in sorted(DIR.glob('*.png')):
    im = Image.open(f).convert('RGBA')
    box = ink_box(im)
    if not box:
        print('%-14s skipped, no ink found' % f.name)
        continue
    mark = im.crop(box)
    target = int(CANVAS * FILL)
    scale = target / max(mark.size)
    mark = mark.resize((max(1, round(mark.width * scale)),
                        max(1, round(mark.height * scale))), Image.LANCZOS)
    out = Image.new('RGBA', (CANVAS, CANVAS), (0, 0, 0, 0))
    out.paste(mark, ((CANVAS - mark.width) // 2, (CANVAS - mark.height) // 2), mark)
    out.save(f)
    print('%-14s ink %sx%s -> mark %sx%s on %d canvas'
          % (f.name, box[2] - box[0], box[3] - box[1], mark.width, mark.height, CANVAS))
