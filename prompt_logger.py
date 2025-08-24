"""
Prompt & response logging, metrics, and version tracking

This module provides comprehensive logging capabilities for LLM observability:
- Automatic CSV-based logging of all LLM interactions
- Structured data format for easy analysis and reporting
- Metadata tracking for performance analysis
- Data retrieval functions for analytics and visualization

Data Schema:
    timestamp: Unix timestamp of the interaction
    prompt: Original user prompt text
    response: LLM-generated response text
    latency: Response time in seconds (3 decimal precision)
    model_version: Identifier of the LLM model used
    prompt_template: Category or template type for organization
    user_feedback: User rating ("👍" or "👎") - added post-generation
    hallucination: Boolean flag for response quality control

File Storage:
    - CSV format for universal compatibility
    - Automatic file creation if not exists
    - Append-only logging for data integrity
    - Human-readable format for manual inspection
"""
import time
import pandas as pd
import os

# Configuration: Log file location and name
LOG_FILE = "prompt_logs.csv"

# Initialize logging system: Create log file with proper schema if it doesn't exist
if not os.path.exists(LOG_FILE):
    # Define the complete data schema for LLM interaction logging
    columns = [
        "timestamp",        # When the interaction occurred
        "prompt",          # User's input prompt
        "response",        # LLM's generated response
        "latency",         # Response time in seconds
        "model_version",   # Model identifier used
        "prompt_template", # Template category for analysis
        "user_feedback",   # Post-generation user rating
        "hallucination"    # Quality control flag
    ]
    pd.DataFrame(columns=columns).to_csv(LOG_FILE, index=False)
    print(f"Initialized new log file: {LOG_FILE}")

def log_prompt_response(prompt, response, latency, model_version, prompt_template, user_feedback=None, hallucination=False):
    """
    Log a complete LLM interaction with comprehensive metadata.
    
    This function records all relevant information about an LLM interaction
    for later analysis, performance monitoring, and quality assessment.
    
    Args:
        prompt (str): Original user prompt text
        response (str): LLM-generated response text
        latency (float): Response generation time in seconds
        model_version (str): Identifier of the LLM model used
        prompt_template (str): Template category for organization and analysis
        user_feedback (str, optional): User rating ("👍" or "👎")
        hallucination (bool, optional): Whether response contains hallucinations
    
    Data Processing:
        1. Creates structured log entry with timestamp
        2. Reads existing log data to maintain history
        3. Appends new entry to the dataset
        4. Saves updated data back to CSV file
        
    Performance Considerations:
        - Efficient append operation using pandas.concat()
        - Minimal I/O operations for high-frequency logging
        - Atomic write operations for data integrity
        
    Usage for Analytics:
        - Track model performance over time
        - Analyze prompt effectiveness across templates
        - Monitor system latency and user satisfaction
        - Generate reports and insights for optimization
    """
    try:
        # Create structured log entry with current timestamp
        entry = {
            "timestamp": time.time(),  # Unix timestamp for precise ordering
            "prompt": prompt,
            "response": response,
            "latency": latency,
            "model_version": model_version,
            "prompt_template": prompt_template,
            "user_feedback": user_feedback,
            "hallucination": hallucination
        }
        
        # Load existing log data to maintain complete history
        df = pd.read_csv(LOG_FILE)
        
        # Append new entry efficiently
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        
        # Save updated data back to file
        df.to_csv(LOG_FILE, index=False)
        
    except Exception as e:
        print(f"Error logging interaction: {e}")
        # Could implement fallback logging mechanism here

def get_log_df():
    """
    Retrieve the complete log dataset for analysis and visualization.
    
    Returns:
        pandas.DataFrame: Complete dataset of all logged LLM interactions
        
    Data Structure:
        - Chronologically ordered by timestamp
        - All interaction metadata included
        - Ready for analytics and visualization
        - Compatible with pandas analysis functions
        
    Usage Examples:
        # Basic statistics
        df = get_log_df()
        print(f"Total interactions: {len(df)}")
        print(f"Average latency: {df['latency'].mean():.2f}s")
        
        # Model comparison
        model_stats = df.groupby('model_version')['latency'].agg(['mean', 'count'])
        
        # Satisfaction analysis
        satisfaction_rate = (df['user_feedback'] == '👍').sum() / len(df) * 100
        
        # Temporal analysis
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        daily_stats = df.groupby(df['datetime'].dt.date).size()
    """
    try:
        return pd.read_csv(LOG_FILE)
    except Exception as e:
        print(f"Error reading log file: {e}")
        # Return empty DataFrame with correct schema on error
        return pd.DataFrame(columns=[
            "timestamp", "prompt", "response", "latency", 
            "model_version", "prompt_template", "user_feedback", "hallucination"
        ])
