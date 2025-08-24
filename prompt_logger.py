"""
Prompt & response logging, metrics, and version tracking
"""
import time
import pandas as pd
import os

LOG_FILE = "prompt_logs.csv"

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["timestamp","prompt","response","latency","model_version","prompt_template","user_feedback","hallucination"]).to_csv(LOG_FILE, index=False)

def log_prompt_response(prompt, response, latency, model_version, prompt_template, user_feedback=None, hallucination=False):
    entry = {
        "timestamp": time.time(),
        "prompt": prompt,
        "response": response,
        "latency": latency,
        "model_version": model_version,
        "prompt_template": prompt_template,
        "user_feedback": user_feedback,
        "hallucination": hallucination
    }
    df = pd.read_csv(LOG_FILE)
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)

def get_log_df():
    return pd.read_csv(LOG_FILE)
