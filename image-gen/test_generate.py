"""Cheap smoke test: one 1024x1024 standard-quality image."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import openai_image_client as c  # noqa: E402

PROMPT = ("A minimal modern social media post background, warm sunburst gradient, "
          "clean negative space for text overlay, flat design, no text.")
OUT = Path(__file__).parent / "output" / "test_image.png"

try:
    path = c.generate_image(PROMPT, "1024x1024", "standard", OUT)
    print(f"SUCCESS: saved {path}\nModel used: {c._model}")
except Exception as e:
    # Never print str(e): API auth errors echo a masked fragment of the key.
    print(f"FAILURE: {type(e).__name__} (HTTP status: {getattr(e, 'status_code', 'n/a')})")
    sys.exit(1)
