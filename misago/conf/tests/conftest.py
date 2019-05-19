import pytest

from ..models import Setting


@pytest.fixture
def lazy_setting(db):
    return Setting.objects.create(
        setting="lazy_setting", dry_value="Hello", is_lazy=True, field_extra={}
    )


@pytest.fixture
def lazy_setting_without_value(db):
    return Setting.objects.create(
        setting="lazy_setting", dry_value="", is_lazy=True, field_extra={}
    )


@pytest.fixture
def private_setting(db):
    return Setting.objects.create(
        setting="private_setting", dry_value="Hello", is_public=False, field_extra={}
    )


@pytest.fixture
def public_setting(db):
    return Setting.objects.create(
        setting="public_setting", dry_value="Hello", is_public=True, field_extra={}
    )
