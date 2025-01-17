
# from playwright.async_api import async_playwright
# import logging

# class BrowserManager:
#     async def __aenter__(self):
#         self.playwright = await async_playwright().start()
#         self.browser = await self.playwright.chromium.launch(headless=True)
#         return self
        
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         if hasattr(self, 'browser'):
#             await self.browser.close()
#         if hasattr(self, 'playwright'):
#             await self.playwright.stop()
            
#     async def get_page_content(self, url: str) -> str:
#         logging.info(f"Fetching content from URL: {url}")
#         page = await self.browser.new_page()
#         try:
#             # Navigate to the page
#             await page.goto(url, wait_until="networkidle")
#             logging.info("Page loaded successfully")
            
#             # Scroll to load dynamic content
#             for _ in range(3):
#                 await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#                 await page.wait_for_timeout(60000)
            
#             content = await page.content()
#             logging.info("Content retrieved successfully")
#             return content
#         except Exception as e:
#             logging.error(f"Error fetching page content: {str(e)}")
#             raise
#         finally:
#             await page.close()
from playwright.async_api import async_playwright, Page
import logging
import asyncio


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
                # Navigate to the page with a higher timeout
                await page.goto(url, timeout=60000, wait_until="domcontentloaded")
                logging.info("Page loaded successfully")

                # Scroll to the bottom incrementally to load dynamic content
                await self._scroll_page(page)
                
                # Retrieve page content
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


# Example usage:
# async with BrowserManager() as browser_manager:
#     content = await browser_manager.get_page_content("https://example.com")
#     print(content)
