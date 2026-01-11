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
    back_to_main_keyboard
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
        
        # Additional routing will be added in Part 2
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
        from services.search_service import SearchService
        summary = self.search.get_filter_summary(
            city=filters.get('city'),
            min_rooms=filters.get('min_rooms'),
            max_rooms=filters.get('max_rooms'),
            max_price=filters.get('max_price'),
            min_surface=filters.get('min_surface'),
            offer_type=filters.get('offer_type')
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
        
        # This will be implemented in Part 2
        await query.answer("🔍 Searching...")
        # TODO: Implement actual search
