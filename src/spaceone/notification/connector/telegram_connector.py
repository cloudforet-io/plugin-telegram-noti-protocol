import logging
import asyncio
import telegram

from spaceone.core.connector import BaseConnector

__all__ = ['TelegramConnector']
_LOGGER = logging.getLogger(__name__)


def retry_handler(times: int = 3) -> callable:
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    _LOGGER.error(f'[retry_request] Error: {e}, retry {i}', exc_info=True)
                    await asyncio.sleep(1)

            raise Exception(f'[retry_request] Retry failed after {times} times')

        return wrapper

    return decorator


class TelegramConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = telegram.Bot(token=kwargs.get('token'))

    @retry_handler(times=5)
    async def send_message(self, chat_id: str, message, reply_markup=None, image_url=None) -> None:
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
