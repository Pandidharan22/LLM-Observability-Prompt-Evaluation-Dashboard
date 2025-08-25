# LLM Observability & Prompt Evaluation Dashboard

## 🚀 Project Overview

The **LLM Observability & Prompt Evaluation Dashboard** is a comprehensive full-stack application designed for real-time monitoring, analytics, and evaluation of Large Language Model interactions. This professional-grade dashboard provides deep insights into prompt performance, response quality, cost metrics, latency tracking, and A/B testing capabilities for prompt optimization.

## 🎯 Core Features

### 1. Real-time LLM Monitoring
- **Request/Response Tracking**: Comprehensive logging of all LLM API calls with precise timestamps
- **Performance Metrics**: Advanced tracking of latency, token usage, and cost per request
- **Error Monitoring**: Intelligent capture and categorization of API failures and timeouts
- **Rate Limiting Visualization**: Real-time monitoring of API quota usage across multiple providers

### 2. Advanced Prompt Evaluation System
- **Automatic Scoring**: Multiple evaluation metrics including BLEU, ROUGE, and semantic similarity
- **Custom Evaluators**: Flexible framework for user-defined evaluation criteria
- **A/B Testing**: Statistical comparison of prompt versions with significance testing
- **Version Control**: Complete tracking of prompt iterations and performance history

### 3. Interactive Real-time Dashboard
- **Live Charts**: Real-time updating metrics using WebSocket connections
- **Advanced Filtering**: Sophisticated filtering by date, model, prompt type, and user
- **Export Capabilities**: Comprehensive report downloads in CSV/JSON formats
- **Intelligent Alerts**: Configurable alerts for performance degradation and anomalies

### 4. Multi-Provider LLM Support
- **OpenAI Integration**: Full support for GPT-3.5, GPT-4, and GPT-4o models
- **Anthropic Claude**: Integration with Haiku, Sonnet, and Opus models
- **Open Source Models**: Ollama integration for local model deployment
- **Extensible Architecture**: Plugin-based system for easy addition of new providers

### 5. Analytics & Business Intelligence
- **Cost Analytics**: Detailed breakdown by provider, model, and time period
- **Performance Trends**: Historical analysis with predictive trend algorithms
- **User Behavior Analytics**: Comprehensive tracking of usage patterns and popular prompts
- **Quality Scoring**: Aggregate evaluation metrics with drill-down capabilities

## 🏗️ Technical Architecture

### Frontend Stack
```
React 18 + TypeScript + Tailwind CSS
├── Components/
│   ├── Dashboard/
│   │   ├── MetricsCards.tsx      # Real-time metric displays
│   │   ├── LiveChart.tsx         # WebSocket-powered charts
│   │   └── AlertPanel.tsx        # Alert management interface
│   ├── PromptEvaluation/
│   │   ├── EvaluationForm.tsx    # Evaluation configuration
│   │   ├── ComparisonView.tsx    # A/B testing interface
│   │   └── ResultsTable.tsx     # Results visualization
│   └── Shared/
│       ├── DatePicker.tsx        # Date range selection
│       ├── FilterPanel.tsx       # Advanced filtering
│       └── ExportButton.tsx      # Data export functionality
├── Pages/
│   ├── Dashboard.tsx             # Main dashboard view
│   ├── Prompts.tsx              # Prompt management
│   ├── Evaluations.tsx          # Evaluation results
│   └── Settings.tsx             # Configuration panel
├── Hooks/
│   ├── useWebSocket.ts          # Real-time data connection
│   ├── useMetrics.ts            # Metrics data management
│   └── useEvaluations.ts        # Evaluation state management
└── Utils/
    ├── api.ts                   # API client configuration
    ├── evaluation.ts            # Evaluation utilities
    └── constants.ts             # Application constants
```

### Backend Architecture
```
FastAPI + Python 3.11 + PostgreSQL + Redis
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── llm.py           # LLM provider endpoints
│   │   │   ├── evaluations.py  # Evaluation management
│   │   │   ├── metrics.py      # Metrics aggregation
│   │   │   └── websocket.py    # Real-time communication
│   │   └── dependencies.py     # Dependency injection
│   ├── core/
│   │   ├── config.py           # Application configuration
│   │   ├── database.py         # Database connection
│   │   └── security.py         # Authentication & authorization
│   ├── models/
│   │   ├── llm_request.py      # LLM request data models
│   │   ├── evaluation.py       # Evaluation data models
│   │   └── user.py             # User management models
│   ├── services/
│   │   ├── llm_providers/
│   │   │   ├── openai_provider.py    # OpenAI integration
│   │   │   ├── anthropic_provider.py # Anthropic integration
│   │   │   └── ollama_provider.py    # Ollama integration
│   │   ├── evaluation_engine.py      # Evaluation processing
│   │   ├── metrics_aggregator.py     # Metrics calculation
│   │   └── websocket_manager.py      # WebSocket management
│   └── utils/
│       ├── evaluation_metrics.py     # Evaluation algorithms
│       ├── cost_calculator.py        # Cost tracking utilities
│       └── data_processor.py         # Data processing helpers
```

### Database Schema (PostgreSQL + TimescaleDB)
```sql
-- Core Tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE llm_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    prompt_id UUID REFERENCES prompts(id),
    provider VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    request_payload JSONB NOT NULL,
    response_payload JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    latency_ms INTEGER,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_usd DECIMAL(10,6),
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

CREATE TABLE prompts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id UUID REFERENCES llm_requests(id),
    evaluator_type VARCHAR(50) NOT NULL,
    score DECIMAL(5,4),
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Additional tables for alerts, cost tracking, prompt versions, etc.
```

## 📊 Key Metrics & KPIs

### Dashboard Metrics Cards
- **Total Requests**: Real-time count with 24h trend
- **Average Latency**: Response time in milliseconds
- **Total Cost**: USD spend with provider breakdown
- **Success Rate**: Percentage of successful requests
- **Active Prompts**: Number of prompts in rotation
- **Evaluation Score**: Average quality score across all evaluations

### Real-time Visualizations
- **Request Volume**: Time-series line charts
- **Latency Distribution**: Histogram of response times
- **Cost Breakdown**: Provider and model cost analysis
- **Error Rate Tracking**: Time-series error percentage
- **Token Usage**: Input/output token consumption trends

## 🔧 Setup & Installation

### Prerequisites
```bash
# Required Software
- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- Redis 7
- Docker & Docker Compose
- Git
```

### Development Environment Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd LLM-Observability-Prompt-Evaluation-Dashboard
   ```

2. **Backend Setup**
   ```bash
   # Create Python virtual environment
   python -m venv venv
   venv\Scripts\activate  # On Windows
   
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   copy .env.example .env
   # Edit .env with your configuration
   ```

3. **Database Setup**
   ```bash
   # Start PostgreSQL and Redis with Docker
   docker-compose up -d postgres redis
   
   # Run database migrations
   alembic upgrade head
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Start the Application**
   ```bash
   # Backend (in root directory)
   uvicorn app.main:app --reload
   
   # Frontend (in frontend directory)
   npm run dev
   ```

### Production Deployment

#### Docker Compose Deployment
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
    environment:
      - REACT_APP_API_URL=http://backend:8000

  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - postgres
      - redis

  postgres:
    image: timescale/timescaledb:latest
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  worker:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    command: celery worker -A app.worker -l info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
```

## 🔌 API Documentation

### Core Endpoints

#### LLM Management
```python
POST /api/v1/llm/request          # Submit LLM request
GET  /api/v1/llm/requests         # List user requests
GET  /api/v1/llm/requests/{id}    # Get specific request
DELETE /api/v1/llm/requests/{id}  # Delete request
```

#### Metrics & Analytics
```python
GET  /api/v1/metrics/dashboard    # Dashboard overview metrics
GET  /api/v1/metrics/performance  # Performance analytics
GET  /api/v1/metrics/costs        # Cost breakdown
GET  /api/v1/metrics/trends       # Historical trends
```

#### Evaluation System
```python
POST /api/v1/evaluations/         # Create new evaluation
GET  /api/v1/evaluations/         # List evaluations
GET  /api/v1/evaluations/{id}     # Get evaluation details
POST /api/v1/evaluations/compare  # A/B test comparison
```

#### Prompt Management
```python
POST /api/v1/prompts/             # Create new prompt
GET  /api/v1/prompts/             # List user prompts
PUT  /api/v1/prompts/{id}         # Update prompt
DELETE /api/v1/prompts/{id}       # Delete prompt
POST /api/v1/prompts/compare      # Compare prompt versions
```

#### Real-time Communication
```python
WebSocket /ws/metrics             # Real-time metrics updates
WebSocket /ws/evaluations         # Evaluation status updates
WebSocket /ws/alerts              # Alert notifications
```

## 🧪 Testing Strategy

### Backend Testing
```bash
# Unit Tests (pytest)
pytest tests/unit/ -v --cov=app --cov-report=html

# Integration Tests
pytest tests/integration/ -v

# Load Testing (locust)
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

### Frontend Testing
```bash
# Unit & Integration Tests
npm run test

# E2E Tests (Playwright)
npm run test:e2e

# Performance Tests
npm run lighthouse
```

## 📈 Performance Optimization

### Backend Optimizations
- **Database Indexing**: Composite indexes on query-heavy columns
- **Caching Strategy**: Redis for metrics aggregation and session management
- **Connection Pooling**: Optimized PostgreSQL connections
- **Async Processing**: Celery workers for evaluation tasks
- **Query Optimization**: Database views for complex analytics

### Frontend Optimizations
- **Code Splitting**: Lazy loading of dashboard components
- **Memoization**: React.memo for expensive renders
- **Virtual Scrolling**: Efficient handling of large datasets
- **WebSocket Throttling**: Optimized real-time updates
- **Bundle Optimization**: Tree shaking and dynamic imports

## 🔒 Security Features

### Authentication & Authorization
- **JWT Tokens**: Short-lived access tokens with refresh mechanism
- **Role-Based Access Control**: Granular permission system
- **API Key Management**: External integration authentication
- **Rate Limiting**: Protection against API abuse

### Data Protection
- **Input Sanitization**: XSS and injection prevention
- **Data Encryption**: At-rest encryption for sensitive data
- **Audit Logging**: Comprehensive user action tracking
- **CORS Configuration**: Secure cross-origin policies

## 📊 Evaluation Metrics

### Automated Evaluation Metrics
```python
class EvaluationMetrics:
    def bleu_score(reference: str, candidate: str) -> float:
        """BLEU score for text similarity"""
        
    def rouge_score(reference: str, candidate: str) -> Dict[str, float]:
        """ROUGE-L, ROUGE-1, ROUGE-2 scores"""
        
    def semantic_similarity(text1: str, text2: str) -> float:
        """Cosine similarity using sentence embeddings"""
        
    def custom_evaluator(criteria: Dict, response: str) -> float:
        """User-defined evaluation criteria"""
        
    def statistical_significance(results_a: List, results_b: List) -> Dict:
        """A/B test statistical analysis"""
```

### Custom Evaluation Framework
- **Criteria Definition**: Flexible evaluation criteria setup
- **Scoring Algorithms**: Multiple scoring methodologies
- **Batch Processing**: Efficient evaluation of large datasets
- **Result Aggregation**: Statistical analysis and reporting


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support & Community

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: [Project Wiki](https://github.com/your-repo/wiki)
- **Contact**: [your-email@example.com](mailto:your-email@example.com)

---

**Built with ❤️ for the AI Engineering Community**

*This project aims to democratize LLM observability and make advanced prompt evaluation accessible to all AI practitioners.*