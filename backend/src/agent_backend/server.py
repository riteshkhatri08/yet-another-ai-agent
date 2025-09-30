from .config import settings
from fastapi import FastAPI

import logging
import uvicorn

log = logging.getLogger(__name__)


app = FastAPI()


def main():
    log.info("Server is running")
    uvicorn.run(app, host=settings.host, port=settings.port)
