from ariadne import EnumType

from ...avatars.types import AvatarType

avatar_type_enum = EnumType("AvatarType", AvatarType)

shared_enums = [avatar_type_enum]
