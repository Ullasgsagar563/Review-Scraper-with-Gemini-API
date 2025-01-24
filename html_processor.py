

from bs4 import BeautifulSoup
import re
from typing import List
import logging

class HTMLProcessor:
    @staticmethod
    def clean_html(html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unnecessary elements
        for element in soup(['script', 'style', 'link', 'meta']):
            element.decompose()
        
        # Find review section
        review_section = soup.find('div', id=re.compile(r'reviews|ratings', re.I))
        if not review_section:
            review_section = soup.find('div', class_=re.compile(r'reviews|ratings', re.I))
        
        return str(review_section or soup)

    @staticmethod
    def extract_review_elements(html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')
        review_elements = []
        
        # Common patterns for Shopify and other e-commerce reviews
        patterns = [
            {'class': re.compile(r'review|rating|spr-review', re.I)},
            {'data-review': True},
            {'itemprop': 'review'},
            {'class': 'spr-review'},  # Specific to Shopify Product Reviews
        ]
        
        for pattern in patterns:
            elements = soup.find_all(attrs=pattern)
            review_elements.extend(elements)
            
        if review_elements:
            logging.info(f"Found {len(review_elements)} review elements")
        else:
            logging.warning("No review elements found")
            
        return '\n'.join(str(element) for element in review_elements)

