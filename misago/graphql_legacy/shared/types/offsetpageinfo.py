from ariadne import ObjectType

offset_page_info_type = ObjectType("OffsetPageInfo")
offset_page_info_type.set_alias("hasNextPage", "has_next_page")
offset_page_info_type.set_alias("hasPreviousPage", "has_previous_page")
offset_page_info_type.set_alias("nextPage", "next_page")
offset_page_info_type.set_alias("previousPage", "previous_page")
