from unittest.mock import Mock

import pytest

from ..providers import Providers


@pytest.fixture
def providers():
    obj = Providers()
    obj.add(
        provider="facebook",
        name="Facebook",
        settings={"scope": ["email"]},
        admin_form=True,
        admin_template="form.html",
    )
    return obj


def test_provider_can_be_added_to_providers():
    providers = Providers()
    providers.add(
        provider="facebook",
        name="Facebook",
        settings={"scope": ["email"]},
        admin_form=True,
        admin_template="form.html",
    )

    assert providers.dict() == {
        "facebook": {
            "provider": "facebook",
            "name": "Facebook",
            "settings": {"scope": ["email"]},
            "admin_form": True,
            "admin_template": "form.html",
        }
    }
    assert providers.list() == [
        {
            "provider": "facebook",
            "name": "Facebook",
            "settings": {"scope": ["email"]},
            "admin_form": True,
            "admin_template": "form.html",
        }
    ]


def test_providers_list_is_resorted_when_new_provider_is_added(providers):
    providers.add(
        provider="auth", name="Auth", admin_form=True, admin_template="form.html"
    )

    assert providers.list() == [
        {
            "provider": "auth",
            "name": "Auth",
            "settings": {},
            "admin_form": True,
            "admin_template": "form.html",
        },
        {
            "provider": "facebook",
            "name": "Facebook",
            "settings": {"scope": ["email"]},
            "admin_form": True,
            "admin_template": "form.html",
        },
    ]


def test_util_returns_true_for_existing_provider(providers):
    assert providers.is_registered("facebook") is True


def test_util_returns_false_for_nonexisting_provider(providers):
    assert providers.is_registered("github") is False


def test_getter_returns_given_provider_name(providers):
    assert providers.get_name("facebook") == "Facebook"


def test_getter_returns_given_provider_settings(providers):
    assert providers.get_settings("facebook") == {"scope": ["email"]}


def test_getter_returns_given_provider_admin_form_class(providers):
    assert providers.get_admin_form_class("facebook") is True


def test_getter_returns_given_provider_admin_template_name(providers):
    assert providers.get_admin_template_name("facebook") == "form.html"
