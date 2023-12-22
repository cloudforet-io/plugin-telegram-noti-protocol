import html
import logging
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
    @check_required(["options", "message", "notification_type"])
    def dispatch(self, params):
        """
        Args:
            params:
                - options
                - message :
                - notification_type : INFO || ERROR || SUCCESS || WARNING
                - secret_data
        """
        channel_data = params.get("channel_data", {})
        notification_type = params["notification_type"]
        message = params["message"]
        options = params.get("options")

        telegram_token = channel_data.get("token")  # bot token
        chat_id = channel_data.get("chat_id")

        kwargs = {}

        # Get Message
        final_message = self._make_telegram_message_attachment(
            message, notification_type
        )

        # Check if callback exists
        if "callback" in message:
            kwargs["callbacks"] = message["callbacks"]

        # Check if image_url exists
        if "image_url" in message:
            kwargs["image_url"] = message["image_url"]

        noti_mgr: NotificationManager = self.locator.get_manager("NotificationManager")
        noti_mgr.dispatch(
            token=telegram_token, chat_id=chat_id, message=final_message, **kwargs
        )

    def _make_telegram_message_attachment(self, message, notification_type):
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
        link = message.get("link")
        title = self._handle_escape_characters(message.get("title"))
        print("HERE?")
        print(title)
        description = self._handle_escape_characters(message.get("description"))
        tags = message.get("tags", [])

        message_attachments = []

        if link:
            if title:
                message.update(
                    {
                        "title": "\n"
                        + "<b>"
                        + f"[{notification_type}]"
                        + "</b> "
                        + '<a href="'
                        + link
                        + '"'
                        + ">"
                        + f"{title}"
                        + "</a>"
                    }
                )
                message_attachments.append(message["title"])
        else:
            message.update(
                {
                    "title": "\n"
                    + "<b>"
                    + f"[{notification_type}]"
                    + "</b> "
                    + f"{title}"
                }
            )
            message_attachments.append(message["title"])

        if description:
            message_attachments.append("\n" + description + "\n")

        if tags:
            tag_attachments = ""
            for tag in tags:
                tag_key = self._handle_escape_characters(tag["key"])
                tag_value = self._handle_escape_characters(tag["value"])
                # update key
                key_str = "\n" + "<b>" + "- " + tag_key + "</b>"
                value_str = "<pre>" + tag_value + "</pre>"

                # update tag
                tag_str = key_str + ": " + value_str
                tag_attachments += tag_str + " "

            message_attachments.append(tag_attachments)

        message_final = " ".join(message_attachments)

        return message_final[:MAX_MESSAGE_LENGTH]

    @staticmethod
    def _handle_escape_characters(message_string):
        return html.escape(message_string)
