import logging
import os
import telegram
from telegram.ext import Updater

from spaceone.core import utils
from spaceone.tester import TestCase, print_json

_LOGGER = logging.getLogger(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN', None)
# bot = telegram.Bot(token=TOKEN)
# bot.send_message(text='SpaceONE TEST NOOO', chat_id='-549309904')

if TOKEN == None:
    print("""
##################################################
# ERROR
#
# Configure your Telegram Token first for test
##################################################
example)

export TELEGRAM_TOKEN=<YOUR_TELEGRAM_TOKEN>

""")
    exit


class TestTelegramNotification(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get('SPACEONE_TEST_CONFIG_FILE', './config.yml'))
    endpoints = config.get('ENDPOINTS', {})
    secret_data = {
        'token': TOKEN,
        'group_name': 'SpaceTestgroup2',
    }

    def test_init(self):
        v_info = self.notification.Protocol.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {}
        self.notification.Protocol.verify({'options': options, 'secret_data': self.secret_data})

    def test_dispatch(self):
        options = {}

        self.notification.Notification.dispatch({
            'options': options,
            'message': {'message': 'SpaceONE loves me'},  # TODO : QUESTION!!
            'notification_type': 'INFO',
            'secret_data': self.secret_data
        })
