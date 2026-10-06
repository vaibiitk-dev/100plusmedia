# Security

**OPENAI_API_KEY is restricted to image-generation calls only.** Do not use for chat/completions/embeddings. Any PR adding non-image usage of this key should be rejected.

- Never commit `.env` or any real key (`.env.example` holds placeholders only).
- Never print or log the key value.
- The only code allowed to use the key is `image-gen/openai_image_client.py`.
  It calls `images.generate` for generation, plus a read-only `models.list`
  (`GET /v1/models`) to confirm which image model the account can use. No other
  endpoints are permitted.
