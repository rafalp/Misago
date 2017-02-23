from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO


UserModel = get_user_model()


class CreateSuperuserTests(TestCase):
    def test_create_superuser(self):
        """command creates superuser"""
        out = StringIO()

        call_command(
            "createsuperuser",
            interactive=False,
            username="joe",
            email="joe@somewhere.org",
            password="Pass.123",
            stdout=out,
        )

        new_user = UserModel.objects.order_by('-id')[:1][0]

        self.assertEqual(
            out.getvalue().splitlines()[-1].strip(),
            'Superuser #%s has been created successfully.' % new_user.pk,
        )

        self.assertEqual(new_user.username, 'joe')
        self.assertEqual(new_user.email, 'joe@somewhere.org')
        self.assertTrue(new_user.check_password("Pass.123"))
