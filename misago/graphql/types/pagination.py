from ariadne import ObjectType

from ...database.paginator import Paginator


pagination_type = ObjectType("Pagination")
pagination_type.set_alias("perPage", "per_page")


@pagination_type.field("count")
def resolve_count(obj: Paginator, *_) -> int:
    return obj.get_count()


@pagination_type.field("pages")
def resolve_pages(obj: Paginator, *_) -> int:
    return obj.get_pages()
