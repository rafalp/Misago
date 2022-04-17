from ariadne import ObjectType

settings_type = ObjectType("Settings")

settings_type.set_alias("jwtExp", "jwt_exp")
settings_type.set_alias("postsPerPage", "posts_per_page")
settings_type.set_alias("postsPerPageOrphans", "posts_per_page_orphans")
settings_type.set_alias("threadsPerPage", "threads_per_page")
