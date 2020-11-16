from ariadne.contrib.django.views import GraphQLView
from django.conf.urls import url

from .schema import schema


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # GraphQL API
        urlpatterns.namespace(r"^graphql/", "graphql")
        urlpatterns.patterns(
            "graphql", url(r"^$", GraphQLView.as_view(schema=schema), name="index")
        )
