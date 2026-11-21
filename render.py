#!/usr/bin/env python3
"""Saturday 21 November 2026 front page, v2 — PIL + Noto vector type.

A fresh render for news-image-20261121 v2. One 1024x1024 cream front
page: masthead naming the day, a six-number strip, three large hero
scenes, a 4-column grid of the remaining 14 stories, and a numbered
world map with one dot per story. Every letter is Noto Sans / Noto
Serif vector type. Deterministic: fixed seeds, no clock, no network.

v2 fixes v1's date errors: every story here happened, or was first
reported, on Saturday 21 November 2026 (see LOCKED.md for the audit).
17 stories, 7 regions.
"""
import json
import math
import random
from pathlib import Path

WORK = Path("/home/hatch/workspace/makefun/news-image-20261121-v2-work")
REPO = Path("/home/hatch/workspace/makefun/news-image-20261121-v2-work/repo")
GEO = Path("/home/hatch/workspace/makefun/news-image-20261117-work/world-110m.geojson")
OUT = REPO / "entry.png"

W, H = 1024, 1024
CREAM = (247, 241, 226)
PAPER = (255, 252, 244)
INK = (28, 38, 48)
SOFT = (84, 96, 104)
GOLD = (158, 118, 8)
GOLDD = (132, 98, 2)
RULE = (210, 198, 170)
SEA = (214, 230, 236)
LAND = (196, 206, 180)
EDGE = (164, 178, 148)
RED = (186, 52, 40)

FD = Path("/usr/share/fonts/truetype/noto")


def fnt(name, size):
    return ImageFont.truetype(str(FD / name), size)


from PIL import Image, ImageDraw, ImageFont

F_KICK = fnt("NotoSans-Bold.ttf", 15)
F_TITLE = fnt("NotoSerif-Bold.ttf", 46)
F_SUB = fnt("NotoSans-Regular.ttf", 13)
F_BIG = fnt("NotoSans-CondensedBold.ttf", 22)
F_LBL = fnt("NotoSans-Regular.ttf", 10)
F_HKICK = fnt("NotoSans-Bold.ttf", 11)
F_HHEAD = fnt("NotoSans-CondensedBold.ttf", 21)
F_HBODY = fnt("NotoSans-Regular.ttf", 12)
F_GKICK = fnt("NotoSans-Bold.ttf", 9)
F_GHEAD = fnt("NotoSans-CondensedBold.ttf", 13)
F_MTITLE = fnt("NotoSans-Bold.ttf", 13)
F_MLBL = fnt("NotoSans-Bold.ttf", 10)
F_MNUM = fnt("NotoSans-Bold.ttf", 9)
F_FOOT = fnt("NotoSans-Regular.ttf", 10)


def wrap(d, text, font, maxw):
    """Greedy word wrap to lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, font, fill, lead):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lead
    return y


def vgrad(size, top, bottom):
    """Vertical gradient, returned as RGBA."""
    w, h = size
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for yy in range(h):
        t = yy / max(h - 1, 1)
        px[0, yy] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return strip.resize((w, h)).convert("RGBA")


def speckle(img, n, seed):
    rng = random.Random(seed)
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    w, h = img.size
    for _ in range(n):
        x, y = rng.randrange(w), rng.randrange(h)
        c = (255, 255, 255) if rng.random() < 0.5 else (70, 60, 40)
        d.point((x, y), fill=c + (7,))
    img.alpha_composite(ov)


# ------------------------------------------------------------------ heroes
def scene_cop(w, h):
    """COP31 hall at night: big round emblem, long curved table, flags."""
    img = vgrad((w, h), (226, 206, 164), (188, 156, 104)).convert("RGBA")
    d = ImageDraw.Draw(img)
    rng = random.Random(101)
    # dark wood ceiling band
    d.rectangle([0, 0, w, 10], fill=(96, 70, 44, 255))
    # round emblem on the wall, left
    cx, cy, r = 66, 52, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(18, 64, 84, 255),
              outline=(240, 214, 140, 255), width=3)
    d.text((cx, cy - 16), "COP31", font=fnt("NotoSans-CondensedBold.ttf", 22),
           fill=(255, 255, 255, 255), anchor="ma")
    d.text((cx, cy + 8), "ANTALYA", font=fnt("NotoSans-Bold.ttf", 11),
           fill=(150, 205, 220, 255), anchor="ma")
    # wall clock, right — talks running past midnight
    d.ellipse([w - 62, 16, w - 22, 56], fill=(250, 246, 232, 255),
              outline=(90, 70, 40, 255), width=2)
    d.line([(w - 42, 36), (w - 42, 22)], fill=(40, 40, 40, 255), width=2)
    d.line([(w - 42, 36), (w - 52, 44)], fill=(40, 40, 40, 255), width=2)
    d.text((w - 42, 62), "OVERTIME", font=fnt("NotoSans-Bold.ttf", 9),
           fill=(120, 60, 20, 255), anchor="ma")
    # delegates: heads and shoulders along the table
    suits = [(44, 66, 118), (96, 44, 54), (54, 96, 64), (76, 76, 88),
             (118, 84, 44), (60, 60, 110)]
    for i, suit in enumerate(suits):
        hx = 30 + i * 52
        d.ellipse([hx - 9, 78, hx + 9, 96], fill=(224, 186, 150, 255))
        d.pieslice([hx - 9, 78, hx + 9, 88], 180, 360, fill=(58, 44, 30, 255))
        d.polygon([(hx - 17, 104), (hx + 17, 104), (hx + 12, 94), (hx - 12, 94)],
                  fill=suit + (255,))
    # long table with a green runner and papers
    d.polygon([(8, 104), (w - 8, 104), (w - 2, h - 2), (2, h - 2)],
              fill=(96, 62, 34, 255))
    d.polygon([(30, 108), (w - 30, 108), (w - 16, 120), (16, 120)],
              fill=(140, 190, 180, 255))
    for i in range(6):
        px = 44 + i * 46
        d.rectangle([px - 10, 114, px + 10, 121], fill=(246, 241, 226, 255))
        d.line([(px, 114), (px - 2, 106)], fill=(36, 36, 36, 255), width=2)
    # small flags on the table
    cols = [(176, 54, 40), (40, 92, 140), (238, 198, 58), (58, 138, 78)]
    for i, col in enumerate(cols):
        fx = 60 + i * 62
        d.polygon([(fx, 128), (fx + 20, 128), (fx + 10, 138)], fill=col + (255,))
    return img


def scene_riyadh(w, h):
    """Riyadh at night: skyline, one tall tower, three intercept flashes."""
    img = vgrad((w, h), (12, 20, 44), (48, 60, 96)).convert("RGBA")
    d = ImageDraw.Draw(img)
    rng = random.Random(102)
    for _ in range(70):
        x, y = rng.randrange(w), rng.randrange(0, 60)
        d.point((x, y), fill=(220, 228, 245, rng.randrange(80, 190)))
    # crescent moon
    d.ellipse([20, 8, 46, 34], fill=(232, 234, 220, 235))
    d.ellipse([28, 6, 50, 32], fill=(14, 22, 46, 255))
    # skyline: low blocks with lit windows
    x = 0
    while x < w:
        bw = rng.randrange(22, 46)
        bh = rng.randrange(24, 52)
        d.rectangle([x, 98 - bh, x + bw, 98], fill=(18, 26, 50, 255))
        for _ in range(bw // 6):
            wx = x + rng.randrange(3, max(4, bw - 4))
            wy = 98 - bh + rng.randrange(4, max(5, bh - 5))
            d.rectangle([wx, wy, wx + 2, wy + 3], fill=(240, 200, 90, 190))
        x += bw + 5
    # tall tower, centre, with a lit crown
    tx = w // 2 - 14
    d.polygon([(tx, 98), (tx + 4, 22), (tx + 24, 22), (tx + 28, 98)],
              fill=(28, 38, 64, 255))
    for wy in range(30, 92, 9):
        d.rectangle([tx + 6, wy, tx + 22, wy + 4], fill=(250, 210, 110, 220))
    d.ellipse([tx + 9, 12, tx + 19, 22], fill=(255, 90, 60, 255))
    # three intercept flashes with radiating spikes
    for bx, by in ((66, 26), (150, 40), (246, 24)):
        for r, a in ((16, 50), (10, 110), (5, 190)):
            d.ellipse([bx - r, by - r // 2, bx + r, by + r // 2],
                      fill=(255, 170, 60, a))
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            ex = bx + int(20 * math.cos(rad))
            ey = by + int(11 * math.sin(rad))
            d.line([(bx, by), (ex, ey)], fill=(255, 220, 140, 200), width=2)
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(255, 255, 255, 255))
    # rising trails
    d.arc([30, 66, 130, 150], 205, 335, fill=(200, 215, 235, 200), width=2)
    d.arc([170, 60, 270, 150], 205, 335, fill=(200, 215, 235, 200), width=2)
    # street glow
    d.rectangle([0, 98, w, h], fill=(16, 24, 46, 255))
    for sx in range(8, w, 24):
        d.ellipse([sx, 106, sx + 5, 111], fill=(250, 200, 90, 220))
    return img


def scene_kyiv(w, h):
    """Kyiv at night: apartment blocks, one burning, drones overhead."""
    img = vgrad((w, h), (16, 24, 50), (54, 52, 70)).convert("RGBA")
    d = ImageDraw.Draw(img)
    rng = random.Random(103)
    for _ in range(55):
        x, y = rng.randrange(w), rng.randrange(0, 52)
        d.point((x, y), fill=(210, 218, 240, rng.randrange(70, 170)))
    # apartment blocks
    blocks = [(0, 46, 58, 98), (62, 60, 52, 98), (118, 38, 64, 98),
              (186, 54, 56, 98), (246, 42, 76, 98)]
    for bx, by, bw, bb in blocks:
        d.rectangle([bx, by, bx + bw, bb], fill=(22, 28, 48, 255))
        for wy in range(by + 6, bb - 6, 12):
            for wx in range(bx + 5, bx + bw - 6, 11):
                if rng.random() < 0.5:
                    d.rectangle([wx, wy, wx + 4, wy + 6],
                                fill=(240, 200, 90, 200))
    # fire on the centre block: glow, flames, smoke
    fx = 150
    for r, a in ((20, 50), (13, 100), (8, 170)):
        d.ellipse([fx - r, 60 - r // 2, fx + r, 60 + r // 2],
                  fill=(255, 140, 40, a))
    for ox, fh, col in ((-11, 24, (255, 190, 60)), (0, 34, (255, 120, 30)),
                        (11, 22, (255, 200, 90))):
        d.polygon([(fx + ox - 6, 64), (fx + ox, 64 - fh), (fx + ox + 6, 64)],
                  fill=col + (255,))
    for sx, sy, sr in ((142, 42, 12), (156, 30, 15), (140, 20, 17), (164, 38, 10)):
        d.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2],
                  fill=(74, 74, 88, 120))
    # drones: small dark crosses with a red light
    for dx, dy in ((48, 20), (232, 28), (290, 16)):
        d.line([(dx - 7, dy), (dx + 7, dy)], fill=(10, 12, 20, 255), width=2)
        d.line([(dx, dy - 4), (dx, dy + 4)], fill=(10, 12, 20, 255), width=2)
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 70, 50, 255))
    # street with an orange reflection under the fire
    d.rectangle([0, 98, w, h], fill=(14, 18, 34, 255))
    for yy in range(102, h, 6):
        rw = 40 - (yy - 102) // 2
        d.line([(fx - rw // 2, yy), (fx + rw // 2, yy)],
               fill=(255, 150, 50, 80), width=2)
    return img


SCENES = {1: scene_cop, 2: scene_riyadh, 3: scene_kyiv}

HEROES = [
    dict(n=1, tag="TÜRKIYE · CLIMATE", head="COP31 OVERTIME IN ANTALYA",
         sub="Talks run past the Friday deadline; the draft drops all "
             "fossil-fuel language."),
    dict(n=2, tag="SAUDI ARABIA · DEFENCE", head="RIYADH INTERCEPTS 3 MISSILES",
         sub="Three Houthi missiles downed over Riyadh early Saturday, "
             "the third night of alerts."),
    dict(n=3, tag="UKRAINE · WAR", head="RUSSIA STRIKES UKRAINE AGAIN",
         sub="3 missiles, 148 drones; a boy, 7, and a paramedic killed "
             "in Kryvyi Rih; 58 hurt."),
]

NUMBERS = [
    ("3", "missiles over Riyadh"),
    ("148", "drones at Ukraine"),
    ("6.7", "Peru quake"),
    ("200", "nations at COP31"),
    ("-5.28%", "Nasdaq"),
    ("146", "safe in Davao"),
]

# n, tag, headline, lat, lon, display lat, display lon, map label, label side
GRID = [
    (4, "SPACE · MERCURY", "BepiColombo arrives at Mercury", 49.87, 8.65, 48.0, 10.0, "Darmstadt", "below"),
    (5, "IRAN · GULF", "Iran says it downed a US MQ-9", 26.5, 56.3, 28.5, 59.0, "Hormuz", "above"),
    (6, "PERU · QUAKE", "M6.7 quake shakes the Andes", -11.2, -75.9, None, None, "Junín", "below"),
    (7, "IRAQ · FIRE", "Basra power station fire", 30.5, 47.8, 34.0, 52.0, "Basra", "above"),
    (8, "MARKETS · USA", "Markets rout: Nasdaq -5.28%", 40.7, -74.0, None, None, "New York", "above"),
    (9, "ETHIOPIA · CLIMATE", "Addis Ababa to host COP32", 9.0, 38.7, None, None, "Addis Ababa", "below"),
    (10, "STRAIT OF HORMUZ · SWIM", "Pugh completes Hormuz swim", 26.6, 55.8, 22.0, 60.0, "Pugh swim", "below"),
    (11, "INDIA · CRICKET", "Rahul completes SENA set", -41.3, 174.8, None, None, "Wellington", "above"),
    (12, "GAZA · CONFLICT", "Israeli strikes kill Palestinians in Gaza", 31.5, 34.5, None, None, "Gaza", "left"),
    (13, "SOUTH KOREA · EDUCATION", "100m-won reward for reporting exam cheating", 37.5, 127.0, None, None, "Seoul", "below"),
    (14, "YEMEN · WAR", "Houthis say 41 killed in Yemen strikes", 15.3, 44.2, None, None, "Sanaa", "below"),
    (15, "SOUTH KOREA · SPORT", "Choi wins 1000m gold in Seoul", 37.5, 127.0, 42.0, 120.0, "Choi", "above"),
    (16, "SOUTH KOREA · SPORT", "Boer wins 500m; Shin first 1500m gold", 37.5, 127.0, 33.0, 134.0, "Short track", "below"),
    (17, "PHILIPPINES · AVIATION", "Air Niugini jet lands safely in Davao", 7.1, 125.6, None, None, "Davao", "below"),
]

HERO_DOTS = [
    (1, 36.9, 30.7, None, None, "Antalya", "above"),
    (2, 24.7, 46.7, None, None, "Riyadh", "below"),
    (3, 50.45, 30.52, None, None, "Kyiv", "above"),
]


def load_land():
    data = json.loads(GEO.read_text())
    rings = []
    for feat in data["features"]:
        geom = feat["geometry"]
        if geom["type"] == "Polygon":
            rings.append(geom["coordinates"])
        elif geom["type"] == "MultiPolygon":
            rings.extend(geom["coordinates"])
    return rings


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (83.0 - lat) / 141.0 * (y1 - y0)
    return x, y


def draw_map(d, box, img):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    tile = Image.new("RGBA", (bw, bh), SEA + (255,))
    td = ImageDraw.Draw(tile)
    local = (0, 0, bw, bh)
    for ring in load_land():
        for poly in ring:
            pts = []
            for lon, lat in poly:
                if lon < -180 or lon > 180:
                    continue
                pts.append(project(lon, max(lat, -58.0), local))
            if len(pts) > 2:
                td.polygon(pts, fill=LAND, outline=EDGE)
    for lon in range(-150, 181, 30):
        xa, _ = project(lon, 83, local)
        td.line([(xa, 0), (xa, bh)], fill=(255, 255, 255, 70), width=1)
    img.alpha_composite(tile, (x0, y0))
    dots = list(HERO_DOTS) + [
        (n, lat, lon, dlat, dlon, lbl, side)
        for (n, _t, _h, lat, lon, dlat, dlon, lbl, side) in GRID
    ]
    placed = {}
    for num, lat, lon, dlat, dlon, label, side in dots:
        tx, ty = project(lon, lat, box)
        cx, cy = project(dlon if dlon is not None else lon,
                         dlat if dlat is not None else lat, box)
        placed[num] = (cx, cy)
        if (cx, cy) != (tx, ty):
            d.line([(cx, cy), (tx, ty)], fill=(90, 90, 90, 220), width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=(90, 90, 90, 255))
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255, 255))
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
        tw = d.textlength(str(num), font=F_MNUM)
        d.text((cx - tw / 2, cy - 5), str(num), font=F_MNUM, fill=(255, 255, 255))
    for num, lat, lon, dlat, dlon, label, side in dots:
        if not label:
            continue
        cx, cy = placed[num]
        tw = d.textlength(label, font=F_MLBL)
        if side == "left":
            lx, ly = cx - tw - 11, cy - 6
        elif side == "below":
            lx, ly = cx - tw / 2, cy + 10
        elif side == "right":
            lx, ly = cx + 11, cy - 6
        else:
            lx, ly = cx - tw / 2, cy - 21
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            d.text((lx + ox, ly + oy), label, font=F_MLBL, fill=(255, 255, 255))
        d.text((lx, ly), label, font=F_MLBL, fill=INK)


def build():
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    speckle(img, 2400, 2126)

    # masthead
    kick = "THE DAY IN WORLD NEWS  ·  17 STORIES, 7 REGIONS"
    kw = d.textlength(kick, font=F_KICK)
    d.text(((W - kw) / 2, 10), kick, font=F_KICK, fill=GOLDD)
    title = "Saturday, 21 November 2026"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 30), title, font=F_TITLE, fill=INK)
    sub = "Every story on this page happened, or was first reported, on this day."
    sw = d.textlength(sub, font=F_SUB)
    d.text(((W - sw) / 2, 82), sub, font=F_SUB, fill=SOFT)
    d.line([(16, 104), (W - 16, 104)], fill=RULE, width=2)

    # numbers strip
    d.rounded_rectangle([16, 110, W - 16, 148], radius=8, fill=PAPER,
                        outline=RULE, width=1)
    cw = (W - 32) / 6
    for i, (num, lbl) in enumerate(NUMBERS):
        cx = 16 + cw * i + cw / 2
        nw = d.textlength(num, font=F_BIG)
        d.text((cx - nw / 2, 112), num, font=F_BIG, fill=GOLDD)
        lw = d.textlength(lbl, font=F_LBL)
        d.text((cx - lw / 2, 137), lbl, font=F_LBL, fill=SOFT)
        if i:
            x = 16 + cw * i
            d.line([(x, 118), (x, 142)], fill=RULE, width=1)

    # heroes
    colw, x0, iy, ih = 322, 16, 154, 140
    cy, chh = 294, 88
    for idx, hero in enumerate(HEROES):
        x = x0 + idx * (colw + 13)
        scene = SCENES[hero["n"]](colw, ih)
        img.alpha_composite(scene, (x, iy))
        d.rectangle([x, iy, x + colw, iy + ih], outline=RULE, width=1)
        d.rounded_rectangle([x, cy, x + colw, cy + chh], radius=8,
                            fill=PAPER, outline=RULE, width=1)
        bx, by = x + 12, cy - 13
        d.ellipse([bx, by, bx + 26, by + 26], fill=GOLD)
        d.ellipse([bx, by, bx + 26, by + 26], outline=(255, 255, 255), width=2)
        nw = d.textlength(str(hero["n"]), font=F_MNUM)
        d.text((bx + 13 - nw / 2, by + 7), str(hero["n"]), font=F_MNUM,
               fill=(255, 255, 255))
        d.text((x + 46, cy + 7), f"{hero['n']}  ·  {hero['tag']}",
               font=F_HKICK, fill=GOLDD)
        hlines = wrap(d, hero["head"], F_HHEAD, colw - 24)[:2]
        y = draw_lines(d, x + 12, cy + 25, hlines, F_HHEAD, INK, 22)
        blines = wrap(d, hero["sub"], F_HBODY, colw - 24)
        keep = 2 if len(hlines) == 1 else 1
        draw_lines(d, x + 12, y + 1, blines[:keep], F_HBODY, SOFT, 14)

    # grid: 14 stories, 4 columns, last row centred
    cols = 4
    gw = (W - 32 - (cols - 1) * 8) // cols
    gh, gap = 48, 4
    gy = 388
    rows = (len(GRID) + cols - 1) // cols
    for i, (num, tag, head, _lat, _lon, _dl, _do, _lb, _sd) in enumerate(GRID):
        r, c = divmod(i, cols)
        in_row = min(cols, len(GRID) - r * cols)
        xoff = (cols - in_row) * (gw + gap) // 2
        x = 16 + xoff + c * (gw + gap)
        y = gy + r * (gh + gap)
        d.rounded_rectangle([x, y, x + gw, y + gh], radius=7, fill=PAPER,
                            outline=RULE, width=1)
        d.ellipse([x + 7, y + 5, x + 21, y + 19], fill=GOLD)
        nw = d.textlength(str(num), font=F_MNUM)
        d.text((x + 14 - nw / 2, y + 10), str(num), font=F_MNUM,
               fill=(255, 255, 255))
        kick = f"{num}  ·  {tag}"
        while d.textlength(kick, font=F_GKICK) > gw - 30 and " " in kick:
            kick = kick.rsplit(" ", 1)[0] + "…"
        d.text((x + 26, y + 7), kick, font=F_GKICK, fill=GOLDD)
        hlines = wrap(d, head, F_GHEAD, gw - 16)[:2]
        draw_lines(d, x + 8, y + 21, hlines, F_GHEAD, INK, 13)

    # map card — taller than v1, since the grid is shorter
    my = gy + rows * (gh + gap) + 14
    d.rounded_rectangle([16, my, W - 16, 980], radius=8, fill=PAPER,
                        outline=RULE, width=1)
    d.text((26, my + 8), "WHERE IT HAPPENED", font=F_MTITLE, fill=GOLDD)
    note = "One numbered dot per story — find it in the list above."
    nw = d.textlength(note, font=F_LBL)
    d.text((W - 26 - nw, my + 10), note, font=F_LBL, fill=SOFT)
    draw_map(d, (26, my + 30, W - 26, 972), img)

    # footer
    foot_l = "All 17 stories happened, or were first reported, on Saturday, 21 November 2026."
    foot_r = "Claims are worded as claims; no toll is printed where reports differ."
    d.text((16, 988), foot_l, font=F_FOOT, fill=SOFT)
    rw = d.textlength(foot_r, font=F_FOOT)
    d.text((W - 16 - rw, 988), foot_r, font=F_FOOT, fill=SOFT)

    rgb = img.convert("RGB")
    rgb.save(OUT, "PNG")
    rgb.save(WORK / "entry.png", "PNG")
    print(f"saved {OUT} {OUT.stat().st_size} bytes {rgb.size}")


if __name__ == "__main__":
    build()
