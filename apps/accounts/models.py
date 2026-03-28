from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)
    website_url = models.URLField(blank=True)
    social_x = models.URLField(blank=True)
    social_discord = models.CharField(max_length=80, blank=True)
    email_digest_enabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username
