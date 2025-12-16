import json
from typing import Any

import aiohttp
import modal

vllm_image = (
    modal.Image.from_registry("nvidia/cuda:12.8.0-devel-ubuntu22.04", add_python="3.12")
    .entrypoint([])
    .uv_pip_install(
        "vllm==0.11.2",
        "huggingface-hub==0.36.0",
        "flashinfer-python==0.5.2",
    )
    .env({"HF_XET_HIGH_PERFORMANCE": "1"})
)

# Local path in the volume
MODEL_PATH = "/models/N-ATLaS-FP8"
MODEL_NAME = "n-atlas"  # What clients will use to reference it

# Mount your quantized model volume
model_vol = modal.Volume.from_name("quantized-models")
vllm_cache_vol = modal.Volume.from_name("vllm-cache", create_if_missing=True)

FAST_BOOT = True

app = modal.App("natlas-vllm")

N_GPU = 1
MINUTES = 60
VLLM_PORT = 8000


@app.function(
    image=vllm_image,
    gpu=f"H100:{N_GPU}",
    scaledown_window=15 * MINUTES,
    timeout=10 * MINUTES,
    volumes={
        "/models": model_vol,  # Your quantized model
        "/root/.cache/vllm": vllm_cache_vol,
    },
)
@modal.concurrent(max_inputs=32)
@modal.web_server(port=VLLM_PORT, startup_timeout=10 * MINUTES)
def serve():
    import subprocess

    cmd = [
        "vllm",
        "serve",
        MODEL_PATH,  # Local path instead of HF repo
        "--served-model-name", MODEL_NAME,
        "--host", "0.0.0.0",
        "--port", str(VLLM_PORT),
        "--uvicorn-log-level=info",
    ]

    cmd += ["--enforce-eager" if FAST_BOOT else "--no-enforce-eager"]
    cmd += ["--tensor-parallel-size", str(N_GPU)]

    print(cmd)
    subprocess.Popen(" ".join(cmd), shell=True)