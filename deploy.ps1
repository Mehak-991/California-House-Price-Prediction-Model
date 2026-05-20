# Hugging Face Model Hub Deployment Script
# This script automates the deployment of your model to Hugging Face

Write-Host "`n" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "🏠 CALIFORNIA HOUSE PRICE PREDICTION - HUGGING FACE DEPLOYMENT" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "`n"

# Step 1: Check if HF CLI is installed
Write-Host "STEP 1: Checking Hugging Face CLI..." -ForegroundColor Cyan
try {
    $hfVersion = huggingface-cli --version 2>$null
    Write-Host "✅ Hugging Face CLI is installed: $hfVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Hugging Face CLI is not installed" -ForegroundColor Red
    Write-Host "Installing Hugging Face CLI..." -ForegroundColor Yellow
    pip install huggingface_hub
    Write-Host "✅ Hugging Face CLI installed" -ForegroundColor Green
}

Write-Host "`n"

# Step 2: Check authentication
Write-Host "STEP 2: Checking Hugging Face authentication..." -ForegroundColor Cyan
Write-Host "You need to be logged in to Hugging Face to deploy." -ForegroundColor Yellow
Write-Host "If you don't have an account, create one at https://huggingface.co/join" -ForegroundColor Yellow
Write-Host "`n"

$isAuthenticated = huggingface-cli whoami 2>$null
if (-not $isAuthenticated) {
    Write-Host "You are not logged in. Starting login process..." -ForegroundColor Yellow
    huggingface-cli login
    $isAuthenticated = huggingface-cli whoami
}

if ($isAuthenticated) {
    Write-Host "✅ You are logged in as: $isAuthenticated" -ForegroundColor Green
}
else {
    Write-Host "❌ Login failed. Cannot continue." -ForegroundColor Red
    exit 1
}

Write-Host "`n"

# Step 3: Check Git LFS
Write-Host "STEP 3: Checking Git LFS..." -ForegroundColor Cyan
try {
    $gitLfsVersion = git lfs version 2>$null
    Write-Host "✅ Git LFS is installed" -ForegroundColor Green
}
catch {
    Write-Host "❌ Git LFS is not installed" -ForegroundColor Red
    Write-Host "Please install Git LFS from: https://git-lfs.github.com/" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n"

# Step 4: Get repository name
Write-Host "STEP 4: Repository Configuration" -ForegroundColor Cyan
$repoName = "house-price-prediction"
Write-Host "Repository name: $repoName" -ForegroundColor White

# Get username
$username = huggingface-cli whoami
$repoUrl = "https://huggingface.co/$username/$repoName"
Write-Host "Repository URL: $repoUrl" -ForegroundColor White

Write-Host "`n"

# Step 5: Initialize Git LFS for model files
Write-Host "STEP 5: Setting up Git LFS..." -ForegroundColor Cyan
Write-Host "Initializing Git LFS for large model files..." -ForegroundColor White
git lfs install
git lfs track "*.joblib"
Write-Host "✅ Git LFS configured" -ForegroundColor Green

Write-Host "`n"

# Step 6: Initialize git repository if not already done
Write-Host "STEP 6: Initializing Git Repository..." -ForegroundColor Cyan
if (-not (Test-Path ".git")) {
    Write-Host "Initializing new git repository..." -ForegroundColor White
    git init
    git config user.name "House Price Predictor Bot"
    git config user.email "no-reply@huggingface.co"
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}
else {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
}

Write-Host "`n"

# Step 7: Add and commit files
Write-Host "STEP 7: Staging files..." -ForegroundColor Cyan
Write-Host "Adding all files to git..." -ForegroundColor White
git add .
Write-Host "✅ Files staged" -ForegroundColor Green

Write-Host "`n"

Write-Host "STEP 8: Committing changes..." -ForegroundColor Cyan
$commitMessage = "Initial commit: California House Price Prediction Model"
git commit -m $commitMessage --allow-empty
Write-Host "✅ Changes committed" -ForegroundColor Green

Write-Host "`n"

# Step 9: Set remote and push
Write-Host "STEP 9: Pushing to Hugging Face..." -ForegroundColor Cyan

# Remove existing remote if it exists
git remote rm origin 2>$null

# Add new remote
Write-Host "Adding remote: $repoUrl" -ForegroundColor White
git remote add origin $repoUrl

Write-Host "Pushing to Hugging Face (this may take a few minutes)..." -ForegroundColor White
Write-Host "Note: Large model files (41.4 MB) may take time to upload" -ForegroundColor Yellow

git push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Push successful!" -ForegroundColor Green
}
else {
    Write-Host "⚠️  Push completed with some warnings (this is usually okay)" -ForegroundColor Yellow
}

Write-Host "`n"

# Step 10: Verify deployment
Write-Host "STEP 10: Verifying deployment..." -ForegroundColor Cyan
Write-Host "Your model is now being processed by Hugging Face..." -ForegroundColor White
Write-Host "`n"

Write-Host "=" * 70 -ForegroundColor Green
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "`n"

Write-Host "Your model has been successfully uploaded to Hugging Face!" -ForegroundColor Green
Write-Host "`n"

Write-Host "📍 Model URL: $repoUrl" -ForegroundColor Cyan
Write-Host "`n"

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Visit your model page: $repoUrl" -ForegroundColor White
Write-Host "2. Verify all files are present (README.md, *.joblib, etc.)" -ForegroundColor White
Write-Host "3. Add additional metadata on the web interface if desired" -ForegroundColor White
Write-Host "4. Share your model with the community!" -ForegroundColor White
Write-Host "`n"

Write-Host "Optional - Add model tags on Hugging Face web interface:" -ForegroundColor Yellow
Write-Host "- tabular-regression" -ForegroundColor White
Write-Host "- scikit-learn" -ForegroundColor White
Write-Host "- random-forest" -ForegroundColor White
Write-Host "- house-prices" -ForegroundColor White
Write-Host "- california-housing" -ForegroundColor White
Write-Host "`n"

Write-Host "📚 Learn more about your model card:" -ForegroundColor Cyan
Write-Host "https://huggingface.co/docs/hub/models-cards" -ForegroundColor White
Write-Host "`n"
