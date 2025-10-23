from agent_backend.helper.connection_manager import manager as connection_manager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from agent_backend.services.llm import stream_local_llm, simple_user_messages
import json
import logging

log = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("")
async def chat_post(payload: dict = Body(...)):
    """Stream response from local LLM as NDJSON lines.
    Each line: {"delta": "text"} and a final {"done": true} line.
    Payload: {"message": "text"}
    Frontend parses each line and appends delta.
    """
    message = payload.get("message")
    if not message:
        return JSONResponse({"error": "message required"}, status_code=400)

    messages = await simple_user_messages(message)

    async def gen():
        # Kick off stream with a meta line
        yield json.dumps({"meta": {"model": "local", "role": "assistant"}}) + "\n"
        async for piece in stream_local_llm(messages):
            yield json.dumps({"delta": piece}) + "\n"
        yield json.dumps({"done": True}) + "\n"

    return StreamingResponse(gen(), media_type="application/x-ndjson")
