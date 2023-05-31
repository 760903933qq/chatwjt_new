import os
from django.core.asgi import get_asgi_application
from app.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatwjt_django.settings")
os.environ.setdefault("OPEN_AI_KEY", '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')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
})
