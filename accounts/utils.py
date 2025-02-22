from django.conf import settings
from datetime import datetime, timezone, timedelta
import jwt
from accounts.models import RefreshToken


async def create_access_token(user_id):
    access_token_payload = {
        "user_id": user_id,
        "iat": datetime.now(tz=timezone.utc),
        "exp": datetime.utcnow() + timedelta(hours=12),
    }
    return jwt.encode(access_token_payload, settings.JWT_SECRET_KEY)


async def create_refresh_token(user_id):
    refresh_token, created = await RefreshToken.objects.aget_or_create(user_id=user_id)
    if not created:
        refresh_token.expires_at = datetime.now() + timedelta(days=1)
        refresh_token.is_active = True
        await refresh_token.asave()
    return refresh_token
