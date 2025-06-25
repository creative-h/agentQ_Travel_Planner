"""Travel services for TripyTrek."""

import logging
from typing import Dict, Any, List, Optional, Union
import pandas as pd
import os

from models.summarizer import DestinationSummarizer
from models.review_classifier import ReviewClassifier
from models.recommendation_engine import RecommendationEngine
from utils import load_config

logger = logging.getLogger(__name__)

class TravelService:
    """
    Service layer connecting the models with the UI.
    Handles business logic and coordinates model interactions.
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize travel service.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
        self.summarizer = DestinationSummarizer(config_path)
        self.review_classifier = ReviewClassifier(config_path)
        self.recommendation_engine = RecommendationEngine(config_path)
        
        logger.info("TravelService initialized")
    
    def generate_destination_summary(self, destination_name: str, description: str) -> Dict[str, Any]:
        """
        Generate a summary for a destination.
        
        Args:
            destination_name: Name of the destination
            description: Text description of the destination
            
        Returns:
            Dictionary with summary and formatting
        """
        logger.info(f"Generating summary for {destination_name}")
        
        try:
            summary = self.summarizer.summarize(description)
            formatted_summary = self.summarizer.format_travel_highlight(summary, destination_name)
            
            return {
                "destination": destination_name,
                "original_length": len(description),
                "summary_length": len(summary),
                "summary": summary,
                "formatted_summary": formatted_summary,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return {
                "destination": destination_name,
                "success": False,
                "error": str(e)
            }
    
    def analyze_review(self, review_title: str, review_text: str) -> Dict[str, Any]:
        """
        Analyze a travel review.
        
        Args:
            review_title: Title of the review
            review_text: Full text of the review
            
        Returns:
            Dictionary with ratings and analysis
        """
        logger.info(f"Analyzing review: {review_title}")
        
        try:
            analysis = self.review_classifier.analyze_review(review_text, review_title)
            
            return {
                "title": review_title,
                "success": True,
                "overall_score": analysis["overall_score"],
                "category_ratings": analysis["category_ratings"],
                "pros": analysis["pros"],
                "cons": analysis["cons"],
                "summary": analysis["summary"]
            }
        except Exception as e:
            logger.error(f"Error analyzing review: {e}")
            return {
                "title": review_title,
                "success": False,
                "error": str(e)
            }
    
    def get_recommendations(self, interests: List[str], 
                           budget: int, 
                           previous_destinations: List[str] = None) -> Dict[str, Any]:
        """
        Get destination recommendations.
        
        Args:
            interests: List of user interests
            budget: Daily budget in USD
            previous_destinations: List of previously visited destinations
            
        Returns:
            Dictionary with recommended destinations
        """
        logger.info(f"Getting recommendations for interests: {interests}, budget: ${budget}")
        
        try:
            recommendations = self.recommendation_engine.recommend_destinations(
                user_interests=interests,
                budget=budget,
                previous_destinations=previous_destinations or []
            )
            
            return {
                "success": True,
                "count": len(recommendations),
                "recommendations": recommendations,
                "user_inputs": {
                    "interests": interests,
                    "budget": budget,
                    "previous_destinations": previous_destinations or []
                }
            }
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return {
                "success": False,
                "error": str(e),
                "user_inputs": {
                    "interests": interests,
                    "budget": budget
                }
            }
    
    def get_similar_destinations(self, destination_name: str) -> Dict[str, Any]:
        """
        Get destinations similar to a specified one.
        
        Args:
            destination_name: Name of the target destination
            
        Returns:
            Dictionary with similar destinations
        """
        logger.info(f"Finding destinations similar to: {destination_name}")
        
        try:
            similar = self.recommendation_engine.similar_destinations(destination_name)
            
            return {
                "success": True,
                "target_destination": destination_name,
                "similar_destinations": similar,
                "count": len(similar)
            }
        except Exception as e:
            logger.error(f"Error finding similar destinations: {e}")
            return {
                "success": False,
                "target_destination": destination_name,
                "error": str(e)
            }
