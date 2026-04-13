import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import urbanx.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urbanx.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            urbanx.routing.websocket_urlpatterns
        )
    ),
})
