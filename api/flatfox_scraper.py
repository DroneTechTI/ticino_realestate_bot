"""
Flatfox Scraper using Selenium

This module scrapes Flatfox website since their API is completely broken.
"""

import logging
import time
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class FlatfoxScraper:
    """Scrapes Flatfox website for property listings"""
    
    def __init__(self):
        """Initialize the scraper with headless Chrome"""
        self.driver = None
        self._init_driver()
    
    def _init_driver(self):
        """Initialize Chrome driver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            # Auto-install ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def search_properties(self, 
                         city: Optional[str] = None,
                         min_rooms: Optional[float] = None,
                         max_rooms: Optional[float] = None,
                         max_price: Optional[int] = None,
                         offer_type: Optional[str] = None) -> List[dict]:
        """
        Search for properties by scraping Flatfox website
        
        Args:
            city: City name
            min_rooms: Minimum rooms
            max_rooms: Maximum rooms
            max_price: Maximum price
            offer_type: 'rent' or 'buy'
            
        Returns:
            List of property dictionaries
        """
        try:
            # Build search URL
            base_url = "https://flatfox.ch/en/search/?"
            params = []
            
            if city:
                params.append(f"location={city}")
            if offer_type:
                offer = "rent" if offer_type.upper() == "RENT" else "buy"
                params.append(f"offer_type={offer}")
            if max_price:
                params.append(f"price_max={max_price}")
            if min_rooms:
                params.append(f"rooms_min={min_rooms}")
            if max_rooms:
                params.append(f"rooms_max={max_rooms}")
            
            # Add Ticino bounding box
            params.append("east=9.04")
            params.append("north=46.23")
            params.append("south=45.83")
            params.append("west=8.75")
            
            url = base_url + "&".join(params)
            
            logger.info(f"Scraping URL: {url}")
            self.driver.get(url)
            
            # Wait for listings to load (React app)
            time.sleep(5)  # Give time for JavaScript to execute
            
            # Try to wait for listing cards
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "search-result"))
                )
            except:
                logger.warning("Timeout waiting for search results")
            
            # Extract listings from page
            properties = self._extract_listings()
            
            logger.info(f"Scraped {len(properties)} properties")
            return properties
            
        except Exception as e:
            logger.error(f"Error scraping Flatfox: {e}", exc_info=True)
            return []
    
    def _extract_listings(self) -> List[dict]:
        """Extract listing data from current page"""
        properties = []
        
        try:
            # Get page source and look for data
            page_source = self.driver.page_source
            
            # Try to find listing elements
            # Flatfox uses different selectors, try multiple
            selectors = [
                "search-result",
                "listing-card",
                "property-card",
                "flat-listing"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CLASS_NAME, selector)
                    if elements:
                        logger.info(f"Found {len(elements)} elements with class '{selector}'")
                        
                        for elem in elements:
                            try:
                                prop_data = self._parse_listing_element(elem)
                                if prop_data:
                                    properties.append(prop_data)
                            except Exception as e:
                                logger.debug(f"Error parsing element: {e}")
                        
                        if properties:
                            break
                except:
                    continue
            
            # If no listings found with elements, try to find in page JSON
            if not properties:
                properties = self._extract_from_json()
            
        except Exception as e:
            logger.error(f"Error extracting listings: {e}")
        
        return properties
    
    def _parse_listing_element(self, element) -> Optional[dict]:
        """Parse a single listing element"""
        try:
            # Extract text and attributes
            text = element.text
            html = element.get_attribute('innerHTML')
            
            # Try to extract data
            prop = {
                'title': '',
                'city': '',
                'rooms': None,
                'price': None,
                'url': ''
            }
            
            # Look for links
            links = element.find_elements(By.TAG_NAME, 'a')
            if links:
                prop['url'] = links[0].get_attribute('href')
            
            # Parse text for data
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if 'room' in line.lower():
                    # Extract room number
                    try:
                        rooms = float(line.split()[0])
                        prop['rooms'] = rooms
                    except:
                        pass
                elif 'chf' in line.lower():
                    # Extract price
                    try:
                        price_str = line.replace('CHF', '').replace("'", '').replace(',', '').strip()
                        price = int(price_str.split()[0])
                        prop['price'] = price
                    except:
                        pass
            
            return prop if prop['url'] else None
            
        except Exception as e:
            logger.debug(f"Error parsing element: {e}")
            return None
    
    def _extract_from_json(self) -> List[dict]:
        """Try to extract data from embedded JSON in page"""
        try:
            page_source = self.driver.page_source
            
            # Look for JSON data patterns
            import re
            import json
            
            # Try to find window.__INITIAL_STATE__ or similar
            patterns = [
                r'window\.__INITIAL_STATE__\s*=\s*({.+?});',
                r'window\.__DATA__\s*=\s*({.+?});',
                r'initialState\s*=\s*({.+?});'
            ]
            
            for pattern in patterns:
                matches = re.search(pattern, page_source, re.DOTALL)
                if matches:
                    try:
                        data = json.loads(matches.group(1))
                        logger.info("Found JSON data in page!")
                        # Process JSON data
                        return self._process_json_data(data)
                    except:
                        continue
            
        except Exception as e:
            logger.debug(f"Could not extract JSON: {e}")
        
        return []
    
    def _process_json_data(self, data: dict) -> List[dict]:
        """Process extracted JSON data"""
        properties = []
        # This would need to be adapted based on actual JSON structure
        # For now, return empty
        return properties
    
    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Chrome driver closed")
            except:
                pass
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close()
