#!/usr/bin/env bash
set -e

echo "Python version:"
python --version

echo "Installing dependencies with binary-only preference..."
pip install --upgrade pip
pip install --prefer-binary -r requirements.txt

echo "Build complete."
