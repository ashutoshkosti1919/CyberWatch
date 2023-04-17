from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
import app.routing
from app.ddos import GenerateConsumer
from app import consumers
from django.conf.urls import url
from django.urls import path
from django.urls import re_path
from . import consumers
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from app import consumers 
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from consumers import RFIDConsumer


application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
   "websocket": URLRouter([
        path("ws/", consumers.MyConsumer.as_asgi()),
    ]),
    'http': 
    # AuthMiddlewareStack(
        URLRouter(
            app.routing.http_urlpatterns
        # )
    ),
    # 'http' : app,
    "channel": ChannelNameRouter({
        "alert-generate": GenerateConsumer,
        # "test_worker": app.consumers.TestWorker,
        # "thunbnails-delete": consumers.DeleteConsumer,
    }),
})


websocket_urlpatterns = [
    path('ws/rfid/', RFIDConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

