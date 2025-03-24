import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from src.config.constants import ADMIN_COMMANDS, ERROR_MESSAGES, SUMMARY_TEMPLATE
from src.summarizer.openai_summarizer import OpenAISummarizer
from datetime import datetime

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, application: Application, config):
        self.application = application
        self.config = config
        self.messages = []
        self.summarizer = OpenAISummarizer(config.OPENAI_API_KEY)
        self.setup_handlers()

    def setup_handlers(self):
        """Setup bot handlers"""
        # Store reference to this bot in application
        self.application.bot_data["bot"] = self
        
        # Add command handlers
        self.application.add_handler(CommandHandler("status", self.handle_status))
        self.application.add_handler(CommandHandler("summary", self.handle_summary))
        
        # Add message handler for group messages
        self.application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=self.config.TELEGRAM_GROUP_ID),
                self.handle_message
            )
        )
        
        logger.info("Bot handlers setup completed")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming group messages."""
        try:
            if update.message and update.message.text:
                logger.info(f"Received message: {update.message.text[:50]}...")
                self.messages.append({
                    'timestamp': update.message.date.timestamp(),
                    'text': update.message.text
                })
                logger.info(f"Message stored successfully. Total messages: {len(self.messages)}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")

    async def handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        try:
            logger.info("Status command received")
            response = f"Bot is running. Stored messages: {len(self.messages)}"
            await update.message.reply_text(response)
            logger.info(f"Status response sent: {response}")
        except Exception as e:
            logger.error(f"Error in status handler: {e}")
            await update.message.reply_text("Error processing status command")

    async def handle_summary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /summary command to generate and post summary immediately"""
        try:
            logger.info("Summary command received")
            # Check if the command is from the configured group
            if update.message.chat.id != self.config.TELEGRAM_GROUP_ID:
                await update.message.reply_text(ERROR_MESSAGES["permission_denied"])
                return

            # Get reference to scheduler
            scheduler = self.application.bot_data.get("scheduler")
            if scheduler:
                await update.message.reply_text("Generating summary...")
                await scheduler.post_summary()
                logger.info("Manual summary generated and posted successfully")
            else:
                await update.message.reply_text("Error: Scheduler not initialized")
        except Exception as e:
            logger.error(f"Error in summary handler: {e}")
            await update.message.reply_text(f"Error generating summary: {str(e)}")

    async def generate_summary(self):
        """Generate summary from stored messages"""
        if not self.messages:
            return "No messages to summarize."
        
        try:
            return await self.summarizer.generate_summary(self.messages)
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            today = datetime.now().strftime("%b %d")
            return SUMMARY_TEMPLATE.format(
                date=today,
                content="⚠️ Error generating summary. Please try again later."
            ) 