from typing import Annotated

from pydantic import BaseModel, Field

class BaseRequest(BaseModel):
    session_hash: Annotated[str, Field()]

class ContentRequest(BaseRequest):
    content: Annotated[str, Field()]

class RagFileRequest(BaseRequest):
    file: Annotated[str, Field()]

class Message(BaseModel):
    role: str = Field(default="user")
    content: str = Field()

class LLMRequest(BaseModel):
    model: str = Field(default="gemma-3-1b-it-qat")
    messages: list[Message] = Field(default_factory=list)
    temperature: float = Field(default=0.7)
    stream: bool =  False


