# from bs4 import BeautifulSoup
# import re
# from typing import List
# import logging

# class HTMLProcessor:
#     @staticmethod
#     def clean_html(html_content: str) -> str:
#         soup = BeautifulSoup(html_content, 'html.parser')
        
#         # Remove unnecessary elements
#         for element in soup(['script', 'style', 'link', 'meta']):
#             element.decompose()
        
#         # Find review section
#         review_section = soup.find('div', id=re.compile(r'reviews|ratings', re.I))
#         if not review_section:
#             review_section = soup.find('div', class_=re.compile(r'reviews|ratings', re.I))
        
#         return str(review_section or soup)

#     @staticmethod
#     def extract_review_elements(html_content: str) -> str:
#         soup = BeautifulSoup(html_content, 'html.parser')
#         review_elements = []
        
#         # Common patterns for Shopify and other e-commerce reviews
#         patterns = [
#             {'class': re.compile(r'review|rating|spr-review', re.I)},
#             {'data-review': True},
#             {'itemprop': 'review'},
#             {'class': 'spr-review'},  # Specific to Shopify Product Reviews
#         ]
        
#         for pattern in patterns:
#             elements = soup.find_all(attrs=pattern)
#             review_elements.extend(elements)
            
#         if review_elements:
#             logging.info(f"Found {len(review_elements)} review elements")
#         else:
#             logging.warning("No review elements found")
            
#         return '\n'.join(str(element) for element in review_elements)

#     @staticmethod
#     def extract_reviews_with_selectors(html_content: str, selectors: dict) -> List[dict]:
#         soup = BeautifulSoup(html_content, 'html.parser')
#         reviews = []
        
#         # Try multiple selectors for review containers
#         container_selectors = selectors['container_selector'].split(', ')
#         all_containers = []
#         for selector in container_selectors:
#             containers = soup.select(selector)
#             if containers:
#                 all_containers.extend(containers)
                
#         if not all_containers:
#             logging.warning("No review containers found with provided selectors")
#             # Fallback: try to find reviews by common patterns
#             all_containers = soup.find_all(class_=re.compile(r'review|spr-review', re.I))
        
#         logging.info(f"Found {len(all_containers)} review containers")
        
#         for container in all_containers:
#             try:
#                 # Extract review components using multiple potential selectors
#                 title = None
#                 for selector in selectors['title_selector'].split(', '):
#                     title_elem = container.select_one(selector)
#                     if title_elem:
#                         title = title_elem.get_text().strip()
#                         break
                        
#                 body = None
#                 for selector in selectors['body_selector'].split(', '):
#                     body_elem = container.select_one(selector)
#                     if body_elem:
#                         body = body_elem.get_text().strip()
#                         break
                
#                 if not body:  # Skip if no review body found
#                     continue
                    
#                 # Extract rating
#                 rating = 0
#                 for selector in selectors['rating_selector'].split(', '):
#                     rating_elem = container.select_one(selector)
#                     if rating_elem:
#                         rating_text = rating_elem.get_text()
#                         # Try to extract numeric rating
#                         numbers = re.findall(r'\d+\.?\d*', rating_text)
#                         if numbers:
#                             try:
#                                 rating = int(float(numbers[0]))
#                                 break
#                             except ValueError:
#                                 continue
                
#                 # Extract reviewer name
#                 reviewer = "Anonymous"
#                 for selector in selectors['reviewer_selector'].split(', '):
#                     reviewer_elem = container.select_one(selector)
#                     if reviewer_elem:
#                         reviewer = reviewer_elem.get_text().strip()
#                         break
                
#                 review = {
#                     'title': title or "No Title",
#                     'body': body,
#                     'rating': min(max(rating, 0), 5),  # Ensure rating is between 0 and 5
#                     'reviewer': reviewer
#                 }
#                 reviews.append(review)
                
#             except Exception as e:
#                 logging.error(f"Error extracting review: {str(e)}")
#                 continue
                
#         logging.info(f"Successfully extracted {len(reviews)} reviews")
#         return reviews  

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

