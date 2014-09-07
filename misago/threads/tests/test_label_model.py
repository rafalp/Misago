from django.test import TestCase

from misago.forums.models import Forum

from misago.threads.models import Label


class LabelsManagerTests(TestCase):
    def setUp(self):
        Label.objects.clear_cache()

    def test_get_cached_labels(self):
        """get_cached_labels and get_cached_labels_dict work as intented"""
        test_labels = (
            Label.objects.create(name="Label 1"),
            Label.objects.create(name="Label 2"),
            Label.objects.create(name="Label 3"),
            Label.objects.create(name="Label 4"),
        )

        db_labels = Label.objects.get_cached_labels()
        self.assertEqual(len(db_labels), len(test_labels))
        for label in db_labels:
            self.assertIn(label, test_labels)

        db_labels = Label.objects.get_cached_labels_dict()
        self.assertEqual(len(db_labels), len(test_labels))
        for label in test_labels:
            self.assertEqual(db_labels[label.pk], label)

    def test_get_forum_labels(self):
        """get_forum_labels returns labels for forum"""
        forum = Forum.objects.all_forums().filter(role='forum')[:1][0]

        test_labels = (
            Label.objects.create(name="Label 1"),
            Label.objects.create(name="Label 2"),
            Label.objects.create(name="Label 3"),
            Label.objects.create(name="Label 4"),
        )

        test_labels[0].forums.add(forum)
        test_labels[2].forums.add(forum)

        forum_labels = Label.objects.get_forum_labels(forum)
        self.assertEqual(len(forum_labels), 2)
        self.assertIn(test_labels[0], forum_labels)
        self.assertIn(test_labels[2], forum_labels)
        self.assertNotIn(test_labels[1], forum_labels)
        self.assertNotIn(test_labels[3], forum_labels)
