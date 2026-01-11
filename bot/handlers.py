"""
Command and Callback Handlers for Ticino Real Estate Bot

This module contains all handlers for user interactions with the bot.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database.db_manager import DatabaseManager
from services.search_service import SearchService
from services.notification_service import NotificationService
from bot.messages import get_message, SUPPORTED_LANGUAGES
from bot.keyboards_i18n import (
    language_selection_keyboard,
    main_menu_keyboard,
    settings_keyboard,
    search_type_keyboard,
    filter_menu_keyboard,
    offer_type_keyboard,
    pagination_keyboard,
    alert_list_keyboard,
    alert_actions_keyboard,
    confirm_keyboard,
    cancel_keyboard,
    back_to_main_keyboard,
    category_keyboard
)
from bot.keyboards import (
    city_suggestions_keyboard,
    room_presets_keyboard,
    price_presets_keyboard,
    surface_presets_keyboard
)
from utils.helpers import (
    validate_room_number,
    validate_price,
    validate_surface
)

logger = logging.getLogger(__name__)


class BotHandlers:
    """Container for all bot command and callback handlers"""
    
    def __init__(self, 
                 db_manager: DatabaseManager,
                 search_service: SearchService,
                 notification_service: NotificationService):
        """
        Initialize handlers with required services
        
        Args:
            db_manager: Database manager instance
            search_service: Search service instance
            notification_service: Notification service instance
        """
        self.db = db_manager
        self.search = search_service
        self.notifier = notification_service
    
    def get_user_lang(self, user_id: int) -> str:
        """Get user's preferred language"""
        return self.db.get_user_language(user_id)
    
    # ==================== COMMAND HANDLERS ====================
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /start command
        Shows language selection for new users, main menu for existing users
        """
        user = update.effective_user
        user_id = user.id
        
        logger.info(f"User {user_id} ({user.username}) started the bot")
        
        # Check if user exists
        existing_user = self.db.get_user(user_id)
        
        if not existing_user:
            # New user - show language selection
            await update.message.reply_text(
                "🌍 <b>Welcome! Willkommen! Benvenuto!</b>\n\n"
                "Please select your preferred language:\n"
                "Bitte wählen Sie Ihre bevorzugte Sprache:\n"
                "Seleziona la tua lingua preferita:",
                parse_mode=ParseMode.HTML,
                reply_markup=language_selection_keyboard()
            )
        else:
            # Existing user - show main menu
            lang = self.get_user_lang(user_id)
            welcome_msg = get_message('welcome', lang)
            
            await update.message.reply_text(
                welcome_msg,
                parse_mode=ParseMode.HTML,
                reply_markup=main_menu_keyboard(lang)
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        help_msg = get_message('help', lang)
        
        await update.message.reply_text(
            help_msg,
            parse_mode=ParseMode.HTML,
            reply_markup=back_to_main_keyboard(lang)
        )
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /search command - quick search"""
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        prompt_msg = get_message('search_type_prompt', lang)
        
        await update.message.reply_text(
            prompt_msg,
            parse_mode=ParseMode.HTML,
            reply_markup=search_type_keyboard(lang)
        )
    
    async def filters_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /filters command - manage filters"""
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        filter_msg = get_message('filter_menu', lang)
        
        await update.message.reply_text(
            filter_msg,
            parse_mode=ParseMode.HTML,
            reply_markup=filter_menu_keyboard(lang)
        )
    
    async def alerts_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /alerts command - manage alerts"""
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        # Get user's alerts
        alerts = self.db.get_user_alerts(user_id, active_only=False)
        
        if alerts:
            # Format alerts for keyboard
            alert_list = []
            for alert in alerts:
                from utils.helpers import format_alert_summary
                summary = format_alert_summary(alert)
                alert_list.append((alert.alert_id, summary, alert.is_active))
            
            msg = get_message('alerts_menu', lang)
            await update.message.reply_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=alert_list_keyboard(alert_list, lang, has_alerts=True)
            )
        else:
            msg = get_message('no_alerts', lang)
            await update.message.reply_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=alert_list_keyboard([], lang, has_alerts=False)
            )
    
    async def language_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /language command - change language"""
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('language_select', lang)
        
        await update.message.reply_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=language_selection_keyboard()
        )
    
    # ==================== CALLBACK QUERY HANDLERS ====================
    
    async def callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Main callback query handler
        Routes callbacks to appropriate handlers
        """
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        data = query.data
        
        logger.info(f"Callback from user {user_id}: {data}")
        
        # Language selection
        if data.startswith('lang_'):
            await self.handle_language_selection(update, context)
        
        # Main menu navigation
        elif data == 'back_main':
            await self.show_main_menu(update, context)
        elif data == 'menu_search':
            await self.show_search_menu(update, context)
        elif data == 'menu_filters':
            await self.show_filters_menu(update, context)
        elif data == 'menu_alerts':
            await self.show_alerts_menu(update, context)
        elif data == 'menu_stats':
            await self.show_statistics(update, context)
        elif data == 'menu_settings':
            await self.show_settings_menu(update, context)
        elif data == 'menu_help':
            await self.show_help(update, context)
        
        # Settings
        elif data == 'settings_language':
            await self.show_language_selection(update, context)
        
        # Filter management
        elif data == 'filter_city':
            await self.show_city_filter(update, context)
        elif data == 'filter_category':
            await self.show_category_filter(update, context)
        elif data == 'filter_rooms':
            await self.show_rooms_filter(update, context)
        elif data == 'filter_price':
            await self.show_price_filter(update, context)
        elif data == 'filter_surface':
            await self.show_surface_filter(update, context)
        elif data == 'filter_type':
            await self.show_type_filter(update, context)
        elif data == 'filter_clear':
            await self.clear_filters(update, context)
        elif data == 'filter_search':
            await self.search_with_filters(update, context)
        
        # Search type selection
        elif data.startswith('search_type_'):
            await self.handle_search_type(update, context)
        
        # City filter callbacks
        elif data.startswith('city_'):
            await self.handle_city_selection(update, context)
        
        # Rooms filter callbacks
        elif data.startswith('rooms_'):
            await self.handle_rooms_selection(update, context)
        
        # Price filter callbacks
        elif data.startswith('price_'):
            await self.handle_price_selection(update, context)
        
        # Surface filter callbacks
        elif data.startswith('surface_'):
            await self.handle_surface_selection(update, context)
        
        # Type filter callbacks
        elif data.startswith('set_type_'):
            await self.handle_type_selection(update, context)
        
        # Category filter callbacks
        elif data.startswith('category_'):
            await self.handle_category_selection(update, context)
        
        # Pagination and property navigation
        elif data.startswith('page_'):
            await self.handle_pagination(update, context)
        elif data.startswith('prop_'):
            await self.handle_property_navigation(update, context)
        
        # Alert management
        elif data.startswith('alert_'):
            await self.handle_alert_action(update, context)
        
        # Confirmation dialogs
        elif data.startswith('confirm_') or data.startswith('cancel_'):
            await self.handle_confirmation(update, context)
        
        # Cancel input
        elif data == 'cancel_input':
            await self.cancel_input(update, context)
        
        # Navigation
        elif data == 'back_filters':
            await self.show_filters_menu(update, context)
        
        else:
            lang = self.get_user_lang(user_id)
            await query.edit_message_text(
                get_message('error_generic', lang),
                parse_mode=ParseMode.HTML
            )
    
    # ==================== MENU HANDLERS ====================
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show main menu"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('welcome', lang)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu_keyboard(lang)
        )
    
    async def show_search_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show search type selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('search_type_prompt', lang)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=search_type_keyboard(lang)
        )
    
    async def show_filters_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show filter management menu"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        # Get current filters from user_data
        filters = context.user_data.get('filters', {})
        
        # Build filter summary
        summary = self.search.get_filter_summary(
            city=filters.get('city'),
            min_rooms=filters.get('min_rooms'),
            max_rooms=filters.get('max_rooms'),
            max_price=filters.get('max_price'),
            min_surface=filters.get('min_surface'),
            offer_type=filters.get('offer_type'),
            object_category=filters.get('object_category')
        )
        
        msg = get_message('filter_menu', lang) + f"\n\n{summary}"
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=filter_menu_keyboard(lang)
        )
    
    async def show_alerts_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show alerts management menu"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        # Get user's alerts
        alerts = self.db.get_user_alerts(user_id, active_only=False)
        
        if alerts:
            from utils.helpers import format_alert_summary
            alert_list = []
            for alert in alerts:
                summary = format_alert_summary(alert)
                alert_list.append((alert.alert_id, summary, alert.is_active))
            
            msg = get_message('alerts_menu', lang)
            await query.edit_message_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=alert_list_keyboard(alert_list, lang, has_alerts=True)
            )
        else:
            msg = get_message('no_alerts', lang)
            await query.edit_message_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=alert_list_keyboard([], lang, has_alerts=False)
            )
    
    async def show_statistics(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user statistics"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        # Get user info and stats
        user = self.db.get_user(user_id)
        stats = self.db.get_user_stats(user_id)
        
        member_since = user.created_at.strftime('%d.%m.%Y') if user else 'Unknown'
        
        msg = get_message('user_stats', lang,
                         active_alerts=stats['active_alerts'],
                         properties_received=stats['properties_received'],
                         member_since=member_since)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=back_to_main_keyboard(lang)
        )
    
    async def show_settings_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show settings menu"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        from bot.messages import LANGUAGE_NAMES
        current_lang_name = LANGUAGE_NAMES.get(lang, 'Unknown')
        
        msg = f"⚙️ <b>Settings / Einstellungen / Impostazioni</b>\n\n"
        msg += f"Current language: {current_lang_name}"
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=settings_keyboard(lang)
        )
    
    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('help', lang)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=back_to_main_keyboard(lang)
        )
    
    # ==================== LANGUAGE HANDLERS ====================
    
    async def show_language_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show language selection menu"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('language_select', lang)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=language_selection_keyboard()
        )
    
    async def handle_language_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection callback"""
        query = update.callback_query
        user = update.effective_user
        user_id = user.id
        
        # Extract language code from callback data (lang_it, lang_de, lang_en)
        lang_code = query.data.split('_')[1]
        
        if lang_code not in SUPPORTED_LANGUAGES:
            lang_code = 'it'
        
        # Check if user exists
        existing_user = self.db.get_user(user_id)
        
        if not existing_user:
            # New user - create with selected language
            self.db.add_user(user_id, user.username, user.first_name, lang_code)
            logger.info(f"New user {user_id} registered with language {lang_code}")
        else:
            # Existing user - update language
            self.db.set_user_language(user_id, lang_code)
            logger.info(f"User {user_id} changed language to {lang_code}")
        
        # Show confirmation and main menu
        confirm_msg = get_message('language_changed', lang_code)
        welcome_msg = get_message('welcome', lang_code)
        
        await query.edit_message_text(
            f"{confirm_msg}\n\n{welcome_msg}",
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu_keyboard(lang_code)
        )
    
    # ==================== FILTER HANDLERS ====================
    
    async def show_city_filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show city filter selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('filter_city_prompt', lang)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=city_suggestions_keyboard()
        )
    
    async def show_rooms_filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show rooms filter selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('filter_rooms_prompt', lang)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=room_presets_keyboard()
        )
    
    async def show_price_filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show price filter selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('filter_price_prompt', lang)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=price_presets_keyboard()
        )
    
    async def show_surface_filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show surface filter selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('filter_surface_prompt', lang)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=surface_presets_keyboard()
        )
    
    async def show_type_filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show offer type filter selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('filter_type_prompt', lang)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=offer_type_keyboard(lang)
        )
    
    async def show_category_filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show property category filter selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        msg = get_message('filter_category_prompt', lang)
        
        await query.edit_message_text(
            msg,
            parse_mode=ParseMode.HTML,
            reply_markup=category_keyboard(lang)
        )
    
    async def clear_filters(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clear all filters"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        # Clear filters from context
        context.user_data['filters'] = {}
        
        msg = get_message('filters_cleared', lang)
        
        await query.answer(msg)
        await self.show_filters_menu(update, context)
    
    async def search_with_filters(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Execute search with current filters"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        # Get filters from context
        filters = context.user_data.get('filters', {})
        
        # Check if any filter is set
        if not self.search.has_any_filter(**filters):
            await query.answer("⚠️ Please set at least one filter first!")
            return
        
        # Execute search
        await self.execute_search(update, context, filters)
    
    # ==================== SEARCH EXECUTION ====================
    
    async def handle_search_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle search type selection (RENT/SALE/ALL)"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        # Extract search type from callback data
        search_type = query.data.split('_')[-1]  # search_type_RENT -> RENT
        
        # Initialize filters if not exists
        if 'filters' not in context.user_data:
            context.user_data['filters'] = {}
        
        # Set offer type filter
        if search_type != 'ALL':
            context.user_data['filters']['offer_type'] = search_type
        
        await query.answer(f"🔍 Searching...")
        
        # Execute search with just the type filter
        await self.execute_search(update, context, context.user_data['filters'])
    
    async def execute_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE, filters: dict):
        """Execute property search and display results"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        # Perform search (page 1)
        total_count, properties, total_pages = self.search.search_properties(
            city=filters.get('city'),
            min_rooms=filters.get('min_rooms'),
            max_rooms=filters.get('max_rooms'),
            max_price=filters.get('max_price'),
            min_surface=filters.get('min_surface'),
            offer_type=filters.get('offer_type'),
            object_category=filters.get('object_category'),
            page=1,
            per_page=5
        )
        
        # Save search context with properties
        context.user_data['last_search'] = {
            'filters': filters.copy(),
            'current_page': 1,
            'total_pages': total_pages,
            'total_count': total_count,
            'current_property_index': 0,
            'properties': properties  # Store current page properties
        }
        
        if total_count == 0:
            # No results
            msg = get_message('no_results', lang)
            await query.edit_message_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=back_to_main_keyboard(lang)
            )
            return
        
        # Answer callback
        await query.answer()
        
        # Send first property in single message with navigation
        await self.send_property_with_navigation(query.message, user_id, context, lang)
    
    async def handle_pagination(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle pagination navigation"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        # Parse callback data: page_prev_2 or page_next_1
        parts = query.data.split('_')
        action = parts[1]  # prev or next
        current_page = int(parts[2])
        
        # Calculate new page
        if action == 'prev':
            new_page = current_page - 1
        else:  # next
            new_page = current_page + 1
        
        # Get search context
        last_search = context.user_data.get('last_search')
        if not last_search:
            await query.answer("❌ Search expired, please start a new search")
            return
        
        filters = last_search['filters']
        total_pages = last_search['total_pages']
        
        # Validate page number
        if new_page < 1 or new_page > total_pages:
            await query.answer("❌ Invalid page")
            return
        
        await query.answer(f"📄 Loading page {new_page}...")
        
        # Perform search for new page
        total_count, properties, _ = self.search.search_properties(
            city=filters.get('city'),
            min_rooms=filters.get('min_rooms'),
            max_rooms=filters.get('max_rooms'),
            max_price=filters.get('max_price'),
            min_surface=filters.get('min_surface'),
            offer_type=filters.get('offer_type'),
            object_category=filters.get('object_category'),
            page=new_page,
            per_page=5
        )
        
        # Update search context
        context.user_data['last_search']['current_page'] = new_page
        context.user_data['last_search']['current_property_index'] = 0
        context.user_data['last_search']['properties'] = properties
        
        # Update to first property of new page
        await self.send_property_with_navigation(query.message, user_id, context, lang, edit_message=True)
    
    # ==================== FILTER PRESET HANDLERS ====================
    
    async def handle_city_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle city selection from presets"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        city_code = query.data.split('_', 1)[1]  # city_Lugano -> Lugano
        
        if 'filters' not in context.user_data:
            context.user_data['filters'] = {}
        
        if city_code == 'NONE':
            # Remove city filter
            context.user_data['filters'].pop('city', None)
            await query.answer("📍 City filter removed")
        elif city_code == 'custom':
            # Ask for custom input
            msg = get_message('filter_city_input', lang)
            await query.edit_message_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=cancel_keyboard(lang)
            )
            context.user_data['waiting_for'] = 'city'
            return
        else:
            # Set city
            context.user_data['filters']['city'] = city_code
            confirm_msg = get_message('filter_city_set', lang, city=city_code)
            await query.answer(confirm_msg)
        
        # Return to filters menu
        await self.show_filters_menu(update, context)
    
    async def handle_rooms_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle rooms selection from presets"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        rooms_code = query.data.split('_', 1)[1]  # rooms_1_2 -> 1_2
        
        if 'filters' not in context.user_data:
            context.user_data['filters'] = {}
        
        if rooms_code == 'NONE':
            # Remove rooms filter
            context.user_data['filters'].pop('min_rooms', None)
            context.user_data['filters'].pop('max_rooms', None)
            await query.answer("🛏️ Rooms filter removed")
        elif rooms_code == 'custom':
            # Ask for custom input
            msg = get_message('filter_rooms_input', lang)
            await query.edit_message_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=cancel_keyboard(lang)
            )
            context.user_data['waiting_for'] = 'rooms_min'
            return
        else:
            # Parse range: 1_2, 3_4, etc.
            parts = rooms_code.split('_')
            min_rooms = float(parts[0])
            max_rooms = float(parts[1]) if len(parts) > 1 else None
            
            context.user_data['filters']['min_rooms'] = min_rooms
            if max_rooms and max_rooms < 99:
                context.user_data['filters']['max_rooms'] = max_rooms
            else:
                context.user_data['filters'].pop('max_rooms', None)
            
            confirm_msg = get_message('filter_rooms_set', lang, 
                                     min=min_rooms, 
                                     max=max_rooms if max_rooms and max_rooms < 99 else '∞')
            await query.answer(confirm_msg)
        
        await self.show_filters_menu(update, context)
    
    async def handle_price_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle price selection from presets"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        price_code = query.data.split('_', 1)[1]  # price_2000 -> 2000
        
        if 'filters' not in context.user_data:
            context.user_data['filters'] = {}
        
        if price_code == 'NONE':
            context.user_data['filters'].pop('max_price', None)
            await query.answer("💰 Price filter removed")
        elif price_code == 'custom':
            msg = get_message('filter_price_input', lang)
            await query.edit_message_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=cancel_keyboard(lang)
            )
            context.user_data['waiting_for'] = 'price'
            return
        else:
            price = int(price_code)
            context.user_data['filters']['max_price'] = price
            from utils.helpers import format_number_with_apostrophe
            confirm_msg = get_message('filter_price_set', lang, 
                                     price=format_number_with_apostrophe(price))
            await query.answer(confirm_msg)
        
        await self.show_filters_menu(update, context)
    
    async def handle_surface_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle surface selection from presets"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        surface_code = query.data.split('_', 1)[1]  # surface_50 -> 50
        
        if 'filters' not in context.user_data:
            context.user_data['filters'] = {}
        
        if surface_code == 'NONE':
            context.user_data['filters'].pop('min_surface', None)
            await query.answer("📐 Surface filter removed")
        elif surface_code == 'custom':
            msg = get_message('filter_surface_input', lang)
            await query.edit_message_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=cancel_keyboard(lang)
            )
            context.user_data['waiting_for'] = 'surface'
            return
        else:
            surface = int(surface_code)
            context.user_data['filters']['min_surface'] = surface
            confirm_msg = get_message('filter_surface_set', lang, surface=surface)
            await query.answer(confirm_msg)
        
        await self.show_filters_menu(update, context)
    
    async def handle_type_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle offer type selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        type_code = query.data.split('_', 2)[2]  # set_type_RENT -> RENT
        
        if 'filters' not in context.user_data:
            context.user_data['filters'] = {}
        
        if type_code == 'NONE':
            context.user_data['filters'].pop('offer_type', None)
            await query.answer("🏷️ Type filter removed")
        elif type_code == 'RENT':
            context.user_data['filters']['offer_type'] = 'RENT'
            confirm_msg = get_message('filter_type_set_rent', lang)
            await query.answer(confirm_msg)
        elif type_code == 'SALE':
            context.user_data['filters']['offer_type'] = 'SALE'
            confirm_msg = get_message('filter_type_set_sale', lang)
            await query.answer(confirm_msg)
        
        await self.show_filters_menu(update, context)
    
    async def handle_category_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle property category selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        category_code = query.data.split('_', 1)[1]  # category_APARTMENT -> APARTMENT
        
        if 'filters' not in context.user_data:
            context.user_data['filters'] = {}
        
        if category_code == 'NONE':
            context.user_data['filters'].pop('object_category', None)
            await query.answer("🏠 Category filter removed")
        else:
            context.user_data['filters']['object_category'] = category_code
            from bot.category_keyboard import get_category_label
            cat_label = get_category_label(category_code, lang)
            confirm_msg = get_message('filter_category_set', lang, category=cat_label)
            await query.answer(confirm_msg)
        
        await self.show_filters_menu(update, context)
    
    # ==================== TEXT INPUT HANDLERS ====================
    
    async def handle_text_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text input from user for custom filter values"""
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        text = update.message.text.strip()
        
        waiting_for = context.user_data.get('waiting_for')
        
        if not waiting_for:
            return  # Not waiting for input
        
        if 'filters' not in context.user_data:
            context.user_data['filters'] = {}
        
        # Process based on what we're waiting for
        if waiting_for == 'city':
            context.user_data['filters']['city'] = text
            msg = get_message('filter_city_set', lang, city=text)
            await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
        
        elif waiting_for == 'rooms_min':
            rooms = validate_room_number(text)
            if rooms:
                context.user_data['filters']['min_rooms'] = rooms
                context.user_data['waiting_for'] = 'rooms_max'
                msg = f"✅ Min rooms: {rooms}\n\nNow enter max rooms (or type 'skip'):"
                await update.message.reply_text(msg)
                return
            else:
                msg = get_message('error_invalid_input', lang)
                await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
                return
        
        elif waiting_for == 'rooms_max':
            if text.lower() == 'skip':
                context.user_data['filters'].pop('max_rooms', None)
            else:
                rooms = validate_room_number(text)
                if rooms:
                    context.user_data['filters']['max_rooms'] = rooms
                else:
                    msg = get_message('error_invalid_input', lang)
                    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
                    return
            
            min_r = context.user_data['filters'].get('min_rooms', 0)
            max_r = context.user_data['filters'].get('max_rooms', '∞')
            msg = get_message('filter_rooms_set', lang, min=min_r, max=max_r)
            await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
        
        elif waiting_for == 'price':
            price = validate_price(text)
            if price:
                context.user_data['filters']['max_price'] = price
                from utils.helpers import format_number_with_apostrophe
                msg = get_message('filter_price_set', lang, 
                                 price=format_number_with_apostrophe(price))
                await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
            else:
                msg = get_message('error_invalid_input', lang)
                await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
                return
        
        elif waiting_for == 'surface':
            surface = validate_surface(text)
            if surface:
                context.user_data['filters']['min_surface'] = surface
                msg = get_message('filter_surface_set', lang, surface=surface)
                await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
            else:
                msg = get_message('error_invalid_input', lang)
                await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
                return
        
        # Clear waiting state
        context.user_data.pop('waiting_for', None)
        
        # Show filters menu
        filter_msg = get_message('filter_menu', lang)
        await update.message.reply_text(
            filter_msg,
            parse_mode=ParseMode.HTML,
            reply_markup=filter_menu_keyboard(lang)
        )
    
    async def cancel_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel text input operation"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        
        context.user_data.pop('waiting_for', None)
        
        msg = get_message('operation_cancelled', lang)
        await query.answer(msg)
        await self.show_filters_menu(update, context)
    
    # ==================== ALERT HANDLERS ====================
    
    async def handle_alert_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle alert-related actions"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        data = query.data
        
        if data == 'alert_create':
            # Create alert from current filters
            filters = context.user_data.get('filters', {})
            
            if not self.search.has_any_filter(**filters):
                await query.answer("⚠️ Please set filters first!")
                await self.show_filters_menu(update, context)
                return
            
            # Create alert
            alert_id = self.db.add_alert(
                user_id=user_id,
                city=filters.get('city'),
                min_rooms=filters.get('min_rooms'),
                max_rooms=filters.get('max_rooms'),
                max_price=filters.get('max_price'),
                min_surface=filters.get('min_surface'),
                offer_type=filters.get('offer_type'),
                object_category=filters.get('object_category')
            )
            
            if alert_id:
                msg = get_message('alert_created', lang)
                await query.edit_message_text(
                    msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=back_to_main_keyboard(lang)
                )
            else:
                msg = get_message('error_generic', lang)
                await query.edit_message_text(msg, parse_mode=ParseMode.HTML)
        
        elif data.startswith('alert_view_'):
            # View alert details
            alert_id = int(data.split('_')[2])
            alerts = self.db.get_user_alerts(user_id, active_only=False)
            alert = next((a for a in alerts if a.alert_id == alert_id), None)
            
            if alert:
                from utils.helpers import format_alert_summary
                summary = format_alert_summary(alert)
                msg = f"🔔 <b>Alert #{alert_id}</b>\n\n{summary}"
                
                await query.edit_message_text(
                    msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=alert_actions_keyboard(alert_id, alert.is_active, lang)
                )
        
        elif data.startswith('alert_toggle_'):
            # Toggle alert active status
            alert_id = int(data.split('_')[2])
            success = self.db.toggle_alert(alert_id, user_id)
            
            if success:
                msg = get_message('alert_toggled', lang)
                await query.answer(msg)
                await self.show_alerts_menu(update, context)
        
        elif data.startswith('alert_search_'):
            # Search with alert filters
            alert_id = int(data.split('_')[2])
            alerts = self.db.get_user_alerts(user_id, active_only=False)
            alert = next((a for a in alerts if a.alert_id == alert_id), None)
            
            if alert:
                # Load alert filters into context
                context.user_data['filters'] = {
                    'city': alert.city,
                    'min_rooms': alert.min_rooms,
                    'max_rooms': alert.max_rooms,
                    'max_price': alert.max_price,
                    'min_surface': alert.min_surface,
                    'offer_type': alert.offer_type,
                    'object_category': getattr(alert, 'object_category', None)
                }
                await query.answer("🔍 Searching...")
                await self.execute_search(update, context, context.user_data['filters'])
        
        elif data.startswith('alert_delete_confirm_'):
            # Show delete confirmation
            alert_id = int(data.split('_')[3])
            msg = get_message('confirm_delete_alert', lang)
            
            await query.edit_message_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=confirm_keyboard('delete_alert', alert_id, lang)
            )
    
    async def handle_confirmation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle confirmation dialogs"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        data = query.data
        
        if data.startswith('confirm_delete_alert_'):
            # Confirmed delete
            alert_id = int(data.split('_')[3])
            success = self.db.delete_alert(alert_id, user_id)
            
            if success:
                msg = get_message('alert_deleted', lang)
                await query.answer(msg)
                await self.show_alerts_menu(update, context)
        
        elif data.startswith('cancel_delete_alert_'):
            # Cancelled delete
            msg = get_message('operation_cancelled', lang)
            await query.answer(msg)
            await self.show_alerts_menu(update, context)
    
    # ==================== PROPERTY NAVIGATION ====================
    
    async def send_property_with_navigation(self, message, user_id: int, context: ContextTypes.DEFAULT_TYPE, 
                                           lang: str, edit_message: bool = False):
        """Send property with navigation buttons in single message"""
        last_search = context.user_data.get('last_search')
        if not last_search:
            return
        
        properties = last_search.get('properties', [])
        if not properties:
            return
        
        current_index = last_search.get('current_property_index', 0)
        current_page = last_search.get('current_page', 1)
        total_pages = last_search.get('total_pages', 1)
        total_count = last_search.get('total_count', 0)
        
        prop = properties[current_index]
        
        # Format property message
        from utils.helpers import format_property_message
        prop_msg = format_property_message(prop, include_description=True)
        
        # Add navigation info
        prop_position = (current_page - 1) * 5 + current_index + 1
        header = f"📍 <b>Property {prop_position} of {total_count}</b> (Page {current_page}/{total_pages})\n\n"
        full_msg = header + prop_msg
        
        # Build navigation keyboard
        keyboard = []
        nav_row = []
        
        # Previous property button
        if current_index > 0:
            nav_row.append(InlineKeyboardButton("⬅️ Previous", callback_data="prop_prev"))
        
        # Property counter
        nav_row.append(InlineKeyboardButton(
            f"📄 {current_index + 1}/{len(properties)}", 
            callback_data="prop_info"
        ))
        
        # Next property button
        if current_index < len(properties) - 1:
            nav_row.append(InlineKeyboardButton("Next ➡️", callback_data="prop_next"))
        
        keyboard.append(nav_row)
        
        # Page navigation row
        page_row = []
        if current_page > 1:
            page_row.append(InlineKeyboardButton("⏮️ Prev Page", callback_data=f"page_prev_{current_page}"))
        if current_page < total_pages:
            page_row.append(InlineKeyboardButton("Next Page ⏭️", callback_data=f"page_next_{current_page}"))
        
        if page_row:
            keyboard.append(page_row)
        
        # Action buttons
        keyboard.append([
            InlineKeyboardButton(get_label('new_search', lang), callback_data="menu_search"),
            InlineKeyboardButton(get_label('main_menu', lang), callback_data="back_main")
        ])
        
        from telegram import InlineKeyboardMarkup
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send or edit message (without images to avoid spam)
        try:
            if edit_message:
                await message.edit_text(
                    full_msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )
            else:
                await message.reply_text(
                    full_msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )
        except Exception as e:
            logger.error(f"Error sending property with navigation: {e}")
    
    async def handle_property_navigation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle property navigation within same page"""
        query = update.callback_query
        user_id = update.effective_user.id
        lang = self.get_user_lang(user_id)
        data = query.data
        
        last_search = context.user_data.get('last_search')
        if not last_search:
            await query.answer("❌ Search expired")
            return
        
        properties = last_search.get('properties', [])
        current_index = last_search.get('current_property_index', 0)
        
        if data == 'prop_prev':
            if current_index > 0:
                context.user_data['last_search']['current_property_index'] = current_index - 1
                await self.send_property_with_navigation(query.message, user_id, context, lang, edit_message=True)
                await query.answer()
            else:
                await query.answer("⚠️ First property")
        
        elif data == 'prop_next':
            if current_index < len(properties) - 1:
                context.user_data['last_search']['current_property_index'] = current_index + 1
                await self.send_property_with_navigation(query.message, user_id, context, lang, edit_message=True)
                await query.answer()
            else:
                await query.answer("⚠️ Last property on this page")
        
        elif data == 'prop_info':
            await query.answer(f"Property {current_index + 1} of {len(properties)} on this page")
