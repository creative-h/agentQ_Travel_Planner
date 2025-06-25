"""Utility functions for the TripyTrek application."""

import os
import yaml
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict containing configuration parameters
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

def setup_logging(log_level: str = "INFO") -> None:
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def ensure_directories() -> None:
    """Create necessary directories if they don't exist."""
    directories = ["data", "models", "config", "notebooks", "services", "ui"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create subdirectories
    data_dirs = ["data/raw", "data/processed", "data/cache"]
    for directory in data_dirs:
        os.makedirs(directory, exist_ok=True)

def cache_result(func):
    """Decorator to cache function results."""
    cache = {}
    
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper
