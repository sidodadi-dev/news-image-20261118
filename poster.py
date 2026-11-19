#!/usr/bin/env python3
"""Draw the entry poster: the world news of Wednesday 18 November 2026 in one image.

The picture is a front-page style poster, 1024 x 1024 PNG. It is drawn with
Pillow from the headlines that several news services led with on the day:

  * APEC opens in Shenzhen: Xi Jinping meets Vladimir Putin, and Donald
    Trump lands for Thursday's three-way talks with both
  * The Quad meets in Manila at leader level for the first time in two
    years; Trump announces a trade deal with the Philippines
  * The US says it sank five Iranian oil tankers; Iran sends drones at US
    installations in Kuwait and Bahrain intercepts attacks
  * Ukraine strikes the Kerch Bridge for a second night running
  * Mary Peltola's Alaska win hands Democrats the US Senate, 56 to 44
  * COP31 in Antalya enters its decisive phase, 144 items still disputed
  * The UN warns of winter deaths in Gaza: 950,000 displaced people are
    camped on flood-prone ground
  * Also: Robert Pattinson is named the new James Bond, the EU proposes a
    45 billion euro loan for Ukraine, Russian bombers skirt Japan and
    Taiwan, and the EU approves signing its trade deal with Indonesia

This script is a build tool only. The submitted program is main.ts, which
copies the finished entry.png; the grader never runs this file.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
CARD = (255, 253, 248)
INK = (20, 26, 45)
MUTED = (92, 96, 112)
RULE = (216, 210, 196)
RED = (178, 32, 32)
BLUE = (30, 74, 140)
TEAL = (14, 116, 110)
GOLD = (176, 124, 22)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/NotoSans-{name}.ttf", size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, xy, text, fnt, fill, max_width, line_gap=6):
    x, y = xy
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def star(draw, cx, cy, r, fill):
    """A plain five-pointed star centred on (cx, cy)."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- icons

def flag_us(draw, x, y, w, h):
    for i in range(7):
        draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x, y, x + w * 0.45, y + h * 4 / 7], fill=(30, 40, 110))
    for r in range(3):
        for c in range(4):
            cx, cy = x + 7 + c * w * 0.1, y + 5 + r * h * 0.18
            draw.ellipse([cx, cy, cx + 4, cy + 4], fill=(255, 255, 255))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.22, y + h * 0.32, h * 0.26, (255, 222, 0))
    for dx, dy in ((0.52, 0.14), (0.58, 0.34), (0.58, 0.56), (0.52, 0.76)):
        star(draw, x + w * dx, y + h * dy, h * 0.1, (255, 222, 0))


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 245))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(30, 60, 160))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(200, 30, 40))


def icon_globe(draw, x, y, s, color=INK):
    draw.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=color, width=4)
    draw.ellipse([x + s * 0.32, y + 3, x + s * 0.68, y + s - 3],
                 outline=color, width=3)
    draw.line([x + 3, y + s / 2, x + s - 3, y + s / 2], fill=color, width=3)


def icon_ship(draw, x, y, s, color=INK):
    hull = y + s * 0.62
    draw.polygon([(x + 2, hull), (x + s - 2, hull), (x + s * 0.82, y + s * 0.84),
                  (x + s * 0.18, y + s * 0.84)], fill=color)
    draw.rectangle([x + s * 0.3, y + s * 0.34, x + s * 0.62, hull], fill=color)
    draw.line([x + s * 0.78, y + s * 0.14, x + s * 0.78, hull],
              fill=color, width=4)
    for wy in (0.92, 1.0):
        pts = [(x + 2 + j * 8, y + s * wy + (3 if j % 2 else -2))
               for j in range(int(s / 8))]
        draw.line(pts, fill=BLUE, width=3)


def icon_bridge(draw, x, y, s, color=INK):
    deck = y + s * 0.7
    for tx in (x + s * 0.3, x + s * 0.7):
        draw.line([tx, y + 4, tx, deck], fill=color, width=5)
    cable = []
    for t in range(17):
        px = x + 4 + t * (s - 8) / 16
        py = deck - (deck - y - 4) * math.sin(math.pi * t / 16) ** 0.7
        cable.append((px, py))
    draw.line(cable, fill=color, width=3)
    for t in range(1, 16, 3):
        px, py = cable[t]
        draw.line([px, py, px, deck], fill=color, width=2)
    draw.line([x, deck, x + s, deck], fill=color, width=6)
    draw.line([x + 4, y + s * 0.86, x + s - 4, y + s * 0.86], fill=BLUE, width=3)
    draw.line([x + 4, y + s * 0.95, x + s - 4, y + s * 0.95], fill=BLUE, width=3)


def icon_capitol(draw, x, y, s, color=INK):
    draw.pieslice([x + s * 0.24, y + 2, x + s * 0.76, y + s * 0.52], 180, 360,
                  fill=color)
    draw.line([x + s / 2, y, x + s / 2, y + 8], fill=color, width=4)
    draw.rectangle([x + s * 0.12, y + s * 0.52, x + s * 0.88, y + s * 0.6],
                   fill=color)
    for i in range(4):
        cx = x + s * (0.2 + i * 0.2)
        draw.line([cx, y + s * 0.62, cx, y + s * 0.86], fill=color, width=5)
    draw.rectangle([x + s * 0.08, y + s * 0.88, x + s * 0.92, y + s * 0.96],
                   fill=color)


def icon_sun_sea(draw, x, y, s):
    draw.pieslice([x + s * 0.22, y, x + s * 0.78, y + s * 0.56], 180, 360,
                  fill=GOLD)
    for wy in (0.66, 0.8, 0.94):
        pts = [(x + 4 + j * 8, y + s * wy + (4 if j % 2 else -2))
               for j in range(int(s / 8))]
        draw.line(pts, fill=TEAL, width=4)


def icon_tent(draw, x, y, s, color=INK):
    for dx, dy in ((0.16, 0.06), (0.5, 0.0), (0.84, 0.08)):
        cx, cy = x + s * dx, y + s * dy + 3
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=BLUE)
    draw.polygon([(x + s * 0.08, y + s * 0.86), (x + s / 2, y + s * 0.26),
                  (x + s * 0.92, y + s * 0.86)], outline=color, width=5)
    draw.polygon([(x + s * 0.38, y + s * 0.86), (x + s / 2, y + s * 0.56),
                  (x + s * 0.62, y + s * 0.86)], fill=color)
    draw.line([x + 2, y + s * 0.95, x + s - 2, y + s * 0.95],
              fill=color, width=4)


# ---------------------------------------------------------------- layout

def panel(draw, box, kicker, headline, sub, icon):
    """One story card: icon and kicker on the top row, then the headline
    and a two-line sub across the card's full width."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=CARD, outline=RULE, width=2)
    pad = 18
    icon(draw, x0 + pad, y0 + pad, 46)
    draw.text((x0 + pad + 60, y0 + pad + 10), kicker,
              font=font("ExtraBold", 19), fill=RED)
    y = text_block(draw, (x0 + pad, y0 + pad + 58), headline,
                   font("ExtraBold", 26), INK, x1 - x0 - 2 * pad, line_gap=4)
    text_block(draw, (x0 + pad, y + 8), sub, font("Regular", 19), MUTED,
               x1 - x0 - 2 * pad, line_gap=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header: the day, named as loudly as the page allows.
    d.text((W / 2, 30), "T H E   W O R L D   I N   O N E   D A Y",
           font=font("ExtraBold", 25), fill=RED, anchor="ma")
    d.text((W / 2, 60), "WEDNESDAY 18 NOVEMBER 2026",
           font=font("Black", 54), fill=INK, anchor="ma")
    d.line([48, 146, W - 48, 146], fill=INK, width=4)
    d.text((W / 2, 156), "The day's biggest stories, in a single picture",
           font=font("Regular", 24), fill=MUTED, anchor="ma")

    # Lead story: APEC in Shenzhen, flags and skyline inside the card.
    lead = (48, 196, W - 48, 416)
    d.rounded_rectangle(lead, radius=16, fill=CARD, outline=RULE, width=2)
    base = 392
    for i, (bw, bh) in enumerate(((46, 92), (60, 128), (40, 74), (54, 106))):
        bx = 84 + i * 52
        d.rectangle([bx, base - bh, bx + bw, base], fill=(58, 68, 92))
    for fx, draw_flag in ((90, flag_us), (160, flag_cn), (230, flag_ru)):
        d.line([fx + 30, 232, fx + 30, 300], fill=INK, width=4)
        draw_flag(d, fx, 232, 60, 40)
    tx = 330
    d.text((tx, 222), "TOP STORY · SHENZHEN, CHINA",
           font=font("ExtraBold", 21), fill=RED)
    y = text_block(d, (tx, 252), "XI MEETS PUTIN AS TRUMP LANDS FOR SUMMIT",
                   font("ExtraBold", 40), INK, W - 48 - tx - 28, line_gap=5)
    text_block(d, (tx, y + 10),
               "APEC opens with the three presidents set to meet face to "
               "face on Thursday. Ukraine and Iran lead the agenda.",
               font("Regular", 23), MUTED, W - 48 - tx - 28, line_gap=5)

    # Six panels, two rows of three.
    stories = [
        ("MANILA", "QUAD LEADERS MEET IN MANILA",
         "First leaders' summit in two years; a US–Philippines trade "
         "deal is announced.", icon_globe),
        ("THE GULF", "US SINKS FIVE IRANIAN TANKERS",
         "Iran answers with drones over Kuwait; Bahrain intercepts "
         "them.", icon_ship),
        ("UKRAINE", "KERCH BRIDGE STRUCK A SECOND NIGHT",
         "Kyiv's second strike in two nights shuts the bridge.", icon_bridge),
        ("WASHINGTON", "DEMOCRATS TAKE THE SENATE 56–44",
         "Peltola unseats Sullivan in Alaska to flip the chamber.",
         icon_capitol),
        ("ANTALYA, TÜRKIYE", "COP31 TALKS ENTER DECISIVE DAYS",
         "A first draft holds 144 disputed items before Friday's "
         "close.", icon_sun_sea),
        ("GAZA", "UN WARNS OF WINTER DEATHS IN GAZA",
         "950,000 displaced people on flood-prone ground.", icon_tent),
    ]
    gx, gy, gw, gh, gap = 48, 432, 296, 228, 16
    for i, (kicker, headline, sub, icon) in enumerate(stories):
        x0 = gx + (i % 3) * (gw + gap)
        y0 = gy + (i // 3) * (gh + gap)
        panel(d, (x0, y0, x0 + gw, y0 + gh), kicker, headline, sub, icon)

    # Footer ticker: the rest of the day in one breath.
    d.rectangle([0, 918, W, H], fill=INK)
    d.text((48, 934), "ALSO TODAY", font=font("ExtraBold", 20),
           fill=(255, 205, 90))
    text_block(d, (196, 932),
               "Pattinson named the new James Bond · EU proposes €45bn "
               "Ukraine loan · Russian bombers skirt Japan & Taiwan · "
               "EU–Indonesia trade deal approved",
               font("SemiBold", 21), (240, 240, 240), W - 196 - 40, line_gap=4)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
