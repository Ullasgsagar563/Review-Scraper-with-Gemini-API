# Description: This file contains the code to manage the browser instance and fetch the content of a web page using Playwright.
from playwright.async_api import async_playwright, Page
import logging
import asyncio

# Define a class to manage the browser instance

class BrowserManager:
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'browser'):
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()

    async def get_page_content(self, url: str, retries: int = 3) -> str:
        logging.info(f"Fetching content from URL: {url}")
        page = await self.browser.new_page()

        for attempt in range(retries):
            try:
                # Load the page and wait for it to load completely
                await page.goto(url, timeout=60000, wait_until="domcontentloaded")
                logging.info("Page loaded successfully")

                # Scroll the page to load dynamic content
                await self._scroll_page(page)
                
                # Get the HTML content of the page
                content = await page.content()
                logging.info("Content retrieved successfully")
                return content

            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < retries - 1:
                    await asyncio.sleep(5)  # Wait before retrying
                else:
                    raise Exception(f"Failed to fetch content from {url} after {retries} attempts")

            finally:
                await page.close()
        

    # Define a method to scroll the page to load dynamic content
    async def _scroll_page(self, page: Page, scroll_delay: int = 1000, max_scrolls: int = 10):
        """Scroll the page to the bottom to trigger dynamic content loading."""
        logging.info("Scrolling the page to load dynamic content")
        for _ in range(max_scrolls):
            previous_height = await page.evaluate("document.body.scrollHeight")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(scroll_delay / 1000)  # Convert milliseconds to seconds
            current_height = await page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                break  # Stop scrolling if no more content is loaded
        logging.info("Scrolling complete")

