from fastapi.routing import APIRouter
from starlette.responses import JSONResponse
import httpx

from api.src.settings import AppSettings

api_router = APIRouter(prefix="/chat")

@api_router.get("/")
async def get_chat() -> JSONResponse:
    return JSONResponse({"result": "all works fine"})

@api_router.post("/")
async def post_message(input: str):
    url = f"{AppSettings().LLM_HOST}/v1/chat/completions"
    with httpx.AsyncClient() as client:
        response = await client.post(url, data={"messages": [{"role": "user", "content": "Say this is a test!"}]})
        if response.status_code == 200:
            return JSONResponse(response.json)

