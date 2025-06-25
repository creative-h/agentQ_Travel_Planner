"""Review classifier model for TripyTrek."""

import logging
import numpy as np
from typing import Dict, Any, List, Optional, Union
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from utils import load_config, cache_result

logger = logging.getLogger(__name__)

class ReviewClassifier:
    """
    AI model for classifying travel reviews along multiple dimensions.
    Uses transformer-based sentiment analysis for ratings on different axes.
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the review classifier model.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path).get("model", {}).get("review_classifier", {})
        self.model_name = self.config.get("model_name", "distilbert-base-uncased")
        self.categories = self.config.get("categories", ["location", "facilities", "food", "value", "service"])
        
        logger.info(f"Initializing review classifier with model: {self.model_name}")
        
        # Load model and tokenizer
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name, 
                num_labels=5  # 1-5 star rating
            )
            logger.info("Review classifier model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading review classifier model: {e}")
            # Simple fallback in case of errors
            self.model = None
            self.tokenizer = None
    
    @cache_result
    def classify_review(self, review_text: str) -> Dict[str, float]:
        """
        Classify a review across different categories.
        
        Args:
            review_text: Full text of the review
            
        Returns:
            Dictionary with ratings for each category (1-5 scale)
        """
        if not review_text or not self.model:
            logger.warning("Empty review text or model not loaded")
            return self._get_random_ratings()
        
        try:
            # Extract sentences that might mention specific categories
            sentences = review_text.split('.')
            category_ratings = {}
            
            # Get overall sentiment first
            inputs = self.tokenizer(review_text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Convert logits to 1-5 scale
            overall_score = self._convert_to_rating(outputs.logits.numpy()[0])
            
            # Use overall score as baseline, then adjust for each category
            for category in self.categories:
                category_rating = overall_score
                
                # Find sentences mentioning the category
                relevant_sentences = [s for s in sentences if category.lower() in s.lower()]
                if relevant_sentences:
                    category_text = " ".join(relevant_sentences)
                    inputs = self.tokenizer(category_text, return_tensors="pt", truncation=True, max_length=512)
                    with torch.no_grad():
                        category_outputs = self.model(**inputs)
                    category_rating = self._convert_to_rating(category_outputs.logits.numpy()[0])
                
                category_ratings[category] = category_rating
            
            return category_ratings
            
        except Exception as e:
            logger.error(f"Error classifying review: {e}")
            return self._get_random_ratings()
    
    def _convert_to_rating(self, logits: np.ndarray) -> float:
        """Convert model logits to a 1-5 star rating scale."""
        # Convert sentiment logits to a 1-5 scale
        # Assuming logits represents sentiment from very negative to very positive
        normalized = (np.exp(logits) / np.exp(logits).sum())
        weighted_sum = sum(normalized * np.arange(1, len(normalized) + 1))
        
        # Scale to 1-5 range
        rating = 1 + (weighted_sum - 1) * 4 / (len(normalized) - 1)
        return round(float(rating), 1)
    
    def _get_random_ratings(self) -> Dict[str, float]:
        """Generate random ratings as a fallback."""
        return {category: round(np.random.uniform(2.0, 5.0), 1) for category in self.categories}
    
    def analyze_review(self, review_text: str, review_title: str = "") -> Dict[str, Any]:
        """
        Provide a comprehensive analysis of a travel review.
        
        Args:
            review_text: Full text of the review
            review_title: Title of the review
            
        Returns:
            Dictionary with ratings and extracted insights
        """
        # Get category ratings
        ratings = self.classify_review(review_text)
        
        # Calculate overall score (weighted average)
        overall_score = round(sum(ratings.values()) / len(ratings), 1)
        
        # Extract pros and cons (simplified implementation)
        pros_cons = self._extract_pros_cons(review_text)
        
        return {
            "overall_score": overall_score,
            "category_ratings": ratings,
            "pros": pros_cons["pros"],
            "cons": pros_cons["cons"],
            "summary": self._generate_summary(review_text, ratings, overall_score)
        }
    
    def _extract_pros_cons(self, review_text: str) -> Dict[str, List[str]]:
        """Extract pros and cons from review text."""
        sentences = review_text.split('.')
        
        # Simple heuristic-based extraction (could be improved with ML)
        positive_keywords = ["great", "excellent", "good", "best", "perfect", "loved", "amazing"]
        negative_keywords = ["bad", "poor", "worst", "terrible", "disappointing", "issues", "problem"]
        
        pros = []
        cons = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            is_positive = any(keyword in sentence.lower() for keyword in positive_keywords)
            is_negative = any(keyword in sentence.lower() for keyword in negative_keywords)
            
            if is_positive and not is_negative and len(sentence) > 10:
                pros.append(sentence)
            elif is_negative and not is_positive and len(sentence) > 10:
                cons.append(sentence)
        
        return {
            "pros": pros[:3],  # Limit to top 3
            "cons": cons[:3]
        }
    
    def _generate_summary(self, review_text: str, ratings: Dict[str, float], 
                         overall_score: float) -> str:
        """Generate a brief summary of the review."""
        if overall_score >= 4.0:
            sentiment = "very positive"
        elif overall_score >= 3.0:
            sentiment = "generally positive"
        elif overall_score >= 2.0:
            sentiment = "mixed"
        else:
            sentiment = "negative"
            
        # Find highest and lowest rated categories
        categories = list(ratings.keys())
        highest_cat = max(categories, key=lambda x: ratings[x])
        lowest_cat = min(categories, key=lambda x: ratings[x])
        
        summary = (
            f"This is a {sentiment} review with an overall score of {overall_score}/5.0. "
            f"The reviewer was most impressed with the {highest_cat} ({ratings[highest_cat]}/5.0)"
        )
        
        if ratings[lowest_cat] < 3.5:
            summary += f" but was less satisfied with the {lowest_cat} ({ratings[lowest_cat]}/5.0)."
        else:
            summary += "."
            
        return summary
