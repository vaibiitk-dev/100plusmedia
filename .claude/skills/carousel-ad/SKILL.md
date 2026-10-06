---
name: carousel-ad
description: Create a branded multi-slide carousel ad (Meta/Instagram/Facebook/LinkedIn, 1080x1350) for 100 Plus Academy from the user's own photos and a landing page, plus ad copy. Use when asked for a carousel post/ad, social ad creative, or event promo from supplied photos or a website URL.
---

# Carousel ad (100 Plus Academy)

Follow `brand-assets/BRAND_GUIDELINES.md` (colors, League Spartan + Poppins,
official logo, exact contact details). Never invent facts, results or quotes.
Worked example: `campaigns/2026-10_idod-carousel/`.

## Steps
1. **Read the source page** the user gives (curl + strip HTML). Extract offer,
   dates, audience, price, CTA link, partners, proof points. Use only those facts.
2. **Look at the photos.** Pick a role for each: hook, problem, proof, how it
   works, offer, CTA. Note faces, minors, sensitive on-screen text, posters.
3. **Create** `campaigns/<YYYY-MM>_<name>/` with `photos/` (copy uploads from
   `/root/.claude/uploads/...`), copy `build_template.py` there as `build.py`,
   and edit the slide functions. Default 6 slides, 1080x1350 (4:5):
   1 hook (big headline + free/offer label + "Swipe"), 2 problem,
   3 proof/event recap, 4 how it works, 5 offer details (when/where/who),
   6 CTA (full logo lockup, big button, URL, phone, partner credit).
4. **Build** `python build.py`; render a contact sheet and LOOK at it. Fix text
   overflow, contrast and empty space. Zoom into any blurred area.
5. **Write `AD_COPY.md`**: Meta primary text, headline (<=40 chars), description,
   CTA button, per-card headlines, Instagram caption + hashtags, targeting
   (parents, local radius), pre-publish checklist.
6. **Deliver** slides + copy with SendUserFile.

## Rules
- Logo: composite real PNG (`brand.apply_logo`), never AI-drawn. Slide 6 uses
  the square lockup with tagline.
- Text via PIL with brand fonts in `brand-assets/fonts/`; photos darkened with
  a navy gradient where text sits on them.
- Blur sensitive on-screen text (e.g. explicit/self-harm stats) before use.
- Keep photos and rendered slides OUT of git (public repo, identifiable
  minors): campaign `.gitignore` = `photos/` + `slides/`. Commit only
  `build.py`, `README.md`, `AD_COPY.md`. Ask before committing images.
- Remind the user: written parental consent for visible students, and consent
  from any named partner.
- Don't use OPENAI_API_KEY here; real photos need no generation. If a
  generated background is wanted, use `image-gen/` (image-only key).
- Commit/push to the branch the session specifies; no PR unless asked.

## AI-art variant
For a richer design: adapt `campaigns/2026-10_idod-carousel/gen_art.py` (text-free
`images.generate` backgrounds via `image-gen/`) and `build_ai.py` (art + rounded
photo cards + white panels behind text so art never sits under copy). Never send
real student photos to OpenAI (images.edit is not an approved endpoint in SECURITY.md).
