import asyncio
import logging
from src.bot.telegram_bot import TelegramBot
from src.scheduler.cron import SummaryScheduler
from src.config.settings import load_config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    # Load configuration
    config = load_config()
    
    # Initialize bot and scheduler
    bot = TelegramBot(config)
    scheduler = SummaryScheduler(bot, config)
    
    # Start the scheduler
    scheduler.start()
    
    # Start the bot
    await bot.start()
    
    # Keep the bot running
    await bot.run_polling()

if __name__ == '__main__':
    asyncio.run(main()) 