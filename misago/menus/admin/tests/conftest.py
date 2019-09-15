import pytest
from django.urls import reverse

from ...models import MenuItem


@pytest.fixture
def list_url(admin_client):
    return reverse("misago:admin:settings:items:index")


@pytest.fixture
def menu_item(superuser):
    return MenuItem.objects.create(
        menu=MenuItem.POSITION_TOP,
        title="Test TMLA",
        item="https://top_menu_item_admin.com",
        order=0,
    )


@pytest.fixture
def other_menu_item(superuser):
    return MenuItem.objects.create(
        menu=MenuItem.POSITION_BOTH,
        title="Other Menu Item",
        item="https://other_menu_item.com",
        css_class="other-menu-item",
        rel="noopener noreferrer",
        target="_blank",
        order=1,
    )
