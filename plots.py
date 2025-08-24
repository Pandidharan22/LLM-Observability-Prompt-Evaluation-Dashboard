"""
Functions for metric visualization (plots)

This module creates real-time visualizations for LLM performance monitoring.
It provides three key charts that help analyze different aspects of LLM performance:
1. User feedback distribution (satisfaction metrics)
2. Hallucination detection (quality control metrics)  
3. Latency trends (performance metrics)
"""
import matplotlib.pyplot as plt
import pandas as pd

def plot_metrics(df):
    """
    Generate comprehensive LLM performance visualizations from logged data.
    
    Creates a three-panel dashboard showing key performance indicators:
    - User satisfaction distribution
    - Quality control metrics (hallucinations)
    - System performance trends (latency)
    
    Args:
        df (pandas.DataFrame): DataFrame containing logged LLM interactions with columns:
            - user_feedback: User ratings ("👍" or "👎")
            - hallucination: Boolean flags for hallucinated responses
            - latency: Response times in seconds
    
    Returns:
        matplotlib.figure.Figure: Multi-panel figure with three subplots
    
    Chart Details:
        1. Feedback Distribution (Bar Chart):
           - Shows thumbs up vs thumbs down counts
           - Green bars for positive feedback, red for negative
           - Helps assess overall user satisfaction
           
        2. Hallucination Count (Bar Chart):
           - Total count of responses flagged as hallucinations
           - Critical quality control metric
           - Helps identify model reliability issues
           
        3. Latency Trend (Line Chart):
           - Response time progression over requests
           - Helps identify performance bottlenecks
           - Shows system efficiency trends
    
    Usage for Performance Analysis:
        - Monitor user satisfaction trends (feedback chart)
        - Track quality degradation (hallucination chart)
        - Identify performance issues (latency chart)
        - Compare metrics before/after model changes
        - Generate reports for stakeholders
    """
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    
    # Chart 1: User Feedback Distribution
    # Analyzes user satisfaction with thumbs up/down counts
    thumbs = df["user_feedback"].value_counts()
    if not thumbs.empty:
        # Use text labels instead of emoji to avoid font issues
        labels = ["Positive" if x=="👍" else "Negative" for x in thumbs.index]
        colors = ["green" if x=="👍" else "red" for x in thumbs.index]
        axs[0].bar(labels, thumbs.values, color=colors)
        axs[0].set_title("User Feedback Distribution")
        axs[0].set_ylabel("Count")
        # Add satisfaction rate as text
        total_feedback = thumbs.sum()
        thumbs_up = thumbs.get("👍", 0)
        satisfaction_rate = (thumbs_up / total_feedback * 100) if total_feedback > 0 else 0
        axs[0].text(0.5, 0.95, f'Satisfaction: {satisfaction_rate:.1f}%', 
                   transform=axs[0].transAxes, ha='center', va='top')
    else:
        axs[0].set_title("User Feedback Distribution\n(No data)")
        axs[0].set_ylabel("Count")
    
    # Chart 2: Hallucination Detection
    # Quality control metric for response accuracy
    halluc_count = df["hallucination"].sum() if "hallucination" in df.columns else 0
    total_responses = len(df)
    halluc_rate = (halluc_count / total_responses * 100) if total_responses > 0 else 0
    
    axs[1].bar(["Hallucinations"], [halluc_count], color='orange')
    axs[1].set_title("Quality Control")
    axs[1].set_ylabel("Count")
    # Add hallucination rate as text
    axs[1].text(0.5, 0.95, f'Rate: {halluc_rate:.1f}%', 
               transform=axs[1].transAxes, ha='center', va='top')
    
    # Chart 3: Latency Performance Trend
    # System performance monitoring over time
    if not df.empty and "latency" in df.columns:
        latencies = df["latency"].reset_index(drop=True)
        axs[2].plot(latencies, color='blue', linewidth=2)
        axs[2].set_title("Response Latency Trend")
        axs[2].set_xlabel("Request Number")
        axs[2].set_ylabel("Latency (seconds)")
        # Add average latency as text
        avg_latency = latencies.mean()
        axs[2].text(0.5, 0.95, f'Avg: {avg_latency:.2f}s', 
                   transform=axs[2].transAxes, ha='center', va='top')
        # Add trend line if enough data points
        if len(latencies) > 5:
            z = np.polyfit(range(len(latencies)), latencies, 1)
            p = np.poly1d(z)
            axs[2].plot(range(len(latencies)), p(range(len(latencies))), 
                       "r--", alpha=0.8, linewidth=1, label='Trend')
    else:
        axs[2].set_title("Response Latency Trend\n(No data)")
    
    plt.tight_layout()
    return fig

# Import numpy for trend analysis
try:
    import numpy as np
except ImportError:
    # Fallback if numpy is not available
    def plot_metrics(df):
        fig, axs = plt.subplots(1, 3, figsize=(12, 4))
        
        # Simplified version without trend analysis
        thumbs = df["user_feedback"].value_counts()
        if not thumbs.empty:
            axs[0].bar(thumbs.index.astype(str), thumbs.values, 
                      color=["green" if x=="👍" else "red" for x in thumbs.index])
        axs[0].set_title("Feedback")
        
        halluc_count = df["hallucination"].sum() if "hallucination" in df.columns else 0
        axs[1].bar(["Hallucinations"], [halluc_count])
        axs[1].set_title("Hallucinations")
        
        if not df.empty and "latency" in df.columns:
            axs[2].plot(df["latency"])
        axs[2].set_title("Latency Trend")
        
        plt.tight_layout()
        return fig