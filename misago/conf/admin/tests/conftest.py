import pytest

from ...models import Setting


@pytest.fixture
def setting(db):
    return Setting.objects.get(setting="forum_name")
