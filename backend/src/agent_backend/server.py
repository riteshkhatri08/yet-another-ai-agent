from .config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent_backend.routes.chat import router as chat_router
import logging
import uvicorn

log = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


def main():
    log.info("Server is running")
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__": 
    main()
