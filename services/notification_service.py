"""
Notification Service for Ticino Real Estate Bot

This module handles automatic notifications to users when new properties
matching their alert criteria become available.
"""

import logging
from typing import List, Optional
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram import Bot, InputMediaPhoto
from telegram.error import TelegramError

from services.search_service import SearchService
from database.models import Property
from utils.helpers import (
    format_property_message,
    prepare_media_group,
    format_property_caption
)

logger = logging.getLogger(__name__)


class NotificationService:
    """Handles automatic property notifications"""
    
    def __init__(self, bot: Bot, search_service: SearchService, check_interval_minutes: int = 60):
        """
        Initialize the notification service
        
        Args:
            bot: Telegram Bot instance
            search_service: SearchService instance
            check_interval_minutes: How often to check for new properties
        """
        self.bot = bot
        self.search_service = search_service
        self.check_interval = check_interval_minutes
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    def start(self):
        """Start the notification scheduler"""
        if self.is_running:
            logger.warning("Notification service already running")
            return
        
        logger.info(f"Starting notification service (check interval: {self.check_interval} minutes)")
        
        # Schedule periodic checks
        self.scheduler.add_job(
            self.check_and_notify_all,
            trigger=IntervalTrigger(minutes=self.check_interval),
            id='check_new_properties',
            name='Check for new properties',
            replace_existing=True
        )
        
        self.scheduler.start()
        self.is_running = True
        
        logger.info("Notification service started successfully")
    
    def stop(self):
        """Stop the notification scheduler"""
        if not self.is_running:
            logger.warning("Notification service not running")
            return
        
        logger.info("Stopping notification service")
        self.scheduler.shutdown(wait=False)
        self.is_running = False
        logger.info("Notification service stopped")
    
    async def check_and_notify_all(self):
        """
        Check all active alerts for new properties and send notifications
        This method is called periodically by the scheduler
        """
        logger.info("=== Starting notification check cycle ===")
        start_time = datetime.now()
        
        try:
            # Get new properties for all alerts
            user_properties = self.search_service.check_all_alerts_for_new_properties()
            
            if not user_properties:
                logger.info("No new properties found for any user")
                return
            
            # Send notifications to users
            total_sent = 0
            for user_id, properties in user_properties.items():
                logger.info(f"Notifying user {user_id} about {len(properties)} new properties")
                
                for prop in properties:
                    success = await self.send_property_notification(user_id, prop)
                    if success:
                        total_sent += 1
                        # Mark as notified
                        self.search_service.mark_property_as_notified(user_id, prop.pk)
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"=== Notification cycle completed: {total_sent} properties sent in {duration:.2f}s ===")
            
        except Exception as e:
            logger.error(f"Error in notification cycle: {e}", exc_info=True)
    
    async def send_property_notification(self, user_id: int, prop: Property) -> bool:
        """
        Send a property notification to a user
        
        Args:
            user_id: Telegram user ID
            prop: Property object to send
            
        Returns:
            True if sent successfully
        """
        try:
            # Add notification header
            header = "🔔 <b>New Property Alert!</b>\n\n"
            
            # Format property message
            message = format_property_message(prop, include_description=True)
            full_message = header + message
            
            # Send with images if available
            if prop.images:
                if len(prop.images) == 1:
                    # Single image
                    await self.bot.send_photo(
                        chat_id=user_id,
                        photo=prop.images[0],
                        caption=full_message,
                        parse_mode='HTML'
                    )
                else:
                    # Multiple images - send as media group
                    media_group = prepare_media_group(prop)
                    await self.bot.send_media_group(
                        chat_id=user_id,
                        media=media_group
                    )
                    
                    # Send detailed message separately
                    await self.bot.send_message(
                        chat_id=user_id,
                        text=full_message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
            else:
                # No images - send text only
                await self.bot.send_message(
                    chat_id=user_id,
                    text=full_message,
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
            
            logger.info(f"Sent property {prop.pk} notification to user {user_id}")
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram error sending notification to user {user_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending notification to user {user_id}: {e}", exc_info=True)
            return False
    
    async def send_property_to_user(self, user_id: int, prop: Property) -> bool:
        """
        Send a property to a user (for manual search results)
        
        Args:
            user_id: Telegram user ID
            prop: Property object to send
            
        Returns:
            True if sent successfully
        """
        try:
            # Format property message
            message = format_property_message(prop, include_description=True)
            
            # Send with images if available
            if prop.images:
                if len(prop.images) == 1:
                    # Single image
                    await self.bot.send_photo(
                        chat_id=user_id,
                        photo=prop.images[0],
                        caption=message,
                        parse_mode='HTML'
                    )
                else:
                    # Multiple images - send as media group
                    media_group = prepare_media_group(prop)
                    await self.bot.send_media_group(
                        chat_id=user_id,
                        media=media_group
                    )
                    
                    # Send detailed message separately
                    await self.bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
            else:
                # No images - send text only
                await self.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
            
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram error sending property to user {user_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending property to user {user_id}: {e}", exc_info=True)
            return False
    
    async def send_properties_batch(self, user_id: int, properties: List[Property]) -> int:
        """
        Send multiple properties to a user
        
        Args:
            user_id: Telegram user ID
            properties: List of Property objects
            
        Returns:
            Number of properties successfully sent
        """
        sent_count = 0
        
        for prop in properties:
            success = await self.send_property_to_user(user_id, prop)
            if success:
                sent_count += 1
        
        return sent_count
    
    async def test_notification(self, user_id: int) -> bool:
        """
        Send a test notification to verify the system is working
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if test notification sent successfully
        """
        try:
            test_message = (
                "✅ <b>Test Notification</b>\n\n"
                "Your notification system is working correctly!\n\n"
                "You will receive alerts here when new properties "
                "matching your criteria become available."
            )
            
            await self.bot.send_message(
                chat_id=user_id,
                text=test_message,
                parse_mode='HTML'
            )
            
            logger.info(f"Test notification sent to user {user_id}")
            return True
            
        except TelegramError as e:
            logger.error(f"Error sending test notification to user {user_id}: {e}")
            return False
    
    def get_status(self) -> dict:
        """
        Get notification service status
        
        Returns:
            Dictionary with status information
        """
        return {
            'running': self.is_running,
            'check_interval_minutes': self.check_interval,
            'next_check': self.scheduler.get_job('check_new_properties').next_run_time if self.is_running else None
        }
