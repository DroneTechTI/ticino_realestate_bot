"""
Configuration Template for Ticino Real Estate Bot

IMPORTANT: 
1. Copy this file to 'config.py'
2. Fill in your actual values
3. Never commit 'config.py' to version control
"""

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get it from @BotFather

# Flatfox API Configuration
FLATFOX_API_URL = "https://flatfox.ch/api/v1/public-listing/"

# Database Configuration
DATABASE_NAME = "realestate_bot.db"

# Notification Settings
CHECK_INTERVAL_MINUTES = 60  # Check for new listings every 60 minutes
MAX_RESULTS_PER_PAGE = 5     # Number of results to show per page

# API Cache Settings
API_CACHE_HOURS = 1          # Cache properties for 1 hour
API_BULK_FETCH_SIZE = 3000   # Fetch 3000 properties at once (gives ~60 Ticino)

# Telegraph Configuration (for long descriptions)
TELEGRAPH_AUTHOR = "Ticino Real Estate"
TELEGRAPH_AUTHOR_URL = ""

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "bot.log"

# Ticino Cities (examples - users can input any city)
TICINO_CITIES_EXAMPLES = [
    "Lugano", "Bellinzona", "Locarno", "Mendrisio", "Chiasso",
    "Ascona", "Losone", "Minusio", "Biasca", "Giubiasco"
]
