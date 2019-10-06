from ariadne import ObjectType


user_type = ObjectType("User")

user_type.set_alias("joinedAt", "joined_at")
user_type.set_alias("isModerator", "is_moderator")
