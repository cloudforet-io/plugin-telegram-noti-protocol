from spaceone.api.notification.plugin import notification_pb2_grpc, notification_pb2
from spaceone.core.pygrpc import BaseAPI
from spaceone.core.pygrpc.message_type import *
from spaceone.notification.service import NotificationService


class Notification(BaseAPI, notification_pb2_grpc.NotificationServicer):
    pb2 = notification_pb2
    pb2_grpc = notification_pb2_grpc

    def dispatch(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('NotificationService', metadata) as notification_svc:
            notification_svc.dispatch(params)
            return self.locator.get_info('EmptyInfo')
