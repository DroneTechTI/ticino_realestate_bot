"""
Multilingual Messages for Ticino Real Estate Bot

This module contains all bot messages in multiple languages:
- Italian (IT) - Default
- German (DE)
- English (EN)
"""

# Supported languages
SUPPORTED_LANGUAGES = ['it', 'de', 'en']
DEFAULT_LANGUAGE = 'it'

# Language names for display
LANGUAGE_NAMES = {
    'it': '🇮🇹 Italiano',
    'de': '🇩🇪 Deutsch',
    'en': '🇬🇧 English'
}

# All bot messages organized by key and language
MESSAGES = {
    # Welcome and Start
    'welcome': {
        'it': (
            "🏠 <b>Benvenuto su Ticino Real Estate Bot!</b>\n\n"
            "Trova il tuo immobile ideale in Ticino con filtri personalizzati "
            "e ricevi notifiche automatiche per nuovi annunci.\n\n"
            "<b>Cosa posso fare per te:</b>\n"
            "🔍 Cercare immobili con filtri avanzati\n"
            "💾 Salvare le tue ricerche preferite\n"
            "🔔 Ricevere notifiche automatiche\n"
            "📊 Vedere statistiche personalizzate\n\n"
            "Seleziona un'opzione dal menu qui sotto per iniziare!"
        ),
        'de': (
            "🏠 <b>Willkommen beim Ticino Real Estate Bot!</b>\n\n"
            "Finden Sie Ihre ideale Immobilie im Tessin mit personalisierten Filtern "
            "und erhalten Sie automatische Benachrichtigungen für neue Anzeigen.\n\n"
            "<b>Was ich für Sie tun kann:</b>\n"
            "🔍 Immobilien mit erweiterten Filtern suchen\n"
            "💾 Ihre Lieblingssuchen speichern\n"
            "🔔 Automatische Benachrichtigungen erhalten\n"
            "📊 Personalisierte Statistiken anzeigen\n\n"
            "Wählen Sie eine Option aus dem Menü unten, um zu beginnen!"
        ),
        'en': (
            "🏠 <b>Welcome to Ticino Real Estate Bot!</b>\n\n"
            "Find your ideal property in Ticino with personalized filters "
            "and receive automatic notifications for new listings.\n\n"
            "<b>What I can do for you:</b>\n"
            "🔍 Search properties with advanced filters\n"
            "💾 Save your favorite searches\n"
            "🔔 Receive automatic notifications\n"
            "📊 View personalized statistics\n\n"
            "Select an option from the menu below to get started!"
        )
    },
    
    # Help
    'help': {
        'it': (
            "❓ <b>Guida all'uso del Bot</b>\n\n"
            "<b>Comandi disponibili:</b>\n"
            "/start - Avvia il bot e mostra il menu principale\n"
            "/search - Cerca immobili\n"
            "/filters - Gestisci i tuoi filtri di ricerca\n"
            "/alerts - Gestisci i tuoi alert\n"
            "/language - Cambia lingua\n"
            "/help - Mostra questa guida\n\n"
            "<b>Come funziona:</b>\n"
            "1️⃣ Imposta i tuoi filtri (città, locali, prezzo, ecc.)\n"
            "2️⃣ Cerca immobili o salva un alert\n"
            "3️⃣ Ricevi notifiche automatiche quando escono nuovi annunci\n\n"
            "<b>Filtri disponibili:</b>\n"
            "📍 Città del Ticino\n"
            "🛏️ Numero di locali (min/max)\n"
            "💰 Prezzo massimo\n"
            "📐 Superficie minima\n"
            "🏷️ Tipo (affitto/vendita)\n\n"
            "Per qualsiasi domanda, contattami con il pulsante qui sotto!"
        ),
        'de': (
            "❓ <b>Bot-Bedienungsanleitung</b>\n\n"
            "<b>Verfügbare Befehle:</b>\n"
            "/start - Bot starten und Hauptmenü anzeigen\n"
            "/search - Immobilien suchen\n"
            "/filters - Suchfilter verwalten\n"
            "/alerts - Benachrichtigungen verwalten\n"
            "/language - Sprache ändern\n"
            "/help - Diese Anleitung anzeigen\n\n"
            "<b>Wie es funktioniert:</b>\n"
            "1️⃣ Legen Sie Ihre Filter fest (Stadt, Zimmer, Preis, etc.)\n"
            "2️⃣ Suchen Sie nach Immobilien oder speichern Sie eine Benachrichtigung\n"
            "3️⃣ Erhalten Sie automatische Benachrichtigungen bei neuen Anzeigen\n\n"
            "<b>Verfügbare Filter:</b>\n"
            "📍 Städte im Tessin\n"
            "🛏️ Anzahl Zimmer (min/max)\n"
            "💰 Höchstpreis\n"
            "📐 Mindestfläche\n"
            "🏷️ Typ (Miete/Kauf)\n\n"
            "Bei Fragen kontaktieren Sie mich über die Schaltfläche unten!"
        ),
        'en': (
            "❓ <b>Bot User Guide</b>\n\n"
            "<b>Available commands:</b>\n"
            "/start - Start the bot and show main menu\n"
            "/search - Search properties\n"
            "/filters - Manage your search filters\n"
            "/alerts - Manage your alerts\n"
            "/language - Change language\n"
            "/help - Show this guide\n\n"
            "<b>How it works:</b>\n"
            "1️⃣ Set your filters (city, rooms, price, etc.)\n"
            "2️⃣ Search properties or save an alert\n"
            "3️⃣ Receive automatic notifications for new listings\n\n"
            "<b>Available filters:</b>\n"
            "📍 Cities in Ticino\n"
            "🛏️ Number of rooms (min/max)\n"
            "💰 Maximum price\n"
            "📐 Minimum surface\n"
            "🏷️ Type (rent/sale)\n\n"
            "For any questions, contact me using the button below!"
        )
    },
    
    # Language selection
    'language_select': {
        'it': "🌍 <b>Seleziona la tua lingua</b>\n\nScegli la lingua preferita per il bot:",
        'de': "🌍 <b>Wählen Sie Ihre Sprache</b>\n\nWählen Sie Ihre bevorzugte Bot-Sprache:",
        'en': "🌍 <b>Select your language</b>\n\nChoose your preferred bot language:"
    },
    
    'language_changed': {
        'it': "✅ Lingua cambiata in Italiano!",
        'de': "✅ Sprache auf Deutsch geändert!",
        'en': "✅ Language changed to English!"
    },
    
    # Search
    'search_type_prompt': {
        'it': "🔍 <b>Ricerca Immobili</b>\n\nCosa stai cercando?",
        'de': "🔍 <b>Immobiliensuche</b>\n\nWas suchen Sie?",
        'en': "🔍 <b>Property Search</b>\n\nWhat are you looking for?"
    },
    
    'no_results': {
        'it': (
            "😕 <b>Nessun risultato trovato</b>\n\n"
            "Non ho trovato immobili che corrispondono ai tuoi criteri.\n\n"
            "Suggerimenti:\n"
            "• Prova a rimuovere alcuni filtri\n"
            "• Aumenta il prezzo massimo\n"
            "• Riduci la superficie minima\n"
            "• Cambia città o cerca senza filtro città"
        ),
        'de': (
            "😕 <b>Keine Ergebnisse gefunden</b>\n\n"
            "Ich habe keine Immobilien gefunden, die Ihren Kriterien entsprechen.\n\n"
            "Vorschläge:\n"
            "• Versuchen Sie, einige Filter zu entfernen\n"
            "• Erhöhen Sie den Höchstpreis\n"
            "• Reduzieren Sie die Mindestfläche\n"
            "• Ändern Sie die Stadt oder suchen Sie ohne Stadtfilter"
        ),
        'en': (
            "😕 <b>No results found</b>\n\n"
            "I couldn't find any properties matching your criteria.\n\n"
            "Suggestions:\n"
            "• Try removing some filters\n"
            "• Increase maximum price\n"
            "• Reduce minimum surface\n"
            "• Change city or search without city filter"
        )
    },
    
    'search_results_header': {
        'it': "✅ <b>Trovati {count} immobili</b>\n\nMostrando pagina {page} di {total_pages}",
        'de': "✅ <b>{count} Immobilien gefunden</b>\n\nSeite {page} von {total_pages}",
        'en': "✅ <b>Found {count} properties</b>\n\nShowing page {page} of {total_pages}"
    },
    
    # Filters
    'filter_menu': {
        'it': "⚙️ <b>Gestione Filtri</b>\n\nImposta i tuoi criteri di ricerca:",
        'de': "⚙️ <b>Filter verwalten</b>\n\nLegen Sie Ihre Suchkriterien fest:",
        'en': "⚙️ <b>Manage Filters</b>\n\nSet your search criteria:"
    },
    
    'filter_city_prompt': {
        'it': "📍 <b>Seleziona Città</b>\n\nScegli una città o inserisci il nome di un comune del Ticino:",
        'de': "📍 <b>Stadt auswählen</b>\n\nWählen Sie eine Stadt oder geben Sie den Namen einer Tessiner Gemeinde ein:",
        'en': "📍 <b>Select City</b>\n\nChoose a city or enter the name of a Ticino municipality:"
    },
    
    'filter_city_input': {
        'it': "📍 Inserisci il nome della città:\n\n(Es: Lugano, Bellinzona, Locarno, etc.)",
        'de': "📍 Geben Sie den Stadtnamen ein:\n\n(Z.B.: Lugano, Bellinzona, Locarno, etc.)",
        'en': "📍 Enter the city name:\n\n(Ex: Lugano, Bellinzona, Locarno, etc.)"
    },
    
    'filter_city_set': {
        'it': "✅ Città impostata: <b>{city}</b>",
        'de': "✅ Stadt festgelegt: <b>{city}</b>",
        'en': "✅ City set: <b>{city}</b>"
    },
    
    'filter_rooms_prompt': {
        'it': "🛏️ <b>Numero di Locali</b>\n\nSeleziona un range o inserisci valori personalizzati:",
        'de': "🛏️ <b>Anzahl Zimmer</b>\n\nWählen Sie einen Bereich oder geben Sie eigene Werte ein:",
        'en': "🛏️ <b>Number of Rooms</b>\n\nSelect a range or enter custom values:"
    },
    
    'filter_rooms_input': {
        'it': "🛏️ Inserisci il numero minimo di locali:\n\n(Es: 2, 2.5, 3, 3.5, etc.)",
        'de': "🛏️ Geben Sie die Mindestzahl der Zimmer ein:\n\n(Z.B.: 2, 2.5, 3, 3.5, etc.)",
        'en': "🛏️ Enter minimum number of rooms:\n\n(Ex: 2, 2.5, 3, 3.5, etc.)"
    },
    
    'filter_rooms_set': {
        'it': "✅ Locali impostati: <b>{min} - {max}</b>",
        'de': "✅ Zimmer festgelegt: <b>{min} - {max}</b>",
        'en': "✅ Rooms set: <b>{min} - {max}</b>"
    },
    
    'filter_price_prompt': {
        'it': "💰 <b>Prezzo Massimo</b>\n\nSeleziona una fascia di prezzo o inserisci un valore personalizzato:",
        'de': "💰 <b>Höchstpreis</b>\n\nWählen Sie eine Preisspanne oder geben Sie einen eigenen Wert ein:",
        'en': "💰 <b>Maximum Price</b>\n\nSelect a price range or enter a custom value:"
    },
    
    'filter_price_input': {
        'it': "💰 Inserisci il prezzo massimo in CHF:\n\n(Es: 2000, 2500, 3000, etc.)",
        'de': "💰 Geben Sie den Höchstpreis in CHF ein:\n\n(Z.B.: 2000, 2500, 3000, etc.)",
        'en': "💰 Enter maximum price in CHF:\n\n(Ex: 2000, 2500, 3000, etc.)"
    },
    
    'filter_price_set': {
        'it': "✅ Prezzo massimo: <b>CHF {price}</b>",
        'de': "✅ Höchstpreis: <b>CHF {price}</b>",
        'en': "✅ Maximum price: <b>CHF {price}</b>"
    },
    
    'filter_surface_prompt': {
        'it': "📐 <b>Superficie Minima</b>\n\nSeleziona una superficie minima o inserisci un valore personalizzato:",
        'de': "📐 <b>Mindestfläche</b>\n\nWählen Sie eine Mindestfläche oder geben Sie einen eigenen Wert ein:",
        'en': "📐 <b>Minimum Surface</b>\n\nSelect a minimum surface or enter a custom value:"
    },
    
    'filter_surface_input': {
        'it': "📐 Inserisci la superficie minima in m²:\n\n(Es: 50, 70, 90, 120, etc.)",
        'de': "📐 Geben Sie die Mindestfläche in m² ein:\n\n(Z.B.: 50, 70, 90, 120, etc.)",
        'en': "📐 Enter minimum surface in m²:\n\n(Ex: 50, 70, 90, 120, etc.)"
    },
    
    'filter_surface_set': {
        'it': "✅ Superficie minima: <b>{surface} m²</b>",
        'de': "✅ Mindestfläche: <b>{surface} m²</b>",
        'en': "✅ Minimum surface: <b>{surface} m²</b>"
    },
    
    'filter_type_prompt': {
        'it': "🏷️ <b>Tipo di Immobile</b>\n\nCosa stai cercando?",
        'de': "🏷️ <b>Immobilientyp</b>\n\nWas suchen Sie?",
        'en': "🏷️ <b>Property Type</b>\n\nWhat are you looking for?"
    },
    
    'filter_type_set_rent': {
        'it': "✅ Tipo impostato: <b>Affitto</b>",
        'de': "✅ Typ festgelegt: <b>Miete</b>",
        'en': "✅ Type set: <b>Rent</b>"
    },
    
    'filter_type_set_sale': {
        'it': "✅ Tipo impostato: <b>Vendita</b>",
        'de': "✅ Typ festgelegt: <b>Kauf</b>",
        'en': "✅ Type set: <b>Sale</b>"
    },
    
    'filters_cleared': {
        'it': "🗑️ Tutti i filtri sono stati rimossi!",
        'de': "🗑️ Alle Filter wurden entfernt!",
        'en': "🗑️ All filters have been cleared!"
    },
    
    # Alerts
    'alerts_menu': {
        'it': "🔔 <b>I Miei Alert</b>\n\nGestisci i tuoi alert di notifica:",
        'de': "🔔 <b>Meine Benachrichtigungen</b>\n\nVerwalten Sie Ihre Benachrichtigungen:",
        'en': "🔔 <b>My Alerts</b>\n\nManage your notification alerts:"
    },
    
    'no_alerts': {
        'it': "📭 Non hai ancora nessun alert attivo.\n\nCrea un alert per ricevere notifiche automatiche!",
        'de': "📭 Sie haben noch keine aktiven Benachrichtigungen.\n\nErstellen Sie eine Benachrichtigung, um automatische Updates zu erhalten!",
        'en': "📭 You don't have any active alerts yet.\n\nCreate an alert to receive automatic notifications!"
    },
    
    'alert_created': {
        'it': "✅ <b>Alert creato con successo!</b>\n\nRiceverai notifiche quando usciranno nuovi annunci corrispondenti ai tuoi criteri.",
        'de': "✅ <b>Benachrichtigung erfolgreich erstellt!</b>\n\nSie erhalten Benachrichtigungen, wenn neue Anzeigen Ihren Kriterien entsprechen.",
        'en': "✅ <b>Alert created successfully!</b>\n\nYou'll receive notifications when new listings match your criteria."
    },
    
    'alert_deleted': {
        'it': "🗑️ Alert eliminato con successo!",
        'de': "🗑️ Benachrichtigung erfolgreich gelöscht!",
        'en': "🗑️ Alert deleted successfully!"
    },
    
    'alert_toggled': {
        'it': "✅ Stato dell'alert modificato!",
        'de': "✅ Benachrichtigungsstatus geändert!",
        'en': "✅ Alert status changed!"
    },
    
    # Statistics
    'user_stats': {
        'it': (
            "📊 <b>Le Tue Statistiche</b>\n\n"
            "🔔 Alert attivi: {active_alerts}\n"
            "📬 Immobili ricevuti: {properties_received}\n"
            "📅 Iscritto dal: {member_since}"
        ),
        'de': (
            "📊 <b>Ihre Statistiken</b>\n\n"
            "🔔 Aktive Benachrichtigungen: {active_alerts}\n"
            "📬 Erhaltene Immobilien: {properties_received}\n"
            "📅 Mitglied seit: {member_since}"
        ),
        'en': (
            "📊 <b>Your Statistics</b>\n\n"
            "🔔 Active alerts: {active_alerts}\n"
            "📬 Properties received: {properties_received}\n"
            "📅 Member since: {member_since}"
        )
    },
    
    # Errors
    'error_generic': {
        'it': "❌ Si è verificato un errore. Riprova più tardi.",
        'de': "❌ Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.",
        'en': "❌ An error occurred. Please try again later."
    },
    
    'error_invalid_input': {
        'it': "❌ Input non valido. Riprova.",
        'de': "❌ Ungültige Eingabe. Bitte versuchen Sie es erneut.",
        'en': "❌ Invalid input. Please try again."
    },
    
    'operation_cancelled': {
        'it': "❌ Operazione annullata.",
        'de': "❌ Vorgang abgebrochen.",
        'en': "❌ Operation cancelled."
    },
    
    # Confirmation
    'confirm_delete_alert': {
        'it': "⚠️ Sei sicuro di voler eliminare questo alert?",
        'de': "⚠️ Möchten Sie diese Benachrichtigung wirklich löschen?",
        'en': "⚠️ Are you sure you want to delete this alert?"
    }
}


def get_message(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """
    Get a message in the specified language
    
    Args:
        key: Message key
        lang: Language code (it, de, en)
        **kwargs: Format parameters for the message
        
    Returns:
        Formatted message string
    """
    # Validate language
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    
    # Get message
    if key not in MESSAGES:
        return f"[Missing message: {key}]"
    
    message = MESSAGES[key].get(lang, MESSAGES[key].get(DEFAULT_LANGUAGE, ''))
    
    # Format with parameters if provided
    try:
        return message.format(**kwargs)
    except KeyError:
        return message
