from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.core.context_processors import invalidate_notification_count
from apps.dm.context_processors import invalidate_dm_context
from apps.dm.models import DirectConversation, DirectMessage
from apps.forum.models import Category, Notification, Post, ReputationGrant, Thread

User = get_user_model()


@override_settings(CAPTCHA_ENABLED=False)
class AuthFlowTests(TestCase):
    def test_register_and_login(self):
        User.objects.create_superuser(username="admin", email="admin@example.com", password="AdminPass123!")
        resp = self.client.post(
            reverse("accounts:register"),
            data={
                "username": "tester",
                "email": "tester@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "accept_terms": "on",
                "accept_privacy": "on",
            },
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(User.objects.filter(username="tester").exists())

        login_resp = self.client.post(
            reverse("accounts:login"),
            data={"username": "tester", "password": "StrongPass123!"},
            follow=True,
        )
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("_auth_user_id", self.client.session)

    def test_user_card_shows_forum_stats_and_recent_activity(self):
        viewer = User.objects.create_user(username="viewer", email="viewer@example.com", password="StrongPass123!")
        target = User.objects.create_user(username="target", email="target@example.com", password="StrongPass123!")
        self.client.login(username="viewer", password="StrongPass123!")
        category = Category.objects.create(name="General", slug="general")
        thread = Thread.objects.create(category=category, author=target, title="Recent topic", body_markdown="hello")
        post = Post.objects.create(thread=thread, author=target, body_markdown="Recent useful reply")
        ReputationGrant.objects.create(actor=viewer, recipient=target, post=post)

        response = self.client.get(reverse("accounts:profile_card", kwargs={"username": target.username}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Forum Stats")
        self.assertContains(response, "Recent Topics")
        self.assertContains(response, "Recent Replies")
        self.assertContains(response, "Recent topic")

    def test_shell_state_returns_live_inbox_counts(self):
        owner = User.objects.create_user(username="owner", email="owner@example.com", password="StrongPass123!")
        sender = User.objects.create_user(username="sender", email="sender@example.com", password="StrongPass123!")
        conversation = DirectConversation.for_users(owner, sender)
        direct_message = DirectMessage.objects.create(conversation=conversation, sender=sender, recipient=owner)
        direct_message.set_body("ping")
        direct_message.save(update_fields=["body_encrypted"])
        Notification.objects.create(
            recipient=owner,
            actor=sender,
            kind="mention",
            body="sender mentioned you",
        )
        invalidate_dm_context(owner.id)
        invalidate_notification_count(owner.id)

        self.client.login(username="owner", password="StrongPass123!")
        response = self.client.get(reverse("accounts:shell_state"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "unread_dm_count": 1,
                "unread_notifications_count": 1,
                "inbox_total": 2,
                "has_dm_access": True,
            },
        )
