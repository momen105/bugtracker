# asgi.py

import os

# ✅ প্রথমে settings module define করুন
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bugtracker.settings')

# ✅ তারপর django setup করুন
import django
django.setup()

# ✅ তারপর বাকিগুলো import করুন
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from bugtracker.jwt_middleware import JWTAuthMiddleware  # Custom middleware
from apps.tracker.routing import websocket_urlpatterns    # Your websocket routes

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
