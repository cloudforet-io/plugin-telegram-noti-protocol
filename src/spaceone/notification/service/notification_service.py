import logging
import telegram

from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram import InlineKeyboardButton
from spaceone.core.service import *
from spaceone.notification.error import *
from spaceone.notification.manager.notification_manager import NotificationManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class NotificationService(BaseService):
    CHATS_DICT = {}

    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(['options', 'message', 'notification_type'])
    def dispatch(self, params):
        """
        Args:
            params:
                - options
                - message :
                - notification_type : INFO || ERROR || SUCCESS || WARNING
                - secret_data
        """
        secret_data = params.get('secret_data', {})
        channel_data = params.get('channel_data', {})
        notification_type = params['notification_type']
        message = params['message']
        options = params.get('options')
        group_list = options.get('group_list')

        self.CHATS_DICT = options.get('chats_dict')

        telegram_token = secret_data.get('token')  # bot token
        group_name = channel_data.get('group_name')

        bot = telegram.Bot(telegram_token)
        updater = Updater(token=telegram_token, use_context=True)
        dispatcher = updater.dispatcher

        def start(update, context):  # Callback function of '/start' command
            chat_id = str(update.effective_chat.id)
            chat_title = str(update.effective_chat.title)
            self.CHATS_DICT[chat_id] = chat_title   # save chat lists

            group_list.append(update.effective_chat.id)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Start subscribing SpaceONE alert bot.")

        def stop(update, context): # Callback function of '/stop' command
            chat_id = str(update.effective_chat.id)
            del(self.CHATS_DICT[chat_id])
            context.bot.send_message(chat_id=update.effective_chat.id, text="Stop subscribing SpaceONE alert bot.")

        start_handler = CommandHandler('start', start)
        stop_handler = CommandHandler('stop', stop)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(stop_handler)

        updater.start_polling()
        # updater.idle()

        chat_id = self._get_chat_id(group_name=group_name, chats_dict=self.CHATS_DICT)

        # Get Message
        final_message = self._make_telegram_message_attachment(message)

        # Check if callback exists
        if message.get('callbacks'):
            callback = True
        else:
            callback = False

        noti_mgr: NotificationManager = self.locator.get_manager('NotificationManager')
        noti_mgr.dispatch(token=telegram_token, chat_id=chat_id, message=final_message, callback=callback, updater=updater, dispatcher=dispatcher)

    def _get_dispatch_chat_id(self, updates, group_name):
        try:
            for update in updates:
                if update.my_chat_member:  # Update object's metadata class
                    pass
                else:
                    chat_title = update.message.chat.title

                    if str(chat_title) == group_name:
                        chat_id = update.message.chat.id
                        return chat_id

        except Exception as e:
            _LOGGER.error(f'[_get_dispatch_chat_id] Cannot find the chat id for the group name: {getattr(e, "message", e)}')
            raise ValueError

    def _make_telegram_message_attachment(self, message):
        message_attachments = []

        if message.get('title'):
            message.update({
                'title': '<b>' + message['title'] + '</b>'
            })
            message_attachments.append(message['title'])

        if message.get('description'):
            message_attachments.append(message['description'])

        if message.get('link'):
            link_parse = '<b>Link: </b> <a href="' + message['link'] + '"' + '>' + f'{message["link"]}' + "</a>"
            message.update({
                'link': link_parse
            })
            message_attachments.append(message['link'])

        if message.get('tags'):
            tag_attachments = ''
            for tag in message['tags']:
                # update key
                key_str = '<b>' + tag['key'] + '</b>'
                value_str = '<pre>' + tag['value'] + '</pre>'

                # update tag
                tag_str = key_str + ": " + value_str
                tag_attachments += tag_str + ", "

            message_attachments.append(tag_attachments)

        message_final = ', '.join(message_attachments)
        return message_final

    def _get_chat_id(self, group_name, chats_dict):
        try:
            for k, v in chats_dict.items():
                if v == group_name:
                    return k

        except Exception as e:
                _LOGGER.error(f'[_get_chat_id] Cannot find the chat id for the group name: {getattr(e, "message", e)}')
                raise ValueError
