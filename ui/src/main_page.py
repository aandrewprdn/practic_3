import logging
import uuid

import gradio as gr
from httpx import AsyncClient

ui_logger = logging.getLogger("ui")

async def answer(content, history, request: gr.Request):
    ui_logger.debug(f"History: {history}")
    ui_logger.debug(f"Content: {content}")
    ui_logger.debug(f"Session: {request.session_hash}")

    if len(history):
        history.append({"id": uuid.uuid4()})

    api_endpoint = "/"
    model = {"content": content["text"], "session_hash": request.session_hash}
    if len(content["files"]) > 0:
        api_endpoint = "/file/"
        model = {"file": content["files"], "session_hash": request.session_hash}

    async with AsyncClient() as client:
        res = await client.post(f"http://127.0.0.1:3000/api/v1/chat{api_endpoint}", json=model, timeout=10)
        msg: str = res.json()["response"]
        return msg



demo = gr.ChatInterface(
        answer,
        textbox=gr.MultimodalTextbox(
            interactive=True,
            file_count="single",
            placeholder="Enter message or upload file...",
            show_label=False,
            sources=["upload"],
        ),
        type="messages",
        title="AI chatbot",
        description="Ask whatever you want",
        multimodal=False,
    )
