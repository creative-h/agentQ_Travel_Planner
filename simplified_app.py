"""Simplified TripyTrek application with minimal dependencies."""

import os
import sys
import logging
from pathlib import Path
import gradio as gr
import random

# Set up simple logging
logging.basicConfig(level=logging.INFO, 
                   format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Sample data for the app
SAMPLE_DESTINATIONS = [
    {
        "name": "Bali, Indonesia",
        "description": "Tropical paradise with beautiful beaches, vibrant culture, and lush rice terraces.",
        "budget_level": "medium",
        "categories": ["beach", "culture", "nature", "food"],
        "avg_cost_per_day": 50,
    },
    {
        "name": "Paris, France",
        "description": "City of lights and romance with iconic landmarks, world-class museums, and exquisite cuisine.",
        "budget_level": "high",
        "categories": ["culture", "food", "history", "city"],
        "avg_cost_per_day": 150,
    },
    {
        "name": "Kyoto, Japan",
        "description": "Ancient capital with thousands of temples, traditional gardens, and geisha culture.",
        "budget_level": "high",
        "categories": ["culture", "history", "food", "nature"],
        "avg_cost_per_day": 100,
    },
    {
        "name": "Bangkok, Thailand",
        "description": "Bustling metropolis with ornate shrines, vibrant street life, and world-renowned street food.",
        "budget_level": "low",
        "categories": ["food", "culture", "city", "budget"],
        "avg_cost_per_day": 30,
    },
    {
        "name": "New York City, USA",
        "description": "Iconic skyline, Broadway shows, diverse neighborhoods, and world-class museums and restaurants.",
        "budget_level": "high",
        "categories": ["city", "culture", "food", "nightlife", "shopping"],
        "avg_cost_per_day": 200,
    }
]

class SimplifiedTripyTrekApp:
    """A simplified version of the TripyTrek application with mock responses."""
    
    def __init__(self):
        """Initialize the simplified TripyTrek application."""
        self.title = "TripyTrek - AI Travel Discovery"
        self.description = "Explore destinations, read AI-generated reviews, and get personalized recommendations"
        logger.info("Simplified TripyTrek initialized")
    
    def generate_summary(self, destination_name, description):
        """Generate a simplified destination summary."""
        if not destination_name or not description:
            return "Please provide both destination name and description.", ""
        
        # Create a mock summary (about 40% of the original length)
        words = description.split()
        summary_length = max(3, len(words) // 3)
        selected_words = []
        
        # Select random sentences from the description
        sentences = description.split(". ")
        selected_sentences = random.sample(sentences, min(3, len(sentences)))
        summary = ". ".join(selected_sentences)
        
        formatted = f"""✨ TRIPYTREK HIGHLIGHT: {destination_name.upper()} ✨

{summary}

Discover more about {destination_name} on TripyTrek."""
        
        return summary, formatted
    
    def get_recommendations(self, interests, budget, previous_destinations_str):
        """Get destination recommendations based on user preferences."""
        if not interests:
            return {"error": "Please select at least one interest"}, "Please select your travel interests."
        
        # Filter destinations based on interests and budget
        recommended = []
        for dest in SAMPLE_DESTINATIONS:
            # Skip if in previous destinations
            if previous_destinations_str and dest["name"].lower() in previous_destinations_str.lower():
                continue
                
            # Calculate match scores
            interest_match = sum(1 for i in interests if i in dest["categories"]) / len(interests)
            budget_match = 1.0 if dest["avg_cost_per_day"] <= budget else max(0, 1 - ((dest["avg_cost_per_day"] - budget) / budget))
            total_score = 0.6 * interest_match + 0.4 * budget_match
            
            if total_score > 0.3:  # Minimum threshold
                recommended.append({
                    "name": dest["name"],
                    "description": dest["description"],
                    "budget_level": dest["budget_level"],
                    "avg_cost_per_day": dest["avg_cost_per_day"],
                    "score": round(total_score, 2),
                    "match_details": {
                        "budget_match": round(budget_match, 2),
                        "interest_match": round(interest_match, 2)
                    },
                    "categories": dest["categories"]
                })
        
        # Sort by score
        recommended.sort(key=lambda x: x["score"], reverse=True)
        
        # Create response objects
        result = {
            "success": True,
            "count": len(recommended),
            "recommendations": recommended
        }
        
        # Create details markdown
        if recommended:
            details_md = f"## Your Personalized Travel Recommendations\n\n"
            details_md += f"Based on your interests in {', '.join(interests)} with a ${budget}/day budget.\n\n"
            
            for i, rec in enumerate(recommended, 1):
                details_md += f"### {i}. {rec['name']} - {int(rec['score']*100)}% Match\n"
                details_md += f"{rec['description']}\n\n"
                details_md += f"**Budget Level:** {rec['budget_level'].capitalize()} (${rec['avg_cost_per_day']}/day)\n\n"
                details_md += f"**Match Details:** Budget match: {int(rec['match_details']['budget_match']*100)}%, "
                details_md += f"Interest match: {int(rec['match_details']['interest_match']*100)}%\n\n"
                details_md += f"**Categories:** {', '.join(rec['categories'])}\n\n"
                details_md += "---\n\n"
        else:
            details_md = "No destinations match your criteria. Try adjusting your interests or budget."
        
        return result, details_md
    
    def analyze_review(self, review_title, review_text):
        """Analyze a travel review using simplified mock responses."""
        if not review_title or not review_text:
            return {"error": "Please provide both review title and text"}, "Please complete all fields."
        
        # Generate mock ratings for different categories
        categories = ["location", "facilities", "food", "value", "service"]
        ratings = {cat: round(random.uniform(3.0, 5.0), 1) for cat in categories}
        
        # Calculate overall score
        overall_score = round(sum(ratings.values()) / len(ratings), 1)
        
        # Extract mock pros and cons
        sentences = review_text.split(". ")
        pros = sentences[:min(3, len(sentences) // 2)]
        cons = []
        
        # If the review is long enough, add some cons
        if len(sentences) > 5:
            cons = sentences[len(sentences) // 2:min(len(sentences), len(sentences) // 2 + 2)]
        
        # Create result objects
        result = {
            "success": True,
            "title": review_title,
            "overall_score": overall_score,
            "category_ratings": ratings,
            "pros": pros,
            "cons": cons
        }
        
        # Create details markdown
        details_md = f"## Review Analysis: {review_title}\n\n"
        details_md += f"### Overall Score: {overall_score}/5.0\n\n"
        
        # Create rating table
        details_md += "| Category | Rating |\n"
        details_md += "|---------|--------|\n"
        for category, rating in ratings.items():
            details_md += f"| {category.capitalize()} | {rating}/5.0 |\n"
        
        details_md += "\n### Summary\n"
        if overall_score >= 4.5:
            details_md += "This is an excellent review with very high ratings across all categories.\n\n"
        elif overall_score >= 4.0:
            details_md += "This is a very positive review with good ratings across most categories.\n\n"
        elif overall_score >= 3.5:
            details_md += "This is a generally positive review with some areas for improvement.\n\n"
        else:
            details_md += "This is a mixed review with several aspects that could be improved.\n\n"
        
        if pros:
            details_md += "### Pros\n"
            for pro in pros:
                details_md += f"✅ {pro}\n"
            details_md += "\n"
        
        if cons:
            details_md += "### Cons\n"
            for con in cons:
                details_md += f"⚠️ {con}\n"
        
        return result, details_md
    
    def create_interface(self):
        """Create the Gradio interface."""
        with gr.Blocks(title=self.title) as interface:
            gr.Markdown(f"""
            # {self.title}
            
            {self.description}
            """)
            
            with gr.Tabs():
                # Destination Summary Tab
                with gr.Tab("Destination Summary"):
                    gr.Markdown("""
                    # ✈️ Destination Summary Generator
                    
                    Provide a description of a travel destination, and our AI will generate a concise, 
                    engaging summary highlighting the key aspects of the destination.
                    """)
                    
                    with gr.Row():
                        with gr.Column(scale=2):
                            destination_name = gr.Textbox(
                                label="Destination Name", 
                                placeholder="e.g., Kyoto, Japan"
                            )
                            destination_description = gr.Textbox(
                                label="Destination Description", 
                                placeholder="Describe the destination in detail...",
                                lines=10
                            )
                            summarize_button = gr.Button("Generate Summary", variant="primary")
                        
                        with gr.Column(scale=3):
                            summary_output = gr.Textbox(
                                label="AI-Generated Summary", 
                                lines=10, 
                                interactive=False
                            )
                            formatted_summary = gr.Markdown(label="Formatted Highlight")
                    
                    summarize_button.click(
                        fn=self.generate_summary,
                        inputs=[destination_name, destination_description],
                        outputs=[summary_output, formatted_summary]
                    )
                
                # Plan My Trip Tab
                with gr.Tab("Plan My Trip"):
                    interests_options = [
                        "beach", "mountains", "city", "culture", "history", "food", 
                        "adventure", "relaxation", "wildlife", "photography", "budget",
                        "luxury", "family", "romantic", "nightlife", "shopping"
                    ]
                    
                    gr.Markdown("""
                    # 🌍 Personalized Trip Planner
                    
                    Tell us about your interests and budget, and we'll recommend destinations 
                    that match your preferences.
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
                        fn=self.get_recommendations,
                        inputs=[interests, budget, previous_destinations],
                        outputs=[recommendation_output, recommendation_details]
                    )
                
                # Review Analyzer Tab
                with gr.Tab("Review Analyzer"):
                    gr.Markdown("""
                    # 🔍 Travel Review Analyzer
                    
                    Upload a travel review and our AI will analyze it, providing ratings for different 
                    aspects and extracting key insights.
                    """)
                    
                    with gr.Row():
                        with gr.Column(scale=2):
                            review_title = gr.Textbox(
                                label="Review Title", 
                                placeholder="e.g., My Stay at Grand Hotel"
                            )
                            review_text = gr.Textbox(
                                label="Review Text", 
                                placeholder="Paste or write your travel review here...",
                                lines=10
                            )
                            analyze_button = gr.Button("Analyze Review", variant="primary")
                        
                        with gr.Column(scale=3):
                            analysis_output = gr.JSON(label="Review Analysis")
                            analysis_summary = gr.Markdown(label="Analysis Summary")
                    
                    analyze_button.click(
                        fn=self.analyze_review,
                        inputs=[review_title, review_text],
                        outputs=[analysis_output, analysis_summary]
                    )
            
            gr.Markdown("""
            ---
            Made with ❤️ by TripyTrek | Powered by AI and Gradio
            """)
        
        return interface
    
    def launch(self, share=True):
        """Launch the Gradio interface."""
        interface = self.create_interface()
        interface.launch(share=share)


if __name__ == "__main__":
    app = SimplifiedTripyTrekApp()
    app.launch()
