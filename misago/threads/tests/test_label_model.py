from django.test import TestCase
from misago.categories.models import Category
from misago.threads.models import Label


class LabelsManagerTests(TestCase):
    def setUp(self):
        Label.objects.clear_cache()

    def tearDown(self):
        Label.objects.clear_cache()

    def test_get_cached_labels(self):
        """get_cached_labels and get_cached_labels_dict work as intented"""
        test_labels = (
            Label.objects.create(name="Label 1", slug="label-1"),
            Label.objects.create(name="Label 2", slug="label-2"),
            Label.objects.create(name="Label 3", slug="label-3"),
            Label.objects.create(name="Label 4", slug="label-4"),
        )

        db_labels = Label.objects.get_cached_labels()
        self.assertEqual(len(db_labels), len(test_labels))
        for label in db_labels:
            self.assertIn(label, test_labels)

        db_labels = Label.objects.get_cached_labels_dict()
        self.assertEqual(len(db_labels), len(test_labels))
        for label in test_labels:
            self.assertEqual(db_labels[label.pk], label)

    def test_get_category_labels(self):
        """get_category_labels returns labels for category"""
        category = Category.objects.all_categories().filter(role='forum')[:1][0]

        test_labels = (
            Label.objects.create(name="Label 1", slug="label-1"),
            Label.objects.create(name="Label 2", slug="label-2"),
            Label.objects.create(name="Label 3", slug="label-3"),
            Label.objects.create(name="Label 4", slug="label-4"),
        )

        test_labels[0].categories.add(category)
        test_labels[2].categories.add(category)

        category_labels = Label.objects.get_category_labels(category)
        self.assertEqual(len(category_labels), 2)
        self.assertIn(test_labels[0], category_labels)
        self.assertIn(test_labels[2], category_labels)
        self.assertNotIn(test_labels[1], category_labels)
        self.assertNotIn(test_labels[3], category_labels)
