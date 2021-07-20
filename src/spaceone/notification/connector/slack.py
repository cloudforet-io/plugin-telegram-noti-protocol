import logging
import telegram
from ssl import SSLContext
#from slack_sdk import WebClient
#from slack_sdk.errors import SlackApiError


from spaceone.core.connector import BaseConnector

__all__ = ['SlackConnector']
_LOGGER = logging.getLogger(__name__)

sslcert = SSLContext()

class SlackConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.client = WebClient(token=kwargs.get('token'), ssl=sslcert)
        self.bot = telegram.Bot(token=kwargs.get('token'))

    def chat_message(self, channel, message):
        response = self.client.chat_postMessage(channel=f'#{channel}', text=message)
        return response

    def send_message(self, chat_id, message):
        response = self.bot.send_message(chat_id=chat_id, text=message)
