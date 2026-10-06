# 100plusmedia - project rules

## Brand identity is mandatory
Before generating ANY image, post, or marketing copy, read
`brand-assets/BRAND_GUIDELINES.md` (data in `brand-assets/brand.json`) and
**always follow it**: logo usage, colors, fonts, tone, contact details and
proof points. Do not deviate or invent brand facts.

- Use only the official logos in `brand-assets/logos/`; composite them with
  `image-gen/brand.py:apply_logo()` - never have the image model draw the logo.
- Use exact contact details/proof points from the guidelines.
- Keep `brand=True` (default) in `generate_image()`; update brand-assets if the
  brand changes, rather than overriding it in a prompt.
- `OPENAI_API_KEY` is image-generation only (see `SECURITY.md`).
