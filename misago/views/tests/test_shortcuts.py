from django.test import TestCase
from misago.views.shortcuts import check_object_slug, OutdatedSlug


class MockModel(object):
    def __init__(self, slug):
        self.slug = slug


class CheckObjectSlugTests(TestCase):
    def test_is_outdated_slug_exception_not_raised_for_valid_slug(self):
        """
        check_object_slug doesn't raise OutdatedSlug when slugs match
        """
        model = MockModel("test-slug")

        try:
            check_object_slug(model, "test-slug")
        except OutdatedSlug:
            self.fail("check_object_slug raised OutdatedSlug for valid slugs")

    def test_is_outdated_slug_exception_raised_for_invalid_slug(self):
        """
        check_object_slug raises OutdatedSlug when slugs mismatch
        """
        model = MockModel("test-slug")

        with self.assertRaises(OutdatedSlug):
            check_object_slug(model, "wrong-slug")

    def test_is_outdated_slug_exception_raised_with_valid_message(self):
        """
        check_object_slug raises OutdatedSlug with valid message
        """
        correct_slug = "test-slug"
        model = MockModel(correct_slug)

        try:
            check_object_slug(model, "wrong-slug")
        except OutdatedSlug as e:
            self.assertEqual(model, e.args[0])
