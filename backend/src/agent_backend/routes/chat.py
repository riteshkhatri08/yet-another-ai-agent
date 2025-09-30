from agent_backend.helper.connection_manager import manager as connection_manager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
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
