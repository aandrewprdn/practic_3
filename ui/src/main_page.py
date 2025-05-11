import gradio as gr

def answer(message, _):
    return f"Hello {message}"

demo = gr.ChatInterface(
    answer,
    type="messages",
    title="AI chatbot",
    description="Ask whatever you want",
    multimodal=False
)
