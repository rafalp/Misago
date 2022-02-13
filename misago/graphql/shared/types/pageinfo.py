from ariadne import ObjectType

page_info_type = ObjectType("PageInfo")
page_info_type.set_alias("hasNextPage", "has_next_page")
page_info_type.set_alias("hasPreviousPage", "has_previous_page")
page_info_type.set_alias("startCursor", "start_cursor")
page_info_type.set_alias("endCursor", "end_cursor")
page_info_type.set_alias("nextCursor", "next_cursor")
page_info_type.set_alias("previousCursor", "previous_cursor")
