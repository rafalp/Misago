from typing import Tuple

from django.http import Http404

IndexView = Tuple[str, callable]


class IndexViews:
    views: dict[str, IndexView] = {}

    def __init__(self):
        self.views: dict[str, IndexView] = {}

    def add_index_view(self, id_: str, name: str, view: callable):
        self.views[id_] = (name, view)

    def get_choices(self) -> Tuple[Tuple[str, str]]:
        return tuple((key, self.views[key][0]) for key in self.views)

    def get_view(self, id_: str) -> callable:
        return self.views[id_][1]


index_views = IndexViews()


def forum_index(request, *args, **kwargs):
    try:
        view = index_views.get_view(request.settings.index_view)
    except KeyError:
        raise Http404()
    else:
        return view(request, *args, **kwargs, is_index=True)
