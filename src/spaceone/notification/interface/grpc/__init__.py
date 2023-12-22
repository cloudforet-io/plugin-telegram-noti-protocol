from spaceone.core.pygrpc.server import GRPCServer
from .notification import Notification
from .protocol import Protocol

_all_ = ["app"]

app = GRPCServer()
app.add_service(Notification)
app.add_service(Protocol)
