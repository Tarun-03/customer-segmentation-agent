# Customer Segmentation & Personalized Banking Recommendation AI Agent

An AI-powered Retail Banking Customer Segmentation system that combines **Machine Learning**, **FastAPI**, **React**, and **LLM-powered conversational analytics** to help banks understand customer behavior, generate customer personas, recommend personalized banking products, and interact with customer data using natural language.

---

# Features

- Customer Segmentation using K-Means Clustering
- Customer Persona Generation
- Personalized Banking Recommendations
- AI-powered Chatbot using Groq LLM
- Existing Customer Lookup
- New Customer Prediction
- Explainability Engine
- Exploratory Data Analysis (EDA)
- Model Evaluation Dashboard
- Interactive React Frontend
- FastAPI REST API
- Swagger Documentation

---

# Problem Statement

This project was developed for the **Campus Hackathon 2026** under the problem statement:

**Customer Segmentation & Personalization Agent for Retail Banking**

The objective is to build an AI-powered agent capable of:

- Performing automated Exploratory Data Analysis (EDA)
- Segmenting customers using behavioral and financial attributes
- Generating interpretable customer personas
- Providing personalized banking recommendations
- Answering natural language queries using an AI assistant
- Producing explainable insights for customer segmentation

---

# Tech Stack

## Frontend

- React
- JavaScript
- CSS

## Backend

- Python 3.10+
- FastAPI
- Pandas
- NumPy

## Machine Learning

- Scikit-learn
- K-Means Clustering
- Joblib

## Visualization

- Matplotlib
- Seaborn

## AI

- Groq API
- Llama 3.3 (or configured Groq model)

---

# Project Structure

```text
customer-segmentation-agent/

├── app/
│   ├── api/
│   ├── data_engineering/
│   ├── eda/
│   ├── segmentation/
│   ├── tools.py
│   ├── planner.py
│   ├── groq_service.py
│   └── intent_parser.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── models/
│   └── outputs/
│
├── frontend/
│
├── requirements.txt
├── README.md
└── .env
```

---

# Dataset

The project uses a publicly available retail banking marketing dataset obtained from UCI.

Original Dataset:
https://uci-ics-mlr-prod.aws.uci.edu/dataset/222/bank%2Bmarketing

The raw dataset is placed inside:

data/raw/

Additional customer-centric attributes such as:

- Annual Income
- Credit Score
- Account Balance
- Investment Amount
- Digital Banking Score
- Monthly Transactions
- Number of Products
- Account Tenure

were synthetically generated to simulate a realistic retail banking environment suitable for customer segmentation.

These synthetic features were generated solely for educational and hackathon purposes.

---

# LLM Integration

The conversational AI assistant is powered by the Groq API.

Model inference is used for:

- Intent understanding
- Tool selection
- Execution planning
- Natural language response generation

The LLM is not used for machine learning predictions.

Customer segmentation is performed using a trained K-Means clustering model developed using Scikit-learn.

The LLM is responsible only for orchestrating analytical tools and presenting results in natural language.

---

# Clone the Repository

```bash
git clone https://github.com/Tarun-03/customer-segmentation-agent.git

cd customer-segmentation-agent
```

---

# Create Virtual Environment

## Windows

```bash
python -m venv venv

venv\Scripts\activate
```

## macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# Install Dependencies

Backend

```bash
pip install -r requirements.txt
```

Frontend

```bash
cd frontend

npm install
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL_NAME=llama-3.3-70b-versatile
```

You can obtain a free Groq API key from:

https://console.groq.com/

---

# Running the Machine Learning Pipeline

## 1. Data Engineering

```bash
python app/data_engineering/pipeline.py
```

Generates:

```
data/processed/enhanced_bank_dataset.csv
```

---

## 2. Exploratory Data Analysis

```bash
python app/eda/run_eda.py
```

Generated plots are stored in:

```
data/outputs/plots/
```

---

## 3. Train Segmentation Model

```bash
python app/segmentation/run_segmentation.py
```

Generated model files:

```
data/models/kmeans_model.pkl

data/models/preprocessor.pkl
```

Generated datasets:

- clustered_customers.csv
- cluster_summary.csv
- customer_personas.csv
- customer_recommendations.csv

---

# Run Backend

```bash
cd app/api

uvicorn main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# Run Frontend

```bash
cd frontend

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# AI Agent Workflow

The AI assistant follows an agentic workflow:

1. Accepts a natural language query.
2. Identifies the user's intent.
3. Selects the appropriate analytical tool.
4. Executes data analysis.
5. Generates explainable insights.
6. Returns a structured response.

Available tools include:

- EDA Tool
- Segmentation Tool
- Explainability Tool
- Customer Lookup Tool
- Retention Recommendation Tool

---

# Application Pages

### Dashboard

Provides an overview of customer segmentation and project metrics.

### Customer Lookup

Retrieve customer details using Customer ID.

### New Customer Prediction

Predict the cluster and persona for a new customer.

### Model Evaluation

Displays:

- Silhouette Score
- Davies-Bouldin Index
- Calinski-Harabasz Score
- Elbow Curve
- Silhouette Analysis

### EDA Metrics

Includes:

- Age Distribution
- Credit Score Distribution
- Income Distribution
- Job Distribution
- Products Distribution
- Average Investment by Cluster

### AI Assistant

Allows users to interact with customer data using natural language and receive explainable analytical insights.

---

# API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | `/` | Home |
| GET | `/clusters` | Cluster Summary |
| GET | `/personas` | Customer Personas |
| GET | `/recommendations` | Banking Recommendations |
| GET | `/customers/{customer_id}` | Existing Customer Lookup |
| POST | `/predict` | New Customer Prediction |
| POST | `/chat` | AI Chat Assistant |

---

# Output Files

The project generates:

- enhanced_bank_dataset.csv
- clustered_customers.csv
- cluster_summary.csv
- customer_personas.csv
- customer_recommendations.csv
- kmeans_model.pkl
- preprocessor.pkl
- EDA plots

---

# AI Assistance Disclosure

This project was developed with the assistance of AI-powered development tools.

The following tools were used during development:

- **ChatGPT (OpenAI)**
  - Code generation
  - Debugging assistance
  - FastAPI integration
  - React frontend development
  - Documentation
  - Project architecture guidance

- **Claude (Anthropic)**
  - Code review
  - Refactoring suggestions
  - Prompt engineering assistance

All implementation decisions, project integration, testing, debugging, and final validation were performed by the project authors.

---

# License

This project is intended for educational and hackathon purposes.

---