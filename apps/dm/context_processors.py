from django.core.cache import cache
from django.db.models import Q

from apps.dm.models import DirectConversation, DirectMessage


def dm_context(request):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {"unread_dm_count": 0, "has_dm_access": False}
    cache_key = f"dm_ctx_{request.user.id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    unread_count = DirectMessage.objects.filter(recipient=request.user, is_read=False).count()
    has_dm_access = DirectConversation.objects.filter(
        Q(user_low=request.user) | Q(user_high=request.user)
    ).exists()
    payload = {"unread_dm_count": unread_count, "has_dm_access": has_dm_access}
    cache.set(cache_key, payload, timeout=60)
    return payload
