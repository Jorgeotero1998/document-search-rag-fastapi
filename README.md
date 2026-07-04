# Document Search (FTS + RAG) — ES/EN

## Español

Servicio de búsqueda documental con:

- Postgres **Full-Text Search** (GIN index)
- Endpoint de “preguntar” (**RAG**) que cita docs \([1], [2]...\) usando IA opcional

### Endpoints
- `/api/v1/docs` (POST)
- `/api/v1/docs/search?q=...` (GET)
- `/api/v1/docs/ask` (POST, requiere IA habilitada)

---

## English

Document search service with Postgres FTS and optional RAG endpoint with citations.

