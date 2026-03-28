from django.contrib import admin

from apps.presence.models import UserPresence


@admin.register(UserPresence)
class UserPresenceAdmin(admin.ModelAdmin):
    list_display = ("user", "is_online", "last_seen_at")
    list_filter = ("is_online",)
