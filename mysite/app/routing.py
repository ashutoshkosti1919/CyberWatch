from django.conf.urls import url
from django.urls import path
from . import views
from http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from app import consumers
from . import consumers
from . import ddos


application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/", consumers.MyConsumer.as_asgi()),
    ])
})
websocket_urlpatterns = [
    url(r'^ws/api/', consumers.TestConsumer, name='api_ws'),
]

http_urlpatterns = [
    url(r'^api/status/', consumers.ServiceStatus, name='api_status_http'),
    url(r'^api/', consumers.LongPollConsumer, name='api_http'),
    url(r"", AsgiHandler),
]