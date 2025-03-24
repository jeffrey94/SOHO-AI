import logging
from telegram.ext import ApplicationBuilder
from src.config.settings import load_config
from src.bot.telegram_bot import setup_bot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Run the application"""
    try:
        # Load configuration
        config = load_config()
        
        # Create application
        app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Setup bot handlers (synchronously)
        setup_bot(app, config)
        
        # Run the application
        logger.info("Starting bot...")
        app.run_polling(
            allowed_updates=["message", "callback_query", "command"],
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"Error occurred: {e}")

if __name__ == '__main__':
    main() 