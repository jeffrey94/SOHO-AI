import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHANNEL_ID: str
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
        'TELEGRAM_CHANNEL_ID': os.getenv('TELEGRAM_CHANNEL_ID'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    }
    
    # Check for missing required variables
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Optional variables with defaults
    tracking_keywords = os.getenv('TRACKING_KEYWORDS', '').split(',')
    tracking_keywords = [kw.strip() for kw in tracking_keywords if kw.strip()]
    
    return Config(
        TELEGRAM_BOT_TOKEN=required_vars['TELEGRAM_BOT_TOKEN'],
        TELEGRAM_CHANNEL_ID=required_vars['TELEGRAM_CHANNEL_ID'],
        OPENAI_API_KEY=required_vars['OPENAI_API_KEY'],
        SUMMARY_TIME=os.getenv('SUMMARY_TIME', '21:00'),
        TRACKING_KEYWORDS=tracking_keywords,
        TIMEZONE=os.getenv('TIMEZONE', 'UTC')
    ) 