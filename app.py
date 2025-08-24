"""
Main Gradio app/dashboard for LLM Observability & Prompt Evaluation

This is the core application that provides an interactive web interface for:
- Real-time LLM testing and evaluation
- Performance monitoring and metrics collection
- User feedback collection and analysis
- Visual analytics dashboard

Architecture:
1. Gradio web interface for user interaction
2. Real-time LLM inference with latency measurement
3. Comprehensive logging of all interactions
4. Dynamic visualization updates based on user feedback
5. Performance analytics and trend monitoring

Usage:
    python app.py
    
    Then open the provided URL (typically http://localhost:7860) to access the dashboard.
"""
import gradio as gr
from llm_interface import generate_llm_response
from prompt_logger import log_prompt_response, get_log_df
from evaluation_tools import manual_evaluate, get_aggregate_stats
from plots import plot_metrics
import time

# Initialize with existing log data for immediate analytics
log_df = get_log_df()

# Create the main Gradio application interface
with gr.Blocks() as demo:
    gr.Markdown("# LLM Observability & Prompt Evaluation Dashboard")
    gr.Markdown("""
    **Test LLM responses, provide feedback, and monitor performance metrics in real-time.**
    
    📊 **Features**: Latency tracking • User feedback collection • Hallucination detection • Performance analytics
    """)
    
    # Input Section: Prompt configuration and model selection
    with gr.Row():
        prompt = gr.Textbox(
            label="Prompt", 
            lines=2, 
            placeholder="Enter your prompt here...",
            info="The text prompt to send to the LLM"
        )
        prompt_template = gr.Textbox(
            label="Prompt Template", 
            value="Default", 
            lines=1,
            info="Category or template type for organization"
        )
        model_version = gr.Textbox(
            label="Model Version", 
            value="meta-llama/Meta-Llama-3-8B-Instruct", 
            lines=1,
            info="Hugging Face model identifier"
        )
    
    # Response Section: LLM output and action buttons
    with gr.Row():
        submit_btn = gr.Button("Submit", variant="primary")
        response = gr.Textbox(
            label="LLM Response", 
            lines=4, 
            interactive=False,
            info="Generated response from the LLM"
        )
    
    # Evaluation Section: User feedback and quality assessment
    with gr.Row():
        thumbs = gr.Radio(
            ["👍", "👎"], 
            label="Response Quality",
            info="Rate the quality of the LLM response"
        )
        hallucination = gr.Checkbox(
            label="Hallucination Detected?",
            info="Check if the response contains false or fabricated information"
        )
        latency_box = gr.Textbox(
            label="Response Latency (seconds)", 
            interactive=False,
            info="Time taken to generate the response"
        )
    
    # Analytics Section: Real-time performance visualization
    with gr.Row():
        plot = gr.Plot(label="Performance Analytics Dashboard")

    def handle_submit(prompt, prompt_template, model_version):
        """
        Process LLM inference request with performance monitoring.
        
        This function handles the core workflow:
        1. Measures latency by timing the LLM API call
        2. Generates response using the specified model
        3. Logs the interaction for analytics
        4. Returns response and latency for display
        
        Args:
            prompt (str): User's input prompt
            prompt_template (str): Template category for organization
            model_version (str): Model identifier for inference
            
        Returns:
            tuple: (llm_response, latency) for UI display
            
        Performance Tracking:
            - Precise latency measurement using time.time()
            - Automatic logging of all request metadata
            - Error handling for failed requests
        """
        if not prompt.strip():
            return "Please enter a prompt.", 0
            
        try:
            # Measure response latency with high precision
            start = time.time()
            llm_response = generate_llm_response(prompt, model_version)
            latency = round(time.time() - start, 3)
            
            # Log the interaction for analytics and tracking
            log_prompt_response(prompt, llm_response, latency, model_version, prompt_template)
            
            return llm_response, latency
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            # Log errors for debugging
            log_prompt_response(prompt, error_msg, 0, model_version, prompt_template)
            return error_msg, 0

    def handle_feedback(prompt, response, latency, model_version, prompt_template, thumbs, hallucination):
        """
        Process user feedback and update analytics dashboard.
        
        This function manages the evaluation workflow:
        1. Updates the log entry with user feedback
        2. Refreshes the analytics data
        3. Generates updated visualization charts
        4. Returns new plots for real-time dashboard updates
        
        Args:
            prompt (str): Original prompt text
            response (str): LLM's response text
            latency (str): Response latency in seconds
            model_version (str): Model used for generation
            prompt_template (str): Template category
            thumbs (str): User rating ("👍" or "👎")
            hallucination (bool): Hallucination detection flag
            
        Returns:
            matplotlib.figure.Figure: Updated analytics dashboard
            
        Analytics Updates:
            - Real-time metric recalculation
            - Dynamic chart updates
            - Performance trend analysis
        """
        global log_df
        
        if not thumbs:
            # Return current plot if no feedback provided
            return plot_metrics(log_df)
            
        try:
            # Update the log entry with user evaluation
            manual_evaluate(prompt, response, latency, model_version, prompt_template, thumbs, hallucination)
            
            # Refresh analytics data for updated visualizations
            log_df = get_log_df()
            
            # Generate updated performance dashboard
            fig = plot_metrics(log_df)
            return fig
            
        except Exception as e:
            print(f"Error processing feedback: {e}")
            # Return current plot on error
            return plot_metrics(log_df)

    # Wire up the interactive components
    # Submit button triggers LLM inference and latency measurement
    submit_btn.click(
        handle_submit, 
        inputs=[prompt, prompt_template, model_version], 
        outputs=[response, latency_box]
    )
    
    # Feedback changes trigger analytics updates and chart refresh
    thumbs.change(
        handle_feedback, 
        inputs=[prompt, response, latency_box, model_version, prompt_template, thumbs, hallucination], 
        outputs=[plot]
    )
    
    # Initialize the dashboard with existing data
    demo.load(lambda: plot_metrics(log_df), outputs=[plot])

# Launch the application
if __name__ == "__main__":
    demo.launch(
        share=False,  # Set to True to create public link
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,  # Default Gradio port
        show_error=True  # Show detailed error messages
    )
