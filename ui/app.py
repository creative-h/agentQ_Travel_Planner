"""TripyTrek Gradio UI application."""

import os
import sys
import logging
from typing import Dict, Any, List, Optional, Union

import gradio as gr
import pandas as pd
import numpy as np

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.travel_service import TravelService
from utils import load_config, setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Load configuration
config = load_config("config/config.yaml")

class TripyTrekApp:
    """
    TripyTrek Gradio UI application.
    Implements the user interface for the AI-powered travel platform.
    """
    
    def __init__(self):
        """Initialize the TripyTrek Gradio application."""
        self.travel_service = TravelService()
        self.ui_config = config.get("ui", {})
        self.title = self.ui_config.get("title", "TripyTrek - AI Travel Discovery")
        self.description = self.ui_config.get("description", 
                                             "Explore destinations, read AI-generated reviews, and get personalized recommendations")
        self.primary_color = self.ui_config.get("primary_color", "#4B6BFB")
        self.theme = gr.themes.Default().set(
            primary_hue=self.primary_color.lstrip('#'),
        )
        
        logger.info("TripyTrek UI initialized")
    
    def build_destination_summary_tab(self) -> gr.Tab:
        """Build the Destination Summary tab."""
        with gr.Tab("Destination Summary"):
            gr.Markdown("""
            # ✈️ Destination Summary Generator
            
            Provide a description of a travel destination, and our AI will generate a concise, 
            engaging summary highlighting the key aspects of the destination.
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    destination_name = gr.Textbox(label="Destination Name", 
                                                placeholder="e.g., Kyoto, Japan")
                    destination_description = gr.Textbox(label="Destination Description", 
                                                      placeholder="Describe the destination in detail...",
                                                      lines=10)
                    summarize_button = gr.Button("Generate Summary", variant="primary")
                
                with gr.Column(scale=3):
                    summary_output = gr.Textbox(label="AI-Generated Summary", 
                                             lines=10, 
                                             interactive=False)
                    formatted_summary = gr.Markdown(label="Formatted Highlight")
            
            summarize_button.click(
                fn=self._generate_summary,
                inputs=[destination_name, destination_description],
                outputs=[summary_output, formatted_summary]
            )
            
            gr.Markdown("""
            ### Tips for best results:
            - Include specific details about attractions, culture, food, and experiences
            - Mention unique aspects that make this destination special
            - Add practical information like best times to visit
            """)
            
            return gr.Tab
    
    def build_plan_trip_tab(self) -> gr.Tab:
        """Build the Plan My Trip tab."""
        interests_options = [
            "beach", "mountains", "city", "culture", "history", "food", 
            "adventure", "relaxation", "wildlife", "photography", "budget",
            "luxury", "family", "romantic", "nightlife", "shopping"
        ]
        
        with gr.Tab("Plan My Trip"):
            gr.Markdown("""
            # 🌍 Personalized Trip Planner
            
            Tell us about your interests and budget, and we'll recommend destinations that match your preferences.
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    interests = gr.CheckboxGroup(
                        choices=interests_options,
                        label="Your Interests (Select all that apply)"
                    )
                    
                    with gr.Row():
                        budget = gr.Slider(
                            minimum=20, 
                            maximum=500, 
                            value=100, 
                            step=10, 
                            label="Daily Budget (USD)"
                        )
                        budget_display = gr.Number(
                            value=100, 
                            label="Budget Amount"
                        )
                    
                    previous_destinations = gr.Textbox(
                        label="Previously Visited Destinations (Optional)",
                        placeholder="e.g., Paris, Tokyo, Bali",
                        info="Separate destinations with commas"
                    )
                    
                    recommend_button = gr.Button("Find Destinations", variant="primary")
                
                with gr.Column(scale=3):
                    recommendation_output = gr.JSON(label="Your Personalized Recommendations")
                    recommendation_details = gr.Markdown(label="Recommendation Details")
            
            budget.change(
                fn=lambda x: x,
                inputs=[budget],
                outputs=[budget_display]
            )
            
            recommend_button.click(
                fn=self._get_recommendations,
                inputs=[interests, budget, previous_destinations],
                outputs=[recommendation_output, recommendation_details]
            )
            
            return gr.Tab
    
    def build_review_analyzer_tab(self) -> gr.Tab:
        """Build the Review Analyzer tab."""
        with gr.Tab("Review Analyzer"):
            gr.Markdown("""
            # 🔍 Travel Review Analyzer
            
            Upload a travel review and our AI will analyze it, providing ratings for different aspects 
            and extracting key insights.
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    review_title = gr.Textbox(label="Review Title", 
                                           placeholder="e.g., My Stay at Grand Hotel")
                    review_text = gr.Textbox(label="Review Text", 
                                          placeholder="Paste or write your travel review here...",
                                          lines=10)
                    analyze_button = gr.Button("Analyze Review", variant="primary")
                
                with gr.Column(scale=3):
                    analysis_output = gr.JSON(label="Review Analysis")
                    analysis_summary = gr.Markdown(label="Analysis Summary")
            
            analyze_button.click(
                fn=self._analyze_review,
                inputs=[review_title, review_text],
                outputs=[analysis_output, analysis_summary]
            )
            
            return gr.Tab
    
    def _generate_summary(self, destination_name: str, description: str) -> tuple:
        """
        Generate a summary for a destination.
        
        Args:
            destination_name: Name of the destination
            description: Description text
            
        Returns:
            Tuple of (summary text, formatted HTML summary)
        """
        if not destination_name or not description:
            return "Please provide both destination name and description.", "Please complete all fields."
        
        try:
            result = self.travel_service.generate_destination_summary(destination_name, description)
            
            if result["success"]:
                return result["summary"], result["formatted_summary"]
            else:
                return f"Error generating summary: {result.get('error', 'Unknown error')}", ""
        except Exception as e:
            logger.error(f"Error in _generate_summary: {e}")
            return f"An error occurred: {str(e)}", ""
    
    def _get_recommendations(self, interests: List[str], budget: int, 
                           previous_destinations_str: str) -> tuple:
        """
        Get destination recommendations.
        
        Args:
            interests: List of selected interests
            budget: Daily budget in USD
            previous_destinations_str: String of comma-separated destinations
            
        Returns:
            Tuple of (recommendations JSON, markdown details)
        """
        if not interests:
            return {"error": "Please select at least one interest"}, "Please select your travel interests."
        
        # Parse previous destinations if provided
        previous_destinations = []
        if previous_destinations_str:
            previous_destinations = [d.strip() for d in previous_destinations_str.split(",")]
        
        try:
            result = self.travel_service.get_recommendations(interests, budget, previous_destinations)
            
            if result["success"]:
                # Create markdown details
                recommendations = result["recommendations"]
                
                if not recommendations:
                    return result, "No destinations match your criteria. Try adjusting your interests or budget."
                
                details_md = f"## Your Personalized Travel Recommendations\n\n"
                details_md += f"Based on your interests in {', '.join(interests)} with a ${budget}/day budget.\n\n"
                
                for i, rec in enumerate(recommendations, 1):
                    details_md += f"### {i}. {rec['name']} - {int(rec['score']*100)}% Match\n"
                    details_md += f"{rec['description']}\n\n"
                    details_md += f"**Budget Level:** {rec['budget_level'].capitalize()} (${rec['avg_cost_per_day']}/day)\n\n"
                    details_md += f"**Match Details:** Budget match: {int(rec['match_details']['budget_match']*100)}%, "
                    details_md += f"Interest match: {int(rec['match_details']['interest_match']*100)}%\n\n"
                    details_md += f"**Categories:** {', '.join(rec['categories'])}\n\n"
                    details_md += "---\n\n"
                
                return result, details_md
            else:
                return result, f"Error getting recommendations: {result.get('error', 'Unknown error')}"
        except Exception as e:
            logger.error(f"Error in _get_recommendations: {e}")
            return {"error": str(e)}, f"An error occurred: {str(e)}"
    
    def _analyze_review(self, review_title: str, review_text: str) -> tuple:
        """
        Analyze a travel review.
        
        Args:
            review_title: Title of the review
            review_text: Full text of the review
            
        Returns:
            Tuple of (analysis JSON, markdown details)
        """
        if not review_title or not review_text:
            return {"error": "Please provide both review title and text"}, "Please complete all fields."
        
        try:
            result = self.travel_service.analyze_review(review_title, review_text)
            
            if result["success"]:
                # Create markdown details
                details_md = f"## Review Analysis: {review_title}\n\n"
                details_md += f"### Overall Score: {result['overall_score']}/5.0\n\n"
                
                # Create rating table
                details_md += "| Category | Rating |\n"
                details_md += "|---------|--------|\n"
                for category, rating in result["category_ratings"].items():
                    details_md += f"| {category.capitalize()} | {rating}/5.0 |\n"
                
                details_md += "\n### Summary\n"
                details_md += result["summary"] + "\n\n"
                
                if result["pros"]:
                    details_md += "### Pros\n"
                    for pro in result["pros"]:
                        details_md += f"✅ {pro}\n"
                    details_md += "\n"
                
                if result["cons"]:
                    details_md += "### Cons\n"
                    for con in result["cons"]:
                        details_md += f"⚠️ {con}\n"
                
                return result, details_md
            else:
                return result, f"Error analyzing review: {result.get('error', 'Unknown error')}"
        except Exception as e:
            logger.error(f"Error in _analyze_review: {e}")
            return {"error": str(e)}, f"An error occurred: {str(e)}"
    
    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface with all tabs."""
        with gr.Blocks(theme=self.theme, title=self.title) as interface:
            gr.Markdown(f"""
            # {self.title}
            
            {self.description}
            """)
            
            with gr.Tabs():
                self.build_destination_summary_tab()
                self.build_plan_trip_tab()
                self.build_review_analyzer_tab()
            
            gr.Markdown("""
            ---
            Made with ❤️ by TripyTrek | Powered by AI and Gradio
            """)
        
        return interface
    
    def launch(self, share: bool = False):
        """Launch the Gradio interface."""
        interface = self.create_interface()
        interface.launch(share=share)


if __name__ == "__main__":
    app = TripyTrekApp()
    app.launch(share=True)
