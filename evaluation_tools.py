"""
Manual & auto-evaluation logic for LLM responses
"""
import pandas as pd
from prompt_logger import LOG_FILE

def manual_evaluate(prompt, response, latency, model_version, prompt_template, user_feedback, hallucination):
    df = pd.read_csv(LOG_FILE)
    idx = df[(df["prompt"]==prompt) & (df["response"]==response) & (df["latency"]==float(latency))].index
    if len(idx) > 0:
        df.loc[idx[-1], ["user_feedback","hallucination"]] = [user_feedback, hallucination]
        df.to_csv(LOG_FILE, index=False)

def get_aggregate_stats(df):
    total = len(df)
    up = (df["user_feedback"]=="👍").sum()
    down = (df["user_feedback"]=="👎").sum()
    halluc = df["hallucination"].sum() if "hallucination" in df else 0
    avg_latency = df["latency"].mean() if total > 0 else 0
    return {
        "total": total,
        "thumbs_up": up,
        "thumbs_down": down,
        "hallucinations": halluc,
        "avg_latency": avg_latency
    }
