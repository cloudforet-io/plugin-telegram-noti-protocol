import logging
import os
import telegram
from telegram.ext import Updater

from spaceone.core import utils
from spaceone.tester import TestCase, print_json

_LOGGER = logging.getLogger(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN', None)
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
updates = bot.get_updates()
print(updates[1])
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a jiyoon bot, plz talk to me!")

chat_id = updates[0]
bot.send_message(text='Hi Elyor!! OMG SpaceONE ', chat_id=chat_id)
if TOKEN == None:
    print("""
##################################################
# ERROR
#
# Configure your Slack Token first for test
##################################################
example)

export SLACK_TOKEN=<YOUR_SLACK_TOKEN>

""")
    exit


class TestSlackNotification(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get('SPACEONE_TEST_CONFIG_FILE', './config.yml'))
    endpoints = config.get('ENDPOINTS', {})
    secret_data = {
        'token': TOKEN,
        'channel': 'everyone',
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
            'message': {'message': 'SAL LYO JU SE YO'},
            'notification_type': 'INFO',
            'secret_data': self.secret_data
        })
