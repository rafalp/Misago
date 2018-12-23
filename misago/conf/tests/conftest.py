import pytest

from ..models import Setting, SettingsGroup


@pytest.fixture
def settings_group(db):
    return SettingsGroup.objects.create(key="test", name="Test")


@pytest.fixture
def lazy_setting(settings_group):
    return Setting.objects.create(
        group=settings_group,
        setting="lazy_setting",
        name="Lazy setting",
        dry_value="Hello",
        is_lazy=True,
        field_extra={},
    )


@pytest.fixture
def lazy_setting_without_value(settings_group):
    return Setting.objects.create(
        group=settings_group,
        setting="lazy_setting",
        name="Lazy setting",
        dry_value="",
        is_lazy=True,
        field_extra={},
    )


@pytest.fixture
def private_setting(settings_group):
    return Setting.objects.create(
        group=settings_group,
        setting="private_setting",
        name="Private setting",
        dry_value="Hello",
        is_public=False,
        field_extra={},
    )


@pytest.fixture
def public_setting(settings_group):
    return Setting.objects.create(
        group=settings_group,
        setting="public_setting",
        name="Public setting",
        dry_value="Hello",
        is_public=True,
        field_extra={},
    )
