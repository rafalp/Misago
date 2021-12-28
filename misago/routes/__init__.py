from ..conf import settings
from .category import category_route
from .error_500 import error_500_route
from .index import index_route
from .thread import thread_route
from .exceptions import HTTPNotFound, get_exception_handlers


def register_routes(app):
    app.add_route("/", index_route, name="index")
    app.add_route("/c/{slug}/{id:int}/", category_route, name="category")
    app.add_route("/t/{slug}/{id:int}/", thread_route, name="thread")
    app.add_route("/t/{slug}/{id:int}/{page:int}/", thread_route, name="thread")

    if settings.debug:
        app.add_route("/error-500/", error_500_route, include_in_schema=False)
