import modal

app = modal.App("quantize-natlas")

# Create a volume to store the quantized model
output_vol = modal.Volume.from_name("quantized-models", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "llmcompressor",
        "transformers",
        "accelerate",
        "torch",
    )
)


@app.function(
    image=image,
    gpu="A100",
    timeout=30 * 60,
    volumes={"/output": output_vol},
    secrets=[modal.Secret.from_name("huggingface-secret")]  # Add this
)
def quantize():
    import os
    from huggingface_hub import login
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from llmcompressor import oneshot
    from llmcompressor.modifiers.quantization import QuantizationModifier

    login(token=os.environ["HF_TOKEN"])

    MODEL_ID = "NCAIR1/N-ATLaS"
    SAVE_DIR = "/output/N-ATLaS-FP8"

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto",
        torch_dtype="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    recipe = QuantizationModifier(
        targets="Linear",
        scheme="FP8_DYNAMIC",
        ignore=["lm_head"]
    )

    # Pass output_dir directly to oneshot
    oneshot(
        model=model,
        recipe=recipe,
        output_dir=SAVE_DIR
    )

    # Still need to save tokenizer separately
    tokenizer.save_pretrained(SAVE_DIR)

    # Commit the volume so files persist
    output_vol.commit()

    return "Done! Model saved to volume."

@app.local_entrypoint()
def main():
    result = quantize.remote()
    print(result)