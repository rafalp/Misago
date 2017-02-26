from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.subscriptions import make_subscription_aware
from misago.users.models import AnonymousUser


UserModel = get_user_model()


class SubscriptionsTests(TestCase):
    def setUp(self):
        self.category = list(Category.objects.all_categories()[:1])[0]
        self.thread = self.post_thread(timezone.now() - timedelta(days=10))

        self.user = UserModel.objects.create_user("Bob", "bob@test.com", "Pass.123")
        self.anon = AnonymousUser()

    def post_thread(self, datetime):
        return testutils.post_thread(
            category=self.category,
            started_on=datetime,
        )

    def test_anon_subscription(self):
        """make single thread sub aware for anon"""
        make_subscription_aware(self.anon, self.thread)
        self.assertIsNone(self.thread.subscription)

    def test_anon_threads_subscription(self):
        """make multiple threads list sub aware for anon"""
        threads = []
        for _ in range(10):
            threads.append(self.post_thread(timezone.now() - timedelta(days=10)))

        make_subscription_aware(self.anon, threads)

        for thread in threads:
            self.assertIsNone(thread.subscription)

    def test_no_subscription(self):
        """make thread sub aware for authenticated"""
        make_subscription_aware(self.user, self.thread)
        self.assertIsNone(self.thread.subscription)

    def test_subscribed_thread(self):
        """make thread sub aware for authenticated"""
        self.user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=True,
        )

        make_subscription_aware(self.user, self.thread)
        self.assertTrue(self.thread.subscription.send_email)

    def test_threads_no_subscription(self):
        """make mulitple threads sub aware for authenticated"""
        threads = []
        for i in range(10):
            threads.append(self.post_thread(timezone.now() - timedelta(days=10)))

            if i % 3 == 0:
                self.user.subscription_set.create(
                    thread=threads[-1],
                    category=self.category,
                    last_read_on=timezone.now(),
                    send_email=False,
                )
            elif i % 2 == 0:
                self.user.subscription_set.create(
                    thread=threads[-1],
                    category=self.category,
                    last_read_on=timezone.now(),
                    send_email=True,
                )

        make_subscription_aware(self.user, threads)

        for i in range(10):
            if i % 3 == 0:
                self.assertFalse(threads[i].subscription.send_email)
            elif i % 2 == 0:
                self.assertTrue(threads[i].subscription.send_email)
            else:
                self.assertIsNone(threads[i].subscription)
