# image-gen

Image generation for social media static posts. **Image generation only.**

## Financial-control rule
`OPENAI_API_KEY` is for image generation only (client requirement). Never use
it for chat/completions/embeddings; PRs doing so are rejected. See `../SECURITY.md`.

## Run the test
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...        # or load from .env (never commit it)
python image-gen/test_generate.py
```
Uses 1 image, 1024x1024, standard quality. Prints the model used.

## Output
Images are saved to `image-gen/output/` (git-ignored). Default names are
timestamped (`image_YYYYMMDD-HHMMSS.png`); the test writes `test_image.png`.

## Models
The client lists models and uses the first available of `gpt-image-1`,
`dall-e-3`. "GPT Image 2.5 Sunburst (Max)" is not a recognized OpenAI model ID.
Each call logs model, size and quality for cost auditing.

## Adding prompt scripts
Create `image-gen/<name>.py`, import `generate_image` from
`openai_image_client`, and call it with your prompt, size, quality and
output path. Don't call the OpenAI SDK directly from other scripts.
