#!/bin/bash
# Exit on error
set -e

# Print commands for debugging
set -x

# Print environment info
echo "====== ENVIRONMENT INFO ======"
python --version
pip --version
echo "====== END ENVIRONMENT INFO ======"

# Create virtual environment directly with system packages
python -m venv .venv --system-site-packages

# Activate virtual environment
source .venv/bin/activate

# Install only pip and wheel first
pip install --upgrade pip wheel setuptools

# Force reinstall of basic packages without dependencies
echo "====== INSTALLING MINIMAL DEPENDENCIES ======"
pip install --no-deps fastapi uvicorn pydantic python-dotenv requests aiohttp

# Install the rest making sure to skip problematic compile-time dependencies
echo "====== INSTALLING FROM REQUIREMENTS FILE ======"
PYTHON_BINARY_BUILD=0 PIP_NO_BUILD_ISOLATION=1 pip install -r requirements-deploy.txt --no-cache-dir

# Create required directories if needed
mkdir -p logs

# Debug info
echo "====== INSTALLED PACKAGES ======"
pip freeze

# Double check for important packages
echo "====== CHECKING FOR CRITICAL PACKAGES ======"
pip show fastapi || echo "fastapi not installed!"
pip show uvicorn || echo "uvicorn not installed!"
pip show aiohttp || echo "aiohttp not installed!"

# Check if uvicorn is in the path
echo "====== CHECKING FOR UVICORN EXECUTABLE ======"
which uvicorn || echo "uvicorn not found in PATH"
find .venv -name "uvicorn" -type f -executable
