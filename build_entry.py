"""Draws the zech entry image for news-image-20261122.

A modern magazine cover: dark navy background, coloured news panels,
big bold type. Drawn with PIL and system DejaVu fonts only; no network,
no downloads, fully deterministic (same bytes every run).
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

NAVY = (11, 27, 51)
PANEL = (18, 41, 74)
PANEL_EDGE = (52, 96, 150)
WHITE = (255, 255, 255)
LIGHT = (205, 219, 235)
GOLD = (255, 196, 66)
RED = (201, 32, 48)
CRIMSON = (139, 22, 40)
CRIMSON_EDGE = (214, 74, 92)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 66)
F_DATE = font("DejaVuSans-Bold.ttf", 34)
F_TAG = font("DejaVuSans-Bold.ttf", 22)
F_LEAD = font("DejaVuSans-Bold.ttf", 62)
F_LEAD_SUB = font("DejaVuSans.ttf", 27)
F_HEAD = font("DejaVuSans-Bold.ttf", 29)
F_BODY = font("DejaVuSans.ttf", 21)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_panel(draw, x, y, w, h, tag, tag_color, headline, body):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=PANEL, outline=PANEL_EDGE, width=2)
    # coloured tag strip
    draw.rounded_rectangle([x, y, x + w, y + 40], radius=10, fill=tag_color)
    draw.rectangle([x, y + 30, x + w, y + 40], fill=tag_color)
    draw.text((x + 14, y + 8), tag, font=F_TAG, fill=WHITE)
    inner_w = w - 28
    lines = wrap(draw, headline, F_HEAD, inner_w)
    ty = y + 52
    for line in lines:
        draw.text((x + 14, ty), line, font=F_HEAD, fill=WHITE)
        ty += 34
    ty += 4
    for line in wrap(draw, body, F_BODY, inner_w):
        if ty + 26 > y + h - 6:
            break
        draw.text((x + 14, ty), line, font=F_BODY, fill=LIGHT)
        ty += 26


def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # ---- masthead ----
    draw.rectangle([MARGIN, MARGIN, MARGIN + 10, 132], fill=RED)
    draw.text((MARGIN + 22, 30), "THE WORLD TODAY", font=F_TITLE, fill=WHITE)
    draw.text((MARGIN + 22, 100), "SUNDAY, 22 NOVEMBER 2026",
              font=F_DATE, fill=GOLD)
    draw.line([MARGIN, 142, W - MARGIN, 142], fill=GOLD, width=3)

    # ---- lead story ----
    lx, ly, lw, lh = MARGIN, 158, W - 2 * MARGIN, 312
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=12,
                           fill=CRIMSON, outline=CRIMSON_EDGE, width=3)
    draw.text((lx + 24, ly + 20), "LEAD STORY  •  MEXICO",
              font=F_TAG, fill=GOLD)
    lead_lines = ["MEXICO CAPTURES", "\u2018EL CHAPO ISIDRO\u2019"]
    ty = ly + 56
    for line in lead_lines:
        draw.text((lx + 24, ty), line, font=F_LEAD, fill=WHITE)
        ty += 70
    draw.text((lx + 24, ly + 210),
              "Drug lord seized in a major security operation \u2014",
              font=F_LEAD_SUB, fill=LIGHT)
    draw.text((lx + 24, ly + 244),
              "the day\u2019s biggest story.",
              font=F_LEAD_SUB, fill=LIGHT)

    # ---- five more stories ----
    grid_top = 486
    row1_h, row2_h = 258, 236
    gap = 16
    col_w = (W - 2 * MARGIN - 2 * gap) // 3
    stories_row1 = [
        ("TENNIS", (30, 122, 70),
         "ALCARAZ v ZVEREV FOR THE ATP CROWN",
         "Final showdown decides the season-ending title."),
        ("GAZA", (14, 124, 123),
         "ALLIES PRESS ISRAEL TO OPEN GAZA AID",
         "Australia, Canada, Italy and the UK urge access as floods hit Gaza."),
        ("FRANCE", (43, 95, 158),
         "FOURTH WEEKEND OF COST-OF-LIVING PROTESTS",
         "Streets fill again over rising prices."),
    ]
    for i, (tag, color, head, body) in enumerate(stories_row1):
        x = MARGIN + i * (col_w + gap)
        draw_panel(draw, x, grid_top, col_w, row1_h, tag, color, head, body)

    row2_y = grid_top + row1_h + gap
    wide_w = (W - 2 * MARGIN - gap) // 2
    stories_row2 = [
        ("ISRAEL", (107, 63, 160),
         "HERZOG TAPS EISENKOT TO FORM GOVERNMENT",
         "President bypasses Netanyahu in a bid to build a coalition."),
        ("RUGBY", (194, 94, 30),
         "FRANCE REACH NATIONS CHAMPIONSHIP FINAL",
         "Les Bleus to face South Africa for the title."),
    ]
    for i, (tag, color, head, body) in enumerate(stories_row2):
        x = MARGIN + i * (wide_w + gap)
        draw_panel(draw, x, row2_y, wide_w, row2_h, tag, color, head, body)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
