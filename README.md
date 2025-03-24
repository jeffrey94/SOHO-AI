# Telegram Daily Summary Bot

A Telegram bot that automatically summarizes daily operations from a public channel using OpenAI's GPT-4.

## Features

- Monitors a public Telegram channel for operational updates
- Generates structured daily summaries using OpenAI's GPT-4
- Posts summaries at a configurable time (default: 9 PM)
- Admin commands for configuration and monitoring
- Automatic message categorization and formatting

## Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key
- Access to a public Telegram channel

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
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id
OPENAI_API_KEY=your_openai_api_key
SUMMARY_TIME=21:00
TRACKING_KEYWORDS=delivered,preparing,delayed
TIMEZONE=UTC
```

## Usage

1. Start the bot:
```bash
python main.py
```

2. Add the bot to your Telegram channel as an admin with message access.

3. Use admin commands in the channel:
- `/settime HH:MM` - Set summary posting time
- `/setkeywords keyword1,keyword2` - Set tracking keywords
- `/preview` - Preview today's summary
- `/status` - Check bot status and settings

## Project Structure

```
telegram-summary-bot/
├── src/
│   ├── bot/              # Telegram bot implementation
│   ├── summarizer/       # OpenAI integration
│   ├── scheduler/        # Daily summary scheduling
│   ├── config/          # Configuration management
│   └── utils/           # Utility functions
├── tests/               # Test files
├── logs/               # Application logs
├── .env.example        # Example environment variables
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 