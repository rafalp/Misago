from ariadne import ObjectType


def create_page_type(name: str) -> ObjectType:
    page_type = ObjectType(name)
    page_type.set_alias("totalCount", "total_count")
    page_type.set_alias("totalPages", "total_pages")
    page_type.set_alias("pageInfo", "page_info")
    return page_type
