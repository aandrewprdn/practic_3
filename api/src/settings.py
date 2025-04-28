from pydantic_settings import BaseSettings
from typing import Annotated
from pydantic import Field

class AppSettings(BaseSettings):
    PORT: Annotated[str, Field()]
    LLM_HOST: Annotated[str, Field()]
