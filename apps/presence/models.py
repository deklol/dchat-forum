from django.conf import settings
from django.db import models


class UserPresence(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="presence")
    last_seen_at = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user.username} online={self.is_online}"

    class Meta:
        indexes = [
            models.Index(fields=["is_online", "last_seen_at"]),
        ]
