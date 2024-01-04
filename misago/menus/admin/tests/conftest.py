import pytest
from django.urls import reverse

from ...models import MenuItem


@pytest.fixture
def list_url():
    return reverse("misago:admin:settings:menu-items:index")


@pytest.fixture
def menu_item(db):
    return MenuItem.objects.create(
        menu=MenuItem.MENU_NAVBAR,
        title="Test TMLA",
        url="https://top_menu_item_admin.com",
        order=0,
    )


@pytest.fixture
def other_menu_item(db):
    return MenuItem.objects.create(
        menu=MenuItem.MENU_BOTH,
        title="Other Menu Item",
        url="https://other_menu_item.com",
        order=1,
    )
