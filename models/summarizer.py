"""Destination summarizer model for TripyTrek."""

import logging
from typing import Dict, Any, List, Optional, Union
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from utils import load_config, cache_result

logger = logging.getLogger(__name__)

class DestinationSummarizer:
    """
    AI model for summarizing destination descriptions.
    Uses pre-trained transformer models for text summarization.
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the summarizer model.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path).get("model", {}).get("summarizer", {})
        self.model_name = self.config.get("model_name", "facebook/bart-large-cnn")
        self.max_length = self.config.get("max_length", 150)
        self.min_length = self.config.get("min_length", 40)
        
        logger.info(f"Initializing summarizer with model: {self.model_name}")
        
        # Load model and tokenizer
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            logger.info("Summarizer model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading summarizer model: {e}")
            # Fallback to a simpler model in case of errors
            self.model_name = "sshleifer/distilbart-cnn-6-6"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
    
    @cache_result
    def summarize(self, text: str) -> str:
        """
        Generate a concise summary of a destination description.
        
        Args:
            text: Destination description text to summarize
            
        Returns:
            Summarized text highlighting key aspects of the destination
        """
        if not text or len(text.strip()) < 100:
            logger.warning("Input text too short for summarization")
            return text
        
        try:
            # Truncate if text is too long
            max_input_length = 1024
            if len(text) > max_input_length:
                text = text[:max_input_length]
            
            inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
            
            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=self.max_length,
                min_length=self.min_length,
                num_beams=4,
                early_stopping=True
            )
            
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            # Fallback to simple extractive summarization
            sentences = text.split(". ")
            if len(sentences) <= 3:
                return text
            return ". ".join(sentences[:3]) + "."
    
    def format_travel_highlight(self, summary: str, destination: str) -> str:
        """
        Format the summary as a travel highlight.
        
        Args:
            summary: Generated summary text
            destination: Name of the destination
            
        Returns:
            Formatted travel highlight
        """
        return (
            f"✨ TRIPYTREK HIGHLIGHT: {destination.upper()} ✨\n\n"
            f"{summary}\n\n"
            f"Discover more about {destination} on TripyTrek."
        )
