import logging
from pathlib import Path

import httpx
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse, RedirectResponse

from api.src.models import ContentRequest, RagFileRequest, LLMRequest, Message
from endpoints import Endpoints

api_logger = logging.getLogger("api")

api_router = APIRouter(prefix="/chat")


VECTOR_DB: dict[str, list[dict[str, list[float]]]] = {}

@api_router.get("/")
async def get_chat():
    return RedirectResponse(Endpoints.UI)


@api_router.post("/")
async def post_message(model: ContentRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(Endpoints.LLM_COMPLETIONS,
                                     timeout=10,
                                     headers={"Content-Type": "application/json"},
                                     json=LLMRequest(
                                         messages=[Message(
                                             content=model.content
                                         )]
                                     ).model_dump()
        )
        api_logger.debug(f"Response {response.content}")

        if response.status_code == 200:
            return JSONResponse({"response": response.json()["choices"][0]["message"]["content"]})
        else:
            return JSONResponse("{'error': 'Error while model processing'}}")


@api_router.post("/upload")
async def post_rag_file(model: RagFileRequest):
    # Build vocab and document vectors
    data = Path(model.file).read_text(encoding="utf-8")
    api_logger.debug(f"RAG | Data from file: {data}")

    chunks = [sent for sent in data.split('.')]

    async with httpx.AsyncClient() as client:
        for chunk in chunks:
            embedding = await client.post(Endpoints.LLM_COMPLETIONS,
                                           headers={"Content-Type": "application/json"},
                                           json={
                                               "model": "text-embedding-nomic-embed-text-v1.5",
                                               "input": chunk,
                                               "stream": False
                                           })

            VECTOR_DB[model.session_hash].append({chunk: embedding.json()["data"]["embedding"]})

    api_logger.debug(f"Current vector db: {VECTOR_DB}")
    return JSONResponse({"response": "I am ready to answer questions according to the file"})