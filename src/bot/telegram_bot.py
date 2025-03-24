import logging
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from src.config.settings import Config
from src.config.constants import ADMIN_COMMANDS, ERROR_MESSAGES
from src.summarizer.openai_summarizer import OpenAISummarizer

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, config: Config):
        self.config = config
        self.application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        self.summarizer = OpenAISummarizer(config.OPENAI_API_KEY)
        self.messages = []
        
    async def start(self):
        """Initialize bot handlers and start the bot."""
        # Add command handlers
        self.application.add_handler(CommandHandler("settime", self.handle_settime))
        self.application.add_handler(CommandHandler("setkeywords", self.handle_setkeywords))
        self.application.add_handler(CommandHandler("preview", self.handle_preview))
        self.application.add_handler(CommandHandler("status", self.handle_status))
        
        # Add message handler for channel messages
        self.application.add_handler(
            MessageHandler(
                filters.ChatType.CHANNEL & filters.Chat(chat_id=self.config.TELEGRAM_CHANNEL_ID),
                self.handle_channel_message
            )
        )
        
    async def run_polling(self):
        """Start the bot with polling."""
        await self.application.run_polling()
        
    async def handle_channel_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming channel messages."""
        message = update.channel_post
        if message and message.text:
            self.messages.append({
                'timestamp': message.date,
                'text': message.text
            })
            
    async def handle_settime(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /settime command."""
        if not self._is_admin(update.effective_user.id):
            await update.message.reply_text(ERROR_MESSAGES['permission_denied'])
            return
            
        try:
            time = context.args[0]
            # Validate time format (HH:MM)
            datetime.strptime(time, '%H:%M')
            self.config.SUMMARY_TIME = time
            await update.message.reply_text(f"Summary time set to {time}")
        except (ValueError, IndexError):
            await update.message.reply_text(ERROR_MESSAGES['invalid_time'])
            
    async def handle_setkeywords(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /setkeywords command."""
        if not self._is_admin(update.effective_user.id):
            await update.message.reply_text(ERROR_MESSAGES['permission_denied'])
            return
            
        try:
            keywords = [kw.strip() for kw in context.args[0].split(',')]
            self.config.TRACKING_KEYWORDS = keywords
            await update.message.reply_text(f"Keywords set to: {', '.join(keywords)}")
        except (ValueError, IndexError):
            await update.message.reply_text(ERROR_MESSAGES['invalid_keywords'])
            
    async def handle_preview(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /preview command."""
        if not self._is_admin(update.effective_user.id):
            await update.message.reply_text(ERROR_MESSAGES['permission_denied'])
            return
            
        try:
            summary = await self.generate_summary()
            await update.message.reply_text(summary)
        except Exception as e:
            logger.error(f"Error generating preview: {e}")
            await update.message.reply_text(ERROR_MESSAGES['api_error'])
            
    async def handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        if not self._is_admin(update.effective_user.id):
            await update.message.reply_text(ERROR_MESSAGES['permission_denied'])
            return
            
        status_message = (
            f"Bot Status:\n"
            f"Summary Time: {self.config.SUMMARY_TIME}\n"
            f"Tracking Keywords: {', '.join(self.config.TRACKING_KEYWORDS)}\n"
            f"Messages Today: {len(self.messages)}\n"
            f"Timezone: {self.config.TIMEZONE}"
        )
        await update.message.reply_text(status_message)
        
    async def generate_summary(self) -> str:
        """Generate summary of today's messages."""
        if not self.messages:
            return "No messages to summarize today."
            
        try:
            summary = await self.summarizer.generate_summary(self.messages)
            return summary
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            raise
            
    def _is_admin(self, user_id: int) -> bool:
        """Check if user is an admin."""
        # TODO: Implement proper admin checking logic
        return True  # For now, allow all users to use admin commands 