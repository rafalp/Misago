from ariadne_django.views import GraphQLView
from django.urls import path

from .schema import schema


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # GraphQL API
        urlpatterns.namespace("graphql/", "graphql")
        urlpatterns.patterns(
            "graphql", path("", GraphQLView.as_view(schema=schema), name="index")
        )
