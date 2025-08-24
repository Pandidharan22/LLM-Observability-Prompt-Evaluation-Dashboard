"""
Functions for metric visualization (plots)
"""
import matplotlib.pyplot as plt
import pandas as pd

def plot_metrics(df):
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    # Thumbs up/down
    thumbs = df["user_feedback"].value_counts()
    axs[0].bar(thumbs.index.astype(str), thumbs.values, color=["green" if x=="👍" else "red" for x in thumbs.index])
    axs[0].set_title("Feedback")
    # Hallucinations
    axs[1].bar(["Hallucinations"], [df["hallucination"].sum()])
    axs[1].set_title("Hallucinations")
    # Latency
    axs[2].plot(df["latency"])
    axs[2].set_title("Latency Trend")
    plt.tight_layout()
    return fig