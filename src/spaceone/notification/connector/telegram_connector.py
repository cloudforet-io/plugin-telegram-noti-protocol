import logging
import telegram
from spaceone.core.connector import BaseConnector

__all__ = ['TelegramConnector']
_LOGGER = logging.getLogger(__name__)


class TelegramConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = telegram.Bot(token=kwargs.get('token'))

    async def send_message(self, chat_id, message, reply_markup=None, image_url=None):
        try:
            if reply_markup:
                await self.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup,
                                            parse_mode='HTML')
            else:
                await self.bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
            if image_url:
                await self.bot.send_photo(chat_id=chat_id, photo=image_url)
        except telegram.error.BadRequest as e:
            _LOGGER.error(f'[send_message] Error: {e.message} ', exc_info=True)
            _LOGGER.debug(f'[send_message] Sending text message as fallback, chat_id: {chat_id}')
            await self.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            _LOGGER.error(f'[send_message] Error: {e}', exc_info=True)
            _LOGGER.debug(f'[send_message] Sending text message as fallback, chat_id: {chat_id}')
            await self.bot.send_message(chat_id=chat_id, text=message)
