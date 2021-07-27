from spaceone.core.manager import BaseManager
from spaceone.notification.connector.telegram import TelegramConnector
import telegram
from telegram import InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler

class TelegramManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = None

    def set_connector(self, token):
        self.conn: TelegramConnector = self.locator.get_connector('TelegramConnector', token=token)

    def send_message(self, chat_id, message, callback, updater, dispatcher):
        if callback is True:  # if data has callback information
            task_buttons = [[InlineKeyboardButton(text='Acknowledge Alert', callback_data=1)]]
            reply_markup = telegram.InlineKeyboardMarkup(task_buttons)
            self.conn.send_message_callback(chat_id=chat_id, message=message, reply_markup=reply_markup)

            def acknowledge_callback(update, context):  # Callback function of 'Acknowledged' button
                query = update.callback_query
                data = query.data

                if data == '1':  # if user push 'Acknowledged' Button TODO : Request URL?
                    context.bot.send_message(chat_id=update.effective_chat.id, text="This alert is acknowledged.")

            button_callback_handler = CallbackQueryHandler(acknowledge_callback)
            dispatcher.add_handler(button_callback_handler)
            updater.start_polling()

        else:
            self.conn.send_message(chat_id=chat_id, message=message)