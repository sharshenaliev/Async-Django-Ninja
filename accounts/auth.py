from django.conf import settings
from ninja.security import HttpBearer
from ninja.errors import AuthenticationError
import jwt
from accounts.models import RefreshToken
from accounts.utils import create_refresh_token


class RefreshTokenObtain(HttpBearer):
    async def authenticate(self, request, token):
        try:
            token = await RefreshToken.objects.aget(token=token)
            refresh_token = await create_refresh_token(token.user_id)
        except:
            raise AuthenticationError()
        return refresh_token.token


class RefreshTokenDelete(HttpBearer):
    async def authenticate(self, request, token):
        try:
            refresh_token = await RefreshToken.objects.aget(token=token)
            refresh_token.adelete()
        except:
            raise AuthenticationError()
        return refresh_token.token


class AuthBearer(HttpBearer):
    async def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            user_id = payload['user_id']
        except:
            raise AuthenticationError()
        return user_id
