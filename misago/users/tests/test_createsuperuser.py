from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()


def test_superuser_is_created_if_input_is_valid(db):
    out = StringIO()

    call_command(
        "createsuperuser",
        interactive=False,
        username="test",
        email="test@example.com",
        password="password",
        stdout=out,
    )

    command_output = out.getvalue().splitlines()[-1].strip()
    user = User.objects.order_by("-id")[:1][0]

    assert command_output == ("Superuser #%s has been created successfully." % user.pk)

    assert user.username == "test"
    assert user.email == "test@example.com"
    assert user.check_password("password")
