import logging
from datetime import datetime
from typing import List, Dict
import asyncio
from openai import AsyncOpenAI
from src.config.constants import OPENAI_PROMPT, CATEGORIES, SUMMARY_TEMPLATE

logger = logging.getLogger(__name__)

class OpenAISummarizer:
    """OpenAI-powered message summarizer"""
    
    def __init__(self, api_key: str):
        """Initialize with OpenAI API key"""
        self.client = AsyncOpenAI(api_key=api_key)
        
    async def generate_summary(self, messages: List[Dict]) -> str:
        """Generate a summary of messages using OpenAI."""
        if not messages:
            logger.warning("No messages to summarize")
            today = datetime.now().strftime("%b %d")
            return SUMMARY_TEMPLATE.format(
                date=today,
                content="No messages to summarize for today."
            )
            
        try:
            # Format messages for the prompt
            formatted_messages = self._format_messages(messages)
            
            # Create the prompt
            prompt = OPENAI_PROMPT.format(
                messages=formatted_messages,
                categories="\n".join(f"- {cat}" for cat in CATEGORIES.values())
            )
            
            # Call OpenAI API with retry logic
            summary_content = await self._call_openai_with_retry(prompt)
            
            # Format the final message with date
            today = datetime.now().strftime("%b %d")
            return SUMMARY_TEMPLATE.format(
                date=today,
                content=summary_content
            )
            
        except Exception as e:
            logger.error(f"Error generating summary with OpenAI: {str(e)}", exc_info=True)
            raise
    
    async def _call_openai_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """Call OpenAI API with retry logic"""
        retries = 0
        backoff = 1
        
        while retries <= max_retries:
            try:
                response = await self.client.chat.completions.create(
                    model="gpt-4o",  # Using the latest model for better multilingual support
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that creates clear, structured summaries of operational updates. Create bilingual summaries in both Chinese and English, with Chinese first followed by English content for each section."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                retries += 1
                if retries > max_retries:
                    logger.error(f"Failed after {max_retries} retries: {str(e)}")
                    raise
                
                # Exponential backoff
                wait_time = backoff * 2 ** (retries - 1)
                logger.warning(f"OpenAI API error, retrying in {wait_time}s: {str(e)}")
                await asyncio.sleep(wait_time)
            
    def _format_messages(self, messages: List[Dict]) -> str:
        """Format messages for the prompt."""
        if not messages:
            return "No messages"
            
        formatted = []
        for msg in messages:
            # Handle both timestamp formats (datetime object or timestamp float)
            if isinstance(msg['timestamp'], (int, float)):
                timestamp = datetime.fromtimestamp(msg['timestamp']).strftime("%H:%M")
            else:
                timestamp = msg['timestamp'].strftime("%H:%M")
                
            formatted.append(f"[{timestamp}] {msg['text']}")
            
        return "\n".join(formatted) 