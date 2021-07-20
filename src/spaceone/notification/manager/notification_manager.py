from spaceone.core.manager import BaseManager
from spaceone.notification.manager.slack_manager import SlackManager


class NotificationManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, token, slack_channel, message):
        slack_mgr: SlackManager = self.locator.get_manager('SlackManager')
        slack_mgr.set_connector(token)
        slack_mgr.send_message(slack_channel, message)