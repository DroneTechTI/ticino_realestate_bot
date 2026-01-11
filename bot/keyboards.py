"""
Keyboard Layouts for Ticino Real Estate Bot

This module defines all inline keyboards used in the bot.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional, List


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Main menu keyboard
    
    Returns:
        InlineKeyboardMarkup with main menu options
    """
    keyboard = [
        [InlineKeyboardButton("🔍 Search Properties", callback_data="menu_search")],
        [InlineKeyboardButton("⚙️ Manage Filters", callback_data="menu_filters")],
        [InlineKeyboardButton("🔔 My Alerts", callback_data="menu_alerts")],
        [InlineKeyboardButton("📊 Statistics", callback_data="menu_stats")],
        [InlineKeyboardButton("❓ Help", callback_data="menu_help")]
    ]
    return InlineKeyboardMarkup(keyboard)


def search_type_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard to select search type (rent/sale)
    
    Returns:
        InlineKeyboardMarkup with search type options
    """
    keyboard = [
        [InlineKeyboardButton("🏠 Rent", callback_data="search_type_RENT")],
        [InlineKeyboardButton("🏡 Sale", callback_data="search_type_SALE")],
        [InlineKeyboardButton("🔍 All Types", callback_data="search_type_ALL")],
        [InlineKeyboardButton("« Back", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def filter_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Filter management menu keyboard
    
    Returns:
        InlineKeyboardMarkup with filter options
    """
    keyboard = [
        [InlineKeyboardButton("📍 Set City", callback_data="filter_city")],
        [InlineKeyboardButton("🛏️ Set Rooms", callback_data="filter_rooms")],
        [InlineKeyboardButton("💰 Set Max Price", callback_data="filter_price")],
        [InlineKeyboardButton("📐 Set Min Surface", callback_data="filter_surface")],
        [InlineKeyboardButton("🏷️ Set Type (Rent/Sale)", callback_data="filter_type")],
        [InlineKeyboardButton("🗑️ Clear All Filters", callback_data="filter_clear")],
        [InlineKeyboardButton("✅ Search with Filters", callback_data="filter_search")],
        [InlineKeyboardButton("« Back", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def offer_type_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard to select offer type
    
    Returns:
        InlineKeyboardMarkup with offer type options
    """
    keyboard = [
        [InlineKeyboardButton("🏠 Rent", callback_data="set_type_RENT")],
        [InlineKeyboardButton("🏡 Sale", callback_data="set_type_SALE")],
        [InlineKeyboardButton("❌ Remove Filter", callback_data="set_type_NONE")],
        [InlineKeyboardButton("« Back", callback_data="back_filters")]
    ]
    return InlineKeyboardMarkup(keyboard)


def pagination_keyboard(current_page: int, total_pages: int, prefix: str = "page") -> InlineKeyboardMarkup:
    """
    Navigation keyboard for paginated results
    
    Args:
        current_page: Current page number (1-indexed)
        total_pages: Total number of pages
        prefix: Callback data prefix (default: "page")
        
    Returns:
        InlineKeyboardMarkup with navigation buttons
    """
    keyboard = []
    
    # Navigation row
    nav_row = []
    
    if current_page > 1:
        nav_row.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"{prefix}_prev_{current_page}"))
    
    # Page indicator
    nav_row.append(InlineKeyboardButton(f"📄 {current_page}/{total_pages}", callback_data="page_info"))
    
    if current_page < total_pages:
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"{prefix}_next_{current_page}"))
    
    keyboard.append(nav_row)
    
    # Actions row
    action_row = [
        InlineKeyboardButton("🔍 New Search", callback_data="menu_search"),
        InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")
    ]
    keyboard.append(action_row)
    
    return InlineKeyboardMarkup(keyboard)


def alert_list_keyboard(alerts: List[tuple], has_alerts: bool = True) -> InlineKeyboardMarkup:
    """
    Keyboard showing list of user's alerts
    
    Args:
        alerts: List of tuples (alert_id, alert_description, is_active)
        has_alerts: Whether user has any alerts
        
    Returns:
        InlineKeyboardMarkup with alert list
    """
    keyboard = []
    
    if has_alerts:
        # Add button for each alert
        for alert_id, description, is_active in alerts:
            status_icon = "✅" if is_active else "⏸️"
            button_text = f"{status_icon} Alert #{alert_id}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"alert_view_{alert_id}")])
    
    # Action buttons
    keyboard.append([InlineKeyboardButton("➕ Create New Alert", callback_data="alert_create")])
    keyboard.append([InlineKeyboardButton("« Back", callback_data="back_main")])
    
    return InlineKeyboardMarkup(keyboard)


def alert_actions_keyboard(alert_id: int, is_active: bool) -> InlineKeyboardMarkup:
    """
    Keyboard with actions for a specific alert
    
    Args:
        alert_id: Alert ID
        is_active: Whether alert is currently active
        
    Returns:
        InlineKeyboardMarkup with alert actions
    """
    keyboard = []
    
    # Toggle button
    toggle_text = "⏸️ Pause Alert" if is_active else "▶️ Activate Alert"
    keyboard.append([InlineKeyboardButton(toggle_text, callback_data=f"alert_toggle_{alert_id}")])
    
    # Other actions
    keyboard.append([InlineKeyboardButton("🔍 Search Now", callback_data=f"alert_search_{alert_id}")])
    keyboard.append([InlineKeyboardButton("🗑️ Delete Alert", callback_data=f"alert_delete_confirm_{alert_id}")])
    keyboard.append([InlineKeyboardButton("« Back to Alerts", callback_data="menu_alerts")])
    
    return InlineKeyboardMarkup(keyboard)


def confirm_keyboard(action: str, item_id: Optional[int] = None) -> InlineKeyboardMarkup:
    """
    Confirmation keyboard for destructive actions
    
    Args:
        action: Action to confirm (e.g., "delete_alert")
        item_id: Optional item ID
        
    Returns:
        InlineKeyboardMarkup with confirm/cancel buttons
    """
    callback_confirm = f"confirm_{action}_{item_id}" if item_id else f"confirm_{action}"
    callback_cancel = f"cancel_{action}_{item_id}" if item_id else f"cancel_{action}"
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, Confirm", callback_data=callback_confirm),
            InlineKeyboardButton("❌ Cancel", callback_data=callback_cancel)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def save_alert_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard to save current filters as alert
    
    Returns:
        InlineKeyboardMarkup with save options
    """
    keyboard = [
        [InlineKeyboardButton("💾 Save as Alert", callback_data="save_current_filters")],
        [InlineKeyboardButton("🔍 Just Search", callback_data="skip_save_filters")],
        [InlineKeyboardButton("« Back", callback_data="back_filters")]
    ]
    return InlineKeyboardMarkup(keyboard)


def cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Simple cancel keyboard for text input
    
    Returns:
        InlineKeyboardMarkup with cancel button
    """
    keyboard = [
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_input")]
    ]
    return InlineKeyboardMarkup(keyboard)


def back_to_main_keyboard() -> InlineKeyboardMarkup:
    """
    Simple back to main menu keyboard
    
    Returns:
        InlineKeyboardMarkup with back button
    """
    keyboard = [
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def quick_filters_keyboard() -> InlineKeyboardMarkup:
    """
    Quick filter presets keyboard
    
    Returns:
        InlineKeyboardMarkup with quick filter options
    """
    keyboard = [
        [InlineKeyboardButton("🏠 2.5 rooms, Rent", callback_data="quick_2.5_rent")],
        [InlineKeyboardButton("🏠 3.5 rooms, Rent", callback_data="quick_3.5_rent")],
        [InlineKeyboardButton("🏠 4.5 rooms, Rent", callback_data="quick_4.5_rent")],
        [InlineKeyboardButton("🏡 House for Sale", callback_data="quick_house_sale")],
        [InlineKeyboardButton("⚙️ Custom Filters", callback_data="menu_filters")],
        [InlineKeyboardButton("« Back", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def city_suggestions_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard with popular Ticino cities
    
    Returns:
        InlineKeyboardMarkup with city suggestions
    """
    cities = [
        ("Lugano", "city_Lugano"),
        ("Bellinzona", "city_Bellinzona"),
        ("Locarno", "city_Locarno"),
        ("Mendrisio", "city_Mendrisio"),
        ("Chiasso", "city_Chiasso"),
        ("Ascona", "city_Ascona")
    ]
    
    keyboard = []
    
    # Add cities in pairs
    for i in range(0, len(cities), 2):
        row = []
        row.append(InlineKeyboardButton(cities[i][0], callback_data=cities[i][1]))
        if i + 1 < len(cities):
            row.append(InlineKeyboardButton(cities[i+1][0], callback_data=cities[i+1][1]))
        keyboard.append(row)
    
    # Option to enter custom city
    keyboard.append([InlineKeyboardButton("✏️ Altra città / Andere Stadt / Other City", callback_data="city_custom")])
    keyboard.append([InlineKeyboardButton("❌ Rimuovi / Entfernen / Remove", callback_data="city_NONE")])
    keyboard.append([InlineKeyboardButton("« Indietro / Zurück / Back", callback_data="back_filters")])
    
    return InlineKeyboardMarkup(keyboard)


def room_presets_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard with room number presets
    
    Returns:
        InlineKeyboardMarkup with room options
    """
    keyboard = [
        [
            InlineKeyboardButton("1-2 rooms", callback_data="rooms_1_2"),
            InlineKeyboardButton("2-3 rooms", callback_data="rooms_2_3")
        ],
        [
            InlineKeyboardButton("3-4 rooms", callback_data="rooms_3_4"),
            InlineKeyboardButton("4-5 rooms", callback_data="rooms_4_5")
        ],
        [
            InlineKeyboardButton("5+ rooms", callback_data="rooms_5_99")
        ],
        [InlineKeyboardButton("✏️ Personalizza / Anpassen / Custom", callback_data="rooms_custom")],
        [InlineKeyboardButton("❌ Rimuovi / Entfernen / Remove", callback_data="rooms_NONE")],
        [InlineKeyboardButton("« Indietro / Zurück / Back", callback_data="back_filters")]
    ]
    return InlineKeyboardMarkup(keyboard)


def price_presets_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard with price presets
    
    Returns:
        InlineKeyboardMarkup with price options
    """
    keyboard = [
        [
            InlineKeyboardButton("< CHF 1'500", callback_data="price_1500"),
            InlineKeyboardButton("< CHF 2'000", callback_data="price_2000")
        ],
        [
            InlineKeyboardButton("< CHF 2'500", callback_data="price_2500"),
            InlineKeyboardButton("< CHF 3'000", callback_data="price_3000")
        ],
        [
            InlineKeyboardButton("< CHF 4'000", callback_data="price_4000"),
            InlineKeyboardButton("< CHF 5'000", callback_data="price_5000")
        ],
        [InlineKeyboardButton("✏️ Personalizza / Anpassen / Custom", callback_data="price_custom")],
        [InlineKeyboardButton("❌ Rimuovi / Entfernen / Remove", callback_data="price_NONE")],
        [InlineKeyboardButton("« Indietro / Zurück / Back", callback_data="back_filters")]
    ]
    return InlineKeyboardMarkup(keyboard)


def surface_presets_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard with surface area presets
    
    Returns:
        InlineKeyboardMarkup with surface options
    """
    keyboard = [
        [
            InlineKeyboardButton("≥ 50 m²", callback_data="surface_50"),
            InlineKeyboardButton("≥ 70 m²", callback_data="surface_70")
        ],
        [
            InlineKeyboardButton("≥ 90 m²", callback_data="surface_90"),
            InlineKeyboardButton("≥ 120 m²", callback_data="surface_120")
        ],
        [
            InlineKeyboardButton("≥ 150 m²", callback_data="surface_150")
        ],
        [InlineKeyboardButton("✏️ Personalizza / Anpassen / Custom", callback_data="surface_custom")],
        [InlineKeyboardButton("❌ Rimuovi / Entfernen / Remove", callback_data="surface_NONE")],
        [InlineKeyboardButton("« Indietro / Zurück / Back", callback_data="back_filters")]
    ]
    return InlineKeyboardMarkup(keyboard)
