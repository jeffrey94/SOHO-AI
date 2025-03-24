import logging
import asyncio
from telegram.ext import ApplicationBuilder
from src.config.settings import load_config
from src.bot.telegram_bot import TelegramBot
from src.scheduler.cron import SummaryScheduler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Run the bot application"""
    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        # Create application and bot
        app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
        bot = TelegramBot(app, config)
        logger.info("Bot initialized")
        
        # Initialize scheduler 
        scheduler = SummaryScheduler(bot, config)
        app.bot_data["scheduler"] = scheduler
        
        # Register post-initialization hook to start scheduler
        app.post_init = scheduler.start
        app.post_shutdown = scheduler.stop
        
        # Run the bot
        logger.info("Starting bot...")
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        exit(1) 