# Data Storm v7.0 - Latent Demand Estimation Framework

## Team Name
DATA DYNAMOS

---

# Project Overview

The Data Dynamos solution predicts the latent maximum monthly beverage demand for retail outlets across Sri Lanka.

Traditional forecasting methods rely heavily on historical sales averages. However, observed sales often underestimate the true market demand due to operational constraints such as:
- Stock shortages
- Delivery limitations
- Credit restrictions
- Operational inefficiencies

To address this challenge, our team developed a Latent Demand Estimation Framework capable of estimating realistic uncapped outlet demand using:
- Modern medallion data architecture
- Advanced feature engineering
- Geospatial enrichment
- Machine learning models

The project processed over 3.1 million transaction records and generated predictions for 11,121 retail outlets.

---

# Key Results

| Metric | Value |
|---|---|
| R² Score | 0.9943 |
| MAE | 3.40 Liters |
| Total Outlets Predicted | 11,121 |
| Engineered Features | 17 |
| Model | CatBoost Regressor |

---

# Project Architecture

The solution follows a Bronze → Silver → Gold Lakehouse Architecture.

```text
project/
│
├── data/
│   ├── bronze/
│   ├── silver/
│   │   └── rejected/
│   └── gold/
│
├── notebooks/
│   ├── 01_bronze_layer.ipynb
│   ├── 02_silver_layer.ipynb
│   ├── 03_poi_spatial_features.ipynb
│   ├── 04_gold_feature_engineering.ipynb
│   ├── 05_model_training_catboost.ipynb
│   └── 06_final_submission.ipynb
│
├── outputs/
│   ├── Data_Dynamos_predictions.csv
│   
│
├── README.md
├── report.pdf
└── requirements.txt
```

---

# Pipeline Overview

## Bronze Layer — Raw Data Ingestion

Raw datasets were ingested without modifications.

### Sources Included
- Transaction datasets
- Outlet master data
- Product metadata
- Seasonal datasets
- External geospatial datasets

---

## Silver Layer — Data Cleaning & Validation

The Silver Layer focused on data quality assurance and anomaly handling.

### Validation Framework

#### Layer 1 — Schema Validation
- Required column checks
- Data type enforcement
- Null validation

#### Layer 2 — Domain Validation
- Year range validation
- Month validation
- Non-negative sales validation

#### Layer 3 — Referential Integrity
- Outlet ID validation
- SKU validation
- Distributor integrity checks

#### Layer 4 — Statistical Validation
- IQR-based outlier detection
- Distribution consistency checks
- Temporal continuity validation

#### Layer 5 — Deduplication
- Transaction deduplication
- Outlet deduplication
- Holiday dataset deduplication

---

# Rejected Records Quarantine System

Invalid records were isolated rather than permanently deleted.

```text
data/silver/rejected/
├── invalid_transactions.csv
├── invalid_outlets.csv
└── invalid_coordinates.csv
```

### Rejected Categories
- Negative sales values
- Invalid bill values
- Missing outlet IDs
- Invalid geographic coordinates
- Future-dated records

Each quarantined record retained:
- Original row values
- Rejection reason
- Validation layer metadata
- Recovery tracking information

---

# Spatial Enrichment & POI Features

External geospatial intelligence was integrated using:
- OpenStreetMap (OSM)
- OSMnx API
- Government geospatial datasets

### POI Categories
- Schools
- Hospitals
- Bus stations
- Shopping centers

### Spatial Logic
For each outlet:
1. Extract outlet coordinates
2. Identify nearby POIs within 2km
3. Calculate density indicators
4. Generate contextual demand signals

### Engineered Spatial Features
- nearby_schools_count
- transport_proximity
- school_density
- geo_cluster

### Additional Spatial Processing
- KMeans geographic clustering
- Haversine distance calculations
- Batch API processing with caching

---

# Latent Demand Estimation Logic

## The Left-Censored Demand Problem

Observed sales do not always represent true demand because:

```text
Observed Sales = min(True Demand, Operational Constraints)
```

Traditional forecasting models therefore underestimate actual outlet demand.

---

# Demand Ceiling Estimation

The framework estimates outlet potential using the 95th percentile of historical outlet sales.

## Why 95th Percentile?

| Metric | Maximum Sales | 95th Percentile |
|---|---|---|
| Outlier Sensitivity | High | Low |
| Stability | Low | High |
| Realism | Weak | Strong |

This approach preserves realistic high-demand behavior while reducing sensitivity to extreme spikes.

---

# Machine Learning Model

## Model Used
CatBoost Regressor

### Why CatBoost?
- Strong performance on tabular datasets
- Handles non-linear relationships
- Minimal preprocessing requirements
- Feature importance support

### Model Configuration

```python
CatBoostRegressor(
    iterations=500,
    learning_rate=0.05,
    depth=6,
    loss_function='RMSE',
    random_state=42
)
```

---

# Feature Engineering

A total of 17 engineered features were used.

### Key Features
- product_avg_volume
- outlet_avg_volume
- rolling_mean_3
- lag_1
- month_cos
- seasonal encodings
- geographic clusters
- outlet-level aggregates

---

# Model Performance

| Metric | Train | Test |
|---|---|---|
| RMSE | 7.0861 | 7.1881 |
| MAE | 3.3814 | 3.4006 |
| R² Score | 0.9945 | 0.9943 |

### Interpretation
- Model explains 99.43% of sales variance
- Average prediction error is approximately 3.4 liters
- Strong generalization observed on unseen data

---

# Feature Importance

| Rank | Feature | Importance |
|---|---|---|
| 1 | product_avg_volume | 53.96% |
| 2 | outlet_avg_volume | 26.77% |
| 3 | rolling_mean_3 | 8.07% |
| 4 | lag_1 | 5.49% |
| 5 | month_cos | 2.33% |

### Key Insight
Product popularity and outlet historical strength contribute more than 80% of predictive power.

---

# Final Deliverables

## Output Files

### 1. Data_Dynamos_predictions.csv
Contains uncapped outlet demand predictions.

### Columns
- Outlet_ID
- Maximum_Monthly_Liters

---

### 2. catboost_predictions.csv
Detailed prediction outputs from the trained model.

---

### 3. model_clean.ipynb
Production-ready machine learning notebook.

---

# Distribution Statistics

| Statistic | Value |
|---|---|
| Mean Potential | 572.04 liters |
| Median Potential | 420.15 liters |
| Maximum Potential | 5,741.22 liters |

---

# How to Run

## 1. Install Dependencies

```bash
pip install pandas numpy scikit-learn catboost pyarrow osmnx geopandas shapely
```

---

## 2. Run Notebooks in Order

1. `bronze_layer.ipynb`
2. `silver_layer.ipynb`
3. `poi_spatial_features.ipynb`
4. `gold_feature_engineering.ipynb`
5. `model_training_catboost.ipynb`
6. `final_submission.ipynb`

---

# Generative AI Transparency

The following AI tools were used during the competition:
- ChatGPT
- GitHub Copilot
- Perplexity AI

## Areas Supported by GenAI
- Pipeline architecture planning
- Validation framework recommendations
- Feature engineering guidance
- CatBoost parameter tuning suggestions
- Documentation assistance

## Human Validation
All final decisions, validations, and business logic implementations were independently verified by the Data Dynamos team.

GenAI acted only as:
- Engineering accelerator
- Coding assistant
- Documentation helper

---

# Conclusion

The Data Dynamos team successfully developed a complete Latent Demand Estimation Framework capable of predicting realistic uncapped beverage demand across Sri Lankan retail outlets.

The framework combined:
- Modern medallion architecture
- Robust data engineering
- Geospatial enrichment
- Advanced feature engineering
- Machine learning prediction models

## Final Achievements
- Processed over 3.1 million records
- Engineered 17 predictive features
- Achieved 99.43% R² accuracy
- Generated predictions for 11,121 outlets
- Produced actionable insights for FMCG distribution optimization

This solution enables:
- Smarter inventory allocation
- Better outlet prioritization
- Improved supply chain decisions
- Enhanced demand forecasting capabilities

# Report

📄 [Download Technical Summary Report](./Data_Dyna  mos_Technical_Report.pdf)
