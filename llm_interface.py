"""
Meta Llama inference using Hugging Face Transformers

This module provides a unified interface for LLM inference across different model types:
- Chat-based models (Meta-Llama, ChatGPT-style models)
- Text generation models (GPT-2, traditional language models)
- Hosted inference via Hugging Face API

Features:
- Automatic model type detection and appropriate API selection
- Environment-based API token management for security
- Error handling and fallback mechanisms
- Flexible model switching capabilities

Usage:
    Set HF_TOKEN environment variable with your Hugging Face API token
    Call generate_llm_response(prompt, model_version) for inference
"""
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

def generate_llm_response(prompt, model_version="gpt2"):
    """
    Generate LLM response using Hugging Face hosted inference.
    
    This function automatically detects the model type and uses the appropriate
    API endpoint for optimal performance and compatibility.
    
    Args:
        prompt (str): Input text prompt for the LLM
        model_version (str): Hugging Face model identifier
            Examples:
            - "meta-llama/Meta-Llama-3-8B-Instruct" (chat model)
            - "gpt2" (text generation model)
            - "microsoft/DialoGPT-medium" (conversational model)
    
    Returns:
        str: Generated text response from the LLM
        
    Model Type Detection:
        - Chat models: Contains "llama" or "chat" in model name
          Uses chat.completions.create() API for structured conversations
        - Text generation: All other models
          Uses text_generation() API for continuation-based generation
          
    Error Handling:
        - Invalid API tokens
        - Model not found or unavailable
        - Rate limiting or quota exceeded
        - Network connectivity issues
        
    Performance Considerations:
        - Uses hosted inference for fast response times
        - No local model loading required
        - Automatic scaling based on demand
        - Shared compute resources across users
    """
    if not HF_TOKEN:
        return "Error: HF_TOKEN environment variable not set. Please add your Hugging Face API token to .env file."
    
    try:
        # Initialize Hugging Face Inference Client
        client = InferenceClient(api_key=HF_TOKEN)
        
        # Determine model type and use appropriate API
        if "llama" in model_version.lower() or "chat" in model_version.lower():
            # Chat-based models: Use structured conversation format
            messages = [
                {"role": "user", "content": prompt}
            ]
            completion = client.chat.completions.create(
                model=model_version,
                messages=messages,
                max_tokens=512,  # Limit response length
                temperature=0.7,  # Control randomness
            )
            return completion.choices[0].message.content
        else:
            # Text generation models: Use continuation-based generation
            response = client.text_generation(
                prompt, 
                model=model_version, 
                max_new_tokens=256,  # Limit new tokens
                temperature=0.7,  # Control randomness
                do_sample=True,  # Enable sampling
                return_full_text=False  # Return only generated text
            )
            return response
            
    except Exception as e:
        # Return informative error message for debugging
        error_msg = f"Error with model {model_version}: {str(e)}"
        print(f"LLM Interface Error: {error_msg}")
        return error_msg
