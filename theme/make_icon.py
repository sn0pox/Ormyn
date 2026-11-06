"""Regenerates ormyn.ico and ormyn-icon.png in this folder.   pip install pillow numpy

Design: a black pill floating on a dark rounded tile, lit by a pale-gold > gold > amber glow,
with two glowing vertical slit eyes. No other face details.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
S = 1024
PALE, GOLD, AMBER = (255, 233, 166), (255, 200, 61), (226, 142, 18)
stops = [(0.0, PALE), (0.5, GOLD), (1.0, AMBER)]

def make_field(vertical=False):
    yy, xx = np.mgrid[0:S, 0:S]
    t = (yy - 250) / 600 if vertical else (xx * 0.75 + yy * 0.25 - 150) / (S - 300)
    t = np.clip(t, 0, 1)
    f = np.zeros((S, S, 3), np.float32)
    for i in range(3):
        f[..., i] = np.interp(t, [s[0] for s in stops], [s[1][i] for s in stops])
    return Image.fromarray(f.astype(np.uint8)).convert("RGBA")

FIELD, FIELD_V = make_field(), make_field(True)

def shape(fn, blur=0):
    m = Image.new("L", (S, S), 0)
    fn(ImageDraw.Draw(m))
    return m.filter(ImageFilter.GaussianBlur(blur)) if blur else m

def pill(grow):
    return lambda d: d.rounded_rectangle((190 - grow, 330 - grow, 834 + grow, 694 + grow), radius=182 + grow, fill=255)

# dark rounded tile
tile = shape(lambda d: d.rounded_rectangle((0, 0, S - 1, S - 1), radius=230, fill=255))
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
img.paste(Image.new("RGBA", (S, S), (8, 8, 10, 255)), (0, 0), tile)

# glow around the pill
halo = FIELD.copy()
halo.putalpha(shape(pill(80), blur=55).point(lambda v: int(v * 0.72)))
img = Image.alpha_composite(img, halo)

# gradient rim, then the black pill
body = shape(pill(0))
rim = FIELD.copy()
rim.putalpha(ImageChops.subtract(shape(pill(12)), body))
img = Image.alpha_composite(img, rim)
black = Image.new("RGBA", (S, S), (0, 0, 0, 255))
black.putalpha(body)
img = Image.alpha_composite(img, black)

# slit eyes: soft bloom behind, crisp gradient shape on top (4x supersampled edge)
for cx in (402, 622):
    bloom = shape(lambda d: d.rounded_rectangle((cx - 44, 512 - 96, cx + 44, 512 + 96), radius=44, fill=255), blur=26)
    b = FIELD_V.copy()
    b.putalpha(bloom.point(lambda v: int(v * 0.55)))
    img = Image.alpha_composite(img, b)
    box = (cx - 46, 512 - 100, cx + 46, 512 + 100)
    k, w, h = 4, box[2] - box[0], box[3] - box[1]
    m = Image.new("L", (w * k, h * k), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * k - 1, h * k - 1), radius=46 * k, fill=255)
    img.paste(FIELD_V.crop(box), box[:2], m.resize((w, h), Image.LANCZOS))

final = Image.new("RGBA", (S, S), (0, 0, 0, 0))
final.paste(img, (0, 0), tile)
final.save(os.path.join(HERE, "ormyn-icon.png"))
final.save(os.path.join(HERE, "ormyn.ico"), sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("wrote ormyn.ico and ormyn-icon.png")
