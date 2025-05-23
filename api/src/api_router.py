import logging
from pathlib import Path

import httpx
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse, RedirectResponse

from api.src.models import ContentRequest, RagFileRequest, LLMRequest, Message
from api.src.rag import get_embeddings, find_most_similar
from api.src.utils.functions import extract_pages
from api.src.utils.vector_db import VECTOR_DB
from endpoints import Endpoints

api_logger = logging.getLogger("api")

api_router = APIRouter(prefix="/chat")


@api_router.get("/")
async def get_chat():
    """
    Redirects to UI service main page

    Args:
    Returns:
         RedirectResponse
    """
    return RedirectResponse(Endpoints.UI)


@api_router.post("/")
async def post_message(model: ContentRequest):
    """
    Receives text from user which is routed to LLM. Returns LLM response text
    Args:
        model: ContentRequest

    Returns:
         LLM response text
    """
    async with httpx.AsyncClient() as client:
        additional_context = await find_most_similar(
            model.session_hash, model.content, VECTOR_DB, 2
        )
        additional_context_str = ["".join(item[0]) for item in additional_context]

        response = await client.post(
            Endpoints.LLM_COMPLETIONS,
            timeout=10,
            headers={"Content-Type": "application/json"},
            json=LLMRequest(
                messages=[
                    Message(content=model.content),
                    Message(content=additional_context_str, role="system"),
                ]
            ).model_dump(),
        )
        api_logger.debug(f"Response {response.content}")

        if response.status_code == 200:
            return JSONResponse(
                {"response": response.json()["choices"][0]["message"]["content"]}
            )
        else:
            return JSONResponse("{'error': 'Error while model processing'}}")


@api_router.post("/file/")
async def post_rag_file(model: RagFileRequest):
    """
    Receives file which is converted to embeddings and stored for user

    Args:
        model: RagFileRequest
    Returns:
        State whether file is properly processed
    """
    path = Path(model.file)
    data = extract_pages(path)
    data_str = "".join(data)

    api_logger.debug(f"RAG | Data from file: {data}")

    chunks = [sent for sent in data_str.split(".")]
    embeddings = []
    try:
        for chunk in chunks:
            embeddings.append(await get_embeddings(chunk))

        VECTOR_DB[model.session_hash].extend(embeddings)
        api_logger.debug(f"Current vector db: {VECTOR_DB}")
    except TimeoutError:
        return JSONResponse(
            {"response": "Too big amount of data. Try to split onto smaller pieces."}
        )
    except Exception:
        return JSONResponse({"response": "Error occurred while file processing"})
    return JSONResponse(
        {"response": "I am ready to answer questions according to the file"}
    )
