from .config import settings
from fastapi import FastAPI
from agent_backend.routes.chat import router as chat_router
import logging
import uvicorn

log = logging.getLogger(__name__)


app = FastAPI()
app.include_router(chat_router)


def main():
    log.info("Server is running")
    uvicorn.run(app, host=settings.host, port=settings.port)
