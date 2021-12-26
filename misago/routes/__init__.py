from .category import category_route
from .index import index_route
from .thread import thread_route


def register_routes(app):
    app.add_route("/", index_route, name="index")
    app.add_route("/c/{slug}/{id:int}/", category_route, name="category")
    app.add_route("/t/{slug}/{id:int}/", thread_route, name="thread")
