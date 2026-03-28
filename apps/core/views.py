import json
import time
from django.contrib.auth import get_user_model, login
from urllib.parse import unquote, urlparse

from django.http import Http404, HttpRequest, HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import FormView, TemplateView
from django.conf import settings
from pathlib import Path
from django.db import connection
from django.core.cache import cache

from apps.core.forms import FirstRunSetupForm
from apps.core.models import ChangeLogEntry, LegalDocument, SetupState, UserLegalConsent
from apps.core.legal_defaults import PRIMARY_CONTACT_EMAIL_PLACEHOLDER
from apps.presence.models import UserPresence

User = get_user_model()
STARTED_AT = int(time.time())


def operator_contact_email() -> str:
    primary_admin = User.objects.filter(pk=1).only("email").first()
    if primary_admin and primary_admin.email:
        return primary_admin.email
    setup_user = SetupState.objects.select_related("completed_by").order_by("id").first()
    if setup_user and setup_user.completed_by and setup_user.completed_by.email:
        return setup_user.completed_by.email
    admin = User.objects.filter(is_superuser=True).order_by("id").first()
    if admin and admin.email:
        return admin.email
    return ""


def render_legal_body(body_markdown: str, contact_email: str) -> str:
    body = body_markdown or ""
    replacement = contact_email or "replace-with-operator-contact@example.com"
    return body.replace(PRIMARY_CONTACT_EMAIL_PLACEHOLDER, replacement)


class FirstRunSetupView(FormView):
    template_name = "setup.html"
    form_class = FirstRunSetupForm

    def dispatch(self, request, *args, **kwargs):
        if User.objects.exists():
            return redirect("forum:home")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial.setdefault("site_name", "dChat")
        initial.setdefault("theme_preset", "default")
        initial.setdefault("accent_hex", "#f39c12")
        initial.setdefault("bg_hex", "#0f1217")
        initial.setdefault("surface_hex", "#1a1f29")
        initial.setdefault("text_hex", "#e5e7eb")
        initial.setdefault("muted_text_hex", "#9ca3af")
        initial.setdefault("link_hex", "#7cc4ff")
        return initial

    def form_valid(self, form):
        admin_user = form.save()
        SetupState.objects.create(completed_by=admin_user)
        login(self.request, admin_user)
        return redirect("forum:home")


class LegalPageView(TemplateView):
    template_name = "legal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_type = self.kwargs["doc_type"]
        context["document"] = get_object_or_404(LegalDocument, doc_type=doc_type)
        context["legal_contact_email"] = operator_contact_email()
        context["rendered_body_markdown"] = render_legal_body(
            context["document"].body_markdown,
            context["legal_contact_email"],
        )
        return context


class ChangelogView(TemplateView):
    template_name = "changelog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = ChangeLogEntry.objects.all()
        return context


class DocsPageView(TemplateView):
    template_name = "docs_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        file_map = {
            "readme": "README.md",
            "install": "INSTALL.md",
            "faq": "FAQ.md",
            "changelog-file": "CHANGELOG.md",
            "dekcx-theme-notes": "docs/DEKCX_THEME_NOTES.md",
        }
        filename = file_map.get(slug)
        if not filename:
            raise Http404("Document not found")
        path = Path(settings.BASE_DIR) / filename
        if not path.exists():
            raise Http404("Document not found")
        context["doc_title"] = filename
        context["doc_slug"] = slug
        context["doc_body"] = path.read_text(encoding="utf-8")
        context["legal_contact_email"] = operator_contact_email()
        return context


@require_POST
def accept_cookie_consent(request: HttpRequest) -> HttpResponse:
    next_url = (request.POST.get("next") or "").strip()
    if not url_has_allowed_host_and_scheme(next_url, {request.get_host()}, require_https=request.is_secure()):
        next_url = "forum:home"
    response = redirect(next_url)
    response.set_cookie("cookie_consent", "accepted", max_age=60 * 60 * 24 * 365, samesite="Lax")
    if request.user.is_authenticated:
        terms = LegalDocument.objects.filter(doc_type="terms").first()
        privacy = LegalDocument.objects.filter(doc_type="privacy").first()
        cookies = LegalDocument.objects.filter(doc_type="cookies").first()
        UserLegalConsent.objects.get_or_create(
            user=request.user,
            terms_version=terms.version if terms else "",
            privacy_version=privacy.version if privacy else "",
            cookies_version=cookies.version if cookies else "",
        )
    return response


def footer_fragment(request: HttpRequest) -> HttpResponse:
    return render(request, "components/footer.html")


def health_live(_request: HttpRequest) -> HttpResponse:
    return HttpResponse("ok", content_type="text/plain")


def health_ready(_request: HttpRequest) -> HttpResponse:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            _ = cursor.fetchone()
        cache.set("health:ready", "ok", timeout=5)
        return HttpResponse("ready", content_type="text/plain")
    except Exception:
        return HttpResponse("not-ready", status=503, content_type="text/plain")


def metrics(_request: HttpRequest) -> HttpResponse:
    total = int(cache.get("metrics:requests:total", 0) or 0)
    status_2xx = int(cache.get("metrics:requests:status:200", 0) or 0)
    status_4xx = int(cache.get("metrics:requests:status:404", 0) or 0) + int(
        cache.get("metrics:requests:status:403", 0) or 0
    )
    status_5xx = int(cache.get("metrics:requests:status:500", 0) or 0)
    last_ms = int(cache.get("metrics:last_request_ms", 0) or 0)
    uptime = int(time.time()) - STARTED_AT
    payload = "\n".join(
        [
            "# TYPE dchat_requests_total counter",
            f"dchat_requests_total {total}",
            "# TYPE dchat_requests_2xx counter",
            f"dchat_requests_2xx {status_2xx}",
            "# TYPE dchat_requests_4xx counter",
            f"dchat_requests_4xx {status_4xx}",
            "# TYPE dchat_requests_5xx counter",
            f"dchat_requests_5xx {status_5xx}",
            "# TYPE dchat_last_request_ms gauge",
            f"dchat_last_request_ms {last_ms}",
            "# TYPE dchat_uptime_seconds gauge",
            f"dchat_uptime_seconds {uptime}",
            "",
        ]
    )
    return HttpResponse(payload, content_type="text/plain; version=0.0.4")


def outbound_link_warning(request: HttpRequest) -> HttpResponse:
    encoded = request.GET.get("u", "").strip()
    target = unquote(encoded)
    parsed = urlparse(target)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise Http404("Invalid outbound link")

    if request.method == "POST":
        return redirect(target)

    return render(
        request,
        "outbound_link_warning.html",
        {
            "target_url": target,
            "target_host": parsed.netloc,
        },
    )


def presence_events(_request: HttpRequest) -> HttpResponse:
    def event_stream():
        online_count = UserPresence.objects.filter(is_online=True).count()
        payload = json.dumps({"online_count": online_count, "ts": int(time.time())})
        yield f"event: presence\ndata: {payload}\n\n"

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
