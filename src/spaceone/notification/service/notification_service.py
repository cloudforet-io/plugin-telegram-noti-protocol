import logging

from spaceone.core.service import *
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
                - message
                - notification_type
                - secret_data
        """
        secret_data = params.get('secret_data', {})
        notification_type = params['notification_type']
        message = params['message']

        telegram_token = secret_data.get('token')
        channel = secret_data.get('channel')

        noti_mgr: NotificationManager = self.locator.get_manager('NotificationManager')
        noti_mgr.dispatch(telegram_token, channel, f'[{notification_type}] {message["message"]}')
