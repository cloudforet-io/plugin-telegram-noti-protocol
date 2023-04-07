import logging
import telegram
from spaceone.core.connector import BaseConnector
from spaceone.notification.error.telegram_error import *

__all__ = ['TelegramConnector']
_LOGGER = logging.getLogger(__name__)


class TelegramConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = telegram.Bot(token=kwargs.get('token'))

    async def send_message(self, chat_id, message, reply_markup=None, image_url=None):
        if reply_markup:
            await self.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup, parse_mode='HTML')
        else:
            await self.bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')

        if image_url:
            await self.bot.send_photo(chat_id=chat_id, photo=image_url)
