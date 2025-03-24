# Message templates
SUMMARY_TEMPLATE = """
📝 每日运营摘要 / Daily Ops Summary – {date}

{content}
"""

# Categories for summary
CATEGORIES = {
    'delivered': '✅ 已完成订单 / Delivered Orders',
    'in_progress': '🔄 处理中 / In Progress',
    'issues': '⚠️ 问题 / Issues',
    'other': '📌 其他更新 / Other Updates'
}

# OpenAI prompt template
OPENAI_PROMPT = """
Please analyze the following Telegram messages and create a structured bilingual summary in both Chinese and English, with Chinese first.
Focus on order statuses, deliveries, and any issues or delays.

Messages:
{messages}

Please organize the information into these categories:
{categories}

Format the summary in a clear, concise manner with bullet points.
Focus on actionable information and important updates.
For each category, first provide the summary in Chinese, then in English.
"""

# Admin commands
ADMIN_COMMANDS = {
    'status': 'Check bot status and summary settings',
    'summary': 'Generate and post summary immediately',
    'settime': 'Set the time for daily summary (format: HH:MM)',
    'setkeywords': 'Set keywords to track (comma-separated)',
    'preview': 'Preview today\'s summary without posting'
}

# Error messages
ERROR_MESSAGES = {
    'invalid_time': 'Invalid time format. Please use HH:MM format.',
    'invalid_keywords': 'Invalid keywords format. Please provide comma-separated keywords.',
    'permission_denied': 'You do not have permission to use this command.',
    'api_error': 'An error occurred while processing your request.',
    'not_implemented': 'This command is not yet implemented.'
} 