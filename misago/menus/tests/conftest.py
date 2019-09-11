import pytest

from ..models import MenuLink


@pytest.fixture
def menu_link_top(db):
    return MenuLink.objects.create(
        link="https://top_menu_link.com",
        title="Top Menu Link",
        position=MenuLink.POSITION_TOP,
    )


@pytest.fixture
def menu_link_footer(db):
    return MenuLink.objects.create(
        link="https://footer_menu_link.com",
        title="Footer Menu Link",
        position=MenuLink.POSITION_FOOTER,
    )


@pytest.fixture
def menu_link_both(db):
    return MenuLink.objects.create(
        link="https://both_positions_menu_link.com",
        title="Both Positions Menu Link",
        position=MenuLink.POSITION_BOTH,
    )


@pytest.fixture
def menu_link_with_attributes(db):
    return MenuLink.objects.create(
        link="https://menu_link_with_attributes.com",
        title="Menu link with attributes",
        position=MenuLink.POSITION_BOTH,
        rel="noopener nofollow",
        target="_blank",
        css_class="test-link-css-class",
    )


@pytest.fixture
def links_footer(db, menu_link_footer, menu_link_both, menu_link_with_attributes):
    return MenuLink.objects.get_footer_menu_links()


@pytest.fixture
def links_top(db, menu_link_top, menu_link_both, menu_link_with_attributes):
    return MenuLink.objects.get_top_menu_links()
