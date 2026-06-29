---
license: mit
language:
- en
tags:
- tabular-regression
- scikit-learn
- random-forest
- house-prices
- california-housing
- real-estate
- regression
library_name: scikit-learn
metrics:
- rmse
- r2
datasets:
- california-housing
pipeline_tag: tabular-regression
---

# California House Price Prediction Model 🏠

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)

A machine learning model for predicting California house prices based on various features like location, age, size, and proximity to the ocean. This model uses a **Random Forest Regressor** trained on the California Housing dataset and achieves strong predictive performance.

## 📊 Model Overview

- **Model Type**: Random Forest Regressor (scikit-learn)
- **Task**: Regression (Predict median house value)
- **Training Data**: California Housing dataset (20,640 instances)
- **Performance**: Final RMSE on test set: ~$47,000-49,000
- **Features**: 8 numerical features + 1 categorical feature (ocean_proximity)
- **Target**: Median house value in California districts (in USD)

## 🎯 Use Cases

- Real estate price estimation
- Housing market analysis
- Property valuation for California regions
- Educational demonstrations of regression modeling

## 📥 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Mehak-991/house-price-prediction.git
cd house-price-prediction
```

### 2. Set up a Virtual Environment (Python 3.12 recommended)

Using a virtual environment prevents version conflicts with global Python installations (specifically Python 3.14+):

```powershell
# Create virtual environment
py -3.12 -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 🚀 Quick Start

You can run either the custom FastAPI web app or the Gradio interface.

### Option A: Start the FastAPI Web App (Recommended)

This launches the premium custom HTML/CSS/JavaScript web interface.

```powershell
python main.py
```
Open **`http://127.0.0.1:8001`** in your browser.

### Using the Python API

```python
from inference import load_model

# Load the model
predictor = load_model()

# Prepare input data
house_data = {
    'longitude': -122.23,
    'latitude': 37.88,
    'housing_median_age': 41.0,
    'total_rooms': 880.0,
    'total_bedrooms': 129.0,
    'population': 322.0,
    'households': 126.0,
    'median_income': 8.3252,
    'ocean_proximity': 'NEAR BAY'
}

# Make prediction
predicted_price = predictor.predict(house_data)
print(f"Predicted house price: ${predicted_price[0]:,.2f}")
```

### Using the convenience function

```python
from inference import HousePricePredictor

predictor = HousePricePredictor()
predictor.load()

# Predict single house price
price = predictor.predict_single(
    longitude=-122.23,
    latitude=37.88,
    housing_median_age=41.0,
    total_rooms=880.0,
    total_bedrooms=129.0,
    population=322.0,
    households=126.0,
    median_income=8.3252,
    ocean_proximity='NEAR BAY'
)
print(f"Predicted price: ${price:,.2f}")
```

### Batch predictions

```python
import pandas as pd
from inference import load_model

predictor = load_model()

# Prepare multiple houses
houses_df = pd.DataFrame([
    {'longitude': -122.23, 'latitude': 37.88, 'housing_median_age': 41.0,
     'total_rooms': 880.0, 'total_bedrooms': 129.0, 'population': 322.0,
     'households': 126.0, 'median_income': 8.3252, 'ocean_proximity': 'NEAR BAY'},
    {'longitude': -122.22, 'latitude': 37.86, 'housing_median_age': 21.0,
     'total_rooms': 7099.0, 'total_bedrooms': 1106.0, 'population': 2401.0,
     'households': 1138.0, 'median_income': 8.3014, 'ocean_proximity': 'NEAR BAY'},
])

# Predict all at once
predictions = predictor.predict(houses_df)
for i, price in enumerate(predictions):
    print(f"House {i+1}: ${price:,.2f}")
```

## 📋 Input Features

The model requires the following features for prediction:

| Feature | Type | Description | Example |
|---------|------|-------------|---------|
| `longitude` | float | Longitude coordinate of the house | -122.23 |
| `latitude` | float | Latitude coordinate of the house | 37.88 |
| `housing_median_age` | integer | Median age of houses in the district | 41 |
| `total_rooms` | integer | Total number of rooms in the district | 880 |
| `total_bedrooms` | integer | Total number of bedrooms in the district | 129 |
| `population` | integer | Total population in the district | 322 |
| `households` | integer | Total number of households in the district | 126 |
| `median_income` | float | Median income (in tens of thousands USD) | 8.3252 |
| `ocean_proximity` | string | Proximity to ocean | One of: `<1H OCEAN`, `INLAND`, `NEAR OCEAN`, `NEAR BAY`, `ISLAND` |


## 📈 Model Training Details

### Training Process

1. **Data Preprocessing**:
   - Handled missing values using median imputation
   - Created stratified train-test split (80-20) based on income categories
   - Feature engineering: Added derived features (rooms_per_household, etc.)
   - Standardized numerical features using StandardScaler
   - One-hot encoded categorical feature (ocean_proximity)

2. **Model Selection**:
   - Compared Linear Regression, Decision Tree, and Random Forest
   - Random Forest showed best performance

3. **Hyperparameter Tuning**:
   - Used GridSearchCV with 5-fold cross-validation
   - Optimized parameters: `n_estimators`, `max_features`, `bootstrap`
   - Best parameters: `{'max_features': 8, 'n_estimators': 30}`

4. **Evaluation**:
   - Primary metric: RMSE (Root Mean Squared Error)
   - Cross-validation RMSE: ~$49,000
   - Final test set RMSE: ~$47,000-49,000

### Feature Importance

Top features contributing to predictions (from the trained model):

1. Median Income
2. Longitude
3. Latitude
4. Housing Median Age
5. Ocean Proximity

## 📦 Model & Web App Files

- `house_price_model.joblib` - Trained Random Forest model
- `preprocessing_pipeline.joblib` - Data preprocessing pipeline
- `inference.py` - Python inference API
- `main.py` - FastAPI App server
- `static/` - HTML/CSS/JavaScript client frontend interface
- `app.py` - Gradio Application interface
- `housepriceprediction.ipynb` - Underlying Training notebook 

## 🔧 Requirements

- Python 3.12 (recommended) or 3.8+
- scikit-learn == 1.4.2 (pinned to prevent unpickling errors)
- pandas >= 2.0.0
- numpy >= 1.24.0
- joblib >= 1.3.0
- fastapi >= 0.115.0
- uvicorn >= 0.29.0
- gradio >= 4.0.0 (optional, for Gradio UI)

See `requirements.txt` for complete dependencies.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## 📚 References

- Dataset: [California Housing Dataset](https://www.kaggle.com/datasets/camnugent/california-housing-prices)
- Inspired by: *Hands-On Machine Learning with Scikit-Learn and TensorFlow* by Aurélien Géron

## 👤 Author

**YOUR_USERNAME**
- GitHub: [https://github.com/Mehak-991](https://github.com/Mehak-991)

## 🌟 Acknowledgments

- California Housing dataset from the 1990 U.S. Census
- scikit-learn community for excellent ML tools

---

**Note**: This model is trained on 1990 census data and is intended for educational and demonstration purposes. For real-world applications, consider using more recent data and additional features.
