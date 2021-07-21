import logging
import telegram

from telegram.ext import CommandHandler
from spaceone.core.service import *
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
        secret_data = params.get('secret_data', {})
        notification_type = params['notification_type']
        message = params['message']

        telegram_token = secret_data.get('token')  # bot token
        group_name = secret_data.get('group_name')
        bot = telegram.Bot(telegram_token)
        updates = bot.get_updates()
        chat_id = self._get_dispatch_chat_id(updates=updates, group_name=group_name)

        noti_mgr: NotificationManager = self.locator.get_manager('NotificationManager')
        noti_mgr.dispatch(token=telegram_token, chat_id=chat_id, message=message)

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


