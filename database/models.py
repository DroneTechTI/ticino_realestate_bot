"""
Data Models for Ticino Real Estate Bot

This module defines the data structures used throughout the application.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Represents a Telegram user of the bot"""
    user_id: int
    username: Optional[str]
    first_name: str
    created_at: datetime
    is_active: bool = True
    language: str = 'it'  # User's preferred language (it, de, en)


@dataclass
class Alert:
    """Represents a saved search alert for a user"""
    alert_id: Optional[int]
    user_id: int
    city: Optional[str]
    min_rooms: Optional[float]
    max_rooms: Optional[float]
    max_price: Optional[int]
    min_surface: Optional[int]
    offer_type: Optional[str]  # 'RENT' or 'SALE'
    is_active: bool
    created_at: datetime
    object_category: Optional[str] = None  # 'APARTMENT', 'HOUSE', 'PARK', 'INDUSTRY', 'SHARED'


@dataclass
class NotifiedProperty:
    """Tracks properties that have been sent to users to avoid duplicates"""
    id: Optional[int]
    user_id: int
    property_id: int
    notified_at: datetime


@dataclass
class Property:
    """Represents a real estate property from Flatfox API"""
    pk: int
    offer_type: str
    object_category: Optional[str]
    object_type: Optional[str]
    price_display: Optional[float]
    price_unit: Optional[str]
    number_of_rooms: Optional[float]
    livingspace: Optional[float]
    street: Optional[str]
    street_number: Optional[str]
    zipcode: Optional[str]
    city: Optional[str]
    state: Optional[str]
    description: Optional[str]
    availability_date: Optional[str]
    images: list
    agency_name: Optional[str]
    agency_phone: Optional[str]
    agency_email: Optional[str]
    
    def get_full_address(self) -> str:
        """Returns formatted full address"""
        parts = []
        if self.street:
            street_full = self.street
            if self.street_number:
                street_full += f" {self.street_number}"
            parts.append(street_full)
        if self.zipcode and self.city:
            parts.append(f"{self.zipcode} {self.city}")
        return ", ".join(parts) if parts else "Address not available"
    
    def get_price_formatted(self) -> str:
        """Returns formatted price string"""
        if not self.price_display:
            return "Price on request"
        
        price_str = f"CHF {self.price_display:,.0f}".replace(",", "'")
        
        if self.price_unit == "monthly":
            return f"{price_str} / month"
        elif self.price_unit == "once":
            return price_str
        else:
            return f"{price_str} / {self.price_unit}"
    
    def get_rooms_formatted(self) -> str:
        """Returns formatted rooms string"""
        if self.number_of_rooms is None:
            return "Not specified"
        
        try:
            # Format with .5 for half rooms
            if float(self.number_of_rooms) % 1 == 0:
                return f"{int(self.number_of_rooms)} rooms"
            else:
                return f"{self.number_of_rooms} rooms"
        except (TypeError, ValueError):
            return "Not specified"
    
    def get_surface_formatted(self) -> str:
        """Returns formatted surface area string"""
        if self.livingspace is None:
            return "Not specified"
        try:
            return f"{int(self.livingspace)} m²"
        except (TypeError, ValueError):
            return "Not specified"
