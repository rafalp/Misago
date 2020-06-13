from ariadne import ObjectType

from ...validation import PASSWORD_MAX_LENGTH


settings_type = ObjectType("Settings")

settings_type.set_alias("bulkActionLimit", "bulk_action_limit")
settings_type.set_alias("forumIndexHeader", "forum_index_header")
settings_type.set_alias("forumIndexThreads", "forum_index_threads")
settings_type.set_alias("forumIndexTitle", "forum_index_title")
settings_type.set_alias("forumName", "forum_name")
settings_type.set_alias("passwordMinLength", "password_min_length")
settings_type.set_alias("threadTitleMinLength", "thread_title_min_length")
settings_type.set_alias("threadTitleMaxLength", "thread_title_max_length")
settings_type.set_alias("usernameMinLength", "username_min_length")
settings_type.set_alias("usernameMaxLength", "username_max_length")


@settings_type.field("passwordMaxLength")
def resolve_password_max_length(*_):
    return PASSWORD_MAX_LENGTH
