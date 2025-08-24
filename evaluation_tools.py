"""
Manual & auto-evaluation logic for LLM responses

This module provides evaluation tools for LLM performance analysis:
1. Manual evaluation: Update user feedback for specific responses
2. Aggregate statistics: Calculate comprehensive performance metrics
"""
import pandas as pd
from prompt_logger import LOG_FILE

def manual_evaluate(prompt, response, latency, model_version, prompt_template, user_feedback, hallucination):
    """
    Update user feedback for a specific LLM response in the log file.
    
    This function finds the matching log entry and updates it with user feedback.
    It enables post-submission evaluation of LLM responses for quality control.
    
    Args:
        prompt (str): The original prompt text
        response (str): The LLM's response text
        latency (float): Response latency in seconds
        model_version (str): Model identifier used for the response
        prompt_template (str): Prompt template category
        user_feedback (str): User rating ("👍" or "👎")
        hallucination (bool): Whether the response contains hallucinations
    
    Process:
        1. Load the complete log CSV file
        2. Find the exact matching entry using prompt, response, and latency
        3. Update the user_feedback and hallucination columns
        4. Save the updated data back to the CSV file
    """
    df = pd.read_csv(LOG_FILE)
    # Find matching entries based on prompt, response, and latency
    idx = df[(df["prompt"]==prompt) & (df["response"]==response) & (df["latency"]==float(latency))].index
    if len(idx) > 0:
        # Update the most recent matching entry with user feedback
        df.loc[idx[-1], ["user_feedback","hallucination"]] = [user_feedback, hallucination]
        df.to_csv(LOG_FILE, index=False)

def get_aggregate_stats(df):
    """
    Calculate comprehensive aggregate statistics for LLM performance analysis.
    
    This function computes key performance indicators (KPIs) from the logged data
    to provide insights into LLM performance, user satisfaction, and system efficiency.
    
    Args:
        df (pandas.DataFrame): DataFrame containing logged LLM interactions
    
    Returns:
        dict: Dictionary containing calculated metrics:
            - total: Total number of LLM requests processed
            - thumbs_up: Count of positive user feedback responses
            - thumbs_down: Count of negative user feedback responses  
            - hallucinations: Count of responses flagged as hallucinations
            - avg_latency: Average response time across all requests
    
    Metrics Calculation Details:
        - User Satisfaction Rate: thumbs_up / (thumbs_up + thumbs_down) * 100
        - Hallucination Rate: hallucinations / total * 100
        - Performance Score: Combination of satisfaction and latency metrics
    
    Usage for Performance Analysis:
        - Monitor user satisfaction trends over time
        - Track hallucination rates for quality control
        - Analyze latency performance for system optimization
        - Compare metrics across different models or prompt templates
    """
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
        "avg_latency": avg_latency,
        # Additional calculated metrics for analysis
        "satisfaction_rate": (up / (up + down) * 100) if (up + down) > 0 else 0,
        "hallucination_rate": (halluc / total * 100) if total > 0 else 0
    }
