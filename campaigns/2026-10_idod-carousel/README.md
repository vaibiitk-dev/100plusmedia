# 2026-10 I.D.O.D. carousel ad

Six-slide carousel (1080x1350) for the free I.D.O.D. workshop, built from the
first event's photos. It follows `brand-assets/`.

- `build.py` renders `slides/` from `photos/` (`python build.py`)
- `AD_COPY.md` has the Meta primary text, headline, CTA, Instagram caption and hashtags

`photos/` and `slides/` are git-ignored: they show identifiable students and
this repository is public. Keep them out of git unless every parent has given
consent and the owner has approved.

## AI-art version
`gen_art.py` makes 4 backgrounds with `gpt-image-1` (images.generate only,
medium quality, ~4 images; no photos are sent to OpenAI). `build_ai.py` composites them with
the real photos, brand fonts and logo into `slides_ai/` (git-ignored).
