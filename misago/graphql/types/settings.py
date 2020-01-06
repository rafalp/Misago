from ariadne import ObjectType

from ...validation import PASSWORD_MAX_LENGTH


settings_type = ObjectType("Settings")

settings_type.set_alias("forumName", "forum_name")
settings_type.set_alias("passwordMinLength", "password_min_length")
settings_type.set_alias("usernameMinLength", "username_min_length")
settings_type.set_alias("usernameMaxLength", "username_max_length")


@settings_type.field("passwordMaxLength")
def resolve_password_max_length(*_):
    return PASSWORD_MAX_LENGTH
