import logging
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters

logger = logging.getLogger(__name__)

class MessageStore:
    def __init__(self):
        self.messages = []

message_store = MessageStore()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming group messages."""
    try:
        if update.message and update.message.text:
            logger.info(f"Received message: {update.message.text[:50]}...")
            message_store.messages.append({
                'timestamp': update.message.date,
                'text': update.message.text
            })
            logger.info(f"Message stored successfully. Total messages: {len(message_store.messages)}")
    except Exception as e:
        logger.error(f"Error handling message: {e}")

async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    try:
        logger.info("Status command received")
        response = f"Bot is running. Stored messages: {len(message_store.messages)}"
        await update.message.reply_text(response)
        logger.info(f"Status response sent: {response}")
    except Exception as e:
        logger.error(f"Error in status handler: {e}")
        await update.message.reply_text("Error processing status command")

def setup_bot(application, config):
    """Setup bot handlers"""
    # Add command handlers first
    application.add_handler(CommandHandler("status", handle_status))
    
    # Add message handler for group messages with less restrictive filter
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,  # Removed the chat_id filter
            handle_message
        )
    )
    
    logger.info("Bot handlers setup completed") 