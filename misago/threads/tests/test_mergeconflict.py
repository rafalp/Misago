from django.test import TestCase
from rest_framework.exceptions import ValidationError

from .. import test
from ...categories.models import Category
from ...users.test import create_test_user
from ..mergeconflict import MergeConflict


class MergeConflictTests(TestCase):
    def setUp(self):
        self.category = Category.objects.get(slug="first-category")
        self.user = create_test_user("User", "user@example.com")

    def create_plain_thread(self):
        return test.post_thread(self.category)

    def create_poll_thread(self):
        thread = test.post_thread(self.category)
        test.post_poll(thread, self.user)
        return thread

    def create_best_answer_thread(self):
        thread = test.post_thread(self.category)
        best_answer = test.reply_thread(thread)
        thread.set_best_answer(self.user, best_answer)
        thread.synchronize()
        thread.save()
        return thread

    def test_plain_threads_no_conflicts(self):
        """threads without items of interest don't conflict"""
        threads = [self.create_plain_thread() for i in range(10)]
        merge_conflict = MergeConflict(threads=threads)
        self.assertFalse(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_conflicting_fields(), [])

        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(merge_conflict.get_resolution(), {})

    def test_one_best_answer_one_plain(self):
        """thread with best answer and plain thread don't conflict"""
        threads = [self.create_best_answer_thread(), self.create_plain_thread()]
        merge_conflict = MergeConflict(threads=threads)
        self.assertFalse(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_conflicting_fields(), [])

        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(merge_conflict.get_resolution(), {"best_answer": threads[0]})
