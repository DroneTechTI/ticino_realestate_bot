"""
Ticino Real Estate Bot - Main Entry Point

A professional Telegram bot for searching real estate properties in Ticino, Switzerland.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

# Import configuration
try:
    import config
except ImportError:
    print("ERROR: config.py not found!")
    print("Please copy config.example.py to config.py and configure it.")
    sys.exit(1)

# Import components
from database.db_manager import DatabaseManager
from api.flatfox_client import FlatfoxClient
from services.search_service import SearchService
from services.notification_service import NotificationService
from bot.handlers import BotHandlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL),
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Fix console encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logger = logging.getLogger(__name__)


def main():
    """Main function to start the bot"""
    
    logger.info("=" * 60)
    logger.info("Starting Ticino Real Estate Bot")
    logger.info("=" * 60)
    
    # Validate configuration
    if not config.TELEGRAM_BOT_TOKEN or config.TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("TELEGRAM_BOT_TOKEN not configured in config.py!")
        logger.error("Please set a valid bot token from @BotFather")
        sys.exit(1)
    
    try:
        # Initialize services
        logger.info("Initializing services...")
        
        # Database
        db_manager = DatabaseManager(config.DATABASE_NAME)
        logger.info(f"✓ Database initialized: {config.DATABASE_NAME}")
        
        # Flatfox API Client
        flatfox_client = FlatfoxClient(config.FLATFOX_API_URL)
        
        # Test API connection
        if flatfox_client.test_connection():
            logger.info("✓ Flatfox API connection successful")
        else:
            logger.warning("⚠ Could not connect to Flatfox API - bot will start anyway")
        
        # Search Service
        search_service = SearchService(flatfox_client, db_manager)
        logger.info("✓ Search service initialized")
        
        # Build application
        logger.info("Building Telegram application...")
        application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Notification Service (needs bot instance)
        notification_service = NotificationService(
            application.bot,
            search_service,
            config.CHECK_INTERVAL_MINUTES
        )
        logger.info(f"✓ Notification service initialized (check interval: {config.CHECK_INTERVAL_MINUTES} minutes)")
        
        # Initialize handlers
        logger.info("Registering handlers...")
        handlers = BotHandlers(db_manager, search_service, notification_service)
        
        # Register command handlers
        application.add_handler(CommandHandler("start", handlers.start_command))
        application.add_handler(CommandHandler("help", handlers.help_command))
        application.add_handler(CommandHandler("search", handlers.search_command))
        application.add_handler(CommandHandler("filters", handlers.filters_command))
        application.add_handler(CommandHandler("alerts", handlers.alerts_command))
        application.add_handler(CommandHandler("language", handlers.language_command))
        logger.info("✓ Command handlers registered")
        
        # Register callback query handler (for inline buttons)
        application.add_handler(CallbackQueryHandler(handlers.callback_handler))
        logger.info("✓ Callback query handler registered")
        
        # Register message handler for text input (filters)
        application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handlers.handle_text_input
            )
        )
        logger.info("✓ Message handler registered")
        
        # Start notification service
        logger.info("Starting notification scheduler...")
        notification_service.start()
        logger.info("✓ Notification scheduler started")
        
        # Start bot
        logger.info("=" * 60)
        logger.info("✓ Bot started successfully!")
        logger.info("=" * 60)
        logger.info("Press Ctrl+C to stop the bot")
        logger.info("=" * 60)
        
        # Run bot
        application.run_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        logger.info("\nReceived keyboard interrupt, shutting down...")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    
    finally:
        # Cleanup
        logger.info("Stopping notification service...")
        try:
            notification_service.stop()
            logger.info("✓ Notification service stopped")
        except:
            pass
        
        logger.info("=" * 60)
        logger.info("Bot stopped")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
