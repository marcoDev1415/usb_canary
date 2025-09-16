try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError as e:
    if 'slack_sdk' not in str(e):
        raise
import sys

slack_client = None
channel_name = None


def setup(slack, channel):
    global slack_client
    slack_client = WebClient(token=slack['api_key'])
    global channel_name
    channel_name = channel


def run_bot(message, channel):
    try:
        # Verificar si el canal existe
        try:
            response = slack_client.conversations_list()
            channels = response['channels']
            channel_exists = any(ch['name'] == channel for ch in channels)
        except SlackApiError:
            channel_exists = False

        if channel_exists:
            slack_client.chat_postMessage(channel=f"#{channel}", text=message)
        else:
            error_msg = ("Hi! :wave: It looks like some of my settings might be a little frazzled, "
                        "and I can't post messages like normal.")
            slack_client.chat_postMessage(channel="#general", text=error_msg)
    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")
        sys.exit(1)
    except Exception as e:
        print(f"Connection failed. Invalid Slack token or bot ID? Error: {e}")
        sys.exit(1)
