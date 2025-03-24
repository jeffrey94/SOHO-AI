import asyncio
import logging
from datetime import datetime
import pytz
from src.bot.telegram_bot import TelegramBot
from src.config.settings import Config

logger = logging.getLogger(__name__)

class SummaryScheduler:
    def __init__(self, bot: TelegramBot, config: Config):
        self.bot = bot
        self.config = config
        self.timezone = pytz.timezone(config.TIMEZONE)
        self.running = False
        self.task = None
        
    async def start(self):
        """Start the scheduler asynchronously"""
        self.running = True
        self.task = asyncio.create_task(self._run_scheduler())
        
    async def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.task:
            await self.task
            
    async def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            try:
                now = datetime.now(self.timezone)
                target_hour, target_minute = map(int, self.config.SUMMARY_TIME.split(':'))
                
                next_run = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
                if next_run <= now:
                    next_run = next_run.replace(day=next_run.day + 1)
                    
                wait_seconds = (next_run - now).total_seconds()
                logger.info(f"Next summary scheduled for {next_run} ({wait_seconds} seconds from now)")
                
                await asyncio.sleep(wait_seconds)
                
                if self.running:
                    await self._post_summary()
                    
            except Exception as e:
                logger.error(f"Error in scheduler: {e}")
                await asyncio.sleep(60)
                
    async def _post_summary(self):
        """Generate and post the daily summary."""
        try:
            summary = await self.bot.generate_summary()
            await self.bot.application.bot.send_message(
                chat_id=self.config.TELEGRAM_CHANNEL_ID,
                text=summary
            )
            logger.info("Daily summary posted successfully")
            
            # Clear messages for next day
            self.bot.messages = []
            
        except Exception as e:
            logger.error(f"Error posting summary: {e}")
            
    def stop(self):
        """Stop the scheduler."""
        self.running = False 