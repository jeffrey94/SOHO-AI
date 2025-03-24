# Message templates
SUMMARY_TEMPLATE = """
📝 Daily Ops Summary – {date}

{content}
"""

# Categories for summary
CATEGORIES = {
    'delivered': '✅ Delivered Orders',
    'in_progress': '🔄 In Progress',
    'issues': '⚠️ Issues',
    'other': '📌 Other Updates'
}

# OpenAI prompt template
OPENAI_PROMPT = """
Please analyze the following Telegram messages and create a structured summary.
Focus on order statuses, deliveries, and any issues or delays.

Messages:
{messages}

Please organize the information into these categories:
{categories}

Format the summary in a clear, concise manner with bullet points.
Focus on actionable information and important updates.
"""

# Admin commands
ADMIN_COMMANDS = {
    'settime': 'Set the time for daily summary (format: HH:MM)',
    'setkeywords': 'Set keywords to track (comma-separated)',
    'preview': 'Preview today\'s summary',
    'status': 'Check bot status and summary settings'
}

# Error messages
ERROR_MESSAGES = {
    'invalid_time': 'Invalid time format. Please use HH:MM format.',
    'invalid_keywords': 'Invalid keywords format. Please provide comma-separated keywords.',
    'permission_denied': 'You do not have permission to use this command.',
    'api_error': 'An error occurred while processing your request.'
} 