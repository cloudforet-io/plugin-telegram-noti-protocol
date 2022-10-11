import logging
import telegram

from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram import InlineKeyboardButton
from spaceone.core.service import *
from spaceone.notification.conf.telegram_conf import *
from spaceone.notification.error import *
from spaceone.notification.manager.notification_manager import NotificationManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class NotificationService(BaseService):

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
        channel_data = params.get('channel_data', {})
        notification_type = params['notification_type']
        message = params['message']
        options = params.get('options')

        telegram_token = channel_data.get('token')  # bot token
        chat_id = channel_data.get('chat_id')

        updater = Updater(token=telegram_token, use_context=True)  # The Updater class continuously patches new updates from the telegram and delivers them to the Dispatch class.
        dispatcher = updater.dispatcher # Get created dispatcher linked to updater by internal queue
        updater.start_polling()  # Get bots' update regularly
        # updater.idle()  # idle() is a function that keeps the update running without ending.

        kwargs = {}

        # Get Message
        final_message = self._make_telegram_message_attachment(message, notification_type)

        # Check if callback exists
        if message.get('callbacks'):
            kwargs['callbacks'] = message['callbacks']

        # Check if image_url exists
        if message.get('image_url'):
            kwargs['image_url'] = message['image_url']

        kwargs['updater'] = updater
        kwargs['dispatcher'] = dispatcher

        noti_mgr: NotificationManager = self.locator.get_manager('NotificationManager')
        noti_mgr.dispatch(token=telegram_token, chat_id=chat_id, message=final_message, **kwargs)

    @staticmethod
    def _make_telegram_message_attachment(message, notification_type):
        """
        message (dict): {
            'title': 'str',
            'link': 'str',
            'image_url': 'str,
            'description': bool,
            'tags': [
                {
                    'key': '',
                    'value': '',
                    'options': {
                        'short': true|false
                    }
                }
            ],
            'callbacks': [
              {
                'label': 'str',
                'url': 'str',
                'options': 'dict'
              }
            ],
            'occurred_at': 'iso8601'
        }
        """
        message_attachments = []

        if message.get('link'):
            if message.get('title'):
                message.update({
                    'title': '\n' + '<b>' + f'[{notification_type}]' + '</b> ' + '<a href="' + message['link'] + '"' + '>' + f'{message["title"]}' + '</a>'
                })
                message_attachments.append(message['title'])
        else:
            message.update({
                'title': '\n' + '<b>' + f'[{notification_type}]' + '</b> ' + f'{message["title"]}'
            })
            message_attachments.append(message['title'])

        if message.get('description'):
            message_attachments.append('\n' + message['description']+'\n')

        if message.get('tags'):
            tag_attachments = ''
            for tag in message['tags']:
                # update key
                key_str = '\n' + '<b>' + "- " + tag['key'] + '</b>'
                value_str = '<pre>' + tag['value'] + '</pre>'

                # update tag
                tag_str = key_str + ": " + value_str
                tag_attachments += tag_str + " "

            message_attachments.append(tag_attachments)

        message_final = ' '.join(message_attachments)

        return message_final[:MAX_MESSAGE_LENGTH]
