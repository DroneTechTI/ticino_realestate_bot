# 🏠 Ticino Real Estate Bot

A professional Telegram bot for searching real estate properties in Ticino, Switzerland.

## 📋 Features

- 🔍 **Advanced Search**: Search properties with customizable filters
- 📍 **Location-based**: Search in any city/town in Ticino
- 💰 **Price Filters**: Set maximum price limits
- 🏘️ **Room Filters**: Filter by minimum and maximum number of rooms
- 📐 **Surface Filters**: Set minimum living space requirements
- 🔔 **Automatic Alerts**: Get notified when new properties match your criteria
- 📸 **Media Gallery**: View multiple property images in organized albums
- 📝 **Complete Descriptions**: Long descriptions automatically formatted on Telegraph
- 🌐 **User-friendly Interface**: Intuitive inline keyboard navigation

## 🛠️ Technologies

- **Python 3.8+**
- **python-telegram-bot 20.8**: Modern Telegram Bot API wrapper
- **SQLite**: Lightweight embedded database
- **APScheduler**: Automated notification scheduler
- **Telegraph API**: For formatting long property descriptions
- **Flatfox API**: Real estate data source

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Telegram Bot Token (obtain from [@BotFather](https://t.me/botfather))

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd ticino_realestate_bot
```

### Step 2: Create virtual environment (recommended)

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

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configuration

1. Copy the example configuration file:
   ```bash
   cp config.example.py config.py
   ```

2. Edit `config.py` and add your Telegram Bot Token:
   ```python
   TELEGRAM_BOT_TOKEN = "your_actual_bot_token_here"
   ```

## 🚀 Quick Start

### Fast setup (5 minutes):

1. **Get bot token from @BotFather on Telegram**
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Configure:** `cp config.example.py config.py` and add your token
4. **Run:** `python main.py`
5. **Test on Telegram!** 🎉

📖 **Detailed guide:** See `SETUP_GUIDE.md` for complete setup instructions.

⚡ **Quick reference:** See `QUICK_START.md` for fast setup.

### Start the bot

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
./start.sh
```

Or directly with Python:
```bash
python main.py
```

## 🤖 Bot Commands

- `/start` - Start the bot and show main menu
- `/search` - Search for properties with filters
- `/filters` - Manage your saved search filters
- `/myalerts` - View and manage your active alerts
- `/help` - Show help and instructions

## 📊 Database Schema

### Users Table
- `user_id`: Telegram user ID (PRIMARY KEY)
- `username`: Telegram username
- `first_name`: User's first name
- `created_at`: Registration timestamp
- `is_active`: Active status

### Alerts Table
- `alert_id`: Unique alert ID (PRIMARY KEY)
- `user_id`: User who created the alert
- `city`: Target city/location
- `min_rooms`: Minimum number of rooms
- `max_rooms`: Maximum number of rooms
- `max_price`: Maximum price
- `min_surface`: Minimum surface area
- `offer_type`: RENT or SALE
- `is_active`: Alert active status
- `created_at`: Creation timestamp

### Notified Properties Table
- `id`: Record ID (PRIMARY KEY)
- `user_id`: User notified
- `property_id`: Flatfox property ID
- `notified_at`: Notification timestamp

## 🔒 Security Notes

- Never commit `config.py` to version control
- Keep your bot token confidential
- The `.gitignore` file is configured to exclude sensitive files

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For support, please open an issue in the repository.

---

**Made with ❤️ for the Ticino community**
