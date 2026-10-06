"""Generate AI background art (no people, no text) for the I.D.O.D. carousel.

Uses image-gen/openai_image_client.generate_image only (images.generate; the
key is image-generation only per SECURITY.md). No student photos are sent.
The brand brief is prepended automatically.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "image-gen"))
import openai_image_client as c  # noqa: E402

ART = Path(__file__).parent / "art"
ART.mkdir(exist_ok=True)

COMMON = ("Vertical 2:3 flat-vector editorial illustration for a social media carousel "
          "slide, soft grain, lots of clean empty space in the {space} for text. "
          "No text, no letters, no logos, no people. ")
PROMPTS = {
    "hook": COMMON.format(space="lower half") +
            "Calm and hopeful: large concentric bullseye rings partly off-canvas at the top "
            "right with a single arrow in the centre, soft teal and red rings, warm light "
            "gradient, a few floating plus signs.",
    "problem": COMMON.format(space="upper-middle") +
               "Contrast of pressure and calm: tangled red scribble lines and notification "
               "bubbles/phone shapes on the left edge calming into smooth teal waves toward "
               "the right, navy accents, white-to-pale-tint background.",
    "method": COMMON.format(space="centre") +
              "A winding path of four stepping-stone circles climbing diagonally to a "
              "bullseye target, minimal, red and teal circles on a pale background with navy "
              "line accents and tiny plus signs.",
    "cta": COMMON.format(space="centre") +
           "Optimistic sunburst of thin radiating rays from the bottom centre in pale red "
           "and teal tints, scattered plus signs and small bullseye targets, mostly white "
           "background, framing a clean centre.",
}
for key, prompt in PROMPTS.items():
    c.generate_image(prompt, "1024x1536", "medium", output_path=ART / f"{key}.png",
                     name=f"idod-{key}")
