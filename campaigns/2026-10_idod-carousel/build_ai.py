"""AI-art version of the I.D.O.D. carousel: AI backgrounds (gen_art.py) +
real event photos in rounded cards + brand fonts/logo. Run gen_art.py first."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import build as b  # noqa: E402
from build import (C, H, NAVY, NAVY_D, PAD, PHONE, RED, TEAL, TINT, URL, W, WHITE,  # noqa: E402
                   footer, pill, poppins, spartan, swipe, text_block)

ART = b.HERE / "art"
OUT = b.HERE / "slides_ai"


def art_bg(name, offset=0, tint=None):
    a = Image.open(ART / f"{name}.png").convert("RGBA")
    a = a.resize((W, int(a.height * W / a.width)), Image.LANCZOS)
    bg = Image.new("RGBA", (W, H), tint or WHITE)
    bg.alpha_composite(a, (0, -offset))
    return bg


def card(c, img, box, focus=(0.5, 0.5), radius=36, border=RED):
    x0, y0, x1, y1 = box
    ph = b.cover(img, (x1 - x0, y1 - y0), focus).convert("RGBA")
    mask = Image.new("L", ph.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *ph.size), radius, fill=255)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((x0 + 12, y0 + 14, x1 + 12, y1 + 14), radius, fill=(11, 33, 73, 60))
    d.rounded_rectangle((x0 - 8, y0 - 8, x1 + 8, y1 + 8), radius + 6, fill=border)
    c.paste(ph, (x0, y0), mask)


def panel(c, box, alpha=235, radius=32):
    layer = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box, radius, fill=(255, 255, 255, alpha))
    c.alpha_composite(layer)


def s1():
    c = art_bg("hook")
    panel(c, (PAD - 24, 215, 700, 525), 235)
    d = ImageDraw.Draw(c)
    d.text((PAD, 250), "Beyond", font=spartan(130), fill=NAVY_D)
    d.text((PAD, 372), "marks.", font=spartan(130), fill=RED)
    card(c, b.photo("05-teacher-class-wide.jpg"), (PAD, 560, W - PAD, 1020), (0.45, 0.5))
    panel(c, (0, 1060, W, H))
    d = ImageDraw.Draw(c)
    pill(d, (PAD, 1090), "FREE WORKSHOP  ·  CLASSES 6–12", poppins(28, "Bold"), RED, WHITE)
    text_block(d, (PAD, 1170), "Inner Development for Overall Development helps your "
               "child grow calm, composed and confident.", poppins(31), NAVY_D, W - 2 * PAD, 1.25)
    swipe(d, H - 70, dark=False)
    return c


def s2():
    c = art_bg("problem", offset=250)
    panel(c, (PAD - 24, 205, W - PAD + 24, 520), 238)
    d = ImageDraw.Draw(c)
    d.text((PAD, 230), "THE STRUGGLES ARE REAL", font=poppins(26, "Bold"), fill=RED)
    text_block(d, (PAD, 276), "Today's students carry more than a syllabus.",
               spartan(76), NAVY_D, W - 2 * PAD, 1.0)
    card(c, b.photo("03-students-a.jpg"), (PAD + 330, 560, W - PAD, 900), (0.5, 0.4), border=TEAL)
    panel(c, (PAD, 960, W - PAD, 1250), 238)
    d = ImageDraw.Draw(c)
    f = poppins(32, "SemiBold")
    items = ["Exam anxiety", "Digital overwhelm", "Social comparison", "Career pressure"]
    cw = (W - 2 * PAD - 100) // 2
    for i, t in enumerate(items):
        x = PAD + 40 + (i % 2) * (cw + 20)
        y = 995 + (i // 2) * 120
        d.rounded_rectangle((x, y, x + cw, y + 90), 24, fill=TINT if i in (0, 3) else "#E8EEF6")
        d.text((x + 28, y + 45), t, font=f, fill=NAVY_D, anchor="lm")
    footer(d, 2)
    return c


def s3():
    import PIL.ImageFilter as F
    img = b.photo("02-presenter-screen.jpg")
    w, h = img.size
    box = (int(w * 0.38), int(h * 0.37), int(w * 0.80), int(h * 0.55))
    img.paste(img.crop(box).filter(F.GaussianBlur(w // 120)), box)
    c = Image.new("RGBA", (W, H), "#F4F8FC")
    card(c, img, (PAD, 290, W - PAD, 860), (0.42, 0.4))
    d = ImageDraw.Draw(c)
    pill(d, (PAD, 205), "SESSION 1 · COMPLETED", poppins(26, "Bold"), TEAL, WHITE)
    d.text((PAD, 920), "OUR FIRST SESSION", font=poppins(26, "Bold"), fill=RED)
    y = text_block(d, (PAD, 966), "Teens & social media: the real talk.", spartan(70),
                   NAVY_D, W - 2 * PAD, 1.0) + 14
    text_block(d, (PAD, y), "Students explored research on online pressure and "
               "comparison, then talked it through openly, without judgement.",
               poppins(30), NAVY, W - 2 * PAD, 1.3)
    footer(d, 3)
    return c


def s4():
    c = art_bg("method", offset=0)
    card(c, b.photo("01-teacher-class-left.jpg"), (PAD, 230, 600, 600), (0.4, 0.45))
    panel(c, (PAD - 20, 620, W - PAD + 20, H - 40), 242)
    d = ImageDraw.Draw(c)
    d.text((PAD, 640), "HOW EVERY SESSION WORKS", font=poppins(26, "Bold"), fill=RED)
    d.text((PAD, 684), "The 4-Step Method", font=spartan(70), fill=NAVY_D)
    d = ImageDraw.Draw(c)
    steps = [("Open Dialogue", "A safe space to build trust among peers."),
             ("Skill Building", "Evidence-based tools for stress and pressure."),
             ("Hands-on Activity", "Individual or group activities that stick."),
             ("Private Reflection", "Personal reflection for lasting change.")]
    y = 820
    for i, (t, s) in enumerate(steps, 1):
        cx, cy = PAD + 34, y + 34
        d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=RED if i % 2 else TEAL)
        d.text((cx, cy + 2), str(i), font=spartan(36), fill=WHITE, anchor="mm")
        d.text((PAD + 90, y), t, font=poppins(32, "Bold"), fill=NAVY_D)
        d.text((PAD + 90, y + 44), s, font=poppins(26), fill=NAVY)
        y += 108
    footer(d, 4)
    return c


def s6():
    c = art_bg("cta")
    panel(c, (PAD - 20, 140, W - PAD + 20, H - 140), 244, 44)
    d = ImageDraw.Draw(c)
    from PIL import ImageOps
    lock = Image.open(b.brand.BRAND_DIR / "logos" / "100-plus-academy-favicon.png").convert("RGB")
    lock = lock.crop(ImageOps.invert(lock).getbbox())
    lw = 400
    lock = lock.resize((lw, int(lock.height * lw / lock.width)), Image.LANCZOS)
    c.paste(lock, ((W - lw) // 2, 190))
    y = 190 + lock.height + 50
    for line in ("Reserve your", "child's free seat"):
        d.text((W // 2, y), line, font=spartan(80), fill=NAVY_D, anchor="mt")
        y += 84
    d.text((W // 2, y + 20), "Under a minute · No fee · Parents can register",
           font=poppins(28), fill=NAVY, anchor="mt")
    y += 90
    d.rounded_rectangle((PAD + 60, y, W - PAD - 60, y + 104), 52, fill=RED)
    d.text((W // 2, y + 53), "REGISTER FREE", font=spartan(52), fill=WHITE, anchor="mm")
    y += 140
    d.text((W // 2, y), URL, font=poppins(32, "Bold"), fill=RED, anchor="mt")
    d.text((W // 2, y + 56), f"Call / WhatsApp  {PHONE}", font=poppins(32, "SemiBold"),
           fill=NAVY_D, anchor="mt")
    d.text((W // 2, H - 205), "Wed & Sun · Classes 6–12 · Sector 46, Gurugram",
           font=poppins(26, "SemiBold"), fill=NAVY_D, anchor="mt")
    d.text((W // 2, H - 168), "I.D.O.D. Program in partnership with Kailasa Education",
           font=poppins(22), fill=NAVY, anchor="mt")
    return c


def main():
    OUT.mkdir(exist_ok=True)
    fns = [s1, s2, s3, s4, b.slide5, s6]
    for i, fn in enumerate(fns, 1):
        p = OUT / f"idod-carousel-ai_{i:02d}.png"
        fn().convert("RGB").save(p)
        if i < 6:
            b.brand.apply_logo(p, position="top-left",
                               width_frac=0.2)
        print(p)


if __name__ == "__main__":
    main()
