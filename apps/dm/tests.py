from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.dm.models import DirectConversation, DirectMessage

User = get_user_model()


class DirectMessageTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", email="alice@example.com", password="Password123!")
        self.bob = User.objects.create_user(username="bob", email="bob@example.com", password="Password123!")
        self.client.login(username="alice", password="Password123!")

    def test_start_dm_and_send(self):
        resp = self.client.post(
            reverse("dm:start"),
            data={"username": "bob", "body": "hello bob"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        convo = DirectConversation.for_users(self.alice, self.bob)
        self.assertTrue(DirectMessage.objects.filter(conversation=convo, sender=self.alice, recipient=self.bob).exists())

    def test_quick_dm_send(self):
        resp = self.client.post(
            reverse("dm:quick_send", kwargs={"username": "bob"}),
            data={"body": "quick ping"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            DirectMessage.objects.filter(conversation__user_low=self.alice, conversation__user_high=self.bob).exists()
        )
