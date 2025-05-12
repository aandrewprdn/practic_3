import logging

from fastapi.routing import APIRouter
from starlette.responses import JSONResponse, RedirectResponse
import httpx

from api.src.models import ContentRequest
from endpoints import Endpoints

api_router = APIRouter(prefix="/chat")
api_logger = logging.getLogger("api")

@api_router.get("/")
async def get_chat():
    return RedirectResponse(Endpoints.UI)

@api_router.post("/")
async def post_message(model: ContentRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(Endpoints.LLM_COMPLETIONS,
                                     headers={"Content-Type": "application/json"},
                                     json={
                                        "model": "gemma-3-1b-it-qat",
                                        "messages": [
                                          { "role": "user", "content": model.content}
                                        ],
                                        "temperature": 0.7,
                                        "stream": False
                                    }
        )
        api_logger.debug(f"Response {response.content}")

        if response.status_code == 200:
            return JSONResponse(response.json())
        else:
            return JSONResponse("{'error': 'Error while model processing'}}")
