from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.models import AnonymousUser

User = get_user_model()

@database_sync_to_async
def get_user(token_key):
    try:
        access_token = AccessToken(token_key)
        user = User.objects.get(id=access_token['id'])
        print(user)
        return user
    except Exception as e:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        # print(token)
        scope["user"] = await get_user(token) if token else AnonymousUser()
        return await super().__call__(scope, receive, send)
