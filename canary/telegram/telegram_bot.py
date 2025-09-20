try:
    import telepot
except ImportError as e:
    if 'telepot' not in str(e):
        pass

import sys

telegram_server = None
id_client = None


def setup(telegram, client):
    '''
    No setup doing for this moment
    '''

def run_bot(message, id_client, bot_token):
    """Send message using telepot (compatible version)"""
    try:
        bot = telepot.Bot(bot_token)
        bot.sendMessage(int(id_client), message)
        print(f"Mensaje enviado a Telegram: {message[:50]}...")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        # No hacer sys.exit para que el daemon continue funcionando
