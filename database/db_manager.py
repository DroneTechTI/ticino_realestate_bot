"""
Database Manager for Ticino Real Estate Bot

This module handles all database operations using SQLite.
"""

import sqlite3
import logging
from datetime import datetime
from typing import List, Optional, Tuple
from contextlib import contextmanager

from .models import User, Alert, NotifiedProperty

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages all database operations for the bot"""
    
    def __init__(self, db_path: str):
        """
        Initialize the database manager
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def init_database(self):
        """Create all necessary tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    is_active BOOLEAN NOT NULL DEFAULT 1
                )
            """)
            
            # Alerts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    city TEXT,
                    min_rooms REAL,
                    max_rooms REAL,
                    max_price INTEGER,
                    min_surface INTEGER,
                    offer_type TEXT,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    created_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Notified properties table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notified_properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    property_id INTEGER NOT NULL,
                    notified_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    UNIQUE(user_id, property_id)
                )
            """)
            
            # Create indices for better performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_alerts_user_id 
                ON alerts(user_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_notified_user_property 
                ON notified_properties(user_id, property_id)
            """)
            
            logger.info("Database initialized successfully")
    
    # ==================== USER OPERATIONS ====================
    
    def add_user(self, user_id: int, username: Optional[str], first_name: str) -> bool:
        """
        Add a new user or update existing user
        
        Args:
            user_id: Telegram user ID
            username: Telegram username
            first_name: User's first name
            
        Returns:
            True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO users (user_id, username, first_name, created_at, is_active)
                    VALUES (?, ?, ?, ?, 1)
                """, (user_id, username, first_name, datetime.now()))
                logger.info(f"User {user_id} added/updated successfully")
                return True
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            User object or None if not found
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                
                if row:
                    return User(
                        user_id=row['user_id'],
                        username=row['username'],
                        first_name=row['first_name'],
                        created_at=datetime.fromisoformat(row['created_at']),
                        is_active=bool(row['is_active'])
                    )
                return None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
    
    def get_all_active_users(self) -> List[User]:
        """
        Get all active users
        
        Returns:
            List of User objects
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE is_active = 1")
                rows = cursor.fetchall()
                
                return [
                    User(
                        user_id=row['user_id'],
                        username=row['username'],
                        first_name=row['first_name'],
                        created_at=datetime.fromisoformat(row['created_at']),
                        is_active=bool(row['is_active'])
                    )
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"Error getting active users: {e}")
            return []
    
    # ==================== ALERT OPERATIONS ====================
    
    def add_alert(self, user_id: int, city: Optional[str] = None,
                  min_rooms: Optional[float] = None, max_rooms: Optional[float] = None,
                  max_price: Optional[int] = None, min_surface: Optional[int] = None,
                  offer_type: Optional[str] = None) -> Optional[int]:
        """
        Add a new alert for a user
        
        Args:
            user_id: Telegram user ID
            city: Target city
            min_rooms: Minimum number of rooms
            max_rooms: Maximum number of rooms
            max_price: Maximum price
            min_surface: Minimum surface area
            offer_type: 'RENT' or 'SALE'
            
        Returns:
            Alert ID if successful, None otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO alerts (user_id, city, min_rooms, max_rooms, max_price, 
                                       min_surface, offer_type, is_active, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
                """, (user_id, city, min_rooms, max_rooms, max_price, min_surface, 
                      offer_type, datetime.now()))
                
                alert_id = cursor.lastrowid
                logger.info(f"Alert {alert_id} created for user {user_id}")
                return alert_id
        except Exception as e:
            logger.error(f"Error adding alert for user {user_id}: {e}")
            return None
    
    def get_user_alerts(self, user_id: int, active_only: bool = True) -> List[Alert]:
        """
        Get all alerts for a user
        
        Args:
            user_id: Telegram user ID
            active_only: If True, return only active alerts
            
        Returns:
            List of Alert objects
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM alerts WHERE user_id = ?"
                params = [user_id]
                
                if active_only:
                    query += " AND is_active = 1"
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                return [
                    Alert(
                        alert_id=row['alert_id'],
                        user_id=row['user_id'],
                        city=row['city'],
                        min_rooms=row['min_rooms'],
                        max_rooms=row['max_rooms'],
                        max_price=row['max_price'],
                        min_surface=row['min_surface'],
                        offer_type=row['offer_type'],
                        is_active=bool(row['is_active']),
                        created_at=datetime.fromisoformat(row['created_at'])
                    )
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"Error getting alerts for user {user_id}: {e}")
            return []
    
    def get_all_active_alerts(self) -> List[Alert]:
        """
        Get all active alerts from all users
        
        Returns:
            List of Alert objects
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM alerts WHERE is_active = 1")
                rows = cursor.fetchall()
                
                return [
                    Alert(
                        alert_id=row['alert_id'],
                        user_id=row['user_id'],
                        city=row['city'],
                        min_rooms=row['min_rooms'],
                        max_rooms=row['max_rooms'],
                        max_price=row['max_price'],
                        min_surface=row['min_surface'],
                        offer_type=row['offer_type'],
                        is_active=bool(row['is_active']),
                        created_at=datetime.fromisoformat(row['created_at'])
                    )
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"Error getting all active alerts: {e}")
            return []
    
    def delete_alert(self, alert_id: int, user_id: int) -> bool:
        """
        Delete an alert
        
        Args:
            alert_id: Alert ID to delete
            user_id: User ID (for security check)
            
        Returns:
            True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM alerts 
                    WHERE alert_id = ? AND user_id = ?
                """, (alert_id, user_id))
                
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Alert {alert_id} deleted for user {user_id}")
                return success
        except Exception as e:
            logger.error(f"Error deleting alert {alert_id}: {e}")
            return False
    
    def toggle_alert(self, alert_id: int, user_id: int) -> bool:
        """
        Toggle alert active status
        
        Args:
            alert_id: Alert ID
            user_id: User ID (for security check)
            
        Returns:
            True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE alerts 
                    SET is_active = NOT is_active 
                    WHERE alert_id = ? AND user_id = ?
                """, (alert_id, user_id))
                
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Alert {alert_id} toggled for user {user_id}")
                return success
        except Exception as e:
            logger.error(f"Error toggling alert {alert_id}: {e}")
            return False
    
    # ==================== NOTIFIED PROPERTIES OPERATIONS ====================
    
    def add_notified_property(self, user_id: int, property_id: int) -> bool:
        """
        Mark a property as notified to a user
        
        Args:
            user_id: Telegram user ID
            property_id: Flatfox property ID
            
        Returns:
            True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO notified_properties (user_id, property_id, notified_at)
                    VALUES (?, ?, ?)
                """, (user_id, property_id, datetime.now()))
                
                return True
        except Exception as e:
            logger.error(f"Error adding notified property {property_id} for user {user_id}: {e}")
            return False
    
    def is_property_notified(self, user_id: int, property_id: int) -> bool:
        """
        Check if a property has already been notified to a user
        
        Args:
            user_id: Telegram user ID
            property_id: Flatfox property ID
            
        Returns:
            True if already notified
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 1 FROM notified_properties 
                    WHERE user_id = ? AND property_id = ?
                """, (user_id, property_id))
                
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Error checking notified property: {e}")
            return False
    
    def get_user_stats(self, user_id: int) -> dict:
        """
        Get statistics for a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Dictionary with user statistics
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Count active alerts
                cursor.execute("""
                    SELECT COUNT(*) as count FROM alerts 
                    WHERE user_id = ? AND is_active = 1
                """, (user_id,))
                active_alerts = cursor.fetchone()['count']
                
                # Count total notified properties
                cursor.execute("""
                    SELECT COUNT(*) as count FROM notified_properties 
                    WHERE user_id = ?
                """, (user_id,))
                notified_count = cursor.fetchone()['count']
                
                return {
                    'active_alerts': active_alerts,
                    'properties_received': notified_count
                }
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {'active_alerts': 0, 'properties_received': 0}
