import logging
import os
import telegram
from telegram.ext import Updater

from spaceone.core import utils
from spaceone.tester import TestCase, print_json

_LOGGER = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN", None)
CHAT_ID = os.environ.get("CHAT_ID", None)

if TOKEN is None or CHAT_ID is None:
    print(
        """
##################################################
# ERROR
#
# Configure your Telegram Token first for test
##################################################
example)

export TELEGRAM_TOKEN=<YOUR_TELEGRAM_TOKEN>

"""
    )
    exit


class TestTelegramNotification(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    endpoints = config.get("ENDPOINTS", {})
    secret_data = {}
    channel_data = {"token": TOKEN, "chat_id": CHAT_ID}

    def test_init(self):
        v_info = self.notification.Protocol.init({"options": {}})
        print_json(v_info)

    def test_verify(self):
        options = {}
        self.notification.Protocol.verify(
            {"options": options, "secret_data": self.secret_data}
        )

    def test_dispatch(self):
        options = {}

        self.notification.Notification.dispatch(
            {
                "options": options,
                "message": {
                    "title": "",
                    "description": "Threshold Crossed: 3 out of the last 5 datapoints [] were less than the threshold.",
                    "link": "www.spaceone.org",
                    "callbacks": [
                        {
                            "label": "label1",
                            "url": "https://github.com/spaceone-dev",
                            "options": {},
                        },
                        {
                            "label": "label2",
                            "url": "https://github.com/spaceone-dev",
                            "options": {},
                        },
                    ],
                    "image_url": "http://i.imgur.com/pFo28MB.gif",
                    "tags": [
                        {"key": "Alert Number", "value": "#130900"},
                        {"key": "State", "value": "Triggered"},
                        {"key": "Triggered By", "value": "jiyoon@mz.co.kr"},
                        {"key": "Project", "value": "SpaceONE Dev > Belkin Snow"},
                    ],
                },
                "notification_type": "ERROR",
                "secret_data": self.secret_data,
                "channel_data": self.channel_data,
            }
        )
