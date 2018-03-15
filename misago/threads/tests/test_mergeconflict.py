from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.categories.models import Category

from misago.threads import testutils
from misago.threads.mergeconflict import MergeConflict


UserModel = get_user_model()


class MergeConflictTests(TestCase):
    def setUp(self):
        self.category = Category.objects.get(slug='first-category')
        self.user = UserModel.objects.create_user('bob', 'bob@test.com', 'Pass.123')

    def create_plain_thread(self):
        return testutils.post_thread(self.category)

    def create_poll_thread(self):
        thread = testutils.post_thread(self.category)
        testutils.post_poll(thread, self.user)
        return thread

    def create_best_answer_thread(self):
        thread = testutils.post_thread(self.category)
        best_answer = testutils.reply_thread(thread)
        thread.set_best_answer(self.user, best_answer)
        thread.synchronize()
        thread.save()
        return thread

    def test_plain_threads_no_conflicts(self):
        """threads without items of interest don't conflict"""
        threads = [self.create_plain_thread() for i in range(10)]
        merge_conflict = MergeConflict(threads=threads)
        self.assertFalse(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_merge_conflict(), [])

        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(merge_conflict.get_resolution(), {})

    def test_one_best_answer_one_plain(self):
        """thread with best answer and plain thread don't conflict"""
        threads = [
            self.create_best_answer_thread(),
            self.create_plain_thread(),
        ]
        merge_conflict = MergeConflict(threads=threads)
        self.assertFalse(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_merge_conflict(), [])

        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(merge_conflict.get_resolution(), {
            'best_answer': threads[0],
        })

    def test_one_poll_one_plain(self):
        """thread with poll and plain thread don't conflict"""
        threads = [
            self.create_poll_thread(),
            self.create_plain_thread(),
        ]
        merge_conflict = MergeConflict(threads=threads)
        self.assertFalse(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_merge_conflict(), [])

        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(merge_conflict.get_resolution(), {
            'poll': threads[0].poll,
        })

    def test_one_best_answer_one_poll(self):
        """thread with best answer and thread with poll don't conflict"""
        threads = [
            self.create_poll_thread(),
            self.create_best_answer_thread(),
        ]
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
        """three threads with best answer, thread with poll and two plain threads conflict"""
        best_answers = [self.create_best_answer_thread() for i in range(3)]
        polls = [self.create_poll_thread()]
        threads = [
            self.create_plain_thread(),
            self.create_plain_thread(),
        ] + best_answers + polls

        merge_conflict = MergeConflict(threads=threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_merge_conflict(), ['best_answer'])

        # without choice, conflict lists resolutions
        try:
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(merge_conflict.get_merge_conflict(), ['best_answer'])
            self.assertEqual(e.detail, {
                'best_answers': [['0', 'Unmark all best answers']] + [
                    [
                        str(thread.id),
                        thread.title,
                    ] for thread in reversed(best_answers)
                ]
            })

        # conflict validates choice
        try:
            merge_conflict = MergeConflict({'best_answer': threads[0].id}, threads)
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(e.detail, {'best_answer': ['Invalid choice.']})

        # conflict returns selected resolution
        merge_conflict = MergeConflict({'best_answer': best_answers[0].id}, threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_merge_conflict(), ['best_answer'])
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(merge_conflict.get_resolution(), {
            'best_answer': best_answers[0],
            'poll': polls[0].poll,
        })

        # conflict returns no-choice resolution
        merge_conflict = MergeConflict({'best_answer': 0}, threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_merge_conflict(), ['best_answer'])
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(merge_conflict.get_resolution(), {
            'best_answer': None,
            'poll': polls[0].poll,
        })

    def test_one_best_answer_three_poll_two_plain_conflict(self):
        """three threads with best answer, thread with poll and two plain threads conflict"""
        best_answers = [self.create_best_answer_thread()]
        polls = [self.create_poll_thread() for i in range(3)]
        threads = [
            self.create_plain_thread(),
            self.create_plain_thread(),
        ] + best_answers + polls

        merge_conflict = MergeConflict(threads=threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_merge_conflict(), ['poll'])

        # without choice, conflict lists resolutions
        try:
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(merge_conflict.get_merge_conflict(), ['poll'])
            self.assertEqual(e.detail, {
                'polls': [['0', 'Delete all polls']] + [
                    [
                        str(thread.poll.id),
                        thread.poll.question,
                    ] for thread in reversed(polls)
                ]
            })

        # conflict validates choice
        try:
            merge_conflict = MergeConflict({'poll': threads[0].id}, threads)
            merge_conflict.is_valid(raise_exception=True)
            self.fail("merge_conflict.is_valid() should raise ValidationError")
        except ValidationError as e:
            self.assertTrue(merge_conflict.is_merge_conflict())
            self.assertEqual(e.detail, {'poll': ['Invalid choice.']})

        # conflict returns selected resolution
        merge_conflict = MergeConflict({'poll': polls[0].poll.id}, threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_merge_conflict(), ['poll'])
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(merge_conflict.get_resolution(), {
            'best_answer': best_answers[0],
            'poll': polls[0].poll,
        })

        # conflict returns no-choice resolution
        merge_conflict = MergeConflict({'poll': 0}, threads)
        self.assertTrue(merge_conflict.is_merge_conflict())
        self.assertEqual(merge_conflict.get_merge_conflict(), ['poll'])
        merge_conflict.is_valid(raise_exception=True)
        self.assertEqual(merge_conflict.get_resolution(), {
            'best_answer': best_answers[0],
            'poll': None,
        })