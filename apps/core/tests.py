from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.core.legal_defaults import PRIMARY_CONTACT_EMAIL_PLACEHOLDER
from apps.core.models import LegalDocument, SetupState

User = get_user_model()


class SetupFlowTests(TestCase):
    def test_redirect_to_setup_when_no_users(self):
        client = Client()
        response = client.get(reverse("forum:home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/setup/", response.url)

    def test_setup_creates_first_admin(self):
        client = Client()
        response = client.post(
            reverse("setup"),
            data={
                "site_name": "dChat",
                "theme_preset": "default",
                "accent_hex": "#f39c12",
                "bg_hex": "#0f1217",
                "surface_hex": "#1a1f29",
                "text_hex": "#e5e7eb",
                "muted_text_hex": "#9ca3af",
                "link_hex": "#7cc4ff",
                "admin_username": "admin",
                "admin_email": "admin@example.com",
                "admin_password": "SuperStrongPass123!",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="admin", is_superuser=True).exists())
        self.assertTrue(SetupState.objects.exists())
        self.assertTrue(LegalDocument.objects.filter(doc_type="terms", version="v2").exists())
        self.assertTrue(LegalDocument.objects.filter(doc_type="privacy", version="v2").exists())
        self.assertTrue(LegalDocument.objects.filter(doc_type="cookies", version="v2").exists())
        self.assertIn("dChat", LegalDocument.objects.get(doc_type="terms").body_markdown)
        self.assertIn(PRIMARY_CONTACT_EMAIL_PLACEHOLDER, LegalDocument.objects.get(doc_type="privacy").body_markdown)
        legal_page = client.get(reverse("legal_doc", kwargs={"doc_type": "privacy"}))
        self.assertContains(legal_page, "admin@example.com")
