import logging
from datetime import datetime
from typing import List, Dict
from openai import OpenAI
from src.config.constants import OPENAI_PROMPT, CATEGORIES

logger = logging.getLogger(__name__)

class OpenAISummarizer:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        
    async def generate_summary(self, messages: List[Dict]) -> str:
        """Generate a summary of messages using OpenAI."""
        try:
            # Format messages for the prompt
            formatted_messages = self._format_messages(messages)
            
            # Create the prompt
            prompt = OPENAI_PROMPT.format(
                messages=formatted_messages,
                categories="\n".join(CATEGORIES.values())
            )
            
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates clear, structured summaries of operational updates."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract and format the summary
            summary = response.choices[0].message.content
            
            # Format the final message with date
            today = datetime.now().strftime("%b %d")
            return f"📝 Daily Ops Summary – {today}\n\n{summary}"
            
        except Exception as e:
            logger.error(f"Error generating summary with OpenAI: {e}")
            raise
            
    def _format_messages(self, messages: List[Dict]) -> str:
        """Format messages for the prompt."""
        formatted = []
        for msg in messages:
            timestamp = datetime.fromtimestamp(msg['timestamp']).strftime("%H:%M")
            formatted.append(f"[{timestamp}] {msg['text']}")
        return "\n".join(formatted) 