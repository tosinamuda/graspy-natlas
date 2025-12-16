import gradio as gr
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

REPO_ID = "tosinamuda/N-ATLaS-GGUF"
FILENAME = "Q4_K_M.gguf"

model_path = hf_hub_download(
    repo_id=REPO_ID,
    filename=FILENAME,
)

llm = Llama(
    model_path=model_path,
    n_ctx=4096,
    n_threads=8,   # tune this down if Space has fewer cores
)

def chat(message, history):
    history = history or []
    prompt = ""
    for user, bot in history:
        prompt += f"User: {user}\nAssistant: {bot}\n"
    prompt += f"User: {message}\nAssistant:"

    out = llm(
        prompt,
        max_tokens=256,
        temperature=0.7,
        stop=["User:", "Assistant:"],
    )
    reply = out["choices"][0]["text"].strip()
    history.append((message, reply))
    return "", history

with gr.Blocks() as demo:
    gr.Markdown("# N-ATLaS GGUF (Q4) chat")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Message")
    msg.submit(chat, [msg, chatbot], [msg, chatbot])

demo.launch()
