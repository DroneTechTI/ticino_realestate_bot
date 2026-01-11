"""
Flatfox API Client for Ticino Real Estate Bot

This module handles all communication with the Flatfox public API.
"""

import logging
import requests
from typing import List, Optional, Dict, Any
from urllib.parse import urlencode

from database.models import Property

logger = logging.getLogger(__name__)


class FlatfoxClient:
    """Client for interacting with Flatfox public API"""
    
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
        
        # Always filter for Ticino canton
        params['state'] = 'TI'
        
        if city:
            params['city'] = city
        
        if min_rooms is not None:
            params['number_of_rooms_min'] = min_rooms
        
        if max_rooms is not None:
            params['number_of_rooms_max'] = max_rooms
        
        if max_price is not None:
            params['price_display_max'] = max_price
        
        if min_surface is not None:
            params['livingspace_min'] = min_surface
        
        if offer_type:
            params['offer_type'] = offer_type.upper()
        
        if object_category:
            params['object_category'] = object_category.upper()
        
        params['limit'] = limit
        params['offset'] = offset
        
        try:
            logger.info(f"Searching properties with filters: {params}")
            response = self.session.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Found {data.get('count', 0)} total properties")
            
            return data
            
        except requests.exceptions.Timeout:
            logger.error("Request to Flatfox API timed out")
            return {'count': 0, 'next': None, 'previous': None, 'results': []}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Flatfox API: {e}")
            return {'count': 0, 'next': None, 'previous': None, 'results': []}
        
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return {'count': 0, 'next': None, 'previous': None, 'results': []}
    
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
