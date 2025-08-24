# LLM Observability & Prompt Evaluation Dashboard

A comprehensive LLMOps tool for monitoring, evaluating, and analyzing Large Language Model (LLM) performance through an interactive web dashboard built with Gradio.

## 🎯 Project Purpose

This dashboard provides real-time observability and evaluation capabilities for LLM applications, enabling data scientists and ML engineers to:

- **Monitor LLM Performance**: Track response quality, latency, and user satisfaction metrics
- **Evaluate Prompts**: Test different prompts and templates to optimize LLM outputs
- **Detect Issues**: Identify hallucinations and poor responses through user feedback
- **Analyze Trends**: Visualize performance metrics over time for continuous improvement
- **Compare Models**: Test different model versions and configurations

## 🚀 Key Features

### 1. **Interactive Testing Interface**
- Real-time prompt testing with immediate LLM responses
- Support for multiple model versions (Meta-Llama, GPT-2, etc.)
- Customizable prompt templates for categorization
- Instant latency measurement and display

### 2. **Comprehensive Logging System**
- Automatic logging of all prompts, responses, and metadata
- CSV-based storage with timestamps for easy analysis
- Version tracking for models and prompt templates
- Persistent storage of evaluation data

### 3. **User Feedback Collection**
- Thumbs up/down rating system for response quality
- Hallucination detection checkboxes for quality control
- Manual evaluation capabilities for fine-grained assessment
- Real-time feedback integration with analytics

### 4. **Performance Analytics & Visualization**
- Live metrics dashboard with three key visualizations:
  - **Feedback Distribution**: Bar chart showing thumbs up vs. thumbs down
  - **Hallucination Count**: Track detected hallucinations over time
  - **Latency Trends**: Line chart monitoring response time performance
- Aggregate statistics including total requests, satisfaction rates, and average latency

## 🏗️ Architecture & Components

### Core Modules

#### 1. **Dashboard Interface (`app.py`)**
```python
# Main Gradio application providing:
- Interactive web interface for LLM testing
- Real-time metric updates and visualization
- User feedback collection and processing
- Session management and data handling
```

#### 2. **LLM Interface (`llm_interface.py`)**
```python
# Hugging Face integration for LLM inference:
- Support for chat models (Llama, ChatGPT-style models)
- Support for text generation models (GPT-2, etc.)
- Environment-based API key management
- Flexible model switching capabilities
```

#### 3. **Logging System (`prompt_logger.py`)**
```python
# Comprehensive data logging:
- CSV-based storage in 'prompt_logs.csv'
- Automatic timestamp recording
- Metadata tracking (model, template, feedback)
- Data retrieval functions for analytics
```

#### 4. **Evaluation Tools (`evaluation_tools.py`)**
```python
# Manual evaluation and statistics:
- Update user feedback post-submission
- Calculate aggregate performance metrics
- Generate summary statistics for analysis
```

#### 5. **Visualization (`plots.py`)**
```python
# Real-time metric visualization:
- Matplotlib-based charts and graphs
- Dynamic updates based on user feedback
- Multiple chart types for different metrics
```

## 📊 Metrics & Calculations

### Performance Metrics

#### **Latency Measurement**
```python
# Precise timing around LLM API calls
start = time.time()
llm_response = generate_llm_response(prompt, model_version)
latency = round(time.time() - start, 3)  # Millisecond precision
```

#### **User Satisfaction Metrics**
- **Thumbs Up Rate**: `thumbs_up_count / total_responses * 100`
- **Thumbs Down Rate**: `thumbs_down_count / total_responses * 100`
- **Response Quality Score**: Based on user feedback distribution

#### **Quality Assurance Metrics**
- **Hallucination Rate**: `hallucination_count / total_responses * 100`
- **Error Detection**: Manual flagging of problematic responses
- **Response Accuracy**: User-validated quality assessments

#### **Usage Analytics**
- **Total Requests**: Complete count of processed prompts
- **Average Latency**: `sum(all_latencies) / total_requests`
- **Model Performance**: Comparative analysis across different models
- **Template Effectiveness**: Performance breakdown by prompt template

### Data Schema
```csv
timestamp,prompt,response,latency,model_version,prompt_template,user_feedback,hallucination
1756023720.27,"What is AI?","AI is...",2.15,"meta-llama/Meta-Llama-3-8B","Default","👍",False
```

## 🔧 How to Use for Efficient LLM Performance Analysis

### 1. **Setup and Installation**

```bash
# Clone the repository
git clone https://github.com/Pandidharan22/LLM-Observability-Prompt-Evaluation-Dashboard.git
cd LLM-Observability-Prompt-Evaluation-Dashboard

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "HF_TOKEN=your_huggingface_token" > .env
```

### 2. **Launch the Dashboard**

```bash
python app.py
```

The dashboard will be available at `http://localhost:7860` (or the URL shown in terminal).

### 3. **Performance Analysis Workflow**

#### **Step 1: Baseline Testing**
1. **Set up test prompts**: Create a diverse set of prompts covering your use cases
2. **Test with default model**: Run prompts through your primary model
3. **Collect initial metrics**: Gather latency and quality baselines

#### **Step 2: Systematic Evaluation**
1. **Use consistent prompt templates**: Categorize prompts by use case
2. **Provide feedback**: Rate every response for accuracy
3. **Flag issues**: Mark hallucinations and poor responses
4. **Monitor trends**: Watch for performance degradation over time

#### **Step 3: Model Comparison**
1. **Test multiple models**: Compare different model versions
2. **Analyze trade-offs**: Balance latency vs. quality
3. **Identify optimal configurations**: Find best model for each use case

#### **Step 4: Optimization**
1. **Refine prompts**: Improve low-performing prompts based on feedback
2. **Template optimization**: Develop better prompt templates
3. **Performance tuning**: Adjust model parameters based on metrics

### 4. **Best Practices for Analysis**

#### **Data Collection**
- **Consistent testing conditions**: Use similar prompts across models
- **Sufficient sample size**: Collect enough data for statistical significance
- **Diverse prompt sets**: Test edge cases and typical use cases
- **Regular evaluation**: Provide feedback on all responses

#### **Metric Interpretation**
- **Latency analysis**: Monitor for performance regressions
- **Quality trends**: Track satisfaction rates over time
- **Hallucination monitoring**: Identify problematic patterns
- **Usage patterns**: Understand which templates work best

#### **Continuous Improvement**
- **Regular reviews**: Analyze metrics weekly/monthly
- **A/B testing**: Compare different approaches systematically
- **Documentation**: Keep notes on what works and what doesn't
- **Iteration**: Continuously refine based on data insights

### 5. **Advanced Analysis Techniques**

#### **Export Data for Deep Analysis**
```python
import pandas as pd

# Load the log data
df = pd.read_csv('prompt_logs.csv')

# Advanced analytics
latency_by_model = df.groupby('model_version')['latency'].agg(['mean', 'std', 'count'])
satisfaction_by_template = df.groupby('prompt_template')['user_feedback'].value_counts()
```

#### **Performance Monitoring**
- **Set up alerts**: Monitor for unusual latency spikes
- **Track trends**: Identify gradual performance changes
- **Quality assurance**: Regular review of flagged responses
- **Capacity planning**: Understand usage patterns for scaling

## 🛠️ Configuration

### Environment Variables
```bash
HF_TOKEN=your_huggingface_api_token  # Required for model inference
```

### Supported Models
- **Chat Models**: Meta-Llama-3-8B-Instruct, GPT-style chat models
- **Text Generation**: GPT-2, other causal language models
- **Custom Models**: Any Hugging Face hosted model

### Data Storage
- **Log File**: `prompt_logs.csv` (automatically created)
- **Format**: CSV with comprehensive metadata
- **Backup**: Recommended to backup logs regularly

## 📈 Use Cases

### **1. Model Selection & Evaluation**
- Compare response quality across different models
- Analyze latency vs. quality trade-offs
- Identify the best model for specific use cases

### **2. Prompt Engineering**
- Test prompt variations systematically
- Optimize prompts for better responses
- Track prompt template effectiveness

### **3. Quality Assurance**
- Monitor for hallucinations and errors
- Collect user feedback for continuous improvement
- Identify problematic response patterns

### **4. Performance Monitoring**
- Track system performance over time
- Identify performance bottlenecks
- Monitor for degradation or improvements

### **5. User Experience Optimization**
- Understand user satisfaction patterns
- Optimize for better user experience
- Balance performance with quality

## 🤝 Contributing

This project provides a solid foundation for LLM observability. Potential enhancements include:
- Advanced analytics and reporting
- Integration with other LLM platforms
- Automated testing capabilities
- Enhanced visualization options
- Multi-user collaboration features

## 📄 License

MIT License - see LICENSE file for details.