# 🚀 Ticino Real Estate Bot - Setup Guide

Complete step-by-step guide to set up and run the Ticino Real Estate Bot.

---

## 📋 Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Git** (to clone the repository)
- **Telegram account**

---

## 🤖 Step 1: Create Your Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat and send `/newbot`
3. Follow the instructions:
   - Choose a **name** for your bot (e.g., "Ticino Real Estate")
   - Choose a **username** (must end with 'bot', e.g., "ticino_realestate_bot")
4. BotFather will give you a **TOKEN** - copy it! (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. **IMPORTANT**: Keep this token secret! Never share it publicly.

---

## 📥 Step 2: Clone the Repository

```bash
git clone <repository-url>
cd ticino_realestate_bot
```

---

## 🐍 Step 3: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `python-telegram-bot` - Telegram Bot API
- `requests` - HTTP library
- `APScheduler` - Task scheduler
- `telegraph` - For long descriptions
- Other utilities

---

## ⚙️ Step 5: Configure the Bot

1. **Copy the example configuration:**
   ```bash
   cp config.example.py config.py
   ```

2. **Edit `config.py`** with your favorite text editor

3. **Set your bot token:**
   ```python
   TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # Your token from BotFather
   ```

4. **Optional: Adjust other settings:**
   ```python
   CHECK_INTERVAL_MINUTES = 60  # How often to check for new properties (default: 60 minutes)
   MAX_RESULTS_PER_PAGE = 5     # Number of results per page (default: 5)
   LOG_LEVEL = "INFO"           # Logging level (DEBUG, INFO, WARNING, ERROR)
   ```

---

## 🚀 Step 6: Start the Bot

**Option 1: Direct Python execution**
```bash
python main.py
```

**Option 2: Use startup script (Windows)**
```bash
start.bat
```

**Option 3: Use startup script (Linux/Mac)**
```bash
chmod +x start.sh
./start.sh
```

---

## ✅ Step 7: Test Your Bot

1. Open Telegram
2. Search for your bot (the username you chose)
3. Start a chat with your bot
4. Send `/start`
5. The bot should respond with language selection! 🎉

---

## 🎯 Bot Commands

Once the bot is running, you can use these commands:

- `/start` - Start the bot and show main menu
- `/help` - Show help and instructions
- `/search` - Quick property search
- `/filters` - Manage search filters
- `/alerts` - Manage notification alerts
- `/language` - Change bot language

---

## 🌍 Supported Languages

The bot interface is available in:
- 🇮🇹 **Italian** (default)
- 🇩🇪 **German**
- 🇬🇧 **English**

Property listings are shown in their original language (as published by agencies).

---

## 📊 How It Works

1. **Set Filters**: Choose your preferences (city, rooms, price, surface, type)
2. **Search**: Get immediate results matching your criteria
3. **Save Alerts**: Create alerts to receive automatic notifications
4. **Receive Notifications**: Get notified when new properties match your saved alerts

The bot checks for new properties every hour (configurable) and sends notifications automatically.

---

## 🔧 Configuration Options

### Database
- `DATABASE_NAME`: SQLite database file (default: `realestate_bot.db`)

### Notifications
- `CHECK_INTERVAL_MINUTES`: How often to check for new properties (default: 60)
- `MAX_RESULTS_PER_PAGE`: Results per page (default: 5)

### Telegraph
- `TELEGRAPH_AUTHOR`: Author name for long descriptions
- `TELEGRAPH_AUTHOR_URL`: Author URL (optional)

### Logging
- `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FILE`: Log file name (default: `bot.log`)

---

## 🛑 Stopping the Bot

Press `Ctrl+C` in the terminal to stop the bot gracefully.

The bot will:
1. Stop accepting new messages
2. Stop the notification scheduler
3. Close database connections
4. Exit cleanly

---

## 📝 Logs

Logs are saved to `bot.log` and also displayed in the console.

Check logs for:
- User interactions
- API calls
- Notifications sent
- Errors and warnings

---

## ❓ Troubleshooting

### Bot doesn't respond
- Check that `config.py` has the correct token
- Verify the bot is running (`python main.py`)
- Check logs for errors

### No notifications received
- Verify you have active alerts (`/alerts`)
- Check `CHECK_INTERVAL_MINUTES` in config
- Look at logs for notification cycle information

### API errors
- Check internet connection
- Flatfox API might be temporarily unavailable
- The bot will continue working when API is back online

### Database errors
- Make sure the bot has write permissions in its directory
- Delete `realestate_bot.db` to start fresh (will lose all data)

---

## 🔒 Security Notes

1. **Never commit `config.py` to Git** - it contains your bot token
2. The `.gitignore` file excludes `config.py` automatically
3. Keep your bot token secret
4. If token is compromised, revoke it via @BotFather and create a new one

---

## 📚 Project Structure

```
ticino_realestate_bot/
├── main.py                    # Entry point
├── config.py                  # Your configuration (not in Git)
├── config.example.py          # Configuration template
├── requirements.txt           # Dependencies
├── bot/                       # Bot logic
│   ├── handlers.py           # Command and callback handlers
│   ├── keyboards.py          # Inline keyboards (presets)
│   ├── keyboards_i18n.py     # Multilingual keyboards
│   └── messages.py           # Multilingual messages
├── api/                      # External APIs
│   └── flatfox_client.py    # Flatfox API client
├── database/                 # Database
│   ├── db_manager.py        # Database operations
│   └── models.py            # Data models
├── services/                 # Business logic
│   ├── search_service.py    # Search logic
│   └── notification_service.py  # Notification system
└── utils/                    # Utilities
    └── helpers.py           # Helper functions
```

---

## 🆘 Support

For issues, questions, or suggestions:
1. Check the logs (`bot.log`)
2. Review this guide
3. Check `README.md` for additional information
4. Open an issue on the repository

---

## 🎉 Enjoy!

Your Ticino Real Estate Bot is now ready to help users find their ideal property!

The bot will:
- Search thousands of properties in Ticino
- Send automatic notifications for new listings
- Support multiple languages
- Work 24/7 without interruption

**Happy property hunting!** 🏠
