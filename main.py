"""Main entry point for TripyTrek application."""

import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.app import TripyTrekApp
from utils import setup_logging, ensure_directories, load_config

def main():
    """Main entry point for the application."""
    # Ensure required directories exist
    ensure_directories()
    
    # Set up logging
    config = load_config("config/config.yaml")
    log_level = config.get("app", {}).get("log_level", "INFO")
    setup_logging(log_level)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting TripyTrek application")
    
    # Create and launch the app
    app = TripyTrekApp()
    app.launch(share=True)

if __name__ == "__main__":
    main()
