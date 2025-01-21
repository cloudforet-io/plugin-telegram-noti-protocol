import logging
import asyncio
from spaceone.core.manager import BaseManager
from spaceone.notification.connector.telegram_connector import TelegramConnector
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

_LOGGER = logging.getLogger(__name__)


class TelegramManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = None

    def set_connector(self, token: str) -> None:
        self.conn: TelegramConnector = self.locator.get_connector('TelegramConnector', token=token)

    def send_message(self, chat_id: str, message, **kwargs):
        image_url = kwargs.get('image_url')
        callbacks = kwargs.get('callbacks')
        reply_markup = None

        if callbacks:
            task_button_list = []
            for callback in callbacks:
                label = callback.get('label')
                url = callback.get('url')
                task_button = [InlineKeyboardButton(text=label, callback_data="ack", url=url)]
                task_button_list.append(task_button)

            reply_markup = InlineKeyboardMarkup(task_button_list)

        asyncio.run(self.conn.send_message(chat_id=chat_id,
                                           message=message,
                                           reply_markup=reply_markup,
                                           image_url=image_url))
