from django.core.cache import cache
from django.db.models import Q

from apps.dm.models import DirectConversation, DirectMessage


def dm_context_cache_key(user_id: int) -> str:
    return f"dm_ctx_{user_id}"


def invalidate_dm_context(*user_ids: int) -> None:
    for user_id in {user_id for user_id in user_ids if user_id}:
        cache.delete(dm_context_cache_key(user_id))


def get_dm_context_payload(user) -> dict:
    if not getattr(user, "is_authenticated", False):
        return {"unread_dm_count": 0, "has_dm_access": False, "guild_dm_users": []}
    cache_key = dm_context_cache_key(user.id)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    unread_count = DirectMessage.objects.filter(recipient=user, is_read=False).count()
    recent_conversations = list(
        DirectConversation.objects.filter(
            Q(user_low=user) | Q(user_high=user)
        )
        .select_related("user_low", "user_high")
        .order_by("-updated_at")[:4]
    )
    has_dm_access = bool(recent_conversations)
    guild_dm_users = []
    for conversation in recent_conversations:
        other_user = conversation.other_for(user)
        guild_dm_users.append(
            {
                "username": other_user.username,
                "avatar_url": other_user.avatar.url if other_user.avatar else "",
                "initial": other_user.username[:1].upper(),
            }
        )
    if not has_dm_access:
        has_dm_access = DirectConversation.objects.filter(
        Q(user_low=user) | Q(user_high=user)
        ).exists()
    payload = {
        "unread_dm_count": unread_count,
        "has_dm_access": has_dm_access,
        "guild_dm_users": guild_dm_users,
    }
    cache.set(cache_key, payload, timeout=60)
    return payload


def dm_context(request):
    return get_dm_context_payload(getattr(request, "user", None))
