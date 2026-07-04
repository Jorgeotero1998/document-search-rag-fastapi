# Deploy (Render + Vercel) — ES/EN

## Español

### Backend (Render)

1) Subí el repo a GitHub
2) En Render: **New > Blueprint** y elegí el repo
3) Render detecta `render.yaml` y crea:
   - API (web)
   - Worker (Celery)
   - Redis
   - Postgres
4) El backend corre migraciones con `preDeployCommand: alembic upgrade head`

### Frontend (Vercel)

1) En Vercel importá el repo
2) Root Directory: `web`
3) Env var: `VITE_API_BASE_URL=https://<tu-api-render>`

### IA gratis (Groq)

1) Creá una key en Groq
2) En Render, seteá:
   - `LLM_ENABLED=true`
   - `LLM_API_KEY=<tu_key>`
   - `LLM_BASE_URL=https://api.groq.com/openai/v1`
   - `LLM_MODEL=llama-3.1-8b-instant`

---

## English

Render Blueprint for backend + Vercel for frontend. Groq is supported via OpenAI-compatible base URL.

