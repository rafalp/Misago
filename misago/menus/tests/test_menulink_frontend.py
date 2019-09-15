from django.urls import reverse
from bs4 import BeautifulSoup


def test_top_menu_link_in_frontend(client, menu_link_top):
    response = client.get(reverse("misago:index"))
    assert response.status_code == 200
    parser = BeautifulSoup(response.content, "html.parser")
    link = parser.find("a", href=menu_link_top.link)
    assert link is not None
    assert menu_link_top.title == link.getText().strip()


def test_footer_menu_link_in_frontend(client, menu_link_footer):
    response = client.get(reverse("misago:index"))
    assert response.status_code == 200
    parser = BeautifulSoup(response.content, "html.parser")
    link = parser.find("a", href=menu_link_footer.link)
    assert link is not None
    assert menu_link_footer.title == link.getText().strip()


def test_both_menus_link_in_frontend(client, menu_link_both):
    response = client.get(reverse("misago:index"))
    assert response.status_code == 200
    parser = BeautifulSoup(response.content, "html.parser")
    links = parser.find_all("a", href=menu_link_both.link)
    assert links != []
    assert len(links) == 2
    for link in links:
        assert link is not None
        assert menu_link_both.title == link.getText().strip()


def test_menu_link_attributes_in_frontend(client, menu_link_with_attributes):
    response = client.get(reverse("misago:index"))
    assert response.status_code == 200
    parser = BeautifulSoup(response.content, "html.parser")
    link = parser.find("a", href=menu_link_with_attributes.link)
    assert link is not None
    assert menu_link_with_attributes.title == link.getText().strip()
    assert menu_link_with_attributes.rel.split() == link["rel"]
    assert menu_link_with_attributes.target == link["target"]
    assert menu_link_with_attributes.css_class.split() == link["class"]
