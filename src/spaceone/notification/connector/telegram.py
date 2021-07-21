import logging
import telegram
from spaceone.core.connector import BaseConnector

__all__ = ['TelegramConnector']
_LOGGER = logging.getLogger(__name__)


class TelegramConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = telegram.Bot(token=kwargs.get('token'))

    def send_message(self, chat_id, message):
        response = self.bot.send_message(chat_id=chat_id, text=message)
        return response

