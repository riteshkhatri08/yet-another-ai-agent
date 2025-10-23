# Yet Another AI Agent

A minimal full‑stack AI chat application: FastAPI backend streaming local LLM responses to a React + Vite frontend.

## Overview
- Backend (`backend/`): FastAPI service exposing a streaming `/chat` endpoint returning NDJSON incremental deltas from a local LLM (OpenAI compatible API server such as LM Studio).
- Frontend (`frontend/`): React interface with live token streaming and message history.

## Architecture
```
[User Browser] --(fetch POST /chat)--> [FastAPI Backend] --(HTTP stream)--> [Local LLM Server]
                                 ^                                   |
                                 |------ NDJSON streamed back -------|
```
Streaming pattern:
1. Frontend sends `{"message":"..."}` to `/chat`.
2. Backend converts to OpenAI-style messages list and POSTs to local LLM with `stream=true`.
3. LLM yields partial JSON lines; backend parses and re-emits simplified NDJSON `{"delta": "text"}` pieces.
4. Frontend accumulates deltas into final assistant message.

## Quick Start
### Backend
```bash
cd backend
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
# (optionally edit .env for your model)
uvicorn agent_backend.server:app --reload --host 0.0.0.0 --port 8000
```
Make sure a local LLM server is running (default `http://localhost:1234`).

### Frontend
```bash
cd frontend
npm install
echo "VITE_API_BASE_URL=http://localhost:8000" > .env
npm run dev
```
Visit: http://localhost:5173

## Configuration
See `backend/README.md` for details. Nested settings use double underscores (`LLM__HOST`). Environment selection via `APP_ENV` chooses `resources/config.<env>.yaml`.

## Key Files
- `backend/src/agent_backend/server.py` FastAPI app + CORS + router registration
- `backend/src/agent_backend/routes/chat.py` `/chat` streaming endpoint
- `backend/src/agent_backend/services/llm.py` logic to stream LLM responses
- `frontend/src/components/Chat.jsx` UI and streaming assembly
- `frontend/src/lib/api.js` low-level streaming fetch helper

## API Contract
POST `/chat`:
Request: `{ "message": "Hello" }`
Response Content-Type: `application/x-ndjson` lines:
```
{"meta":{"model":"local","role":"assistant"}}
{"delta":"Hi"}
{"delta":" there"}
{"done":true}
```

## Development
Formatting / lint (backend): `black . && isort .`
Type checking: `mypy src`
Frontend build: `npm run build`

## Testing
(Backend) Add tests under `backend/tests/` using `pytest`.
(Frontend) Use Vitest + React Testing Library (not yet added).

## Roadmap
- Persistent conversation store
- Authentication & roles
- Multiple model selection
- WebSocket/SSE fallback
- Frontend message retry & cancellation

## License
MIT

---
Contributions welcome. Open an issue or PR to suggest improvements.
