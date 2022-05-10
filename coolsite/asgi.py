import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import messenger.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coolsite.settings')

import django
django.setup()

application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(messenger.routing.websocket_urlpatterns)

    )
})