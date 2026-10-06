"""Brand layer: every generated image must follow brand-assets/.

BRAND_PROMPT is prepended to prompts by generate_image(). apply_logo()
composites the real logo (never let the image model draw it).
"""
import json
from pathlib import Path

from PIL import Image

BRAND_DIR = Path(__file__).resolve().parent.parent / "brand-assets"
BRAND = json.loads((BRAND_DIR / "brand.json").read_text())
LOGO = BRAND_DIR / "logos" / "100-plus-academy-logo.png"

_c = BRAND["colors"]
BRAND_PROMPT = (
    "Brand: 100 Plus Academy, an Indian coaching institute (JEE, NEET, Boards, "
    "Class 6-12). Style: clean, modern, academic, trustworthy, energetic; flat "
    "vector-like look with generous negative space for text. Palette: mostly "
    f"white/light background, brand red {_c['logo_red']}, teal {_c['logo_teal']} "
    f"accents, navy {_c['navy']}; optional orange {_c['accent_orange']} sparingly; "
    "no purple/green/pink. Motifs: bullseye targets with arrows, students, "
    "science/maths symbols. Do NOT draw any logo, brand name, or text - leave "
    "clear space (top-left/bottom) for the official logo and copy to be added "
    "afterwards. Depict Indian students if people appear. "
)


def apply_logo(image_path, position="top-left", width_frac=0.18, margin_frac=0.04):
    """Paste the official logo onto a white rounded-free plate; saves in place."""
    img = Image.open(image_path).convert("RGBA")
    logo = Image.open(LOGO).convert("RGBA")
    w = int(img.width * width_frac)
    logo = logo.resize((w, int(logo.height * w / logo.width)), Image.LANCZOS)
    m = int(img.width * margin_frac)
    x = m if "left" in position else img.width - w - m
    y = m if "top" in position else img.height - logo.height - m
    plate = Image.new("RGBA", (w + 16, logo.height + 16), (255, 255, 255, 235))
    img.alpha_composite(plate, (x - 8, y - 8))
    img.alpha_composite(logo, (x, y))
    img.convert("RGB").save(image_path)
    return str(image_path)
