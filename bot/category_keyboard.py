"""
Property Category Keyboard with Multilingual Support
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Category translations
CATEGORY_LABELS = {
    'APARTMENT': {
        'it': '🏢 Appartamento',
        'de': '🏢 Wohnung',
        'en': '🏢 Apartment'
    },
    'HOUSE': {
        'it': '🏡 Casa',
        'de': '🏡 Haus',
        'en': '🏡 House'
    },
    'PARK': {
        'it': '🅿️ Parcheggio/Garage',
        'de': '🅿️ Parkplatz/Garage',
        'en': '🅿️ Parking/Garage'
    },
    'INDUSTRY': {
        'it': '🏪 Commerciale/Ufficio',
        'de': '🏪 Gewerbe/Büro',
        'en': '🏪 Commercial/Office'
    },
    'SHARED': {
        'it': '🚪 Stanza Condivisa',
        'de': '🚪 WG-Zimmer',
        'en': '🚪 Shared Room'
    }
}

BACK_LABEL = {
    'it': '« Indietro',
    'de': '« Zurück',
    'en': '« Back'
}

REMOVE_LABEL = {
    'it': '❌ Rimuovi Filtro',
    'de': '❌ Filter entfernen',
    'en': '❌ Remove Filter'
}


def get_category_label(category: str, lang: str = 'it') -> str:
    """Get category label in specified language"""
    if category in CATEGORY_LABELS:
        return CATEGORY_LABELS[category].get(lang, CATEGORY_LABELS[category]['it'])
    return category


def category_keyboard(lang: str = 'it') -> InlineKeyboardMarkup:
    """
    Keyboard with property category options
    
    Args:
        lang: Language code (it, de, en)
        
    Returns:
        InlineKeyboardMarkup with category options
    """
    keyboard = [
        [InlineKeyboardButton(
            get_category_label('APARTMENT', lang),
            callback_data='category_APARTMENT'
        )],
        [InlineKeyboardButton(
            get_category_label('HOUSE', lang),
            callback_data='category_HOUSE'
        )],
        [InlineKeyboardButton(
            get_category_label('PARK', lang),
            callback_data='category_PARK'
        )],
        [InlineKeyboardButton(
            get_category_label('INDUSTRY', lang),
            callback_data='category_INDUSTRY'
        )],
        [InlineKeyboardButton(
            get_category_label('SHARED', lang),
            callback_data='category_SHARED'
        )],
        [InlineKeyboardButton(
            REMOVE_LABEL.get(lang, REMOVE_LABEL['it']),
            callback_data='category_NONE'
        )],
        [InlineKeyboardButton(
            BACK_LABEL.get(lang, BACK_LABEL['it']),
            callback_data='back_filters'
        )]
    ]
    return InlineKeyboardMarkup(keyboard)
