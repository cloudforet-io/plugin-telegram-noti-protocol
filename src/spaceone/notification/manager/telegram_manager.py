from spaceone.core.manager import BaseManager
from spaceone.notification.connector.telegram import TelegramConnector

class TelegramManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = None

    def set_connector(self, token):
        self.conn: TelegramConnector = self.locator.get_connector('TelegramConnector', token=token)

    def send_message(self, chat_id, message):
        self.conn.send_message(chat_id, message)

