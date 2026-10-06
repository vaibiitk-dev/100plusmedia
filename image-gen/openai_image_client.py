"""Restricted OpenAI image-generation client.

FINANCIAL CONTROL: OPENAI_API_KEY may be used ONLY for image generation.
This module exposes a single public function, generate_image(). Never add
chat/completions, embeddings, or any other endpoint here. The only non-image
call is a read-only models listing (GET /v1/models) used to verify which image
model the account has access to; it is free and generates nothing.

Model note: a client once mentioned a model called "GPT Image 2.5 Sunburst
(Max)". That is NOT a recognized OpenAI model ID as of now. The wrapper
instead uses the first verified-available model from MODEL_PREFERENCE.
"""
import base64
import os
import re
from datetime import datetime
from pathlib import Path

import requests
from openai import OpenAI

MODEL_PREFERENCE = ["gpt-image-1", "dall-e-3"]
OUTPUT_DIR = Path(__file__).parent / "output"

_client = None
_model = None


def _get_client():
    global _client
    if _client is None:
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is not set (see .env.example).")
        _client = OpenAI(api_key=key)
    return _client


def _resolve_model():
    """Return the first preferred image model this account can access."""
    global _model
    if _model is None:
        available = {m.id for m in _get_client().models.list()}
        for candidate in MODEL_PREFERENCE:
            if candidate in available:
                _model = candidate
                break
        else:
            raise RuntimeError(
                f"None of {MODEL_PREFERENCE} are available to this account."
            )
    return _model


def _map_quality(model, quality):
    """'standard' is dall-e-3 wording; gpt-image-1 uses low/medium/high/auto."""
    if model == "gpt-image-1":
        return {"standard": "medium", "hd": "high"}.get(quality, quality)
    return {"medium": "standard", "low": "standard", "high": "hd"}.get(quality, quality)


def _slug(text, max_words=5):
    words = re.findall(r"[a-z0-9]+", text.lower())[:max_words]
    return "-".join(words) or "image"


def build_filename(prompt, size, name=None):
    """Easy-to-grab name: YYYY-MM-DD_HHMMSS_<slug>_<WxH>.png (sorts by date)."""
    now = datetime.now()
    slug = _slug(name or prompt)
    return f"{now:%Y-%m-%d_%H%M%S}_{slug}_{size}.png"


def generate_image(prompt, size, quality, output_path=None, name=None):
    """Generate one image and save it in the repo. Returns the saved file path.

    name: short label used in the filename (defaults to the prompt's first words).
    output_path: explicit file path; defaults to
    image-gen/output/YYYY-MM-DD_HHMMSS_<slug>_<size>.png.
    """
    model = _resolve_model()
    q = _map_quality(model, quality)
    print(f"[image-gen] model={model} size={size} quality={q}")

    kwargs = dict(model=model, prompt=prompt, size=size, quality=q, n=1)
    if model == "dall-e-3":
        kwargs["response_format"] = "b64_json"
    result = _get_client().images.generate(**kwargs)
    item = result.data[0]
    if item.b64_json:
        data = base64.b64decode(item.b64_json)
    else:
        data = requests.get(item.url, timeout=60).content

    if output_path is None:
        output_path = OUTPUT_DIR / build_filename(prompt, size, name)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(data)
    print(f"[image-gen] saved {output_path}")
    return str(output_path)
