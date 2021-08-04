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
    config = utils.load_yaml_from_file(os.environ.get('SPACEONE_TEST_CONFIG_FILE', './config.yml'))
    endpoints = config.get('ENDPOINTS', {})
    secret_data = {}
    channel_data = {
        'token': TOKEN,
        'chat_id': '-545874019'
    }

    def test_init(self):
        v_info = self.notification.Protocol.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {}
        self.notification.Protocol.verify({'options': options, 'secret_data': self.secret_data})

    def test_dispatch(self):
        options = {
            'group_list': [],
            'chats_dict': {'-514081686': 'Space3', '-545874019': 'SpaceTestgroup2'}
        }

        self.notification.Notification.dispatch({
            'options': options,
            'message':
                {
                    'title': 'This is title',
                    'description': 'SpaceONE loves jiyooniiii2',
                    'link': 'www.spaceone.org',
                    'callbacks': [{'label': 'callback_label', 'url': 'https://github.com/spaceone-dev', 'options': {}}],
                    'tags': [
                        {
                            'key': 'Alert Number',
                            'value': '#130900'
                        },
                        {
                            'key': 'State',
                            'value': 'Triggered'
                        },
                        {
                            'key': 'Triggered By',
                            'value': 'jiyoon@mz.co.kr'
                        },
                        {
                            'key': 'Project',
                            'value': 'SpaceONE Dev > Belkin Snow'
                        }
                    ],
                },

            'notification_type': 'ERROR',
            'secret_data': self.secret_data,
            'channel_data': self.channel_data
        })
