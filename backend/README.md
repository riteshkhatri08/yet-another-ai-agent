# Agent Backend

FastAPI backend that streams responses from a local LLM server (e.g. LM Studio / OpenAI compatible) to a React/Vite frontend.

## Features
- `/chat` streaming endpoint emitting NDJSON lines with incremental deltas
- Config layering (environment vars + YAML + .env) via Pydantic Settings
- Pluggable local LLM HTTP streaming using OpenAI-style responses
- CORS enabled for local development (`http://localhost:5173`)

## Requirements
- Python >= 3.13
- A local LLM server exposing `POST /v1/chat/completions` (LM Studio or similar)

## Installation
Create and activate a virtual environment (recommended).

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```
Alternatively using uv:
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Configuration
Settings are resolved in this order:
1. Explicit values passed when instantiating `Settings()` (not typical here)
2. Environment variables / `.env`
3. YAML files in `resources/` (`config.yaml` then environment-specific like `config.local.yaml`)

Environment selection uses `APP_ENV` (defaults to `local`).

### Sample `.env.example`
```
APP_ENV=local
HOST=0.0.0.0
PORT=8000
USERNAME=admin
PASSWORD=change-me
LLM__HOST=http://localhost:1234
LLM__MODEL=TheBloke/MyLocalModel
LLM__MAX_TOKENS=512
LLM__TIMEOUT_SECONDS=120
LLM__DEBUG=false
```
Note: nested model fields use double underscore: `LLM__HOST` maps to `settings.llm.host`.

### Sample `resources/config.local.yaml`
```yaml
host: 0.0.0.0
port: 8000
username: admin
password: change-me
llm:
  host: http://localhost:1234
  model: TheBloke/MyLocalModel
  max_tokens: 512
  timeout_seconds: 120
  debug: false
```

## Running
Development (auto-reload) with uvicorn:
```bash
uvicorn agent_backend.server:app --reload --host 0.0.0.0 --port 8000
```
Or via the console script (no reload):
```bash
python -m agent_backend.server
```
If installed: 
```bash
agent-backend
```

## Endpoint
### POST `/chat`
Request JSON:
```json
{ "message": "Hello" }
```
Response: `application/x-ndjson` streaming lines:
```
{"meta":{"model":"local","role":"assistant"}}
{"delta":"Hi there"}
{"delta":"! How can"}
{"delta":" I help?"}
{"done":true}
```
Frontend accumulates each `delta` piece to build full answer.

### Curl Example
```bash
curl -N -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Hello"}'
```

### Python Client Snippet
```python
import httpx
import json

with httpx.Client(timeout=None) as client:
    with client.stream("POST", "http://localhost:8000/chat", json={"message":"Hello"}) as resp:
        for line in resp.iter_lines():
            if not line: continue
            data = json.loads(line)
            if 'delta' in data:
                print(data['delta'], end='', flush=True)
        print()  # newline after done
```

## LLM Integration
`agent_backend/services/llm.py` expects an OpenAI-compatible streaming response from `POST /v1/chat/completions`. Adapt or extend to other providers by adding new async generators.

## Development Scripts
Format & sort imports:
```bash
black . && isort .
```
Type check:
```bash
mypy src
```
Tests (if/when added):
```bash
pytest
```

## Roadmap
- Error classification & structured error responses
- Authentication / API keys
- WebSocket streaming option
- Multiple model selection endpoint
- Persistence of conversation history

## License
MIT
