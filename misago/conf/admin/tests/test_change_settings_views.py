import pytest
from django import forms
from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ... import SETTINGS_CACHE
from ..forms import ChangeSettingsForm
from ..views import ChangeSettingsView


@pytest.fixture(autouse=True)
def messages_mock(mocker):
    return mocker.patch("misago.conf.admin.views.messages")


class Form(ChangeSettingsForm):
    settings = ["forum_name"]

    forum_name = forms.CharField(max_length=255)


class View(ChangeSettingsView):
    form_class = Form

    def render(self, request, context):
        return True


def test_view_loads_form_settings_from_db(setting):
    view = View()
    assert view.get_settings(["forum_name"]) == {setting.setting: setting}


def test_view_raises_value_error_if_requested_setting_is_not_found(setting):
    view = View()
    with pytest.raises(ValueError):
        assert view.get_settings(["forum_name", "nonexisting_setting"])


def test_initial_form_data_is_build_from_settings_dict(setting):
    view = View()
    settings_dict = {setting.setting: setting}
    assert view.get_initial_form_data(settings_dict) == {setting.setting: setting.value}


def test_view_handles_get_request(rf, setting):
    view = View.as_view()
    view(rf.get("/"))


def test_view_handles_post_request(rf, setting):
    view = View.as_view()
    view(rf.post("/", {setting.setting: "New Value"}))


def test_view_changes_setting_on_correct_post_request(rf, setting):
    view = View.as_view()
    view(rf.post("/", {setting.setting: "New Value"}))

    setting.refresh_from_db()
    assert setting.value == "New Value"


def test_view_handles_invalid_post_request(rf, setting):
    view = View.as_view()
    view(rf.post("/", {"invalid_setting": ""}))

    setting.refresh_from_db()
    assert setting.value == "Misago"


def test_view_invalidates_settings_cache_on_correct_post_request(rf, setting):
    with assert_invalidates_cache(SETTINGS_CACHE):
        view = View.as_view()
        view(rf.post("/", {setting.setting: "New Value"}))


def test_analytics_settings_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:analytics:index"))
    assert response.status_code == 200


def test_captcha_settings_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:captcha:index"))
    assert response.status_code == 200


def test_general_settings_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:general:index"))
    assert response.status_code == 200


def test_threads_settings_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:threads:index"))
    assert response.status_code == 200


def test_users_settings_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:users:index"))
    assert response.status_code == 200
