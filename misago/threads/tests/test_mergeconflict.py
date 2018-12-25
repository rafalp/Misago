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

    def test_one_poll_one_plain(self):
        """thread with poll and plain thread don't conflict"""
        threads = [self.create_poll_thread(), self.create_plain_thread()]
        merge_conflict = MergeConflict(threads=threads)
        self.assertFalse(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_conflicting_fields(), [])

        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(merge_conflict.get_resolution(), {"poll": threads[0].poll})

    def test_one_best_answer_one_poll(self):
        """thread with best answer and thread with poll don't conflict"""
        threads = [self.create_poll_thread(), self.create_best_answer_thread()]
        merge_conflict = MergeConflict(threads=threads)
        self.assertFalse(merge_conflict.is_merge_conflict())

    def test_one_best_answer_one_poll_one_plain(self):
        """thread with best answer, thread with poll and plain thread don't conflict"""
        threads = [
            self.create_plain_thread(),
            self.create_poll_thread(),
            self.create_best_answer_thread(),
        ]
        merge_conflict = MergeConflict(threads=threads)
        self.assertFalse(merge_conflict.is_merge_conflict())

    def test_three_best_answers_one_poll_two_plain_conflict(self):
        """
        three threads with best answer, thread with poll and two plain threads conflict
        """
        best_answers = [self.create_best_answer_thread() for i in range(3)]
        polls = [self.create_poll_thread()]
        threads = (
            [self.create_plain_thread(), self.create_plain_thread()]
            + best_answers
            + polls
        )

        merge_conflict = MergeConflict(threads=threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_conflicting_fields(), ["best_answer"])

        # without choice, conflict lists resolutions
        try:
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(merge_conflict.get_conflicting_fields(), ["best_answer"])
            self.assertEqual(
                e.detail,
                {
                    "best_answers": [["0", "Unmark all best answers"]]
                    + [[str(thread.id), thread.title] for thread in best_answers]
                },
            )

        # conflict validates choice
        try:
            merge_conflict = MergeConflict({"best_answer": threads[0].id}, threads)
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(e.detail, {"best_answer": ["Invalid choice."]})

        # conflict returns selected resolution
        merge_conflict = MergeConflict({"best_answer": best_answers[0].id}, threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_conflicting_fields(), ["best_answer"])
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(
            merge_conflict.get_resolution(),
            {"best_answer": best_answers[0], "poll": polls[0].poll},
        )

        # conflict returns no-choice resolution
        merge_conflict = MergeConflict({"best_answer": 0}, threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_conflicting_fields(), ["best_answer"])
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(
            merge_conflict.get_resolution(),
            {"best_answer": None, "poll": polls[0].poll},
        )

    def test_one_best_answer_three_polls_two_plain_conflict(self):
        """
        one thread with best answer, three threads with poll
        and two plain threads conflict
        """
        best_answers = [self.create_best_answer_thread()]
        polls = [self.create_poll_thread() for i in range(3)]
        threads = (
            [self.create_plain_thread(), self.create_plain_thread()]
            + best_answers
            + polls
        )

        merge_conflict = MergeConflict(threads=threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_conflicting_fields(), ["poll"])

        # without choice, conflict lists resolutions
        try:
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(merge_conflict.get_conflicting_fields(), ["poll"])
            self.assertEqual(
                e.detail,
                {
                    "polls": [["0", "Delete all polls"]]
                    + [
                        [
                            str(thread.poll.id),
                            "%s (%s)" % (thread.poll.question, thread.title),
                        ]
                        for thread in polls
                    ]
                },
            )

        # conflict validates choice
        try:
            merge_conflict = MergeConflict({"poll": threads[0].id}, threads)
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(e.detail, {"poll": ["Invalid choice."]})

        # conflict returns selected resolution
        merge_conflict = MergeConflict({"poll": polls[0].poll.id}, threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_conflicting_fields(), ["poll"])
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(
            merge_conflict.get_resolution(),
            {"best_answer": best_answers[0], "poll": polls[0].poll},
        )

        # conflict returns no-choice resolution
        merge_conflict = MergeConflict({"poll": 0}, threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_conflicting_fields(), ["poll"])
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(
            merge_conflict.get_resolution(),
            {"best_answer": best_answers[0], "poll": None},
        )

    def test_three_best_answers_three_polls_two_plain_conflict(self):
        """multiple conflict is handled"""
        best_answers = [self.create_best_answer_thread() for i in range(3)]
        polls = [self.create_poll_thread() for i in range(3)]
        threads = (
            [self.create_plain_thread(), self.create_plain_thread()]
            + best_answers
            + polls
        )

        merge_conflict = MergeConflict(threads=threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(
            merge_conflict.get_conflicting_fields(), ["best_answer", "poll"]
        )

        # without choice, conflict lists all resolutions
        try:
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(
                merge_conflict.get_conflicting_fields(), ["best_answer", "poll"]
            )
            self.assertEqual(
                e.detail,
                {
                    "best_answers": [["0", "Unmark all best answers"]]
                    + [[str(thread.id), thread.title] for thread in best_answers],
                    "polls": [["0", "Delete all polls"]]
                    + [
                        [
                            str(thread.poll.id),
                            "%s (%s)" % (thread.poll.question, thread.title),
                        ]
                        for thread in polls
                    ],
                },
            )

        # conflict validates all choices if single choice was given
        try:
            merge_conflict = MergeConflict({"best_answer": threads[0].id}, threads)
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(
                e.detail,
                {"best_answer": ["Invalid choice."], "poll": ["Invalid choice."]},
            )

        try:
            merge_conflict = MergeConflict({"poll": threads[0].id}, threads)
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(
                e.detail,
                {"best_answer": ["Invalid choice."], "poll": ["Invalid choice."]},
            )

        # conflict validates all choices if all choices were given
        try:
            merge_conflict = MergeConflict(
                {"best_answer": threads[0].id, "poll": threads[0].id}, threads
            )
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(
                e.detail,
                {"best_answer": ["Invalid choice."], "poll": ["Invalid choice."]},
            )

        # conflict returns selected resolutions
        valid_choices = {"best_answer": best_answers[0].id, "poll": polls[0].poll.id}
        merge_conflict = MergeConflict(valid_choices, threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(
            merge_conflict.get_conflicting_fields(), ["best_answer", "poll"]
        )
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(
            merge_conflict.get_resolution(),
            {"best_answer": best_answers[0], "poll": polls[0].poll},
        )

        # conflict returns no-choice resolution
        merge_conflict = MergeConflict({"best_answer": 0, "poll": 0}, threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(
            merge_conflict.get_conflicting_fields(), ["best_answer", "poll"]
        )
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(
            merge_conflict.get_resolution(), {"best_answer": None, "poll": None}
        )

        # conflict allows mixing no-choice with choice
        merge_conflict = MergeConflict(
            {"best_answer": best_answers[0].id, "poll": 0}, threads
        )
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(
            merge_conflict.get_conflicting_fields(), ["best_answer", "poll"]
        )
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(
            merge_conflict.get_resolution(),
            {"best_answer": best_answers[0], "poll": None},
        )

        merge_conflict = MergeConflict(
            {"best_answer": 0, "poll": polls[0].poll.id}, threads
        )
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(
            merge_conflict.get_conflicting_fields(), ["best_answer", "poll"]
        )
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(
            merge_conflict.get_resolution(),
            {"best_answer": None, "poll": polls[0].poll},
        )
