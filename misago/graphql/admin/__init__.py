from django.conf.urls import url

from .views import graphql_view


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # GraphQL API
        urlpatterns.namespace(r"^graphql/", "graphql")
        urlpatterns.patterns("graphql", url(r"^$", graphql_view, name="index"))
