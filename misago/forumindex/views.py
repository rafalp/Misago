from inspect import isclass

from django.http import Http404
from django.utils.translation import pgettext_lazy
from django.views import View

from ..categories.views import index as categories
from ..plugins import extensions
from ..threads.views import ThreadListView

IndexView = tuple[str, callable]


class IndexViews:
    choices: list[tuple[str, str]]
    views: dict[str, IndexView]

    _views_cache: dict[str, IndexView]

    def __init__(self):
        self.choices = []
        self.views = {}
        self._views_cache = {}

    def add_index_view(self, view_id: str, name: str, view: callable):
        self.choices.append((view_id, name))
        self.views[view_id] = view

    def get_choices(self) -> list[tuple[str, str]]:
        return self.choices

    def get_view(self, view_id: str) -> callable:
        if view_id not in self._views_cache:
            view = self.views[view_id]
            if isclass(view) and issubclass(view, View):
                self._views_cache[view_id] = extensions.get(view).as_view()
            else:
                self._views_cache[view_id] = view

        return self._views_cache[view_id]


index_views = IndexViews()

index_views.add_index_view(
    "threads",
    pgettext_lazy("index view choice", "Threads"),
    ThreadListView,
)
index_views.add_index_view(
    "categories",
    pgettext_lazy("index view choice", "Categories"),
    categories,
)


def forum_index(request, *args, **kwargs):
    try:
        view = index_views.get_view(request.settings.index_view)
    except KeyError:
        raise Http404()
    else:
        return view(request, *args, **kwargs, is_index=True)
