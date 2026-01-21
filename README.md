# 🏠 House Price Prediction in Tunisia

This project is an **end-to-end machine learning pipeline** to predict house prices in Tunisia using historical real estate listings. It covers **data collection, preprocessing, feature engineering, exploratory analysis, model experimentation, MLflow tracking, model registry, FastAPI deployment, and Dockerization**.

The main goal is to provide **reliable price predictions** for properties given their surface area, number of rooms, location (governorate), and property type.

---

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Data Collection](#data-collection)
4. [Web Scraping with Scrapy](#web-scraping-with-scrapy)
5. [Data Preprocessing](#data-preprocessing)
6. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
7. [Modeling](#modeling)
8. [Experiment Tracking with MLflow](#experiment-tracking-with-mlflow)
9. [Model Registry](#model-registry)
10. [FastAPI Deployment](#fastapi-deployment)
11. [Docker Deployment](#docker-deployment)

---

## Overview

This project predicts house prices in Tunisia using features such as:

- Surface area (m²)
- Number of rooms
- Governorate (location)
- Property type (apartment or house)

The project showcases **MLOps practices** by integrating **MLflow**, **FastAPI**, and **Docker** for reproducible experiments and production deployment.

---

## Project Structure

```
House_Price_Prediction/
│
├── data/
│   ├── raw/                       # Original CSVs scraped from websites
│   │   ├── mubawab.csv
│   │   ├── tayara.csv
│   │   └── immobilier.csv
│   └── clean/                     # Cleaned CSVs ready for modeling
│
├── housescraper/                  # Scrapy spiders, items, and pipelines
│
├── notebooks/
│   ├── 1_data_preprocessing.ipynb
│   ├── 2_eda.ipynb
│   ├── 3_modeling.ipynb
│   ├── 4_tracking.ipynb
│   └── 5_model_registry.ipynb
│
├── fastapi_app.py                 # FastAPI API serving the production model
├── Dockerfile                     # Docker setup for the API
├── requirements.txt               # Full Python dependencies for development
├── requirements-prod.txt          # Production dependencies
└── README.md
```

---

## Data Collection

The dataset was collected from three real estate platforms:

| Source | Listings Collected |
|--------|-------------------|
| Mubawab.tn | 6,588 |
| Tayara.tn | 1,922 |
| Immobilier.tn | 726 |

**Collected fields for each listing:**

- `price`
- `surface` (m²)
- `rooms`
- `governorate` (location)
- `property_type` (apartment or house)

---

## Web Scraping with Scrapy

- **Spiders:** One per website to extract listings.
- **Items:** Define structured fields for scraped data.
- **Pipelines:**
  - Remove missing or invalid rows
  - Normalize governorate names
  - Merge data from all sources

Raw CSVs are saved in `data/raw/`.

---

## Data Preprocessing

Steps applied to clean and prepare the data:

### 1. Handling Missing Values
- Removed rows with missing `price`, `surface`, `rooms`, `governorate`, or `property_type`.

### 2. Normalization & Transformation
- Log-transform `price` → `log(1 + price)`
- Standardize governorate names

### 3. Outlier Handling
- Extreme but valid values kept for luxury properties

### 4. Feature Engineering
- `rooms_per_surface = rooms / surface`
- `surface_squared = surface ** 2`

**Final dataset saved as:**
```
data/clean/clean_housing_tunisia_model_ready.csv
```

---

## Exploratory Data Analysis (EDA)

EDA highlights:

- Histograms for `price` and `surface` distributions
- Log-transformations to normalize skewed data
- Most listings in urban governorates: **Tunis, Nabeul, Ariana**
- Key features influencing price:
  - Surface area
  - Number of rooms
  - Governorate
  - Property type

EDA notebook: `2_eda.ipynb`.

---

## Modeling

**Models tested:**

| Model | Purpose |
|-------|---------|
| Linear Regression | Baseline model |
| Random Forest | Captures non-linear interactions |
| XGBoost | Gradient boosting for high performance |

**Features:**
- Numeric: `surface`, `surface_squared`, `rooms`, `rooms_per_surface`
- Categorical: `governorate`, `property_type` (one-hot encoded)

---

## Experiment Tracking with MLflow

**Why MLflow:**

- Track multiple model versions
- Log metrics, parameters, and artifacts
- Compare experiment performance

**Experiment highlights:**

- Random vs grouped splits
- Models evaluated with hyperparameter tuning
- Best model: **XGBoost (random split)**
  - RMSE: 0.4877
  - R²: 0.6240

**Run locally:**

```bash
pip install mlflow
mlflow ui
```

Dashboard URL: `http://localhost:5000`

All experiments saved under `mlruns/`.

---

## Model Registry

- Best XGBoost model registered in MLflow Model Registry
- Production-ready with feature columns artifact for input alignment
- Versioned and reproducible deployment

---

## FastAPI Deployment

Production model served via FastAPI (`fastapi_app.py`)

- Handles feature engineering and input alignment

**Example API Request:**

```http
POST /predict
Content-Type: application/json

{
  "surface": 250,
  "rooms": 3,
  "governorate": "Ariana",
  "property_type": "Appart"
}
```

**Example Response:**

```json
{
  "predicted_log_price": 13.49,
  "predicted_price": 722359.88
}
```

Features:
- API aligns input features to training columns dynamically
- One-hot encodes categorical variables on the fly

---

## Docker Deployment

Dockerized API for easy deployment

**Build and run:**

```bash
# Build Docker image
docker build -t house-price-api .

# Run container
docker run -p 8000:8000 house-price-api
```

Access Swagger docs at `http://localhost:8000/docs`

**Dependencies:**

- `requirements.txt` → full development environment
- `requirements-prod.txt` → production environment

---

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run MLflow UI: `mlflow ui`
4. Start FastAPI server: `uvicorn fastapi_app:app --reload`
5. Or use Docker: `docker build -t house-price-api . && docker run -p 8000:8000 house-price-api`
