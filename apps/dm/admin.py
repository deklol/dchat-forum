from django.contrib import admin

from apps.dm.models import DirectConversation, DirectMessage, DirectMessagePreference


@admin.register(DirectConversation)
class DirectConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "user_low", "user_high", "updated_at")
    search_fields = ("user_low__username", "user_high__username")


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "recipient", "is_read", "is_reported", "created_at")
    list_filter = ("is_read", "is_reported")
    search_fields = ("sender__username", "recipient__username", "report_reason")


@admin.register(DirectMessagePreference)
class DirectMessagePreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "allow_incoming", "updated_at")
    list_filter = ("allow_incoming",)
    search_fields = ("user__username",)
