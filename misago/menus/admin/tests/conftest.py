import pytest
from django.urls import reverse

from ...models import MenuLink


@pytest.fixture
def list_url(admin_client):
    return reverse("misago:admin:settings:links:index")


@pytest.fixture
def menu_link(superuser):
    return MenuLink.objects.create(
        position=MenuLink.POSITION_TOP,
        title="Test TMLA",
        link="https://top_menu_link_admin.com",
        order=0,
    )


@pytest.fixture
def other_menu_link(superuser):
    return MenuLink.objects.create(
        position=MenuLink.POSITION_BOTH,
        title="Other Menu Link",
        link="https://other_menu_link.com",
        css_class="other-menu-link",
        rel="noopener noreferrer",
        target="_blank",
        order=1,
    )
