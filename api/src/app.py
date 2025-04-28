from fastapi import FastAPI
from api.src.api_router import api_router

def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    app.include_router(api_router)
    return app