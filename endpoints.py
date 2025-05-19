from enum import StrEnum

from settings import AppSettings

app_settings = AppSettings()

class Endpoints(StrEnum):
    API_CHAT = f"{app_settings.API_HOST}/api/v1/chat/"
    UPLOAD = f"{app_settings.API_HOST}/api/v1/chat/file/"
    LLM_COMPLETIONS = f"{app_settings.LLM_HOST}/v1/chat/completions"
    UI = f"{app_settings.UI_HOST}/"