"""Recommendation engine for TripyTrek."""

import logging
import numpy as np
from typing import Dict, Any, List, Optional, Union, Tuple
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from utils import load_config, cache_result

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    AI-powered recommendation engine for suggesting travel destinations.
    Uses a combination of content-based filtering and rule-based systems.
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the recommendation engine.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path).get("model", {}).get("recommendation_engine", {})
        self.similarity_threshold = self.config.get("similarity_threshold", 0.7)
        self.max_recommendations = self.config.get("max_recommendations", 5)
        self.budget_weight = self.config.get("budget_weight", 0.3)
        self.interest_weight = self.config.get("interest_weight", 0.6)
        self.popularity_weight = self.config.get("popularity_weight", 0.1)
        
        logger.info("Initializing recommendation engine")
        
        # Load embedding model for semantic similarity
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Recommendation embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            self.embedding_model = None
        
        # Load dummy destination data (would be replaced with real data in production)
        self.destinations = self._load_dummy_destinations()
    
    def _load_dummy_destinations(self) -> pd.DataFrame:
        """
        Load dummy destination data for testing and development.
        
        Returns:
            DataFrame containing destination information
        """
        destinations = [
            {
                "id": 1,
                "name": "Bali, Indonesia",
                "description": "Tropical paradise with beautiful beaches, vibrant culture, and lush rice terraces.",
                "budget_level": "medium",  # low, medium, high, luxury
                "categories": ["beach", "culture", "nature", "food"],
                "avg_cost_per_day": 50,  # USD
                "best_seasons": ["April", "May", "June", "September"],
                "popularity": 0.9,  # 0-1 scale
                "image_url": "https://example.com/bali.jpg"
            },
            {
                "id": 2,
                "name": "Paris, France",
                "description": "City of lights and romance with iconic landmarks, world-class museums, and exquisite cuisine.",
                "budget_level": "high",
                "categories": ["culture", "food", "history", "city"],
                "avg_cost_per_day": 150,
                "best_seasons": ["April", "May", "June", "September", "October"],
                "popularity": 0.95,
                "image_url": "https://example.com/paris.jpg"
            },
            {
                "id": 3,
                "name": "Kyoto, Japan",
                "description": "Ancient capital with thousands of temples, traditional gardens, and geisha culture.",
                "budget_level": "high",
                "categories": ["culture", "history", "food", "nature"],
                "avg_cost_per_day": 100,
                "best_seasons": ["March", "April", "October", "November"],
                "popularity": 0.8,
                "image_url": "https://example.com/kyoto.jpg"
            },
            {
                "id": 4,
                "name": "Cusco, Peru",
                "description": "Gateway to Machu Picchu with stunning Incan architecture and high-altitude Andean landscapes.",
                "budget_level": "medium",
                "categories": ["adventure", "history", "culture", "nature"],
                "avg_cost_per_day": 60,
                "best_seasons": ["May", "June", "July", "August", "September"],
                "popularity": 0.7,
                "image_url": "https://example.com/cusco.jpg"
            },
            {
                "id": 5,
                "name": "Cape Town, South Africa",
                "description": "Coastal city with Table Mountain views, diverse culture, and nearby wildlife.",
                "budget_level": "medium",
                "categories": ["nature", "wildlife", "city", "food", "beach"],
                "avg_cost_per_day": 70,
                "best_seasons": ["January", "February", "March", "November", "December"],
                "popularity": 0.75,
                "image_url": "https://example.com/capetown.jpg"
            },
            {
                "id": 6,
                "name": "Bangkok, Thailand",
                "description": "Bustling metropolis with ornate shrines, vibrant street life, and world-renowned street food.",
                "budget_level": "low",
                "categories": ["food", "culture", "city", "budget"],
                "avg_cost_per_day": 30,
                "best_seasons": ["November", "December", "January", "February"],
                "popularity": 0.85,
                "image_url": "https://example.com/bangkok.jpg"
            },
            {
                "id": 7,
                "name": "New York City, USA",
                "description": "Iconic skyline, Broadway shows, diverse neighborhoods, and world-class museums and restaurants.",
                "budget_level": "high",
                "categories": ["city", "culture", "food", "nightlife", "shopping"],
                "avg_cost_per_day": 200,
                "best_seasons": ["April", "May", "September", "October", "December"],
                "popularity": 0.9,
                "image_url": "https://example.com/nyc.jpg"
            },
            {
                "id": 8,
                "name": "Santorini, Greece",
                "description": "Stunning island with white-washed buildings, blue domes, and breathtaking Aegean Sea views.",
                "budget_level": "high",
                "categories": ["beach", "romantic", "food", "luxury"],
                "avg_cost_per_day": 150,
                "best_seasons": ["May", "June", "September", "October"],
                "popularity": 0.85,
                "image_url": "https://example.com/santorini.jpg"
            },
            {
                "id": 9,
                "name": "Hanoi, Vietnam",
                "description": "Ancient capital with French colonial architecture, bustling Old Quarter, and incredible street food.",
                "budget_level": "low",
                "categories": ["food", "culture", "history", "budget", "city"],
                "avg_cost_per_day": 25,
                "best_seasons": ["October", "November", "April", "May"],
                "popularity": 0.7,
                "image_url": "https://example.com/hanoi.jpg"
            },
            {
                "id": 10,
                "name": "Queenstown, New Zealand",
                "description": "Adventure capital surrounded by mountains and lakes, perfect for outdoor activities.",
                "budget_level": "high",
                "categories": ["adventure", "nature", "outdoor", "scenic"],
                "avg_cost_per_day": 120,
                "best_seasons": ["December", "January", "February", "March"],
                "popularity": 0.75,
                "image_url": "https://example.com/queenstown.jpg"
            }
        ]
        
        return pd.DataFrame(destinations)
    
    @cache_result
    def get_destination_embeddings(self) -> Dict[int, np.ndarray]:
        """
        Calculate embeddings for all destinations.
        
        Returns:
            Dictionary mapping destination IDs to embedding vectors
        """
        if not self.embedding_model:
            logger.warning("Embedding model not available")
            return {}
            
        embeddings = {}
        for _, row in self.destinations.iterrows():
            dest_text = f"{row['name']} {row['description']} {' '.join(row['categories'])}"
            embedding = self.embedding_model.encode(dest_text)
            embeddings[row['id']] = embedding
            
        return embeddings
    
    def _calculate_budget_score(self, user_budget: int, destination_cost: int) -> float:
        """
        Calculate how well a destination matches a user's budget.
        
        Args:
            user_budget: User's daily budget in USD
            destination_cost: Destination's average cost per day in USD
            
        Returns:
            Score from 0 to 1, where 1 is a perfect budget match
        """
        # Perfect match if destination is at or under budget
        if destination_cost <= user_budget:
            return 1.0
            
        # Calculate penalty for exceeding budget
        ratio = destination_cost / user_budget
        if ratio > 2:  # More than double the budget
            return 0.0
        
        # Linear penalty between 1x and 2x budget
        return max(0, 1 - (ratio - 1))
    
    def _calculate_interest_match(self, user_interests: List[str], 
                                destination_categories: List[str]) -> float:
        """
        Calculate how well a destination matches a user's interests.
        
        Args:
            user_interests: List of user's travel interests/preferences
            destination_categories: List of destination's categories/tags
            
        Returns:
            Score from 0 to 1, where 1 is a perfect interest match
        """
        if not user_interests or not destination_categories:
            return 0.5  # Neutral score if no data
            
        # Count matching interests
        matches = sum(1 for interest in user_interests 
                     if any(interest.lower() in category.lower() 
                            for category in destination_categories))
                            
        # Calculate match percentage
        if matches == 0:
            return 0.1  # Small baseline score even with no matches
            
        return min(1.0, matches / len(user_interests))
    
    def recommend_destinations(self, user_interests: List[str], 
                              budget: int, 
                              previous_destinations: List[str] = None) -> List[Dict[str, Any]]:
        """
        Generate personalized destination recommendations.
        
        Args:
            user_interests: List of user's travel interests
            budget: User's daily budget in USD
            previous_destinations: List of previously visited destinations
            
        Returns:
            List of recommended destinations with scores and details
        """
        if not user_interests:
            logger.warning("No user interests provided for recommendations")
            # Return popular destinations if no interests specified
            return self._get_popular_destinations()
            
        previous_destinations = previous_destinations or []
        
        # Calculate scores for each destination
        scored_destinations = []
        
        for _, dest in self.destinations.iterrows():
            # Skip already visited destinations
            if dest["name"] in previous_destinations:
                continue
                
            # Calculate component scores
            budget_score = self._calculate_budget_score(budget, dest["avg_cost_per_day"])
            interest_score = self._calculate_interest_match(user_interests, dest["categories"])
            popularity_score = dest["popularity"]
            
            # Calculate weighted total score
            total_score = (
                self.budget_weight * budget_score + 
                self.interest_weight * interest_score +
                self.popularity_weight * popularity_score
            )
            
            # Add to results if score is above threshold
            if total_score >= 0.4:  # Lower threshold to ensure some results
                scored_destinations.append({
                    "id": dest["id"],
                    "name": dest["name"],
                    "description": dest["description"],
                    "budget_level": dest["budget_level"],
                    "avg_cost_per_day": dest["avg_cost_per_day"],
                    "score": round(total_score, 2),
                    "match_details": {
                        "budget_match": round(budget_score, 2),
                        "interest_match": round(interest_score, 2),
                    },
                    "image_url": dest["image_url"],
                    "categories": dest["categories"]
                })
        
        # Sort by score and return top recommendations
        scored_destinations.sort(key=lambda x: x["score"], reverse=True)
        return scored_destinations[:self.max_recommendations]
    
    def _get_popular_destinations(self) -> List[Dict[str, Any]]:
        """Return a list of popular destinations if no user preferences are provided."""
        popular = self.destinations.sort_values("popularity", ascending=False).head(self.max_recommendations)
        
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "budget_level": row["budget_level"],
                "avg_cost_per_day": row["avg_cost_per_day"],
                "score": row["popularity"],
                "match_details": {
                    "popularity": row["popularity"],
                },
                "image_url": row["image_url"],
                "categories": row["categories"]
            }
            for _, row in popular.iterrows()
        ]
    
    def similar_destinations(self, destination_name: str) -> List[Dict[str, Any]]:
        """
        Find destinations similar to a given destination.
        
        Args:
            destination_name: Name of the target destination
            
        Returns:
            List of similar destinations
        """
        # Find the destination in our dataset
        target_dest = self.destinations[self.destinations["name"].str.contains(destination_name, case=False)]
        
        if target_dest.empty:
            logger.warning(f"Destination '{destination_name}' not found")
            return []
            
        target_id = target_dest.iloc[0]["id"]
        
        # Get all destination embeddings
        embeddings = self.get_destination_embeddings()
        if not embeddings:
            # Fallback to category-based matching
            return self._similar_by_category(target_dest.iloc[0])
            
        # Calculate similarities
        target_embedding = embeddings.get(target_id)
        if target_embedding is None:
            return []
            
        similarities = []
        for dest_id, embedding in embeddings.items():
            if dest_id != target_id:
                similarity = cosine_similarity([target_embedding], [embedding])[0][0]
                similarities.append((dest_id, similarity))
        
        # Sort by similarity and get top matches
        similarities.sort(key=lambda x: x[1], reverse=True)
        similar_ids = [id for id, sim in similarities[:5]]
        
        # Get destination details
        similar_dests = []
        for dest_id in similar_ids:
            dest = self.destinations[self.destinations["id"] == dest_id].iloc[0].to_dict()
            similar_dests.append({
                "id": dest["id"],
                "name": dest["name"],
                "description": dest["description"],
                "budget_level": dest["budget_level"],
                "similarity_score": round(next(sim for id, sim in similarities if id == dest_id), 2),
                "image_url": dest["image_url"],
                "categories": dest["categories"]
            })
            
        return similar_dests
    
    def _similar_by_category(self, target_dest: pd.Series) -> List[Dict[str, Any]]:
        """Find similar destinations based on matching categories."""
        target_categories = set(target_dest["categories"])
        results = []
        
        for _, dest in self.destinations.iterrows():
            if dest["id"] == target_dest["id"]:
                continue
                
            # Calculate category overlap
            dest_categories = set(dest["categories"])
            overlap = len(target_categories.intersection(dest_categories))
            
            if overlap > 0:
                similarity_score = overlap / len(target_categories.union(dest_categories))
                
                results.append({
                    "id": dest["id"],
                    "name": dest["name"],
                    "description": dest["description"],
                    "budget_level": dest["budget_level"],
                    "similarity_score": round(similarity_score, 2),
                    "image_url": dest["image_url"],
                    "categories": dest["categories"]
                })
        
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:5]
