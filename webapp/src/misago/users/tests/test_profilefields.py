from django.contrib.auth import get_user_model
from django.test import TestCase

from ..profilefields import ProfileFields

User = get_user_model()


class ProfileFieldsLoadTests(TestCase):
    def test_no_groups(self):
        """profile fields util handles empty list"""
        profilefields = ProfileFields([])
        profilefields.load()

        self.assertFalse(profilefields.fields_dict)

    def test_empty_group(self):
        """profile fields util handles empty group"""
        profilefields = ProfileFields([{"name": "Test", "fields": []}])

        profilefields.load()

        self.assertFalse(profilefields.fields_dict)

    def test_field_defines_fieldname(self):
        """fields need to define fieldname"""
        profilefields = ProfileFields(
            [
                {
                    "name": "Test",
                    "fields": [
                        "misago.users.tests.testfiles.profilefields.NofieldnameField"
                    ],
                }
            ]
        )

        with self.assertRaises(ValueError):
            profilefields.load()

        try:
            profilefields.load()
        except ValueError as e:
            error = str(e)

            self.assertIn(
                "misago.users.tests.testfiles.profilefields.NofieldnameField", error
            )
            self.assertIn("profile field has to specify fieldname attribute", error)

    def test_detect_repeated_imports(self):
        """fields can't be specified multiple times"""
        profilefields = ProfileFields(
            [
                {
                    "name": "Test",
                    "fields": ["misago.users.profilefields.default.TwitterHandleField"],
                },
                {
                    "name": "Other test",
                    "fields": ["misago.users.profilefields.default.TwitterHandleField"],
                },
            ]
        )

        with self.assertRaises(ValueError):
            profilefields.load()

        try:
            profilefields.load()
        except ValueError as e:
            error = str(e)

            self.assertIn(
                "misago.users.profilefields.default.TwitterHandleField", error
            )
            self.assertIn("profile field has been specified twice", error)

    def test_detect_repeated_fieldnames(self):
        """fields can't reuse other field's fieldnames"""
        profilefields = ProfileFields(
            [
                {
                    "name": "Test",
                    "fields": [
                        "misago.users.tests.testfiles.profilefields.FieldnameField"
                    ],
                },
                {
                    "name": "Other test",
                    "fields": [
                        # pylint: disable=line-too-long
                        "misago.users.tests.testfiles.profilefields.RepeatedFieldnameField"
                    ],
                },
            ]
        )

        with self.assertRaises(ValueError):
            profilefields.load()

        try:
            profilefields.load()
        except ValueError as e:
            error = str(e)

            self.assertIn(
                "misago.users.tests.testfiles.profilefields.FieldnameField", error
            )
            self.assertIn(
                "misago.users.tests.testfiles.profilefields.RepeatedFieldnameField",
                error,
            )
            self.assertIn(
                'field defines fieldname "hello" that is already in use by the', error
            )

    def test_field_correct_field(self):
        """util loads correct field"""
        field_path = "misago.users.profilefields.default.RealNameField"

        profilefields = ProfileFields([{"name": "Test", "fields": [field_path]}])

        profilefields.load()

        self.assertIn(field_path, profilefields.fields_dict)
