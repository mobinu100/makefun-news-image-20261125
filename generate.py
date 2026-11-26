"""Draw entry.png: a one-page newspaper summing up 25 Nov 2026 world news.
Deterministic: PIL only, no network, no randomness, no timestamps.
Run: python3 generate.py  -> writes entry.png (1024x1024, <=1 MiB)."""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (179, 39, 30)
NAVY = (20, 52, 92)
TEAL = (15, 90, 90)
GOLD = (196, 138, 0)
GREY = (90, 84, 74)
SKY = (220, 232, 240)
SEA = (20, 52, 92)

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, fill, leading=1.12):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.2)


def rocket(d, x, y, s):
    # chunky rocket on navy
    d.rectangle([x, y, x + s, y + s], fill=NAVY)
    d.polygon([(x + s * 0.50, y + s * 0.12), (x + s * 0.68, y + s * 0.42),
               (x + s * 0.62, y + s * 0.72), (x + s * 0.38, y + s * 0.72),
               (x + s * 0.32, y + s * 0.42)], fill=(240, 240, 235))
    d.polygon([(x + s * 0.50, y + s * 0.12), (x + s * 0.68, y + s * 0.42),
               (x + s * 0.32, y + s * 0.42)], fill=RED)
    d.ellipse([x + s * 0.43, y + s * 0.38, x + s * 0.57, y + s * 0.52], fill=SKY)
    d.polygon([(x + s * 0.50, y + s * 0.72), (x + s * 0.62, y + s * 0.90),
               (x + s * 0.38, y + s * 0.90)], fill=(240, 140, 20))
    for sx, sy in [(0.15, 0.18), (0.85, 0.25), (0.80, 0.80), (0.18, 0.75)]:
        d.ellipse([x + s * sx - 3, y + s * sy - 3, x + s * sx + 3, y + s * sy + 3],
                  fill=(255, 255, 255))


def gavel(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(232, 214, 170))
    d.polygon([(x + s * 0.20, y + s * 0.62), (x + s * 0.68, y + s * 0.14),
               (x + s * 0.78, y + s * 0.24), (x + s * 0.30, y + s * 0.72)], fill=(120, 72, 20))
    d.rectangle([x + s * 0.55, y + s * 0.08, x + s * 0.90, y + s * 0.30], fill=(90, 52, 14))
    d.rectangle([x + s * 0.15, y + s * 0.70, x + s * 0.85, y + s * 0.80], fill=(150, 100, 40))


def chip(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(18, 90, 60))
    for i in range(4):
        px = x + s * (0.18 + i * 0.22)
        d.rectangle([px, y + s * 0.06, px + 8, y + s * 0.20], fill=GOLD)
        d.rectangle([px, y + s * 0.80, px + 8, y + s * 0.94], fill=GOLD)
    d.rectangle([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78], fill=(20, 20, 20))
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62], fill=GOLD)


def tariff(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(210, 228, 228))
    d.rectangle([x + s * 0.14, y + s * 0.55, x + s * 0.50, y + s * 0.80], fill=RED)
    d.rectangle([x + s * 0.54, y + s * 0.55, x + s * 0.86, y + s * 0.80], fill=NAVY)
    d.rectangle([x + s * 0.30, y + s * 0.28, x + s * 0.70, y + s * 0.52], fill=GOLD)
    d.text((x + s * 0.30, y + s * 0.02), "%", font=font(SANS_B, int(s * 0.30)), fill=INK)


def tower(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(222, 222, 216))
    d.rectangle([x + s * 0.38, y + s * 0.30, x + s * 0.62, y + s * 0.92], fill=NAVY)
    d.rectangle([x + s * 0.47, y + s * 0.10, x + s * 0.53, y + s * 0.30], fill=NAVY)
    for i in range(4):
        yy = y + s * (0.38 + i * 0.14)
        d.rectangle([x + s * 0.38, yy, x + s * 0.62, yy + 5], fill=(255, 255, 255))
    d.polygon([(x + s * 0.78, y + s * 0.12), (x + s * 0.88, y + s * 0.28),
               (x + s * 0.68, y + s * 0.28)], fill=RED)


def tanker(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(250, 220, 180))
    d.rectangle([x + s * 0.12, y + s * 0.30, x + s * 0.58, y + s * 0.62], fill=(200, 200, 195))
    d.rectangle([x + s * 0.58, y + s * 0.42, x + s * 0.82, y + s * 0.62], fill=RED)
    d.ellipse([x + s * 0.20, y + s * 0.62, x + s * 0.36, y + s * 0.78], fill=INK)
    d.ellipse([x + s * 0.62, y + s * 0.62, x + s * 0.78, y + s * 0.78], fill=INK)
    d.polygon([(x + s * 0.30, y + s * 0.30), (x + s * 0.40, y + s * 0.10),
               (x + s * 0.50, y + s * 0.30)], fill=(240, 140, 20))


def hero_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w * 0.78, y + h * 0.08, x + w * 0.94, y + h * 0.24], fill=GOLD)
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=SEA)
    # tanker ship
    d.polygon([(x + w * 0.08, y + h * 0.55), (x + w * 0.85, y + h * 0.55),
               (x + w * 0.78, y + h * 0.78), (x + w * 0.15, y + h * 0.78)], fill=(30, 30, 30))
    d.rectangle([x + w * 0.18, y + h * 0.38, x + w * 0.34, y + h * 0.55], fill=RED)
    d.rectangle([x + w * 0.38, y + h * 0.38, x + w * 0.54, y + h * 0.55], fill=(240, 240, 235))
    d.rectangle([x + w * 0.58, y + h * 0.38, x + w * 0.74, y + h * 0.55], fill=GOLD)
    # spiked mines
    for mx, my, r in [(0.88, 0.68, 16), (0.10, 0.88, 13)]:
        cx, cy = x + w * mx, y + h * my
        for k in range(8):
            a = k * math.pi / 4
            d.line([(cx + r * 0.8 * math.cos(a), cy + r * 0.8 * math.sin(a)),
                    (cx + r * 1.5 * math.cos(a), cy + r * 1.5 * math.sin(a))],
                   fill=INK, width=4)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
        d.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4], outline=RED, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=8)

    # ---- masthead (y 8..158) ----
    centered(d, W // 2, 18, "THE WORLD IN ONE DAY", font(SERIF_B, 62), INK)
    d.line([(24, 100), (W - 24, 100)], fill=INK, width=3)
    centered(d, W // 2, 108, "Wednesday 25 November 2026", font(SANS_B, 40), RED)
    d.line([(24, 158), (W - 24, 158)], fill=INK, width=3)

    # ---- hero: Strait of Hormuz (y 170..390) ----
    hy, hh = 170, 220
    hero_ship(d, 24, hy, 330, hh)
    tx = 378
    d.text((tx, hy + 4), "REUTERS: STRAIT OF HORMUZ", font=font(SANS_B, 26), fill=RED)
    text_block(d, tx, hy + 40, "MINES HIT TANKERS IN THE STRAIT", font(SANS_B, 50), 620, INK, 1.05)
    text_block(d, tx, hy + 156, "Iran says tankers struck; US military disputes the claim",
               font(SANS, 26), 620, GREY, 1.1)

    # ---- grid: six stories (y 402..818) ----
    stories = [
        ("REUTERS: SHENZHOU-24", "PAKISTAN'S FIRST ASTRONAUT REACHES ORBIT", rocket, NAVY),
        ("REUTERS: NEW YORK", "HUAWEI CONVICTED IN US TRIAL", gavel, RED),
        ("REUTERS: NVIDIA", "HUANG BACK AS NVIDIA CHIEF", chip, TEAL),
        ("REUTERS: TRADE", "US PROPOSES NEW TARIFFS", tariff, NAVY),
        ("REUTERS: SAUDI ARABIA", "RIYADH TOWER HIT, 11 WOUNDED", tower, RED),
        ("CAIRO: TANKER CRASH", "TANKER CRASH KILLS AT LEAST 30", tanker, TEAL),
    ]
    gy, gh, gap = 402, 132, 10
    cw = (W - 48 - gap) // 2
    for i, (kick, head, pic, col) in enumerate(stories):
        cx = 24 + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (gh + gap)
        d.rectangle([cx, cy, cx + cw, cy + gh], outline=INK, width=2)
        pic(d, cx + 8, cy + 8, 116)
        d.text((cx + 136, cy + 10), kick, font=font(SANS_B, 19), fill=col)
        text_block(d, cx + 136, cy + 38, head, font(SANS_B, 28), cw - 148, INK, 1.08)

    # ---- bottom strip (y 832..1016) ----
    by = 832
    d.line([(24, by), (W - 24, by)], fill=INK, width=3)
    d.text((24, by + 10), "ALSO ON 25 NOVEMBER", font=font(SANS_B, 24), fill=RED)
    items = [
        "Nations urge Russia to halt chemical agents in Ukraine",
        "Spain heads to a snap election on Sunday",
        "Bangladesh lifts garment wage to $139 a month",
    ]
    yy = by + 46
    for it in items:
        d.ellipse([28, yy + 9, 40, yy + 21], fill=RED)
        d.text((52, yy), it, font=font(SANS_B, 28), fill=INK)
        yy += 38
    centered(d, W // 2, yy + 2, "Sources: Reuters  -  AP  -  BBC", font(SANS, 21), GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
