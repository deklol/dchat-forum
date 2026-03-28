from django.contrib.auth.views import PasswordResetView
from django.urls import path

from apps.accounts.views import (
    CaptchaLoginView,
    CaptchaLogoutView,
    DeleteAccountView,
    NotificationsView,
    ProfileDetailView,
    ProfileEditView,
    SignUpView,
    export_personal_data,
    mention_candidates,
    mark_notification_read,
    shell_state,
    user_card_partial,
)

app_name = "accounts"

urlpatterns = [
    path("login/", CaptchaLoginView.as_view(), name="login"),
    path("logout/", CaptchaLogoutView.as_view(), name="logout"),
    path("register/", SignUpView.as_view(), name="register"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("notifications/", NotificationsView.as_view(), name="notifications"),
    path("notifications/<int:notification_id>/read/", mark_notification_read, name="notification_read"),
    path("shell-state/", shell_state, name="shell_state"),
    path("mentions/", mention_candidates, name="mentions"),
    path("privacy/export/", export_personal_data, name="privacy_export"),
    path("privacy/delete/", DeleteAccountView.as_view(), name="privacy_delete"),
    path("u/<slug:username>/", ProfileDetailView.as_view(), name="profile"),
    path("u/<slug:username>/card/", user_card_partial, name="profile_card"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
]
