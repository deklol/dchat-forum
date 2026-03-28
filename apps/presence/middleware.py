from datetime import timedelta

from django.utils import timezone

from apps.presence.models import UserPresence


class PresenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            now = timezone.now()
            stale_before = now - timedelta(minutes=5)
            last_seen = getattr(request.user, "presence", None)
            if not last_seen or (now - last_seen.last_seen_at) > timedelta(seconds=45):
                UserPresence.objects.update_or_create(
                    user=request.user,
                    defaults={"last_seen_at": now, "is_online": True},
                )
            UserPresence.objects.filter(last_seen_at__lt=stale_before, is_online=True).update(is_online=False)
        return response
