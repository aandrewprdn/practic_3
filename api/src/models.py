from typing import Annotated

from pydantic import BaseModel, Field


class ContentRequest(BaseModel):
    content: Annotated[str, Field()]