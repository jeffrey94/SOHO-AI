import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_GROUP_ID: int
    OPENAI_API_KEY: str
    SUMMARY_TIME: str = "21:00"  # Default to 9 PM
    TRACKING_KEYWORDS: List[str] = None
    TIMEZONE: str = "UTC"

def load_config() -> Config:
    """Load configuration from environment variables."""
    load_dotenv()
    
    # Required environment variables
    required_vars = {
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'TELEGRAM_GROUP_ID': os.getenv('TELEGRAM_GROUP_ID'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    }
    
    # Check for missing required variables
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return Config(
        TELEGRAM_BOT_TOKEN=required_vars['TELEGRAM_BOT_TOKEN'],
        TELEGRAM_GROUP_ID=int(required_vars['TELEGRAM_GROUP_ID']),
        OPENAI_API_KEY=required_vars['OPENAI_API_KEY'],
        SUMMARY_TIME=os.getenv('SUMMARY_TIME', '21:00'),
        TRACKING_KEYWORDS=os.getenv('TRACKING_KEYWORDS', '').split(','),
        TIMEZONE=os.getenv('TIMEZONE', 'UTC')
    ) 