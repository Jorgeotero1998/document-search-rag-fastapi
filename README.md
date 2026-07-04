# OteroDocSearch

**EN**: Postgres FTS + RAG (citations)  
**ES**: BÃºsqueda FTS + RAG (con citas)

## Live demo / Demo online
- **Web**: https://<vercel-project>.vercel.app
- **API docs**: https://<render-service>.onrender.com/docs
- **API health**: https://<render-service>.onrender.com/api/v1/health

## Stack
- FastAPI
- PostgreSQL
- FTS
- RAG
- AI (Groq)

## Local setup (Docker)

    cp .env.example .env
    docker compose up --build

## Credentials (demo)

**EN**: Default demo admin is seeded from ADMIN_EMAIL / ADMIN_PASSWORD.
**ES**: El admin demo se crea desde ADMIN_EMAIL / ADMIN_PASSWORD.

## Deploy

**EN**:
- Backend: Render (Blueprint via render.yaml)
- Frontend: Vercel (Root Directory: web)
- Set VITE_API_BASE_URL to your Render URL.

**ES**:
- Backend: Render (Blueprint con render.yaml)
- Frontend: Vercel (Root Directory: web)
- Setear VITE_API_BASE_URL con la URL de Render.
