import pytest
from django.urls import reverse


@pytest.fixture
def users_admin_link(admin_client):
    response = admin_client.get(reverse("misago:admin:users:index"))
    return response["location"]
