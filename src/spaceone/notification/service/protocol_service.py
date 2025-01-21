import logging
from spaceone.core.service import *

_LOGGER = logging.getLogger(__name__)


class ProtocolService(BaseService):
    resource = 'Protocol'

    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        return {'metadata': {
            'data_type': 'SECRET',
            'data': {
                'schema': {
                    'properties': {
                        'chat_id': {
                            'description': 'Chat ID of the group to receive messages in your chats. The Chat ID will most likely be a negative number in the form of -#########.',
                            'minLength': 1,
                            'title': 'Chat ID',
                            'type': 'string',
                            'examples': ['-514081686']
                        },
                        'token': {
                            'description': 'HTTP API token which is your BOT API Token to be used in SpaceONE Alert.',
                            'minLength': 1,
                            'title': 'BOT API Token',
                            'type': 'string',
                            'examples': ['XXXXXXXXX: YYYYYYYYYYYYYYYYYYYYYYYYYYYYY']
                        }
                    },
                    'required': [
                        'chat_id',
                        'token'
                    ],
                    'type': 'object'
                }
            }
        }
        }

    @transaction
    @check_required(['options'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})

        return {}
