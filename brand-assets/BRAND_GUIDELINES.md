# 100 Plus Academy - Brand Guidelines for image generation

Source: https://100plusacademy.com (analysed 2026-10-06). Machine-readable
version: `brand.json`. **These rules apply to every generated image.**

## Logos (`logos/`)
| File | Use |
|---|---|
| `100-plus-academy-logo.png` (238x114, transparent) | Primary logo. Red "100" whose two zeros are archery targets with arrows, teal "+" , red "ACADEMY" wordmark. |
| `100-plus-academy-favicon.png` (500x500, white bg) | Square lockup with tagline "JEE \| NEET \| FOUNDATION". Use for avatars / square placements. |

Rules
- **Never ask the image model to draw the logo** - it will garble it. Generate
  the artwork with clear space, then composite the real PNG on top
  (see `image-gen/brand.py`).
- Keep clear space around the logo of at least the height of the "A" in ACADEMY.
  Do not recolor, stretch, rotate, outline, or place on busy/red backgrounds.
  On dark or red backgrounds use a white rounded plate behind the logo.
- Preferred placement: top-left or bottom-center, ~15-20% of canvas width.
- The source logo is small (238 px wide); request a higher-resolution original
  from the owner for print or large formats.

## Colors
| Role | Hex | Notes |
|---|---|---|
| Brand red (primary) | `#EB1F27` | Logo red; headlines, key shapes, CTAs |
| Deep red | `#D92029` / `#CC0F0F` / `#D10300` | Website headings / hover / emphasis |
| Brand teal (secondary) | `#3BC0CA` | The "+" in the logo; highlights, badges |
| Navy | `#003060`, dark `#0B2149` | Trust / text on light, header bands |
| Orange accent | `#FF6938` | Sparingly: CTA highlights, urgency |
| White | `#FFFFFF` | Dominant background |
| Tints | `#FFF0F0`, `#E0FAFF` | Soft panels |

Palette balance: ~60% white/light neutral, ~25% red, ~10% navy, ~5% teal/orange.
Avoid unrelated hues (purple, green, pink) as dominant colors.

## Typography
- Headlines: **League Spartan** Bold/ExtraBold - tight, confident, geometric.
- Body / captions: **Poppins** Regular-SemiBold.
- Image models render text poorly: generate backgrounds **without text** and add
  all copy with real fonts in a compositing step, or keep any in-image text to
  a few short, simple words and verify spelling.

## Style and tone
- Clean, modern, academic, trustworthy, energetic. Flat or lightly-textured
  vector-style backgrounds, generous negative space for text overlay.
- Imagery themes: students studying, targets/bullseye + arrows (brand motif,
  echoing the logo), physics/maths/biology motifs, achievement and toppers.
- Audience: Indian school students (Class 6-12), parents, JEE/NEET aspirants;
  also NRI/US families for the USA program. Depict Indian students and
  classroom settings; school-appropriate, positive, no stock-photo clichés.
- Never depict or name real students/teachers without permission. Do not invent
  results, ranks, or testimonials; use only the proof points below.

## Fixed facts (use exactly)
- Name: **100 Plus Academy** (also "100+ Academy"). Tagline: **JEE | NEET | Foundation**.
- Phones: **+91 99901 11965**, +91 98731 11965. WhatsApp: +91 92171 40286.
- Email: **info@100plusacademy.com**. Web: **100plusacademy.com**.
- Address: 1387-P, Sector 46, Gurugram, Haryana 122018.
- Social: Instagram `@100plusacademygurgaon`, Facebook `hundredplusacademy`,
  YouTube `@100PLUSACADEMY`.
- Proof points: 4.8/5 Google rating; 20,000+ students taught; 200+ recorded
  courses; 12+ years; IIT/NIT expert faculty; small batches.
- Programs: JEE, NEET, Boards (CBSE/ICSE/IB, Class 6-12), Olympiad, Foundation,
  1-to-1 live classes, USA/foreign admissions (AP/SAT/ACT/IB), free NEET test series.

## Standard footer for social posts
Logo + "100plusacademy.com" + one phone number (+91 99901 11965). Add the
address only on large formats.

## Prompt boilerplate
`image-gen/brand.py` prepends the brand brief to every prompt automatically
(see `BRAND_PROMPT`). Put only the post-specific idea in your prompt.
