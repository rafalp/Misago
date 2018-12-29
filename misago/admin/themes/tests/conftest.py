import pytest

from ....themes.models import Theme


@pytest.fixture
def default_theme(db):
    return Theme.objects.get(is_default=True)


@pytest.fixture
def theme(db):
    return Theme.objects.create(name="Custom theme")


@pytest.fixture
def nonexisting_theme(mocker, default_theme):
    return mocker.Mock(pk=default_theme.pk + 1)
