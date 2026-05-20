# 🚀 Deployment Guide: Hugging Face Model Hub

This guide walks you through deploying your California House Price Prediction model to the Hugging Face Model Hub (not Spaces).

## 📋 Prerequisites

✅ **Already completed:**

- [x] Trained model saved as `house_price_model.joblib`
- [x] Preprocessing pipeline saved as `preprocessing_pipeline.joblib`
- [x] Python inference API (`inference.py`)
- [x] Comprehensive README.md (model card)
- [x] requirements.txt with dependencies
- [x] LICENSE file (MIT)
- [x] .gitattributes for Git LFS
- [x] Example usage script

**You need:**

- [ ] Hugging Face account ([Sign up here](https://huggingface.co/join))
- [ ] Git installed on your system
- [ ] Git LFS installed ([Download here](https://git-lfs.github.com/))
- [ ] Hugging Face CLI installed

## 🔧 Step 1: Install Hugging Face CLI

Open PowerShell and run:

```powershell
pip install huggingface_hub
```

## 🔑 Step 2: Login to Hugging Face

```powershell
huggingface-cli login
```

You'll be prompted to enter your Hugging Face token. Get your token from:
<https://huggingface.co/settings/tokens>

## 📦 Step 3: Initialize Git LFS

Make sure Git LFS is installed and initialized:

```powershell
# Install Git LFS (if not already installed)
# Download from: https://git-lfs.github.com/

# Initialize Git LFS
git lfs install
```

## 🎯 Step 4: Create Model Repository on Hugging Face

### Option A: Using the Web Interface

1. Go to <https://huggingface.co/new>
2. Choose a repository name (e.g., `house-price-prediction`)
3. Set to **Public** or **Private**
4. Click "Create Model"

### Option B: Using CLI

```powershell
huggingface-cli repo create house-price-prediction --type model
```

## 📤 Step 5: Push Your Model

Navigate to your project directory and run:

```powershell
cd "d:\My House Price Project"

# Initialize git (if not already initialized)
git init

# Add Git LFS tracking for model files
git lfs install
git lfs track "*.joblib"

# Add all files
git add .

# Commit
git commit -m "Initial commit: California House Price Prediction Model"

# Add remote (replace YOUR_USERNAME with your Hugging Face username)
git remote add origin https://huggingface.co/YOUR_USERNAME/house-price-prediction

# Push to Hugging Face
git push -u origin main
```

### If you encounter authentication issues

Use your Hugging Face username and your **access token** as password when prompted.

## 🏷️ Step 6: Add Model Tags (Optional but Recommended)

Edit your model card on Hugging Face web interface or add to the top of README.md:

```yaml
---
tags:
- tabular
- regression
- scikit-learn
- house-prices
- california
- random-forest
- real-estate
license: mit
datasets:
- california-housing
metrics:
- rmse
library_name: sklearn
---
```

## ✅ Step 7: Verify Deployment

1. Visit `https://huggingface.co/YOUR_USERNAME/house-price-prediction`
2. Check that all files are visible:
   - README.md displays as model card
   - Model files (*.joblib) show LFS badge
   - inference.py and other files are accessible

## 📥 Step 8: Test Loading from Hub (Optional)

Users can now clone and use your model:

```python
from huggingface_hub import hf_hub_download
import joblib

# Download model files
model_path = hf_hub_download(
    repo_id="YOUR_USERNAME/house-price-prediction",
    filename="house_price_model.joblib"
)
pipeline_path = hf_hub_download(
    repo_id="YOUR_USERNAME/house-price-prediction",
    filename="preprocessing_pipeline.joblib"
)

# Load model
model = joblib.load(model_path)
pipeline = joblib.load(pipeline_path)

print("✅ Model loaded from Hugging Face Hub!")
```

Or simply clone the entire repo:

```bash
git clone https://huggingface.co/YOUR_USERNAME/house-price-prediction
cd house-price-prediction
python inference.py
```

## 🔄 Step 9: Update Your Model (Future Updates)

When you make changes:

```powershell
cd "d:\My House Price Project"

# Make your changes, then:
git add .
git commit -m "Description of changes"
git push
```

## 🌟 Step 10: Make Your Model Discoverable

1. **Add a good description** on the Hugging Face web interface
2. **Add relevant tags**: tabular, regression, scikit-learn, etc.
3. **Fill in the model card** with detailed information
4. **Add examples** in the README
5. **Share on social media** or the Hugging Face forums

## 📊 Difference: Model Hub vs Spaces

You're deploying to **Model Hub** (not Spaces):

| Feature | Model Hub | Spaces |
|---------|-----------|--------|
| Purpose | Host model files + docs | Host interactive demos |
| Files | Model artifacts (.joblib, .pkl, etc.) | App code (app.py, requirements.txt) |
| Interface | Repository with model card | Live web application (Gradio/Streamlit) |
| Usage | Download and use programmatically | Interactive web UI |
| What you did | ✅ This guide | ❌ Different (would need app.py) |

## 🆘 Troubleshooting

### Large file errors?

Make sure Git LFS is properly configured:

```powershell
git lfs track "*.joblib"
git add .gitattributes
git commit -m "Add LFS tracking"
```

### Authentication failed?

Use your Hugging Face access token (not password) when pushing.

### Model not showing up?

Wait a few minutes, then refresh. Check your repository on huggingface.co.

## 🎉 Success

Your model is now on Hugging Face Model Hub!

Next steps:

- Share your model with the community
- Add more examples and documentation
- Consider creating a Gradio Space for an interactive demo (separate from this)
- Collect feedback and iterate

---

**Need help?** Visit the [Hugging Face forums](https://discuss.huggingface.co/)
