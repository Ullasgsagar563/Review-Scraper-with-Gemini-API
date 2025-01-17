import streamlit as st
import requests

# URL of the FastAPI backend
API_URL = "http://localhost:8000/api/reviews"

def get_reviews_from_backend(url: str):
    """
    Make a GET request to the FastAPI backend with the provided URL.
    """
    response = requests.get(API_URL, params={"url": url})
    if response.status_code == 200:
        return response.text  # Return the raw response text
    else:
        return f"Error: {response.status_code} - {response.text}"

def display_reviews(raw_text):
    """
    Display the raw response text in Streamlit.
    """
    st.subheader("Response from Backend")
    st.code(raw_text, language="json")  # Display the raw text with JSON syntax highlighting

# Streamlit UI components
st.title("Review Scraper with Gemini API")
st.write("Enter a product URL to extract reviews.")

# Input field for the URL
url_input = st.text_input("Product URL", "")

# Button to fetch reviews
if st.button("Get Reviews") and url_input:
    with st.spinner("Fetching reviews..."):
        raw_response = get_reviews_from_backend(url_input)
        display_reviews(raw_response)
