# TripyTrek - AI-Powered Travel Platform

TripyTrek is an advanced travel review and discovery platform powered by AI. It helps users explore destinations, generate summaries, analyze reviews, and receive personalized travel recommendations based on their interests and budget.

![TripyTrek](https://raw.githubusercontent.com/yourusername/tripytrek/main/assets/tripytrek_logo.png)

## 🌟 Features

TripyTrek offers several AI-powered features:

- **Destination Summarizer**: Automatically generates concise summaries of travel destinations using NLP models
- **Review Analyzer**: Analyzes hotel and flight reviews to provide ratings on different aspects (location, facilities, food)
- **Recommendation Engine**: Suggests destinations based on user interests, budget, and past behavior

## 📋 Project Structure

```
tripyTrek/
├── config/          # Configuration files
├── data/            # Data loading and processing 
├── models/          # AI models implementation
├── notebooks/       # Experimental notebooks
├── services/        # Business logic and services
├── ui/              # Gradio UI components
├── main.py          # Application entry point
├── requirements.txt # Dependencies
└── README.md        # Documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tripytrek.git
   cd tripytrek
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Launch the TripyTrek application:

```bash
python main.py
```

The application will be available at `http://localhost:7860` in your web browser.

## 💻 Usage Guide

### Destination Summary Tab

1. Enter a destination name (e.g., "Kyoto, Japan")
2. Provide a detailed description of the destination
3. Click "Generate Summary" to get an AI-generated concise highlight

### Plan My Trip Tab

1. Select your travel interests from the checkboxes
2. Adjust your daily budget using the slider
3. Optionally, enter previously visited destinations
4. Click "Find Destinations" to get personalized recommendations

### Review Analyzer Tab

1. Enter a review title
2. Paste the full review text
3. Click "Analyze Review" to get a breakdown of ratings and insights

## 🧠 AI Models

TripyTrek uses several AI models:

- **Summarizer**: BART/T5 for generating concise destination summaries
- **Review Classifier**: BERT-based model for sentiment analysis and aspect-based rating
- **Recommendation Engine**: Hybrid system using content-based filtering and rule-based matching

## 🛠️ Customization

You can customize the application by editing the `config/config.yaml` file:

- Adjust model parameters
- Change UI settings
- Modify application behavior

## 📝 Content Categories

TripyTrek covers the following travel content categories:

- Destinations
- Feature Articles
- Food
- Wildlife
- Flight Reviews
- Hotel Reviews

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Inspired by [TripyTrek.com](https://www.tripytrek.com)
- Built with [Gradio](https://gradio.app/) and [Hugging Face Transformers](https://huggingface.co/transformers/)
