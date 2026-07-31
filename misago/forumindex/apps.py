from django.apps import AppConfig
from django.utils.translation import pgettext_lazy

from ..plugins.extensions import extensions


class MisagoForumIndexConfig(AppConfig):
    name = "misago.forumindex"
    label = "misago_forumindex"
    verbose_name = "Misago Forum Index"

    def ready(self):
        from ..categories.views import index as categories
        from ..threads.views import ThreadListView
        from .views import index_views

        index_views.add_index_view(
            "threads",
            pgettext_lazy("index view choice", "Threads"),
            extensions.get(ThreadListView).as_view(),
        )
        index_views.add_index_view(
            "categories",
            pgettext_lazy("index view choice", "Categories"),
            categories,
        )
