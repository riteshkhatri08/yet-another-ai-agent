import os
import json
import logging
import httpx
from typing import AsyncGenerator, List, Dict, Any
from agent_backend.config import settings

log = logging.getLogger(__name__)

LLM_HOST = settings.llm.host
LLM_MODEL = settings.llm.model

# Stream responses from locally running llm
async def stream_local_llm(messages: List[Dict[str, Any]]) -> AsyncGenerator[str, None]:
    """Stream responses from LM Studio using chat completions.
    """
    url = f"{LLM_HOST}/v1/chat/completions"
    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "stream": True,
        "max_tokens": settings.llm.max_tokens or 2048,
        "temperature": 0.7,
    }
    timeout_seconds = settings.llm.timeout_seconds or 300
    timeout = httpx.Timeout(timeout_seconds)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            async with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                async for raw_line in resp.aiter_lines():
                    if not raw_line:
                        continue
                    # Some servers prefix with 'data:' per SSE; strip if present
                    line = raw_line.lstrip()
                    if line.startswith("data:"):
                        line = line[5:].strip()
                    if line == "[DONE]":
                        break
                    if settings.llm.debug:
                        log.debug("LLM RAW LINE: %s", line)
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        log.debug("Skipping non-JSON line: %s", line)
                        continue
                    # OpenAI-style: choices[0].delta.content
                    choices = data.get("choices") or []
                    if not choices:
                        continue
                    delta = choices[0].get("delta") or {}
                    content_piece = delta.get("content")
                    if content_piece:
                        yield content_piece
        except httpx.HTTPError as e:
            log.error("LLM stream error: %s", e)
            yield "[LLM error]"

async def simple_user_messages(message: str) -> List[Dict[str, Any]]:
    return [{"role": "user", "content": message}]
