import gradio as gr
from httpx import AsyncClient


async def answer(content, _):
    async with AsyncClient() as client:
        res = await client.post(f"http://127.0.0.1:3000/api/v1/chat/", json={"content": content})
        msg: str = res.json()["choices"][0]["message"]["content"]
        return msg

demo = gr.ChatInterface(
    answer,
    type="messages",
    title="AI chatbot",
    description="Ask whatever you want",
    multimodal=False
)
