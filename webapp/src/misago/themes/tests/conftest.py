import pytest

from ..models import Theme


@pytest.fixture
def default_theme(db):
    return Theme.objects.get(is_default=True)


@pytest.fixture
def theme(db):
    return Theme.objects.create(name="Custom theme")


@pytest.fixture
def other_theme(db):
    return Theme.objects.create(name="Other theme")


@pytest.fixture
def active_theme(theme):
    Theme.objects.update(is_active=False)
    theme.is_active = True
    theme.save()
    return theme
