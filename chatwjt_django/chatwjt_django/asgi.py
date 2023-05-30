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
