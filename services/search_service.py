"""
Search Service for Ticino Real Estate Bot

This module handles property search logic, filtering, and pagination.
"""

import logging
from typing import List, Optional, Tuple, Dict, Any

from api.flatfox_client import FlatfoxClient
from database.models import Property, Alert
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class SearchService:
    """Handles property search operations"""
    
    def __init__(self, flatfox_client: FlatfoxClient, db_manager: DatabaseManager):
        """
        Initialize the search service
        
        Args:
            flatfox_client: Flatfox API client instance
            db_manager: Database manager instance
        """
        self.flatfox = flatfox_client
        self.db = db_manager
    
    def search_properties(self,
                         city: Optional[str] = None,
                         min_rooms: Optional[float] = None,
                         max_rooms: Optional[float] = None,
                         max_price: Optional[int] = None,
                         min_surface: Optional[int] = None,
                         offer_type: Optional[str] = None,
                         page: int = 1,
                         per_page: int = 5) -> Tuple[int, List[Property], int]:
        """
        Search for properties with filters and pagination
        
        Args:
            city: City name
            min_rooms: Minimum number of rooms
            max_rooms: Maximum number of rooms
            max_price: Maximum price
            min_surface: Minimum surface area
            offer_type: 'RENT' or 'SALE'
            page: Page number (1-indexed)
            per_page: Results per page
            
        Returns:
            Tuple of (total_count, properties_list, total_pages)
        """
        # Calculate offset for pagination
        offset = (page - 1) * per_page
        
        logger.info(f"Searching properties - Page {page}, Filters: city={city}, "
                   f"rooms={min_rooms}-{max_rooms}, price<={max_price}, "
                   f"surface>={min_surface}, type={offer_type}")
        
        # Call API
        total_count, properties = self.flatfox.search_and_parse(
            city=city,
            min_rooms=min_rooms,
            max_rooms=max_rooms,
            max_price=max_price,
            min_surface=min_surface,
            offer_type=offer_type,
            limit=per_page,
            offset=offset
        )
        
        # Calculate total pages
        total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 0
        
        logger.info(f"Found {total_count} total properties, showing page {page}/{total_pages}")
        
        return total_count, properties, total_pages
    
    def search_with_alert(self, alert: Alert, page: int = 1, per_page: int = 5) -> Tuple[int, List[Property], int]:
        """
        Search properties using saved alert filters
        
        Args:
            alert: Alert object with saved filters
            page: Page number
            per_page: Results per page
            
        Returns:
            Tuple of (total_count, properties_list, total_pages)
        """
        return self.search_properties(
            city=alert.city,
            min_rooms=alert.min_rooms,
            max_rooms=alert.max_rooms,
            max_price=alert.max_price,
            min_surface=alert.min_surface,
            offer_type=alert.offer_type,
            page=page,
            per_page=per_page
        )
    
    def get_property_details(self, property_id: int) -> Optional[Property]:
        """
        Get detailed information for a specific property
        
        Args:
            property_id: Flatfox property ID
            
        Returns:
            Property object or None if not found
        """
        logger.info(f"Fetching details for property {property_id}")
        return self.flatfox.get_property_by_id(property_id)
    
    def check_new_properties_for_alert(self, alert: Alert) -> List[Property]:
        """
        Check for new properties matching an alert's criteria
        Returns only properties not yet notified to the user
        
        Args:
            alert: Alert object with filters
            
        Returns:
            List of new Property objects
        """
        logger.info(f"Checking new properties for alert {alert.alert_id} (user {alert.user_id})")
        
        # Get recent properties from API (last 50)
        properties = self.flatfox.check_new_properties(
            city=alert.city,
            min_rooms=alert.min_rooms,
            max_rooms=alert.max_rooms,
            max_price=alert.max_price,
            min_surface=alert.min_surface,
            offer_type=alert.offer_type,
            limit=50
        )
        
        # Filter out already notified properties
        new_properties = []
        for prop in properties:
            if not self.db.is_property_notified(alert.user_id, prop.pk):
                new_properties.append(prop)
        
        logger.info(f"Found {len(new_properties)} new properties for alert {alert.alert_id}")
        return new_properties
    
    def check_all_alerts_for_new_properties(self) -> Dict[int, List[Property]]:
        """
        Check all active alerts for new properties
        
        Returns:
            Dictionary mapping user_id to list of new properties
        """
        logger.info("Checking all active alerts for new properties")
        
        # Get all active alerts
        alerts = self.db.get_all_active_alerts()
        
        # Dictionary to collect properties per user
        user_properties = {}
        
        for alert in alerts:
            new_properties = self.check_new_properties_for_alert(alert)
            
            if new_properties:
                if alert.user_id not in user_properties:
                    user_properties[alert.user_id] = []
                
                # Add new properties to user's list (avoid duplicates)
                existing_pks = {p.pk for p in user_properties[alert.user_id]}
                for prop in new_properties:
                    if prop.pk not in existing_pks:
                        user_properties[alert.user_id].append(prop)
                        existing_pks.add(prop.pk)
        
        logger.info(f"Found new properties for {len(user_properties)} users")
        return user_properties
    
    def mark_property_as_notified(self, user_id: int, property_id: int) -> bool:
        """
        Mark a property as notified to a user
        
        Args:
            user_id: Telegram user ID
            property_id: Flatfox property ID
            
        Returns:
            True if successful
        """
        return self.db.add_notified_property(user_id, property_id)
    
    def get_filter_summary(self, 
                          city: Optional[str] = None,
                          min_rooms: Optional[float] = None,
                          max_rooms: Optional[float] = None,
                          max_price: Optional[int] = None,
                          min_surface: Optional[int] = None,
                          offer_type: Optional[str] = None) -> str:
        """
        Generate a human-readable summary of active filters
        
        Args:
            Same as search_properties()
            
        Returns:
            Formatted string with filter summary
        """
        filters = []
        
        if city:
            filters.append(f"📍 City: {city}")
        
        if offer_type:
            offer_text = "🏷️ Type: Rent" if offer_type == "RENT" else "🏷️ Type: Sale"
            filters.append(offer_text)
        
        if min_rooms or max_rooms:
            if min_rooms and max_rooms:
                filters.append(f"🛏️ Rooms: {min_rooms} - {max_rooms}")
            elif min_rooms:
                filters.append(f"🛏️ Min rooms: {min_rooms}")
            elif max_rooms:
                filters.append(f"🛏️ Max rooms: {max_rooms}")
        
        if max_price:
            price_str = f"{max_price:,}".replace(",", "'")
            filters.append(f"💰 Max price: CHF {price_str}")
        
        if min_surface:
            filters.append(f"📐 Min surface: {min_surface} m²")
        
        if not filters:
            return "🔍 Searching all properties in Ticino"
        
        return "🔍 <b>Active filters:</b>\n" + "\n".join(filters)
    
    def validate_filters(self,
                        city: Optional[str] = None,
                        min_rooms: Optional[float] = None,
                        max_rooms: Optional[float] = None,
                        max_price: Optional[int] = None,
                        min_surface: Optional[int] = None,
                        offer_type: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate filter values
        
        Args:
            Same as search_properties()
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate rooms
        if min_rooms is not None and max_rooms is not None:
            if min_rooms > max_rooms:
                return False, "❌ Minimum rooms cannot be greater than maximum rooms"
        
        if min_rooms is not None and (min_rooms <= 0 or min_rooms > 20):
            return False, "❌ Minimum rooms must be between 0 and 20"
        
        if max_rooms is not None and (max_rooms <= 0 or max_rooms > 20):
            return False, "❌ Maximum rooms must be between 0 and 20"
        
        # Validate price
        if max_price is not None and (max_price <= 0 or max_price > 50000000):
            return False, "❌ Maximum price must be between 0 and 50'000'000 CHF"
        
        # Validate surface
        if min_surface is not None and (min_surface <= 0 or min_surface > 10000):
            return False, "❌ Minimum surface must be between 0 and 10'000 m²"
        
        # Validate offer type
        if offer_type is not None and offer_type not in ['RENT', 'SALE']:
            return False, "❌ Offer type must be either 'RENT' or 'SALE'"
        
        return True, None
    
    def has_any_filter(self,
                      city: Optional[str] = None,
                      min_rooms: Optional[float] = None,
                      max_rooms: Optional[float] = None,
                      max_price: Optional[int] = None,
                      min_surface: Optional[int] = None,
                      offer_type: Optional[str] = None) -> bool:
        """
        Check if any filter is active
        
        Args:
            Same as search_properties()
            
        Returns:
            True if at least one filter is set
        """
        return any([city, min_rooms, max_rooms, max_price, min_surface, offer_type])
