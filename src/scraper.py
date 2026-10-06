"""
Stock scraper module for FairGame Stock Defender.
Uses Playwright to monitor product pages for stock availability.
"""

import asyncio
import random
import time
from typing import Dict, List, Optional, Callable
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from bs4 import BeautifulSoup
import json


class StockScraper:
    """Headless browser-based stock availability checker."""

    def __init__(self, config: dict):
        """
        Initialize the stock scraper.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.user_agents = config.get("user_agents", [])
        self.check_interval = config.get("check_interval", 10)
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.is_running = False
        self.monitored_products: List[Dict] = []
        self.alert_callback: Optional[Callable] = None

    async def initialize(self):
        """Initialize the Playwright browser instance."""
        self.playwright = await async_playwright().start()

        # Launch browser with anti-detection settings
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ]
        )

        # Create context with realistic user agent
        user_agent = random.choice(self.user_agents) if self.user_agents else (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        self.context = await self.browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="America/New_York",
        )

        # Add stealth scripts to avoid detection
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)

    async def close(self):
        """Close the browser and cleanup resources."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.is_running = False

    def add_product(self, url: str, name: str, store: str, custom_selectors: Optional[Dict] = None):
        """
        Add a product to the monitoring list.

        Args:
            url: Product page URL
            name: Product name
            store: Store name
            custom_selectors: Optional custom CSS selectors for stock detection
        """
        product = {
            "url": url,
            "name": name,
            "store": store,
            "status": "Initializing",
            "last_check": None,
            "custom_selectors": custom_selectors or {},
            "is_in_stock": False,
            "check_count": 0
        }
        self.monitored_products.append(product)

    def remove_product(self, url: str):
        """
        Remove a product from monitoring.

        Args:
            url: Product URL to remove
        """
        self.monitored_products = [p for p in self.monitored_products if p["url"] != url]

    def set_alert_callback(self, callback: Callable):
        """
        Set the callback function for stock alerts.

        Args:
            callback: Function to call when stock is detected
        """
        self.alert_callback = callback

    async def check_product_stock(self, product: Dict) -> Dict:
        """
        Check stock status for a single product.

        Args:
            product: Product dictionary

        Returns:
            Updated product dictionary with status
        """
        page = None
        try:
            page = await self.context.new_page()

            # Set additional headers to appear more like a real browser
            await page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            })

            # Navigate to the product page with timeout
            await page.goto(product["url"], wait_until="networkidle", timeout=30000)

            # Get page content
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")

            # Check for stock indicators
            in_stock = self._detect_stock(soup, product["url"], product["custom_selectors"])

            # Update product status
            product["status"] = "IN STOCK!" if in_stock else "Out of Stock"
            product["is_in_stock"] = in_stock
            product["last_check"] = time.strftime("%H:%M:%S")
            product["check_count"] += 1

            # Trigger alert if stock is detected and wasn't before
            if in_stock and self.alert_callback:
                self.alert_callback(product)

            return product

        except asyncio.TimeoutError:
            product["status"] = "Timeout"
            product["last_check"] = time.strftime("%H:%M:%S")
            return product
        except Exception as e:
            product["status"] = f"Error: {str(e)[:30]}"
            product["last_check"] = time.strftime("%H:%M:%S")
            return product
        finally:
            if page:
                await page.close()

    def _detect_stock(self, soup: BeautifulSoup, url: str, custom_selectors: Dict) -> bool:
        """
        Detect if product is in stock using various indicators.

        Args:
            soup: BeautifulSoup parsed HTML
            url: Product URL for store-specific logic
            custom_selectors: Custom CSS selectors if provided

        Returns:
            True if in stock, False otherwise
        """
        # Use custom selectors if provided
        if custom_selectors:
            in_stock_selector = custom_selectors.get("in_stock")
            out_of_stock_selector = custom_selectors.get("out_of_stock")

            if in_stock_selector:
                element = soup.select_one(in_stock_selector)
                if element and element.get("disabled") is None:
                    return True

            if out_of_stock_selector:
                element = soup.select_one(out_of_stock_selector)
                if element:
                    return False

        # Store-specific detection logic
        store = url.lower()

        # Common "Add to Cart" button indicators
        add_to_cart_patterns = [
            r"add to cart",
            r"add to basket",
            r"buy now",
            r"purchase",
            r"add\s+to\s+cart",
            r"add\s+to\s+basket"
        ]

        # Common "Out of Stock" indicators
        out_of_stock_patterns = [
            r"out of stock",
            r"sold out",
            r"unavailable",
            r"currently unavailable",
            r"temporarily out of stock"
        ]

        # Check for "Add to Cart" or "Buy Now" buttons
        buttons = soup.find_all(["button", "input"], {"type": "submit"})
        for button in buttons:
            text = button.get_text().lower()
            button_id = button.get("id", "").lower()
            button_class = " ".join(button.get("class", [])).lower()

            # Check if button is disabled
            is_disabled = button.get("disabled") is not None or "disabled" in button_class

            if not is_disabled:
                import re
                for pattern in add_to_cart_patterns:
                    if re.search(pattern, text) or re.search(pattern, button_id) or re.search(pattern, button_class):
                        return True

        # Check for out of stock text
        page_text = soup.get_text().lower()
        import re
        for pattern in out_of_stock_patterns:
            if re.search(pattern, page_text):
                return False

        # Check for common stock indicators by store
        if "amazon" in store:
            # Amazon-specific logic
            availability = soup.find(id="availability")
            if availability:
                text = availability.get_text().lower()
                if "in stock" in text:
                    return True
                if "out of stock" in text or "currently unavailable" in text:
                    return False

        elif "bestbuy" in store:
            # Best Buy-specific logic
            add_to_cart = soup.find(class_="add-to-cart-button")
            if add_to_cart and add_to_cart.get("disabled") is None:
                return True

        elif "target" in store:
            # Target-specific logic
            add_button = soup.find("button", {"data-test": "addToCart"})
            if add_button and add_button.get("disabled") is None:
                return True

        elif "walmart" in store:
            # Walmart-specific logic
            add_button = soup.find("button", {"data-automation-id": "add-to-cart"})
            if add_button and add_button.get("disabled") is None:
                return True

        # Default: if no clear indicators, assume out of stock to avoid false positives
        return False

    async def start_monitoring(self):
        """Start the monitoring loop for all products."""
        self.is_running = True

        while self.is_running:
            # Check all products concurrently
            tasks = [self.check_product_stock(product) for product in self.monitored_products]
            await asyncio.gather(*tasks, return_exceptions=True)

            # Wait before next check
            await asyncio.sleep(self.check_interval)

    def stop_monitoring(self):
        """Stop the monitoring loop."""
        self.is_running = False

    def get_product_status(self, url: str) -> Optional[Dict]:
        """
        Get current status of a monitored product.

        Args:
            url: Product URL

        Returns:
            Product dictionary or None if not found
        """
        for product in self.monitored_products:
            if product["url"] == url:
                return product
        return None

    def get_all_products(self) -> List[Dict]:
        """Get all monitored products."""
        return self.monitored_products.copy()
