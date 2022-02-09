from ariadne import ObjectType


def create_page_type(name: str) -> ObjectType:
    type = ObjectType(name)
    type.set_alias("totalCount", "total_count")
    type.set_alias("totalPages", "total_pages")
    type.set_alias("pageInfo", "page_info")
    return type
