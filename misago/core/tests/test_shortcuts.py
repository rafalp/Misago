from django.core.urlresolvers import reverse
from django.test import TestCase
from misago.core.shortcuts import validate_slug, OutdatedSlug
from misago.core.testproject.models import Model


class ValidateSlugTests(TestCase):
    def test_is_outdated_slug_exception_not_raised_for_valid_slug(self):
        """
        check_object_slug doesn't raise OutdatedSlug when slugs match
        """
        model = Model(1, "test-slug")
        validate_slug(model, "test-slug")

    def test_is_outdated_slug_exception_raised_for_invalid_slug(self):
        """
        check_object_slug raises OutdatedSlug when slugs mismatch
        """
        model = Model(1, "test-slug")

        with self.assertRaises(OutdatedSlug):
            validate_slug(model, "wrong-slug")

    def test_is_outdated_slug_exception_raised_with_valid_message(self):
        """
        check_object_slug raises OutdatedSlug with valid message
        """
        correct_slug = "test-slug"
        model = Model(1, correct_slug)

        try:
            validate_slug(model, "wrong-slug")
        except OutdatedSlug as e:
            self.assertEqual(model, e.args[0])


class CheckSlugHandler(TestCase):
    urls = 'misago.core.testproject.urls'

    def test_valid_slug_handle(self):
        """valid slug causes no interruption in view processing"""
        test_kwargs = {'model_slug': 'eric-the-fish', 'model_id': 1}
        response = self.client.get(
            reverse('validate_slug_view', kwargs=test_kwargs))
        self.assertIn("Allright", response.content)

    def test_invalid_slug_handle(self):
        """invalid slug returns in redirect to valid page"""
        test_kwargs = {'model_slug': 'lion-the-eric', 'model_id': 1}
        response = self.client.get(
            reverse('validate_slug_view', kwargs=test_kwargs))

        valid_url = "http://testserver/forum/test-valid-slug/eric-the-fish-1/"
        self.assertEqual(response['Location'], valid_url)
