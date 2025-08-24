# LLM Performance Analysis Usage Guide

## Quick Start

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up your Hugging Face token
echo "HF_TOKEN=your_token_here" > .env

# Launch the dashboard
python app.py
```

### 2. Access the Dashboard
Open your browser to `http://localhost:7860`

## Efficient LLM Performance Analysis Workflow

### Phase 1: Baseline Establishment

#### Step 1: Create Test Prompt Sets
Organize your testing into categories:

**Example Prompt Templates:**
- `Classification` - Text classification tasks
- `QA` - Question answering scenarios  
- `Summarization` - Document summarization requests
- `Creative` - Creative writing prompts
- `Technical` - Code generation or technical explanations

#### Step 2: Initial Model Testing
1. Set **Model Version** to your primary model (e.g., `meta-llama/Meta-Llama-3-8B-Instruct`)
2. Set **Prompt Template** to categorize your test
3. Enter your **Prompt** and click **Submit**
4. Record the **latency** automatically displayed
5. Provide **feedback** (👍/👎) for every response
6. Mark **hallucinations** when detected

### Phase 2: Systematic Evaluation

#### Example Testing Session:
```
Prompt Template: "QA"
Prompt: "What are the benefits of renewable energy?"
Model: meta-llama/Meta-Llama-3-8B-Instruct

Response Generated → Review for:
✓ Accuracy of information
✓ Completeness of answer  
✓ Clarity and coherence
✓ Any factual errors (hallucinations)

Provide feedback immediately after each response.
```

#### Building Your Dataset:
- **Minimum 20 prompts** per template category
- **Diverse complexity levels** (simple to complex)
- **Edge cases** and problematic scenarios
- **Consistent evaluation criteria** across all tests

### Phase 3: Performance Analysis

#### Reading the Dashboard Metrics:

**1. User Feedback Distribution**
- **Green bars (👍)**: Successful responses
- **Red bars (👎)**: Poor quality responses  
- **Satisfaction Rate**: Percentage of positive feedback
- **Target**: >80% satisfaction for production models

**2. Quality Control (Hallucinations)**
- **Orange bar**: Count of hallucinated responses
- **Hallucination Rate**: Percentage of problematic responses
- **Target**: <5% hallucination rate for reliable models

**3. Latency Trend**
- **Blue line**: Response time progression
- **Trend line**: Performance trajectory over time
- **Average latency**: Mean response time
- **Target**: <3 seconds for interactive applications

### Phase 4: Model Comparison

#### A/B Testing Process:
1. **Test Model A** with your prompt set
2. **Record baseline metrics**:
   - Satisfaction rate: __%
   - Hallucination rate: __%  
   - Average latency: __s

3. **Switch to Model B** (change Model Version field)
4. **Test same prompts** with identical criteria
5. **Compare results** using the dashboard

#### Example Comparison:
```
Model A: meta-llama/Meta-Llama-3-8B-Instruct
- Satisfaction: 85%
- Hallucinations: 3%
- Avg Latency: 2.1s

Model B: gpt2
- Satisfaction: 62%  
- Hallucinations: 12%
- Avg Latency: 0.8s

Decision: Model A provides better quality despite higher latency
```

### Phase 5: Optimization & Monitoring

#### Prompt Engineering:
1. **Identify low-performing prompts** (👎 responses)
2. **Refine prompt wording** and test variations
3. **Use effective prompt templates** that show high success rates
4. **Document successful patterns** for reuse

#### Ongoing Monitoring:
- **Daily checks**: Review new interactions and metrics
- **Weekly analysis**: Trend analysis and performance reports
- **Monthly reviews**: Model performance evaluation and optimization

## Advanced Analytics

### Exporting Data for Analysis:
```python
import pandas as pd

# Load the complete dataset
df = pd.read_csv('prompt_logs.csv')

# Model performance comparison
model_comparison = df.groupby('model_version').agg({
    'latency': ['mean', 'std'],
    'user_feedback': lambda x: (x == '👍').sum() / len(x) * 100,
    'hallucination': 'sum'
}).round(2)

print("Model Performance Comparison:")
print(model_comparison)

# Template effectiveness analysis
template_analysis = df.groupby('prompt_template').agg({
    'user_feedback': lambda x: (x == '👍').sum() / len(x) * 100,
    'latency': 'mean',
    'hallucination': lambda x: x.sum() / len(x) * 100
}).round(2)

print("\nPrompt Template Effectiveness:")
print(template_analysis)
```

### Performance Thresholds:

| Metric | Excellent | Good | Needs Improvement |
|--------|-----------|------|------------------|
| Satisfaction Rate | >90% | 80-90% | <80% |
| Hallucination Rate | <2% | 2-5% | >5% |
| Avg Latency (Interactive) | <1s | 1-3s | >3s |
| Avg Latency (Batch) | <5s | 5-10s | >10s |

## Best Practices

### Data Quality:
- ✅ **Rate every response** for accurate metrics
- ✅ **Be consistent** in evaluation criteria  
- ✅ **Document edge cases** and unusual behaviors
- ✅ **Test regularly** to catch performance regressions

### Testing Strategy:
- ✅ **Use representative prompts** from real use cases
- ✅ **Include failure scenarios** to test robustness
- ✅ **Test different prompt lengths** and complexities
- ✅ **Monitor performance over time** for trends

### Model Selection:
- ✅ **Consider quality vs. speed trade-offs**
- ✅ **Test with actual use case prompts**
- ✅ **Validate on edge cases** and difficult scenarios
- ✅ **Monitor costs** and resource usage

## Troubleshooting

### Common Issues:

**Dashboard not loading:**
```bash
# Check if all dependencies are installed
pip install -r requirements.txt

# Verify Hugging Face token
cat .env
```

**Model errors:**
- Verify your `HF_TOKEN` is valid
- Check model name spelling
- Ensure model is publicly available

**Slow responses:**
- Consider using smaller models for faster inference
- Check your internet connection
- Monitor Hugging Face API status

### Getting Help:
- Check the console output for error messages
- Verify your `.env` file contains a valid HF_TOKEN
- Review the prompt_logs.csv file for logged errors
- Test with simpler models like `gpt2` first

## Performance Optimization Tips

1. **Batch Testing**: Test multiple prompts in succession for efficiency
2. **Template Organization**: Use clear, consistent template categories
3. **Regular Reviews**: Check metrics daily during active development
4. **Documentation**: Keep notes on what works and what doesn't
5. **Iterative Improvement**: Continuously refine based on data insights