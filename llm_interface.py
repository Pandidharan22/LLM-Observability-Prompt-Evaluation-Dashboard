"""
Meta Llama inference using Hugging Face Transformers
"""
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

def generate_llm_response(prompt, model_version="gpt2"):
    # Use InferenceClient for hosted inference
    client = InferenceClient(api_key=HF_TOKEN)
    # For chat models, use chat.completions.create; for others, use text_generation
    if "llama" in model_version or "chat" in model_version:
        messages = [
            {"role": "user", "content": prompt}
        ]
        completion = client.chat.completions.create(
            model=model_version,
            messages=messages,
        )
        return completion.choices[0].message.content
    else:
        # For non-chat models like gpt2
        return client.text_generation(prompt, model=model_version, max_new_tokens=256)
