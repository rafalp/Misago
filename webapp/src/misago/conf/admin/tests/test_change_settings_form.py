from django import forms

from ....cache.test import assert_invalidates_cache
from ... import SETTINGS_CACHE
from ..forms import ChangeSettingsForm


class Form(ChangeSettingsForm):
    settings = ["forum_name"]

    forum_name = forms.CharField(max_length=255)


def test_form_updates_setting_on_save(setting):
    form = Form({"forum_name": "New Value"}, request=None)
    assert form.is_valid()
    form.save({"forum_name": setting})

    setting.refresh_from_db()
    assert setting.value == "New Value"


def test_form_invalidates_settings_cache_on_save(setting):
    with assert_invalidates_cache(SETTINGS_CACHE):
        form = Form({"forum_name": "New Value"}, request=None)
        assert form.is_valid()
        form.save({"forum_name": setting})
