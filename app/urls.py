from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.views import (
    ChangelogView,
    DocsPageView,
    FirstRunSetupView,
    LegalPageView,
    accept_cookie_consent,
    footer_fragment,
    health_live,
    health_ready,
    metrics,
    outbound_link_warning,
    presence_events,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("setup/", FirstRunSetupView.as_view(), name="setup"),
    path("changelog/", ChangelogView.as_view(), name="changelog"),
    path("health/live/", health_live, name="health_live"),
    path("health/ready/", health_ready, name="health_ready"),
    path("metrics/", metrics, name="metrics"),
    path("out/", outbound_link_warning, name="outbound_link_warning"),
    path("events/presence/", presence_events, name="presence_events"),
    path("docs/<slug:slug>/", DocsPageView.as_view(), name="docs_page"),
    path("legal/<slug:doc_type>/", LegalPageView.as_view(), name="legal_doc"),
    path("legal/cookies/accept/", accept_cookie_consent, name="accept_cookie_consent"),
    path("footer-fragment/", footer_fragment, name="footer_fragment"),
    path("accounts/", include("apps.accounts.urls")),
    path("dm/", include("apps.dm.urls")),
    path("", include("apps.forum.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
