from spaceone.core.manager import BaseManager
from spaceone.notification.manager.telegram_manager import TelegramManager


class NotificationManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, token, chat_id, message, **kwargs):
        telegram_mgr: TelegramManager = self.locator.get_manager('TelegramManager')
        telegram_mgr.set_connector(token)
        telegram_mgr.send_message(chat_id=chat_id, message=message, **kwargs)
