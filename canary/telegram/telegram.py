import sys

import canary.settings
import canary.telegram.telegram_bot


def load_telegram_settings():
    """
    Opens settings.json and checks all values have been set,
    if they have, creates a list containing these details
    and sets up Slack bot.

    If not exits and notifies user of misconfiguration

    :return: list containing options to use Slack API
    """
    telegram_settings = canary.settings.open_settings()

    telegram = telegram_settings['settings']['telegram']
    # sanity check that the user has actually supplied data
    bot_token = not telegram["bot_token"]
    id_client = not telegram["id_client"]

    if bot_token and id_client:
        sys.exit(128)

    #canary.telegram.telegram_bot.setup(telegram, id_client) #No setup doing for this moment

    return telegram
