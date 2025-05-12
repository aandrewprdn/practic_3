from enum import StrEnum

from settings import AppSettings


class Endpoints(StrEnum):
    API_CHAT = f"{AppSettings().API_HOST}/api/v1/chat/"
    LLM_COMPLETIONS = f"{AppSettings().LLM_HOST}/v1/chat/completions"
    UI = f"{AppSettings().UI_HOST}/"