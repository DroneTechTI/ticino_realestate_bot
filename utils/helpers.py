"""
Helper Functions for Ticino Real Estate Bot

This module contains utility functions for formatting messages,
handling media, and other common operations.
"""

import logging
from typing import Optional, List
from telegraph import Telegraph
from telegram import InputMediaPhoto
from html import escape

from database.models import Property, Alert

logger = logging.getLogger(__name__)

# Initialize Telegraph
telegraph = Telegraph()

try:
    telegraph.create_account(short_name='TicinoRealEstate', author_name='Ticino Real Estate')
    logger.info("Telegraph account created successfully")
except Exception as e:
    logger.warning(f"Telegraph initialization: {e}")


def format_property_message(prop: Property, include_description: bool = True) -> str:
    """
    Format a property into a Telegram message
    
    Args:
        prop: Property object to format
        include_description: Whether to include description in message
        
    Returns:
        Formatted message string
    """
    # Determine property type emoji
    type_emoji = "🏠"
    if prop.object_category == "APPT":
        type_emoji = "🏢"
    elif prop.object_category == "HOUSE":
        type_emoji = "🏡"
    elif prop.object_category == "PARK":
        type_emoji = "🅿️"
    elif prop.object_category == "COMMERCIAL":
        type_emoji = "🏪"
    
    # Build message
    lines = []
    
    # Title with type
    object_type_text = prop.object_type or "Property"
    rooms_text = prop.get_rooms_formatted()
    
    if prop.number_of_rooms is not None and rooms_text != "Not specified":
        title = f"{type_emoji} {object_type_text} - {rooms_text}"
    else:
        title = f"{type_emoji} {object_type_text}"
    lines.append(f"<b>{title}</b>")
    lines.append("")
    
    # Location
    lines.append(f"📍 <b>Location:</b> {prop.get_full_address()}")
    
    # Price
    lines.append(f"💰 <b>Price:</b> {prop.get_price_formatted()}")
    
    # Surface
    surface_text = prop.get_surface_formatted()
    if prop.livingspace is not None and surface_text != "Not specified":
        lines.append(f"📐 <b>Surface:</b> {surface_text}")
    
    # Availability
    if prop.availability_date:
        lines.append(f"📅 <b>Available:</b> {prop.availability_date}")
    
    lines.append("")
    
    # Description handling
    if include_description and prop.description:
        description = prop.description.strip()
        
        # Check description length
        if len(description) <= 1000:
            # Short description - include in message
            lines.append("📝 <b>Description:</b>")
            # Escape HTML special characters
            safe_description = escape(description)
            lines.append(safe_description)
        else:
            # Long description - create Telegraph page
            telegraph_url = create_telegraph_page(prop)
            if telegraph_url:
                lines.append("📝 <b>Full Description:</b>")
                lines.append(f"🔗 <a href='{telegraph_url}'>Click here to read</a>")
            else:
                # Fallback: show truncated description
                lines.append("📝 <b>Description:</b>")
                truncated = escape(description[:500]) + "..."
                lines.append(truncated)
    
    lines.append("")
    
    # Agency contact information
    if prop.agency_name or prop.agency_phone or prop.agency_email:
        lines.append("🏢 <b>Contact Information:</b>")
        
        if prop.agency_name:
            lines.append(f"Agency: {escape(prop.agency_name)}")
        
        if prop.agency_phone:
            lines.append(f"📞 Phone: {escape(prop.agency_phone)}")
        
        if prop.agency_email:
            lines.append(f"📧 Email: {escape(prop.agency_email)}")
    
    return "\n".join(lines)


def create_telegraph_page(prop: Property) -> Optional[str]:
    """
    Create a Telegraph page for a property with long description
    
    Args:
        prop: Property object
        
    Returns:
        Telegraph page URL or None if creation fails
    """
    try:
        # Prepare title
        title = f"{prop.get_rooms_formatted()} in {prop.city or 'Ticino'}"
        if len(title) > 256:
            title = title[:253] + "..."
        
        # Prepare content in HTML format
        html_content = f"<h3>{prop.get_full_address()}</h3>"
        html_content += f"<p><strong>Price:</strong> {prop.get_price_formatted()}</p>"
        
        if prop.livingspace:
            html_content += f"<p><strong>Surface:</strong> {prop.get_surface_formatted()}</p>"
        
        if prop.availability_date:
            html_content += f"<p><strong>Available from:</strong> {prop.availability_date}</p>"
        
        html_content += "<hr>"
        html_content += f"<h4>Description</h4>"
        
        # Format description with paragraphs
        description = prop.description.strip()
        paragraphs = description.split('\n\n')
        for para in paragraphs:
            if para.strip():
                html_content += f"<p>{escape(para.strip())}</p>"
        
        html_content += "<hr>"
        
        if prop.agency_name:
            html_content += f"<p><strong>Agency:</strong> {escape(prop.agency_name)}</p>"
        
        if prop.agency_phone:
            html_content += f"<p><strong>Phone:</strong> {escape(prop.agency_phone)}</p>"
        
        if prop.agency_email:
            html_content += f"<p><strong>Email:</strong> {escape(prop.agency_email)}</p>"
        
        # Create page
        response = telegraph.create_page(
            title=title,
            html_content=html_content,
            author_name='Ticino Real Estate'
        )
        
        page_url = f"https://telegra.ph/{response['path']}"
        logger.info(f"Created Telegraph page for property {prop.pk}: {page_url}")
        return page_url
        
    except Exception as e:
        logger.error(f"Error creating Telegraph page for property {prop.pk}: {e}")
        return None


def prepare_media_group(prop: Property) -> List[InputMediaPhoto]:
    """
    Prepare a media group (album) from property images
    
    Args:
        prop: Property object with images
        
    Returns:
        List of InputMediaPhoto objects (max 10 for Telegram limit)
    """
    media_group = []
    
    # Telegram allows max 10 media items in a group
    max_images = min(len(prop.images), 10)
    
    for i, image_url in enumerate(prop.images[:max_images]):
        # First image gets the caption
        if i == 0:
            caption = format_property_caption(prop)
            media_group.append(InputMediaPhoto(media=image_url, caption=caption, parse_mode='HTML'))
        else:
            media_group.append(InputMediaPhoto(media=image_url))
    
    return media_group


def format_property_caption(prop: Property) -> str:
    """
    Format a short caption for property media
    
    Args:
        prop: Property object
        
    Returns:
        Short formatted caption
    """
    lines = []
    
    # Title
    rooms_text = prop.get_rooms_formatted()
    if prop.number_of_rooms is not None and rooms_text != "Not specified":
        lines.append(f"<b>{rooms_text}</b>")
    
    # Location
    lines.append(f"📍 {prop.get_full_address()}")
    
    # Price
    lines.append(f"💰 {prop.get_price_formatted()}")
    
    # Surface
    surface_text = prop.get_surface_formatted()
    if prop.livingspace is not None and surface_text != "Not specified":
        lines.append(f"📐 {surface_text}")
    
    return "\n".join(lines)


def format_alert_summary(alert: Alert) -> str:
    """
    Format an alert into a readable summary
    
    Args:
        alert: Alert object
        
    Returns:
        Formatted alert description
    """
    parts = []
    
    if alert.city:
        parts.append(f"📍 City: {alert.city}")
    
    if alert.offer_type:
        offer_text = "Rent" if alert.offer_type == "RENT" else "Sale"
        parts.append(f"🏷️ Type: {offer_text}")
    
    if alert.min_rooms or alert.max_rooms:
        if alert.min_rooms and alert.max_rooms:
            parts.append(f"🛏️ Rooms: {alert.min_rooms} - {alert.max_rooms}")
        elif alert.min_rooms:
            parts.append(f"🛏️ Rooms: min {alert.min_rooms}")
        elif alert.max_rooms:
            parts.append(f"🛏️ Rooms: max {alert.max_rooms}")
    
    if alert.max_price:
        parts.append(f"💰 Max Price: CHF {alert.max_price:,}".replace(",", "'"))
    
    if alert.min_surface:
        parts.append(f"📐 Min Surface: {alert.min_surface} m²")
    
    status = "✅ Active" if alert.is_active else "⏸️ Paused"
    parts.append(f"Status: {status}")
    
    return "\n".join(parts)


def validate_room_number(value: str) -> Optional[float]:
    """
    Validate and parse room number input
    
    Args:
        value: User input string
        
    Returns:
        Float number or None if invalid
    """
    try:
        num = float(value.replace(',', '.'))
        if num > 0 and num <= 20:  # Reasonable range
            return num
        return None
    except ValueError:
        return None


def validate_price(value: str) -> Optional[int]:
    """
    Validate and parse price input
    
    Args:
        value: User input string
        
    Returns:
        Integer price or None if invalid
    """
    try:
        # Remove common separators
        clean_value = value.replace("'", "").replace(",", "").replace(".", "").replace(" ", "")
        price = int(clean_value)
        if price > 0 and price <= 50000000:  # Reasonable range
            return price
        return None
    except ValueError:
        return None


def validate_surface(value: str) -> Optional[int]:
    """
    Validate and parse surface area input
    
    Args:
        value: User input string
        
    Returns:
        Integer surface or None if invalid
    """
    try:
        surface = int(value)
        if surface > 0 and surface <= 10000:  # Reasonable range
            return surface
        return None
    except ValueError:
        return None


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_number_with_apostrophe(number: int) -> str:
    """
    Format number with Swiss-style apostrophes (e.g., 1'000'000)
    
    Args:
        number: Number to format
        
    Returns:
        Formatted string
    """
    return f"{number:,}".replace(",", "'")
