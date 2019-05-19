from django.test import TestCase

from ..models import Setting


class SettingModelTests(TestCase):
    def test_real_value(self):
        """setting returns real value correctyly"""
        setting_model = Setting(python_type="list", dry_value="")
        self.assertEqual(setting_model.value, [])

        setting_model = Setting(python_type="list", dry_value="Arthur,Lancelot,Patsy")
        self.assertEqual(setting_model.value, ["Arthur", "Lancelot", "Patsy"])

        setting_model = Setting(python_type="list", default_value="Arthur,Patsy")
        self.assertEqual(setting_model.value, ["Arthur", "Patsy"])

        setting_model = Setting(
            python_type="list",
            dry_value="Arthur,Robin,Patsy",
            default_value="Arthur,Patsy",
        )
        self.assertEqual(setting_model.value, ["Arthur", "Robin", "Patsy"])

    def test_set_value(self):
        """setting sets value correctyly"""
        setting_model = Setting(python_type="int", dry_value="42", default_value="9001")

        setting_model.value = 3000
        self.assertEqual(setting_model.value, 3000)
        self.assertEqual(setting_model.dry_value, "3000")

        setting_model.value = None
        self.assertEqual(setting_model.value, 9001)
        self.assertEqual(setting_model.dry_value, None)
