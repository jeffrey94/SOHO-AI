# Telegram Daily Summary Bot

A Telegram bot that automatically summarizes daily operations from a group chat using OpenAI's GPT models.

## Features

- Monitors a Telegram group for operational updates
- Generates structured daily summaries using OpenAI
- Posts summaries at a configurable time (default: 9 PM)
- Provides a command to generate summaries on demand
- Automatic message categorization and formatting
- Simple error handling and recovery

## Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key
- Access to a Telegram group

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd telegram-summary-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_GROUP_ID=your_group_id_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Bot Settings
SUMMARY_TIME=21:00
TRACKING_KEYWORDS=delivered,preparing,delayed,completed
TIMEZONE=UTC
```

## Usage

1. Start the bot:
```bash
python main.py
```

2. Add the bot to your Telegram group as an admin with message access.

3. Available commands:
- `/status` - Check bot status and message count
- `/summary` - Generate and post summary immediately
- `/settime HH:MM` - Set summary posting time (coming soon)
- `/setkeywords keyword1,keyword2` - Set tracking keywords (coming soon)
- `/preview` - Preview today's summary without posting (coming soon)

## Project Structure

```
telegram-summary-bot/
├── src/
│   ├── bot/            # Telegram bot implementation
│   ├── summarizer/     # OpenAI integration
│   ├── scheduler/      # Daily summary scheduling
│   ├── config/         # Configuration management
│   └── utils/          # Utility functions
├── .env                # Environment variables (not tracked by git)
├── .env.example        # Example environment variables
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 