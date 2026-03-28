from django.conf import settings
from django.core.cache import cache

from apps.accounts.models import User
from apps.core.models import ChangeLogEntry, FooterLink, SiteBranding
from apps.forum.models import Notification


def branding_context(_request):
    branding = SiteBranding.objects.order_by("id").first()
    return {"branding": branding}


def footer_context(_request):
    cached = cache.get("footer_context_v1")
    if cached:
        return cached
    links = list(FooterLink.objects.filter(enabled=True))
    online = list(User.objects.filter(
        presence__is_online=True,
        presence__last_seen_at__isnull=False,
    ).order_by("username")[:20])
    newest = User.objects.order_by("-date_joined").first()
    recent = list(User.objects.exclude(last_login__isnull=True).order_by("-last_login")[:20])
    latest_version = ChangeLogEntry.objects.order_by("-released_at").values_list("version", flat=True).first() or "0.1"
    payload = {
        "footer_links": links,
        "online_users": online,
        "newest_user": newest,
        "recent_logged_in_users": recent,
        "app_version": latest_version,
    }
    cache.set("footer_context_v1", payload, timeout=60)
    return payload


def settings_context(_request):
    return {
        "CAPTCHA_ENABLED": settings.CAPTCHA_ENABLED,
        "CAPTCHA_PROVIDER": settings.CAPTCHA_PROVIDER,
    }


def notifications_context(request):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {"unread_notifications_count": 0}
    cache_key = f"notif_count_{request.user.id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return {"unread_notifications_count": cached}
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    cache.set(cache_key, count, timeout=60)
    return {"unread_notifications_count": count}
