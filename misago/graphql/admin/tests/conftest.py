import pytest
from django.urls import reverse

from ...test import GraphQLTestClient


@pytest.fixture
def admin_graphql_client(admin_client):
    return GraphQLTestClient(admin_client, reverse("misago:admin:graphql:index"))
