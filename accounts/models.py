from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from uuid import uuid4


class RefreshToken(models.Model):
    token = models.UUIDField(default=uuid4, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name="User")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        default=datetime.now() + timedelta(days=1)
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.token)

    def save(self, *args, **kwargs):
        self.token = uuid4()
        super(RefreshToken, self).save(*args, **kwargs)
