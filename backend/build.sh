#!/bin/bash
# Exit on error
set -e

# Print commands for debugging
set -x

# Python version
python --version

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies with minimal deployment requirements
# Using requirements-deploy.txt to avoid any packages that require Rust compilation
pip install -r requirements-deploy.txt

# Create required directories if needed
mkdir -p logs

# List installed packages (for debugging)
pip list

# Verify uvicorn is installed
which uvicorn || echo "uvicorn not found in PATH"
