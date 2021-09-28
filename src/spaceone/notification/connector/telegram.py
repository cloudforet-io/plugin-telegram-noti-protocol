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
        response = self.bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
        return response

    def send_message_callback(self, chat_id, message, reply_markup):
        response = self.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup, parse_mode='HTML')
        return response

    def send_photo(self, chat_id, image_url):
        response = self.bot.send_photo(chat_id=chat_id, photo=image_url)
        return response
