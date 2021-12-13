from spaceone.core.manager import BaseManager
from spaceone.notification.connector.telegram import TelegramConnector
from spaceone.notification.error.telegram import *
import telegram
from telegram import InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler
import logging

_LOGGER = logging.getLogger(__name__)

class TelegramManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = None

    def set_connector(self, token):
        self.conn: TelegramConnector = self.locator.get_connector('TelegramConnector', token=token)

    def send_message(self, chat_id, message, **kwargs):
        callbacks = kwargs.get('callbacks')
        updater = kwargs.get('updater')
        dispatcher = kwargs.get('dispatcher')
        image_url = kwargs.get('image_url')

        if callbacks:  # if data has callback information
            # make buttons
            task_button_list = []
            for callback in callbacks:
                label = callback.get('label')
                url = callback.get('url')
                task_button = [InlineKeyboardButton(text=label, callback_data="ack", url=url)]
                task_button_list.append(task_button)

            reply_markup = telegram.InlineKeyboardMarkup(task_button_list)
            self.conn.send_message_callback(chat_id=chat_id, message=message, reply_markup=reply_markup)

            def acknowledge_callback(update, context):  # Callback function of 'Acknowledged' button
                query = update.callback_query
                data = query.data

                if data == 'ack':  # if user push 'Acknowledged' Button
                    context.bot.send_message(chat_id=update.effective_chat.id, text="This alert is acknowledged.")

            button_callback_handler = CallbackQueryHandler(acknowledge_callback)
            dispatcher.add_handler(button_callback_handler)
            updater.start_polling()

            if image_url:
                try:
                    self.conn.send_photo(chat_id=chat_id, image_url=image_url, kwargs=kwargs)
                except Exception as e:
                    _LOGGER.error(ERROR_NOT_FIND_IMAGE_URL())

        else:
            self.conn.send_message(chat_id=chat_id, message=message)

            if image_url:
                try:
                    self.conn.send_photo(chat_id=chat_id, image_url=image_url)

                except ValueError as e:
                    _LOGGER.error(ERROR_NOT_FIND_IMAGE_URL())
