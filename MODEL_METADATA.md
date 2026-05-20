# Model Metadata for Hugging Face

Add this YAML frontmatter to the top of your README.md on Hugging Face to improve discoverability:

```yaml
---
language:
- en
tags:
- tabular-regression
- regression
- scikit-learn
- sklearn
- random-forest
- house-prices
- california-housing
- real-estate
- price-prediction
- tabular
license: mit
datasets:
- california-housing
metrics:
- rmse
- mean_squared_error
library_name: sklearn
pipeline_tag: tabular-regression
widget:
- text: "Example: Predict house price for NEAR BAY location with median income $83,252"
---
```

## Model Card Sections (Already included in README.md)

Your README.md already includes:

- ✅ Model description and overview
- ✅ Use cases
- ✅ Installation instructions
- ✅ Quick start examples
- ✅ Input feature documentation
- ✅ Training details and evaluation
- ✅ Requirements
- ✅ License information
- ✅ Author information

## Additional Metadata You Can Add

### Model Performance Metrics

Add these details if you have them:

- Training RMSE: ~$49,000 (10-fold cross-validation)
- Test RMSE: ~$47,000-49,000
- R² Score: [Add if calculated]
- MAE (Mean Absolute Error): [Add if calculated]

### Training Information

- Training time: ~30 minutes (on standard CPU)
- Number of trees: 30
- Max features: 8
- Training samples: 16,512
- Test samples: 4,128

### Limitations

Already mentioned:

- Model trained on 1990 census data
- Limited to California housing market
- May not generalize to other regions/time periods

### Bias and Fairness Considerations

Consider adding:

- Geographic bias (California-specific)
- Temporal bias (1990 data)
- Income-based predictions may reinforce existing patterns

## Files Included in Repository

```text
house-price-prediction/
├── house_price_model.joblib          # Trained Random Forest model (41.4 MB)
├── preprocessing_pipeline.joblib     # Scikit-learn preprocessing pipeline (3.8 KB)
├── inference.py                      # Python API for model inference (8.3 KB)
├── example_usage.py                  # Example usage scripts (6.1 KB)
├── test_deployment.py                # Deployment readiness tests (8.1 KB)
├── housepriceprediction.ipynb        # Training notebook with Gradio demo
├── housing.csv                       # Original dataset
├── README.md                         # Model card (comprehensive documentation)
├── requirements.txt                  # Python dependencies
├── LICENSE                           # MIT License
├── .gitattributes                    # Git LFS configuration
├── DEPLOYMENT_GUIDE.md               # Step-by-step deployment guide
└── MODEL_METADATA.md                 # This file (metadata reference)
```

## Recommended Tags for Hugging Face

Primary tags:

- `tabular-regression`
- `scikit-learn`
- `random-forest`

Domain tags:

- `house-prices`
- `real-estate`
- `california-housing`

Technical tags:

- `sklearn`
- `joblib`
- `regression`
- `tabular`

## Example API Usage for Hugging Face

When users want to use your model from Hugging Face:

```python
from huggingface_hub import hf_hub_download
import joblib

# Download files
model_file = hf_hub_download(repo_id="YOUR_USERNAME/house-price-prediction", 
                              filename="house_price_model.joblib")
pipeline_file = hf_hub_download(repo_id="YOUR_USERNAME/house-price-prediction", 
                                 filename="preprocessing_pipeline.joblib")

# Load model
model = joblib.load(model_file)
pipeline = joblib.load(pipeline_file)
```

Or clone the entire repo:

```bash
git clone https://huggingface.co/YOUR_USERNAME/house-price-prediction
cd house-price-prediction
python inference.py
```

## Citation

If someone uses your model, they can cite it as:

```bibtex
@misc{california-house-price-prediction,
  author = {YOUR_USERNAME},
  title = {California House Price Prediction Model},
  year = {2025},
  publisher = {Hugging Face},
  journal = {Hugging Face Model Hub},
  howpublished = {\url{https://huggingface.co/YOUR_USERNAME/house-price-prediction}},
}
```
