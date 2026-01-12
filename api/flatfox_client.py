"""
Flatfox API Client for Ticino Real Estate Bot

This module handles all communication with the Flatfox public API.
"""

import logging
import requests
import time
from typing import List, Optional, Dict, Any
from urllib.parse import urlencode
from datetime import datetime, timedelta

from database.models import Property

logger = logging.getLogger(__name__)


class FlatfoxClient:
    """Client for interacting with Flatfox public API with intelligent caching"""
    
    def __init__(self, api_url: str):
        """
        Initialize the Flatfox API client
        
        Args:
            api_url: Base URL for Flatfox API
        """
        self.api_url = api_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TicinoRealEstateBot/1.0',
            'Accept': 'application/json'
        })
        
        # Cache for bulk fetched properties
        self._cache = []
        self._cache_time = None
        self._cache_duration = timedelta(hours=1)  # Cache for 1 hour
        self._fetch_size = 3000  # Fetch 3000 properties at once
    
    def search_properties(self,
                         city: Optional[str] = None,
                         min_rooms: Optional[float] = None,
                         max_rooms: Optional[float] = None,
                         max_price: Optional[int] = None,
                         min_surface: Optional[int] = None,
                         offer_type: Optional[str] = None,
                         object_category: Optional[str] = None,
                         limit: int = 20,
                         offset: int = 0) -> Dict[str, Any]:
        """
        Search for properties with filters
        
        Args:
            city: City name (e.g., "Lugano")
            min_rooms: Minimum number of rooms
            max_rooms: Maximum number of rooms
            max_price: Maximum price
            min_surface: Minimum living space in m²
            offer_type: 'RENT' or 'SALE'
            object_category: Category (APARTMENT, HOUSE, PARK, INDUSTRY, SHARED)
            limit: Number of results per page
            offset: Pagination offset
            
        Returns:
            Dictionary with 'count', 'next', 'previous', and 'results' keys
        """
        # Build query parameters
        params = {}
        
        # Always filter for Ticino canton (but API doesn't respect it)
        params['state'] = 'TI'
        # We'll fetch multiple pages to get more results
        fetch_limit = 200  # Fetch 200 results total to filter from
        
        # Use correct API syntax according to documentation
        # https://flatfox.ch/en/docs/api/#/resources/public-listing
        
        if city:
            params['city'] = city
        if min_rooms is not None:
            params['number_of_rooms__gte'] = min_rooms  # Greater than or equal
        if max_rooms is not None:
            params['number_of_rooms__lte'] = max_rooms  # Less than or equal
        if max_price is not None:
            params['price_display__lte'] = max_price  # Less than or equal
        if min_surface is not None:
            params['livingspace__gte'] = min_surface  # Greater than or equal
        if offer_type:
            params['offer_type'] = offer_type.upper()
        if object_category:
            # Map our categories to Flatfox codes
            category_map = {
                'APARTMENT': 'APPT',
                'HOUSE': 'HOUSE',
                'PARK': 'PARK',
                'INDUSTRY': 'INDUS',
                'SHARED': 'SHARED'
            }
            flatfox_category = category_map.get(object_category.upper(), object_category.upper())
            params['object_category'] = flatfox_category
        
        try:
            # NEW STRATEGY: Use cached bulk fetch
            # Fetch 3000 properties once per hour and cache them
            all_results = self._get_cached_properties()
            
            # Filter results manually (API doesn't filter properly)
            filtered_results = self._filter_results_manually(
                all_results, city, min_rooms, max_rooms, max_price, 
                min_surface, offer_type, object_category
            )
            
            # Apply pagination on filtered results
            start_idx = offset
            end_idx = offset + limit
            paginated_results = filtered_results[start_idx:end_idx]
            
            # Return modified data with correct count
            filtered_data = {
                'count': len(filtered_results),
                'next': None if end_idx >= len(filtered_results) else 'has_more',
                'previous': None if offset == 0 else 'has_prev',
                'results': paginated_results
            }
            
            logger.info(f"Filtered {len(filtered_results)} properties from cache (page {offset//limit + 1})")
            
            return filtered_data
            
        except requests.exceptions.Timeout:
            logger.error("Request to Flatfox API timed out")
            return {'count': 0, 'next': None, 'previous': None, 'results': []}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Flatfox API: {e}")
            return {'count': 0, 'next': None, 'previous': None, 'results': []}
        
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return {'count': 0, 'next': None, 'previous': None, 'results': []}
    
    def _get_cached_properties(self) -> list:
        """
        Get properties from cache or fetch new batch
        
        Returns:
            List of raw property dictionaries
        """
        # Check if cache is valid
        if self._cache and self._cache_time:
            age = datetime.now() - self._cache_time
            if age < self._cache_duration:
                logger.info(f"Using cached properties ({len(self._cache)} items, age: {age.seconds}s)")
                return self._cache
        
        # Cache expired or doesn't exist - fetch new batch
        logger.info(f"Cache expired or empty, fetching {self._fetch_size} properties from API...")
        start_time = time.time()
        
        all_results = []
        
        # Fetch multiple pages to get 3000 properties
        for page_offset in range(0, self._fetch_size, 100):
            try:
                params = {
                    'limit': 100,
                    'offset': page_offset
                }
                
                if page_offset % 500 == 0:
                    logger.info(f"  Fetching offset {page_offset}...")
                
                response = self.session.get(self.api_url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                page_results = data.get('results', [])
                all_results.extend(page_results)
                
                # Small delay to be nice to API
                time.sleep(0.1)
                
                # Stop if we got less than 100 (no more results)
                if len(page_results) < 100:
                    break
                    
            except Exception as e:
                logger.error(f"Error fetching page at offset {page_offset}: {e}")
                break
        
        elapsed = time.time() - start_time
        
        # Update cache
        self._cache = all_results
        self._cache_time = datetime.now()
        
        # Count Ticino properties
        ti_count = sum(1 for item in all_results if item.get('state') == 'TI')
        
        logger.info(f"✓ Fetched {len(all_results)} properties in {elapsed:.1f}s")
        logger.info(f"  Ticino properties: {ti_count} ({ti_count/len(all_results)*100:.1f}%)")
        logger.info(f"  Cache valid for 1 hour")
        
        return all_results
    
    def _filter_results_manually(self, results: list, city: Optional[str] = None,
                                 min_rooms: Optional[float] = None, max_rooms: Optional[float] = None,
                                 max_price: Optional[int] = None, min_surface: Optional[int] = None,
                                 offer_type: Optional[str] = None, object_category: Optional[str] = None) -> list:
        """
        Filter results manually since API doesn't filter properly
        
        Args:
            results: Raw results from API
            Filters: Same as search_properties
            
        Returns:
            Filtered list of results
        """
        filtered = []
        
        for item in results:
            # ALWAYS filter by Ticino canton first (API ignores it!)
            item_state = item.get('state', '')
            if not item_state or item_state.upper() != 'TI':
                continue  # Skip non-Ticino properties or None state
            
            # Filter by city (case insensitive partial match)
            if city:
                item_city = item.get('city', '').lower()
                if city.lower() not in item_city:
                    continue
            
            # Filter by rooms
            item_rooms = item.get('number_of_rooms')
            if item_rooms is not None:
                try:
                    rooms_float = float(item_rooms)
                    if min_rooms and rooms_float < min_rooms:
                        continue
                    if max_rooms and rooms_float > max_rooms:
                        continue
                except (TypeError, ValueError):
                    pass
            
            # Filter by price
            item_price = item.get('price_display')
            if max_price and item_price:
                try:
                    if float(item_price) > max_price:
                        continue
                except (TypeError, ValueError):
                    pass
            
            # Filter by surface
            item_surface = item.get('livingspace')
            if min_surface and item_surface:
                try:
                    if float(item_surface) < min_surface:
                        continue
                except (TypeError, ValueError):
                    pass
            
            # Filter by offer type
            if offer_type:
                item_type = item.get('offer_type', '').upper()
                if item_type != offer_type.upper():
                    continue
            
            # Filter by category (map our names to Flatfox codes)
            if object_category:
                category_map = {
                    'APARTMENT': 'APPT',
                    'HOUSE': 'HOUSE',
                    'PARK': 'PARK',
                    'INDUSTRY': 'INDUS',
                    'SHARED': 'SHARED'
                }
                expected_category = category_map.get(object_category.upper(), object_category.upper())
                item_category = item.get('object_category', '').upper()
                if item_category != expected_category:
                    continue
            
            # If we got here, item passes all filters
            filtered.append(item)
        
        return filtered
    
    def parse_property(self, data: Dict[str, Any]) -> Optional[Property]:
        """
        Parse API response data into Property object
        
        Args:
            data: Raw property data from API
            
        Returns:
            Property object or None if parsing fails
        """
        try:
            # Extract agency information
            agency_data = data.get('agency', {})
            agency_name = agency_data.get('name') if agency_data else None
            
            # Try to get contact info from various fields
            agency_phone = None
            agency_email = None
            
            # Some listings have contact info in different places
            contact_info = data.get('contact', {})
            if contact_info:
                agency_phone = contact_info.get('phone')
                agency_email = contact_info.get('email')
            
            # Extract image URLs
            images = []
            if data.get('images'):
                for img in data['images']:
                    if isinstance(img, dict):
                        # Try different possible image URL fields
                        img_url = (img.get('url') or 
                                  img.get('url_original') or 
                                  img.get('url_large'))
                        if img_url:
                            # Make sure URL is absolute
                            if img_url.startswith('/'):
                                img_url = f"https://flatfox.ch{img_url}"
                            images.append(img_url)
            
            property_obj = Property(
                pk=data['pk'],
                offer_type=data.get('offer_type'),
                object_category=data.get('object_category'),
                object_type=data.get('object_type'),
                price_display=data.get('price_display'),
                price_unit=data.get('price_unit'),
                number_of_rooms=data.get('number_of_rooms'),
                livingspace=data.get('livingspace'),
                street=data.get('street'),
                street_number=data.get('street_number'),
                zipcode=data.get('zipcode'),
                city=data.get('city'),
                state=data.get('state'),
                description=data.get('description'),
                availability_date=data.get('availability_date'),
                images=images,
                agency_name=agency_name,
                agency_phone=agency_phone,
                agency_email=agency_email
            )
            
            return property_obj
            
        except KeyError as e:
            logger.error(f"Missing required field in property data: {e}")
            return None
        except Exception as e:
            logger.error(f"Error parsing property data: {e}")
            return None
    
    def search_and_parse(self,
                        city: Optional[str] = None,
                        min_rooms: Optional[float] = None,
                        max_rooms: Optional[float] = None,
                        max_price: Optional[int] = None,
                        min_surface: Optional[int] = None,
                        offer_type: Optional[str] = None,
                        object_category: Optional[str] = None,
                        limit: int = 20,
                        offset: int = 0) -> tuple[int, List[Property]]:
        """
        Search properties and parse results into Property objects
        
        Args:
            Same as search_properties()
            
        Returns:
            Tuple of (total_count, list_of_properties)
        """
        result = self.search_properties(
            city=city,
            min_rooms=min_rooms,
            max_rooms=max_rooms,
            max_price=max_price,
            min_surface=min_surface,
            offer_type=offer_type,
            object_category=object_category,
            limit=limit,
            offset=offset
        )
        
        total_count = result.get('count', 0)
        properties = []
        
        for item in result.get('results', []):
            prop = self.parse_property(item)
            if prop:
                properties.append(prop)
        
        logger.info(f"Successfully parsed {len(properties)} properties")
        return total_count, properties
    
    def get_property_by_id(self, property_id: int) -> Optional[Property]:
        """
        Get a specific property by its ID
        
        Args:
            property_id: Flatfox property ID
            
        Returns:
            Property object or None if not found
        """
        try:
            url = f"{self.api_url}?pk={property_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            if results:
                return self.parse_property(results[0])
            
            logger.warning(f"Property {property_id} not found")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching property {property_id}: {e}")
            return None
    
    def check_new_properties(self,
                            city: Optional[str] = None,
                            min_rooms: Optional[float] = None,
                            max_rooms: Optional[float] = None,
                            max_price: Optional[int] = None,
                            min_surface: Optional[int] = None,
                            offer_type: Optional[str] = None,
                            object_category: Optional[str] = None,
                            limit: int = 50) -> List[Property]:
        """
        Check for new properties matching criteria (for notifications)
        Returns most recent listings first
        
        Args:
            Same as search_properties() but with default limit of 50
            
        Returns:
            List of Property objects sorted by most recent
        """
        _, properties = self.search_and_parse(
            city=city,
            min_rooms=min_rooms,
            max_rooms=max_rooms,
            max_price=max_price,
            min_surface=min_surface,
            offer_type=offer_type,
            object_category=object_category,
            limit=limit,
            offset=0
        )
        
        # Properties are already sorted by most recent from API
        return properties
    
    def test_connection(self) -> bool:
        """
        Test if API is reachable
        
        Returns:
            True if API is working
        """
        try:
            response = self.session.get(f"{self.api_url}?limit=1", timeout=5)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"API connection test failed: {e}")
            return False
