# Description: This file contains the FastAPI route for extracting reviews from a given URL.
from fastapi import APIRouter, HTTPException
from pydantic import HttpUrl
from fastapi.responses import PlainTextResponse
import logging
from browser import BrowserManager
from html_processor import HTMLProcessor
import google.generativeai as genai

# Create a new FastAPI router
router = APIRouter()

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyBTwzZtCvGl24kDrCijxQVRzVhX-N39I5c")

# Define the route for extracting reviews
@router.get("/api/reviews", response_class=PlainTextResponse)
async def get_reviews(url: HttpUrl):
    try:
        url_str = str(url)
        processor = HTMLProcessor()

        async with BrowserManager() as browser:
            html_content = await browser.get_page_content(url_str)
            logging.info("Successfully retrieved page content")

        # Clean and process HTML
        cleaned_html = processor.clean_html(html_content)
        review_elements = processor.extract_review_elements(cleaned_html)
        logging.info("Successfully processed HTML")

        # Define the prompt for Gemini
        prompt = f"""
        Extract reviews from the following HTML content and format them into the following structure:
        {{
            "reviews_count": <total number of reviews>,
            "reviews": [
                {{
                    "title": "<review title>",
                    "body": "<review body text>",
                    "rating": <rating out of 5>,
                    "reviewer": "<reviewer's name>"
                }}
            ]
        }}

        HTML content:
        {review_elements}
        """

        # Send the request to Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Return the raw response text from the Gemini API
        return PlainTextResponse(response.text)

    except Exception as e:
        logging.error(f"Error processing reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
