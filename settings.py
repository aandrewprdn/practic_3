from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated
from pydantic import Field

load_dotenv(find_dotenv(".env"))


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    LLM_HOST: str = Field()
    UI_HOST: str = Field()
    API_HOST: Annotated[str, "Host for API server"]
