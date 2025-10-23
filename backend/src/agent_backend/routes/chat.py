from agent_backend.helper.connection_manager import manager as connection_manager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from agent_backend.services.llm import stream_local_llm, simple_user_messages
import json
import logging

log = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


# Chat endpoint via a webscoket connection
@router.websocket("/ws")
async def streaming_chat(websocket: WebSocket):
    log.info("here")
    await connection_manager.connect(websocket)
    try:
        while True:
            message = await connection_manager.receive(websocket)
            log.info(f"Echoing: {message}")
            reply = {"type": "websocket.send", "text": message.get("text")}
            await connection_manager.send(websocket, reply)
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket)
        log.info(f"Client disconnected [{websocket}]")
    except RuntimeError as e:
        log.error("Some Error occured", e)
        await connection_manager.disconnect(websocket)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/chat/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("")
async def get():
    return HTMLResponse(html)


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
