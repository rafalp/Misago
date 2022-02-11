from ariadne import ObjectType

threads_page_type = ObjectType("ThreadsPage")

threads_page_type.set_alias("edges", "results")
threads_page_type.set_alias("hasNext", "has_next")
threads_page_type.set_alias("hasPrevious", "has_previous")
threads_page_type.set_alias("nextCursor", "next_cursor")
threads_page_type.set_alias("previousCursor", "previous_cursor")
