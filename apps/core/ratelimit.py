from __future__ import annotations

import time
from functools import wraps

from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, JsonResponse


def _client_ip(request: HttpRequest) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _hit(key: str, window_seconds: int) -> int:
    now = int(time.time())
    bucket = now // window_seconds
    cache_key = f"rl:{key}:{bucket}"
    count = cache.get(cache_key)
    if count is None:
        cache.set(cache_key, 1, timeout=window_seconds + 2)
        return 1
    count = int(count) + 1
    cache.set(cache_key, count, timeout=window_seconds + 2)
    return count


def rate_limit(
    *,
    key_prefix: str,
    max_ip_hits: int,
    max_user_hits: int,
    window_seconds: int = 60,
) -> callable:
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            ip = _client_ip(request)
            ip_count = _hit(f"{key_prefix}:ip:{ip}", window_seconds)
            if ip_count > max_ip_hits:
                if request.headers.get("Accept", "").find("application/json") >= 0:
                    return JsonResponse({"ok": False, "error": "rate_limited"}, status=429)
                return HttpResponse("Rate limit exceeded. Try again later.", status=429)

            if request.user.is_authenticated:
                user_count = _hit(f"{key_prefix}:user:{request.user.id}", window_seconds)
                if user_count > max_user_hits:
                    if request.headers.get("Accept", "").find("application/json") >= 0:
                        return JsonResponse({"ok": False, "error": "rate_limited"}, status=429)
                    return HttpResponse("Rate limit exceeded. Try again later.", status=429)
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
