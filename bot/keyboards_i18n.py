"""
Multilingual Keyboard Layouts for Ticino Real Estate Bot

This module defines all inline keyboards with multilingual support.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional, List

# Button labels in different languages
BUTTON_LABELS = {
    # Main menu
    'search_properties': {
        'it': '🔍 Cerca Immobili',
        'de': '🔍 Immobilien suchen',
        'en': '🔍 Search Properties'
    },
    'manage_filters': {
        'it': '⚙️ Gestisci Filtri',
        'de': '⚙️ Filter verwalten',
        'en': '⚙️ Manage Filters'
    },
    'my_alerts': {
        'it': '🔔 I Miei Alert',
        'de': '🔔 Meine Benachrichtigungen',
        'en': '🔔 My Alerts'
    },
    'statistics': {
        'it': '📊 Statistiche',
        'de': '📊 Statistiken',
        'en': '📊 Statistics'
    },
    'settings': {
        'it': '⚙️ Impostazioni',
        'de': '⚙️ Einstellungen',
        'en': '⚙️ Settings'
    },
    'help': {
        'it': '❓ Aiuto',
        'de': '❓ Hilfe',
        'en': '❓ Help'
    },
    
    # Search types
    'rent': {
        'it': '🏠 Affitto',
        'de': '🏠 Miete',
        'en': '🏠 Rent'
    },
    'sale': {
        'it': '🏡 Vendita',
        'de': '🏡 Kauf',
        'en': '🏡 Sale'
    },
    'all_types': {
        'it': '🔍 Tutti i Tipi',
        'de': '🔍 Alle Typen',
        'en': '🔍 All Types'
    },
    
    # Filters
    'set_city': {
        'it': '📍 Imposta Città',
        'de': '📍 Stadt festlegen',
        'en': '📍 Set City'
    },
    'set_rooms': {
        'it': '🛏️ Imposta Locali',
        'de': '🛏️ Zimmer festlegen',
        'en': '🛏️ Set Rooms'
    },
    'set_max_price': {
        'it': '💰 Prezzo Massimo',
        'de': '💰 Höchstpreis',
        'en': '💰 Max Price'
    },
    'set_min_surface': {
        'it': '📐 Superficie Minima',
        'de': '📐 Mindestfläche',
        'en': '📐 Min Surface'
    },
    'set_type': {
        'it': '🏷️ Tipo (Affitto/Vendita)',
        'de': '🏷️ Typ (Miete/Kauf)',
        'en': '🏷️ Type (Rent/Sale)'
    },
    'clear_filters': {
        'it': '🗑️ Cancella Tutti',
        'de': '🗑️ Alle löschen',
        'en': '🗑️ Clear All'
    },
    'search_with_filters': {
        'it': '✅ Cerca con Filtri',
        'de': '✅ Mit Filtern suchen',
        'en': '✅ Search with Filters'
    },
    'remove_filter': {
        'it': '❌ Rimuovi Filtro',
        'de': '❌ Filter entfernen',
        'en': '❌ Remove Filter'
    },
    
    # Navigation
    'back': {
        'it': '« Indietro',
        'de': '« Zurück',
        'en': '« Back'
    },
    'previous': {
        'it': '⬅️ Precedente',
        'de': '⬅️ Zurück',
        'en': '⬅️ Previous'
    },
    'next': {
        'it': 'Successivo ➡️',
        'de': 'Weiter ➡️',
        'en': 'Next ➡️'
    },
    'new_search': {
        'it': '🔍 Nuova Ricerca',
        'de': '🔍 Neue Suche',
        'en': '🔍 New Search'
    },
    'main_menu': {
        'it': '🏠 Menu Principale',
        'de': '🏠 Hauptmenü',
        'en': '🏠 Main Menu'
    },
    
    # Alerts
    'create_alert': {
        'it': '➕ Crea Nuovo Alert',
        'de': '➕ Neue Benachrichtigung',
        'en': '➕ Create New Alert'
    },
    'pause_alert': {
        'it': '⏸️ Pausa Alert',
        'de': '⏸️ Benachrichtigung pausieren',
        'en': '⏸️ Pause Alert'
    },
    'activate_alert': {
        'it': '▶️ Attiva Alert',
        'de': '▶️ Benachrichtigung aktivieren',
        'en': '▶️ Activate Alert'
    },
    'search_now': {
        'it': '🔍 Cerca Ora',
        'de': '🔍 Jetzt suchen',
        'en': '🔍 Search Now'
    },
    'delete_alert': {
        'it': '🗑️ Elimina Alert',
        'de': '🗑️ Benachrichtigung löschen',
        'en': '🗑️ Delete Alert'
    },
    'back_to_alerts': {
        'it': '« Torna agli Alert',
        'de': '« Zurück zu Benachrichtigungen',
        'en': '« Back to Alerts'
    },
    
    # Confirmation
    'confirm': {
        'it': '✅ Sì, Conferma',
        'de': '✅ Ja, bestätigen',
        'en': '✅ Yes, Confirm'
    },
    'cancel': {
        'it': '❌ Annulla',
        'de': '❌ Abbrechen',
        'en': '❌ Cancel'
    },
    
    # Other
    'save_alert': {
        'it': '💾 Salva come Alert',
        'de': '💾 Als Benachrichtigung speichern',
        'en': '💾 Save as Alert'
    },
    'just_search': {
        'it': '🔍 Solo Cerca',
        'de': '🔍 Nur suchen',
        'en': '🔍 Just Search'
    },
    'custom': {
        'it': '✏️ Personalizza',
        'de': '✏️ Anpassen',
        'en': '✏️ Custom'
    },
    'enter_other': {
        'it': '✏️ Inserisci Altro',
        'de': '✏️ Andere eingeben',
        'en': '✏️ Enter Other'
    },
    'custom_range': {
        'it': '✏️ Range Personalizzato',
        'de': '✏️ Eigener Bereich',
        'en': '✏️ Custom Range'
    },
    'change_language': {
        'it': '🌍 Cambia Lingua',
        'de': '🌍 Sprache ändern',
        'en': '🌍 Change Language'
    }
}


def get_label(key: str, lang: str = 'it') -> str:
    """Get button label in specified language"""
    if key not in BUTTON_LABELS:
        return key
    return BUTTON_LABELS[key].get(lang, BUTTON_LABELS[key].get('it', key))


def language_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Language selection keyboard (no translation needed)
    
    Returns:
        InlineKeyboardMarkup with language options
    """
    keyboard = [
        [InlineKeyboardButton("🇮🇹 Italiano", callback_data="lang_it")],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
    ]
    return InlineKeyboardMarkup(keyboard)


def main_menu_keyboard(lang: str = 'it') -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_label('search_properties', lang), callback_data="menu_search")],
        [InlineKeyboardButton(get_label('manage_filters', lang), callback_data="menu_filters")],
        [InlineKeyboardButton(get_label('my_alerts', lang), callback_data="menu_alerts")],
        [InlineKeyboardButton(get_label('statistics', lang), callback_data="menu_stats")],
        [
            InlineKeyboardButton(get_label('settings', lang), callback_data="menu_settings"),
            InlineKeyboardButton(get_label('help', lang), callback_data="menu_help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def settings_keyboard(lang: str = 'it') -> InlineKeyboardMarkup:
    """Settings menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_label('change_language', lang), callback_data="settings_language")],
        [InlineKeyboardButton(get_label('back', lang), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def search_type_keyboard(lang: str = 'it') -> InlineKeyboardMarkup:
    """Keyboard to select search type"""
    keyboard = [
        [InlineKeyboardButton(get_label('rent', lang), callback_data="search_type_RENT")],
        [InlineKeyboardButton(get_label('sale', lang), callback_data="search_type_SALE")],
        [InlineKeyboardButton(get_label('all_types', lang), callback_data="search_type_ALL")],
        [InlineKeyboardButton(get_label('back', lang), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def filter_menu_keyboard(lang: str = 'it') -> InlineKeyboardMarkup:
    """Filter management menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_label('set_city', lang), callback_data="filter_city")],
        [InlineKeyboardButton(get_label('set_rooms', lang), callback_data="filter_rooms")],
        [InlineKeyboardButton(get_label('set_max_price', lang), callback_data="filter_price")],
        [InlineKeyboardButton(get_label('set_min_surface', lang), callback_data="filter_surface")],
        [InlineKeyboardButton(get_label('set_type', lang), callback_data="filter_type")],
        [InlineKeyboardButton(get_label('clear_filters', lang), callback_data="filter_clear")],
        [InlineKeyboardButton(get_label('search_with_filters', lang), callback_data="filter_search")],
        [InlineKeyboardButton(get_label('back', lang), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def offer_type_keyboard(lang: str = 'it') -> InlineKeyboardMarkup:
    """Keyboard to select offer type"""
    keyboard = [
        [InlineKeyboardButton(get_label('rent', lang), callback_data="set_type_RENT")],
        [InlineKeyboardButton(get_label('sale', lang), callback_data="set_type_SALE")],
        [InlineKeyboardButton(get_label('remove_filter', lang), callback_data="set_type_NONE")],
        [InlineKeyboardButton(get_label('back', lang), callback_data="back_filters")]
    ]
    return InlineKeyboardMarkup(keyboard)


def pagination_keyboard(current_page: int, total_pages: int, lang: str = 'it', prefix: str = "page") -> InlineKeyboardMarkup:
    """Navigation keyboard for paginated results"""
    keyboard = []
    
    nav_row = []
    if current_page > 1:
        nav_row.append(InlineKeyboardButton(get_label('previous', lang), callback_data=f"{prefix}_prev_{current_page}"))
    
    nav_row.append(InlineKeyboardButton(f"📄 {current_page}/{total_pages}", callback_data="page_info"))
    
    if current_page < total_pages:
        nav_row.append(InlineKeyboardButton(get_label('next', lang), callback_data=f"{prefix}_next_{current_page}"))
    
    keyboard.append(nav_row)
    
    action_row = [
        InlineKeyboardButton(get_label('new_search', lang), callback_data="menu_search"),
        InlineKeyboardButton(get_label('main_menu', lang), callback_data="back_main")
    ]
    keyboard.append(action_row)
    
    return InlineKeyboardMarkup(keyboard)


def alert_list_keyboard(alerts: List[tuple], lang: str = 'it', has_alerts: bool = True) -> InlineKeyboardMarkup:
    """Keyboard showing list of user's alerts"""
    keyboard = []
    
    if has_alerts:
        for alert_id, description, is_active in alerts:
            status_icon = "✅" if is_active else "⏸️"
            button_text = f"{status_icon} Alert #{alert_id}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"alert_view_{alert_id}")])
    
    keyboard.append([InlineKeyboardButton(get_label('create_alert', lang), callback_data="alert_create")])
    keyboard.append([InlineKeyboardButton(get_label('back', lang), callback_data="back_main")])
    
    return InlineKeyboardMarkup(keyboard)


def alert_actions_keyboard(alert_id: int, is_active: bool, lang: str = 'it') -> InlineKeyboardMarkup:
    """Keyboard with actions for a specific alert"""
    keyboard = []
    
    toggle_text = get_label('pause_alert', lang) if is_active else get_label('activate_alert', lang)
    keyboard.append([InlineKeyboardButton(toggle_text, callback_data=f"alert_toggle_{alert_id}")])
    
    keyboard.append([InlineKeyboardButton(get_label('search_now', lang), callback_data=f"alert_search_{alert_id}")])
    keyboard.append([InlineKeyboardButton(get_label('delete_alert', lang), callback_data=f"alert_delete_confirm_{alert_id}")])
    keyboard.append([InlineKeyboardButton(get_label('back_to_alerts', lang), callback_data="menu_alerts")])
    
    return InlineKeyboardMarkup(keyboard)


def confirm_keyboard(action: str, item_id: Optional[int] = None, lang: str = 'it') -> InlineKeyboardMarkup:
    """Confirmation keyboard"""
    callback_confirm = f"confirm_{action}_{item_id}" if item_id else f"confirm_{action}"
    callback_cancel = f"cancel_{action}_{item_id}" if item_id else f"cancel_{action}"
    
    keyboard = [
        [
            InlineKeyboardButton(get_label('confirm', lang), callback_data=callback_confirm),
            InlineKeyboardButton(get_label('cancel', lang), callback_data=callback_cancel)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def cancel_keyboard(lang: str = 'it') -> InlineKeyboardMarkup:
    """Simple cancel keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_label('cancel', lang), callback_data="cancel_input")]
    ]
    return InlineKeyboardMarkup(keyboard)


def back_to_main_keyboard(lang: str = 'it') -> InlineKeyboardMarkup:
    """Back to main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_label('main_menu', lang), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


# Keep existing keyboards from keyboards.py for presets (they use numbers/symbols, no translation needed)
from .keyboards import (
    city_suggestions_keyboard,
    room_presets_keyboard,
    price_presets_keyboard,
    surface_presets_keyboard
)
