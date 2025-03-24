import asyncio
import logging
from datetime import datetime, timedelta
import pytz
from src.bot.telegram_bot import TelegramBot
from src.config.settings import Config

logger = logging.getLogger(__name__)

class SummaryScheduler:
    """Scheduler for daily summary generation and posting"""
    
    def __init__(self, bot: TelegramBot, config: Config):
        """Initialize the scheduler"""
        self.bot = bot
        self.config = config
        self.timezone = pytz.timezone(config.TIMEZONE)
        self.running = False
        self.task = None
        logger.info("Scheduler initialized")
        
    async def start(self, app=None):
        """Start the scheduler - called as Application hook"""
        if self.running:
            return
            
        self.running = True
        # In async context, we can create the task directly
        self.task = asyncio.create_task(self._run_scheduler())
        logger.info("Scheduler started")
        
    async def stop(self, app=None):
        """Stop the scheduler - called as Application hook"""
        logger.info("Stopping scheduler...")
        self.running = False
        
        # Wait for task to complete if it exists
        if self.task:
            try:
                # Give it a short timeout to avoid hanging
                await asyncio.wait_for(asyncio.shield(self.task), timeout=2.0)
            except asyncio.TimeoutError:
                logger.warning("Scheduler task did not complete in time")
            except Exception as e:
                logger.error(f"Error waiting for scheduler task: {str(e)}")
                
        logger.info("Scheduler stopped")
            
    async def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            try:
                # Calculate time until next summary
                next_run, wait_seconds = self._calculate_next_run()
                logger.info(f"Next summary scheduled for {next_run} ({wait_seconds} seconds from now)")
                
                # Break long wait into smaller chunks to allow clean shutdown
                await self._wait_with_checks(wait_seconds)
                
                # Generate and post summary if still running
                if self.running:
                    await self.post_summary()
                    
            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}", exc_info=True)
                await asyncio.sleep(60)  # Wait a minute before retrying
    
    def _calculate_next_run(self):
        """Calculate the next run time and seconds to wait"""
        now = datetime.now(self.timezone)
        target_hour, target_minute = map(int, self.config.SUMMARY_TIME.split(':'))
        
        next_run = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        if next_run <= now:
            next_run = next_run + timedelta(days=1)  # Move to tomorrow
            
        wait_seconds = (next_run - now).total_seconds()
        return next_run, wait_seconds
    
    async def _wait_with_checks(self, total_seconds):
        """Wait for the specified time with periodic checks for shutdown signal"""
        sleep_interval = 30  # Check every 30 seconds
        
        while total_seconds > 0 and self.running:
            await asyncio.sleep(min(sleep_interval, total_seconds))
            total_seconds -= sleep_interval
                
    async def post_summary(self):
        """Generate and post the daily summary"""
        try:
            # Generate summary
            summary = await self.bot.generate_summary()
            
            # Post to Telegram
            await self.bot.application.bot.send_message(
                chat_id=self.config.TELEGRAM_GROUP_ID,
                text=summary
            )
            logger.info("Daily summary posted successfully")
            
            # Clear messages for next day
            self.bot.messages = []
            
        except Exception as e:
            logger.error(f"Error posting summary: {str(e)}", exc_info=True) 