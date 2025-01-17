import google.generativeai as genai
import logging
from typing import Dict

class GeminiHelper:
    def __init__(self):
        # Configure the Gemini API
        api_key = "AIzaSyBTwzZtCvGl24kDrCijxQVRzVhX-N39I5c"  # Replace with your Gemini API key
        genai.configure(api_key=api_key)
        logging.info("Gemini AI initialized")

    def identify_review_selectors(self, html_sample: str) -> Dict[str, str]:
        prompt = f"""
        Analyze this HTML content and identify the most specific CSS selectors for review elements.
        Return only a JSON object with these selectors (no additional text):
        {{
            "container_selector": "selector for the entire review container",
            "title_selector": "selector for review title or heading",
            "body_selector": "selector for review text/body",
            "rating_selector": "selector for rating element (stars or number)",
            "reviewer_selector": "selector for reviewer name"
        }}

        HTML sample:
        {html_sample[:2000]}  # Reduce token size to avoid exceeding limits
        """
        try:
            # Use the `generate_content` method to send a request
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            selectors = response.text
            logging.info(f"Generated selectors: {selectors}")
            return eval(selectors)  # Convert JSON string to dictionary
        except Exception as e:
            logging.error(f"Error getting selectors from Gemini: {str(e)}")
            raise

