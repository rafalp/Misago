from django.urls import reverse

from ....test import assert_has_error_message


def test_exporting_default_theme_sets_error_message(admin_client, default_theme):
    export_link = reverse("misago:admin:themes:export", kwargs={"pk": default_theme.pk})
    response = admin_client.post(export_link)
    assert_has_error_message(response)


def test_exporting_nonexisting_theme_sets_error_message(
    admin_client, nonexisting_theme
):
    export_link = reverse(
        "misago:admin:themes:export", kwargs={"pk": nonexisting_theme.pk}
    )
    response = admin_client.post(export_link)
    assert_has_error_message(response)
