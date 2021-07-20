__all__ = ['PluginInfo']

from spaceone.api.notification.plugin import protocol_pb2
from spaceone.core.pygrpc.message_type import *


def PluginInfo(result):
    result['metadata'] = change_struct_type(result['metadata'])
    return protocol_pb2.PluginInfo(**result)

