import modal

app = modal.App("push-natlas")

output_vol = modal.Volume.from_name("quantized-models")

image = modal.Image.debian_slim(python_version="3.11").pip_install("huggingface_hub")

@app.function(
    image=image,
    volumes={"/output": output_vol},
    secrets=[modal.Secret.from_name("huggingface-secret")],
    timeout=30 * 60  # upload might take a while
)
def push_to_hf():
    import os
    from huggingface_hub import HfApi, login

    login(token=os.environ["HF_TOKEN"])

    api = HfApi()
    api.create_repo("tosinamuda/N-ATLaS-FP8", exist_ok=True)
    api.upload_folder(
        folder_path="/output/N-ATLaS-FP8",
        repo_id="tosinamuda/N-ATLaS-FP8",
        repo_type="model"
    )
    return "Done! https://huggingface.co/tosinamuda/N-ATLaS-FP8"

@app.local_entrypoint()
def main():
    print(push_to_hf.remote())