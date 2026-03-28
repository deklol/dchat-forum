from django.urls import path

from apps.dm.views import dm_conversation, dm_inbox, dm_settings, quick_dm_send, report_dm_message, reported_dm_queue, start_dm

app_name = "dm"

urlpatterns = [
    path("", dm_inbox, name="inbox"),
    path("start/", start_dm, name="start"),
    path("settings/", dm_settings, name="settings"),
    path("u/<slug:username>/", dm_conversation, name="conversation"),
    path("u/<slug:username>/quick-send/", quick_dm_send, name="quick_send"),
    path("messages/<int:message_id>/report/", report_dm_message, name="report_message"),
    path("reported/", reported_dm_queue, name="reported_queue"),
]
