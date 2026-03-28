import time

from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import resolve

User = get_user_model()


class FirstRunSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        path = request.path
        route_name = ""
        try:
            route_name = resolve(path).url_name or ""
        except Exception:
            route_name = ""

        setup_done = User.objects.exists()
        allowed = path.startswith("/setup") or path.startswith("/static/") or path.startswith("/media/")
        if not setup_done and not allowed and route_name != "setup":
            return redirect("setup")
        return self.get_response(request)


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        response["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self' https://challenges.cloudflare.com https://platform.twitter.com; "
            "frame-src https://www.youtube.com https://player.twitch.tv https://platform.twitter.com; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


class RequestMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        started = time.time()
        response = self.get_response(request)
        duration_ms = int((time.time() - started) * 1000)
        self._safe_incr("metrics:requests:total")
        status_bucket = f"metrics:requests:status:{response.status_code}"
        self._safe_incr(status_bucket)
        cache.set("metrics:last_request_ms", duration_ms, timeout=86400)
        return response

    @staticmethod
    def _safe_incr(key: str) -> None:
        try:
            cache.incr(key)
        except Exception:
            value = cache.get(key, 0)
            cache.set(key, int(value) + 1, timeout=86400)
