try:
    from telegram import Bot
    from telegram.error import TelegramError
    import asyncio
except ImportError as e:
    if 'telegram' not in str(e):
        pass

import sys

telegram_server = None
id_client = None


def setup(telegram, client):
    '''
    No setup doing for this moment
    '''

async def send_message_async(bot_token, chat_id, message):
    """Send message asynchronously"""
    bot = Bot(token=bot_token)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        print(f"Telegram Error: {e}")
        sys.exit(1)

def run_bot(message, id_client, bot_token):
    """Send message using asyncio"""
    try:
        # Ejecutar de forma síncrona usando asyncio
        asyncio.run(send_message_async(bot_token, id_client, message))
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        sys.exit(1)
