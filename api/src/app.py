from fastapi import FastAPI
from api.src.api_router import api_router
from api.src.utils.logger import init_logger


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1",
                  redirect_slashes=False)
    app.include_router(api_router)
    init_logger()
    return app