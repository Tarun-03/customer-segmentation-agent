# Customer Segmentation & Personalized Banking Recommendation System

An AI-powered customer segmentation system that groups bank customers using **K-Means Clustering** and generates **personalized banking recommendations** through a rule-based recommendation engine.

## Features

- Customer Segmentation using K-Means Clustering
- Data Engineering & Synthetic Feature Generation
- Exploratory Data Analysis (EDA)
- Cluster Profiling & Customer Personas
- Rule-Based Personalized Recommendations
- REST API using FastAPI
- Interactive Swagger Documentation
- Model Persistence using Joblib

---

# Tech Stack

## Backend

- Python 3.10+
- FastAPI
- Pandas
- NumPy

## Machine Learning

- Scikit-learn
- Joblib

## Visualization

- Matplotlib
- Seaborn

---

# Project Structure

```text
customer-segmentation-agent/

│
├── app/
│   ├── api/
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── schemas.py
│   │   └── recommendation_rules.py
│   │
│   ├── data_engineering/
│   │
│   ├── eda/
│   │
│   └── segmentation/
│       ├── preprocessor.py
│       ├── trainer.py
│       ├── evaluator.py
│       ├── profiler.py
│       ├── personas.py
│       └── recommendation.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── models/
│   └── outputs/
│
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone <repository-url>
```

Move inside the project

```bash
cd customer-segmentation-agent
```

Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Dataset

Place the raw banking dataset inside

```text
data/raw/
```

---

# Running the Pipeline

## 1. Data Engineering

```bash
python app/data_engineering/pipeline.py
```

Output

```
data/processed/enhanced_bank_dataset.csv
```

---

## 2. Exploratory Data Analysis

```bash
python app/eda/run_eda.py
```

Generated plots are saved in

```
data/outputs/plots/
```

---

## 3. Train K-Means Model

```bash
python app/segmentation/run_segmentation.py
```

Generated files

```
data/models/kmeans_model.pkl
data/models/preprocessor.pkl
```

Generated datasets

```
clustered_customers.csv
cluster_summary.csv
customer_personas.csv
customer_recommendations.csv
```

---

# Running the API

Move inside

```bash
cd app/api
```

Run

```bash
uvicorn main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Home

```
GET /
```

---

## Cluster Summary

```
GET /clusters
```

Returns

- Cluster Statistics
- Average Income
- Average Balance
- Average Credit Score

---

## Customer Personas

```
GET /personas
```

Returns customer personas for every cluster.

---

## Recommendations

```
GET /recommendations
```

Returns recommended banking products for each persona.

---

## Existing Customer Lookup

```
GET /customers/{customer_id}
```

Example

```
GET /customers/10
```

Returns

```json
{
  "customer": {},
  "persona": "Digital Professionals",
  "recommendations": []
}
```

---

## Predict New Customer

```
POST /predict
```

Example Request

```json
{
  "age": 24,
  "job": "student",
  "marital": "single",
  "education": "university.degree",
  "housing": "yes",
  "loan": "no",
  "annual_income": 60000,
  "credit_score": 650,
  "account_balance": 15000,
  "digital_banking_score": 85,
  "monthly_transactions": 35,
  "investment_amount": 5000,
  "account_tenure": 2,
  "number_of_products": 1
}
```

Example Response

```json
{
  "predicted_cluster": 2,
  "persona": "Emerging Customers",
  "recommendations": [
    {
      "title": "Basic Savings Account",
      "category": "Cluster Recommendation",
      "reason": "Recommended because you belong to the Emerging Customers segment."
    },
    {
      "title": "Student Savings Account",
      "category": "Banking",
      "reason": "Designed for students with zero minimum balance."
    }
  ],
  "warnings": [
    "Premium credit card approval may be difficult until your credit score improves."
  ]
}
```

---

# Machine Learning Pipeline

```
Raw Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Synthetic Feature Generation
      │
      ▼
EDA
      │
      ▼
Preprocessing
(StandardScaler + OneHotEncoder)
      │
      ▼
K-Means Clustering
      │
      ▼
Cluster Profiling
      │
      ▼
Customer Personas
      │
      ▼
Recommendation Engine
      │
      ▼
FastAPI
```

---

# Rule-Based Recommendation Engine

The recommendation engine provides personalized suggestions based on customer attributes such as:

- Occupation
- Credit Score
- Annual Income
- Account Balance
- Digital Banking Score
- Account Tenure
- Number of Products

Example rules include:

- Student Savings Account
- Wealth Management
- Platinum Credit Card
- Emergency Savings Plan
- Budget Tracking
- Credit Score Improvement Program
- Relationship Manager
- Branch Banking Assistance

---

# Output Files

| File | Description |
|------|-------------|
| enhanced_bank_dataset.csv | Engineered dataset |
| clustered_customers.csv | Customers with assigned clusters |
| cluster_summary.csv | Cluster statistics |
| customer_personas.csv | Personas for each cluster |
| customer_recommendations.csv | Cluster-level product recommendations |
| kmeans_model.pkl | Trained K-Means model |
| preprocessor.pkl | Saved preprocessing pipeline |

---