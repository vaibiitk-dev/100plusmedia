"""Build the I.D.O.D. carousel ad (6 slides, 1080x1350, 4:5 for Meta/Instagram).

Follows brand-assets/BRAND_GUIDELINES.md: brand colors, League Spartan +
Poppins, the official logo composited (never drawn), and only facts from
https://100plusacademy.com/IDOD-PLUS/. Uses real event photos from photos/
(kept out of git: identifiable students). Run: python build.py
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "image-gen"))
import brand  # noqa: E402

C = brand.BRAND["colors"]
RED, TEAL, NAVY, NAVY_D = C["logo_red"], C["logo_teal"], C["navy"], C["navy_dark"]
ORANGE, WHITE, TINT = C["accent_orange"], "#FFFFFF", C["light_red_tint"]
W, H = 1080, 1350
PAD = 72
FONTS = ROOT / "brand-assets" / "fonts"
PHOTOS = HERE / "photos"
OUT = HERE / "slides"
PHONE = brand.BRAND["contact"]["phones"][0]
URL = "100plusacademy.com/IDOD-PLUS"


def spartan(size, weight="ExtraBold"):
    f = ImageFont.truetype(str(FONTS / "LeagueSpartan-Variable.ttf"), size)
    f.set_variation_by_name(weight)
    return f


def poppins(size, weight="Regular"):
    return ImageFont.truetype(str(FONTS / f"Poppins-{weight}.ttf"), size)


def wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=font) <= width:
            line = test
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def text_block(draw, xy, text, font, fill, width, spacing=1.12):
    """Draw wrapped text; returns the y below the block."""
    x, y = xy
    asc, desc = font.getmetrics()
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += int((asc + desc) * spacing)
    return y


def pill(draw, xy, text, font, bg, fg, padx=26, pady=12):
    x, y = xy
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    w, h = r - l + 2 * padx, b - t + 2 * pady
    draw.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=bg)
    draw.text((x + padx - l, y + pady - t), text, font=font, fill=fg)
    return x + w, y + h


def cover(img, size, focus=(0.5, 0.5)):
    return ImageOps.fit(img, size, Image.LANCZOS, centering=focus)


def photo(name):
    return Image.open(PHOTOS / name).convert("RGB")


def gradient(size, top_alpha, bottom_alpha, color=(11, 33, 73)):
    w, h = size
    g = Image.new("L", (1, h))
    for yy in range(h):
        g.putpixel((0, yy), int(top_alpha + (bottom_alpha - top_alpha) * yy / (h - 1)))
    layer = Image.new("RGBA", size, color + (0,))
    layer.putalpha(g.resize(size))
    return layer


def footer(draw, page, total=6, dark=False):
    fg = WHITE if dark else NAVY
    f = poppins(24, "SemiBold")
    draw.text((PAD, H - 62), f"{URL}  ·  {PHONE}", font=f, fill=fg)
    draw.text((W - PAD - 60, H - 62), f"{page}/{total}", font=f, fill=fg)


def swipe(draw, y, dark=True):
    f = poppins(26, "SemiBold")
    fill = WHITE if dark else RED
    x = W - PAD - 34
    draw.polygon([(x, y + 6), (x + 30, y + 21), (x, y + 36)], fill=fill)
    t = "Swipe"
    draw.text((x - 14 - draw.textlength(t, font=f), y), t, font=f, fill=fill)


def photo_top(canvas, img, h, focus):
    canvas.paste(cover(img, (W, h), focus), (0, 0))
    ImageDraw.Draw(canvas).rectangle((0, h, W, h + 10), fill=RED)


# ---- slides -------------------------------------------------------------

def slide1():
    c = Image.new("RGB", (W, H))
    c.paste(cover(photo("05-teacher-class-wide.jpg"), (W, H), (0.45, 0.5)))
    c = c.convert("RGBA")
    c.alpha_composite(gradient((W, 760), 0, 235), (0, H - 760))
    d = ImageDraw.Draw(c)
    y = H - 640
    pill(d, (PAD, y), "FREE WORKSHOP  ·  CLASSES 6–12", poppins(28, "Bold"), RED, WHITE)
    y += 92
    d.text((PAD, y), "Beyond", font=spartan(128), fill=WHITE)
    d.text((PAD, y + 118), "marks.", font=spartan(128), fill=TEAL)
    y += 268
    y = text_block(d, (PAD, y), "Inner Development for Overall Development (I.D.O.D.) "
                   "helps your child grow calm, composed and confident.",
                   poppins(34), WHITE, W - 2 * PAD, 1.25)
    swipe(d, H - 100)
    return c


def slide2():
    c = Image.new("RGBA", (W, H), WHITE)
    photo_top(c, photo("03-students-a.jpg"), 600, (0.5, 0.45))
    d = ImageDraw.Draw(c)
    y = 660
    d.text((PAD, y), "THE STRUGGLES ARE REAL", font=poppins(26, "Bold"), fill=RED)
    y = text_block(d, (PAD, y + 48), "Today's students carry more than a syllabus.",
                   spartan(72), NAVY_D, W - 2 * PAD, 1.0) + 26
    items = [("Exam anxiety", RED), ("Digital overwhelm", NAVY),
             ("Social comparison", NAVY), ("Career pressure", RED)]
    f = poppins(32, "SemiBold")
    cw, ch = (W - 2 * PAD - 24) // 2, 104
    for i, (label, col) in enumerate(items):
        x = PAD + (i % 2) * (cw + 24)
        yy = y + (i // 2) * (ch + 22)
        d.rounded_rectangle((x, yy, x + cw, yy + ch), 22, fill=TINT if col == RED else "#E8EEF6")
        d.rectangle((x, yy + 22, x + 8, yy + ch - 22), fill=col)
        d.text((x + 36, yy + ch // 2), label, font=f, fill=NAVY_D, anchor="lm")
    footer(d, 2)
    return c


def slide3():
    img = photo("02-presenter-screen.jpg")
    # Soften the slide's sensitive bullet text; keep its title readable.
    w, h = img.size
    box = (int(w * 0.38), int(h * 0.37), int(w * 0.80), int(h * 0.55))
    img.paste(img.crop(box).filter(ImageFilter.GaussianBlur(w // 120)), box)
    c = Image.new("RGBA", (W, H), WHITE)
    photo_top(c, img, 700, (0.42, 0.4))
    d = ImageDraw.Draw(c)
    pill(d, (PAD, 40), "SESSION 1 · COMPLETED", poppins(26, "Bold"), TEAL, WHITE)
    y = 760
    d.text((PAD, y), "OUR FIRST SESSION", font=poppins(26, "Bold"), fill=RED)
    y = text_block(d, (PAD, y + 48), "Teens & social media: the real talk.",
                   spartan(72), NAVY_D, W - 2 * PAD, 1.0) + 18
    text_block(d, (PAD, y), "Students explored research on online pressure, "
               "comparison and safety, then talked it through openly, "
               "without judgement.", poppins(32), NAVY, W - 2 * PAD, 1.3)
    footer(d, 3)
    return c


def slide4():
    c = Image.new("RGBA", (W, H), WHITE)
    photo_top(c, photo("01-teacher-class-left.jpg"), 520, (0.4, 0.45))
    d = ImageDraw.Draw(c)
    y = 575
    d.text((PAD, y), "HOW EVERY SESSION WORKS", font=poppins(26, "Bold"), fill=RED)
    d.text((PAD, y + 44), "The 4-Step Method", font=spartan(72), fill=NAVY_D)
    steps = [("Open Dialogue", "A safe space to build trust among peers."),
             ("Skill Building", "Evidence-based tools for stress and pressure."),
             ("Hands-on Activity", "Individual or group activities that stick."),
             ("Private Reflection", "Personal reflection for lasting change.")]
    y += 140
    for i, (t, s) in enumerate(steps, 1):
        cx, cy = PAD + 34, y + 40
        d.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill=RED if i % 2 else TEAL)
        d.text((cx, cy + 2), str(i), font=spartan(40), fill=WHITE, anchor="mm")
        d.text((PAD + 96, y), t, font=poppins(34, "Bold"), fill=NAVY_D)
        d.text((PAD + 96, y + 46), s, font=poppins(27), fill=NAVY)
        y += 118
    footer(d, 4)
    return c


def slide5():
    c = Image.new("RGB", (W, H))
    c.paste(cover(photo("04-students-b.jpg"), (W, H), (0.5, 0.4)))
    c = c.convert("RGBA")
    c.alpha_composite(gradient((W, H), 120, 235))
    d = ImageDraw.Draw(c)
    y = 230
    d.text((PAD, y), "WHEN & WHERE", font=poppins(26, "Bold"), fill=TEAL)
    d.text((PAD, y + 44), "FREE", font=spartan(190), fill=WHITE)
    d.text((PAD, y + 222), "for the first month", font=spartan(64, "Bold"), fill=WHITE)
    rows = [("Every Wednesday & Sunday", "Two sessions a week"),
            ("Classes 6 to 12", "Current & new students welcome"),
            ("100+ Academy, Sector 46", "Gurugram, Haryana")]
    y += 350
    for t, s in rows:
        d.rounded_rectangle((PAD, y, W - PAD, y + 118), 22, fill=(255, 255, 255, 235))
        d.rectangle((PAD, y + 24, PAD + 8, y + 94), fill=RED)
        d.text((PAD + 40, y + 18), t, font=poppins(34, "Bold"), fill=NAVY_D)
        d.text((PAD + 40, y + 66), s, font=poppins(26), fill=NAVY)
        y += 138
    d.text((PAD, y + 20), "1,500+ students have already been through this program.",
           font=poppins(28, "SemiBold"), fill=WHITE)
    footer(d, 5, dark=True)
    return c


def slide6():
    c = Image.new("RGBA", (W, H), WHITE)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 18), fill=RED)
    d.rectangle((0, H - 18, W, H), fill=RED)
    lock = Image.open(brand.BRAND_DIR / "logos" / "100-plus-academy-favicon.png").convert("RGB")
    lock = lock.crop(ImageOps.invert(lock).getbbox())
    lw = 460
    lock = lock.resize((lw, int(lock.height * lw / lock.width)), Image.LANCZOS)
    c.paste(lock, ((W - lw) // 2, 110))
    y = 110 + lock.height + 70
    for line in ("Reserve your", "child's free seat"):
        d.text((W // 2, y), line, font=spartan(84), fill=NAVY_D, anchor="mt")
        y += 88
    y += 20
    d.text((W // 2, y), "Under a minute · No fee · Parents can register",
           font=poppins(30), fill=NAVY, anchor="mt")
    y += 90
    bx0, bx1 = PAD + 60, W - PAD - 60
    d.rounded_rectangle((bx0, y, bx1, y + 110), 55, fill=RED)
    d.text((W // 2, y + 56), "REGISTER FREE", font=spartan(54), fill=WHITE, anchor="mm")
    y += 150
    d.text((W // 2, y), URL, font=poppins(34, "Bold"), fill=RED, anchor="mt")
    y += 64
    d.text((W // 2, y), f"Call / WhatsApp  {PHONE}", font=poppins(34, "SemiBold"),
           fill=NAVY_D, anchor="mt")
    y += 110
    chips = ["Classes 6–12", "Wed & Sun", "Sector 46, Gurugram"]
    f = poppins(28, "SemiBold")
    widths = [d.textlength(t, font=f) + 52 for t in chips]
    x = (W - sum(widths) - 20 * (len(chips) - 1)) // 2
    for t, cw in zip(chips, widths):
        d.rounded_rectangle((x, y, x + cw, y + 64), 32, fill=TINT)
        d.text((x + cw / 2, y + 32), t, font=f, fill=NAVY_D, anchor="mm")
        x += cw + 20
    d.text((W // 2, H - 110), "I.D.O.D. Program in partnership with Kailasa Education",
           font=poppins(24), fill=NAVY, anchor="mt")
    return c


def main():
    OUT.mkdir(exist_ok=True)
    slides = [slide1, slide2, slide3, slide4, slide5, slide6]
    paths = []
    for i, fn in enumerate(slides, 1):
        p = OUT / f"idod-carousel_{i:02d}.png"
        fn().convert("RGB").save(p)
        if i < 6:  # slide 6 already carries the full logo lockup
            pos = "top-right" if i in (3,) else "top-left"
            brand.apply_logo(p, position=pos, width_frac=0.2)
        paths.append(p)
    print("\n".join(str(p) for p in paths))


if __name__ == "__main__":
    main()
