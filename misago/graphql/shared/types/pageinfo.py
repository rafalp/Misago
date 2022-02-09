from ariadne import ObjectType

page_info_type = ObjectType("PageInfo")
page_info_type.set_alias("hasNext", "has_next")
page_info_type.set_alias("hasPrevious", "has_previous")
