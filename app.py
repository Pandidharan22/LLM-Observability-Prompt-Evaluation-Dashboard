"""
Main Gradio app/dashboard for LLM Observability & Prompt Evaluation
"""
import gradio as gr
from llm_interface import generate_llm_response
from prompt_logger import log_prompt_response, get_log_df
from evaluation_tools import manual_evaluate, get_aggregate_stats
from plots import plot_metrics
import time

# Load logs for stats and plots
log_df = get_log_df()

with gr.Blocks() as demo:
    gr.Markdown("# LLM Observability & Prompt Evaluation Dashboard")
    with gr.Row():
        prompt = gr.Textbox(label="Prompt", lines=2)
        prompt_template = gr.Textbox(label="Prompt Template", value="Default", lines=1)
        model_version = gr.Textbox(label="Model Version", value="meta-llama/Meta-Llama-3-8B-Instruct", lines=1)
    with gr.Row():
        submit_btn = gr.Button("Submit")
        response = gr.Textbox(label="LLM Response", lines=4)
    with gr.Row():
        thumbs = gr.Radio(["👍", "👎"], label="Feedback")
        hallucination = gr.Checkbox(label="Hallucination?")
        latency_box = gr.Textbox(label="Latency (s)", interactive=False)
    with gr.Row():
        plot = gr.Plot(label="Evaluation Metrics")

    def handle_submit(prompt, prompt_template, model_version):
        start = time.time()
        llm_response = generate_llm_response(prompt, model_version)
        latency = round(time.time() - start, 3)
        log_prompt_response(prompt, llm_response, latency, model_version, prompt_template)
        return llm_response, latency

    def handle_feedback(prompt, response, latency, model_version, prompt_template, thumbs, hallucination):
        manual_evaluate(prompt, response, latency, model_version, prompt_template, thumbs, hallucination)
        global log_df
        log_df = get_log_df()
        fig = plot_metrics(log_df)
        return fig

    submit_btn.click(handle_submit, inputs=[prompt, prompt_template, model_version], outputs=[response, latency_box])
    thumbs.change(handle_feedback, inputs=[prompt, response, latency_box, model_version, prompt_template, thumbs, hallucination], outputs=[plot])

demo.launch()
