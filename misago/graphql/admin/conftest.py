import pytest
from django.urls import reverse


@pytest.fixture
def admin_graphql_link():
    return reverse("misago:admin:graphql:index")
