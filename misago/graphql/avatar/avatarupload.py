from typing import Dict, List

from ariadne_graphql_modules import DeferredType, ObjectType, gql
from graphql import GraphQLResolveInfo
from starlette.datastructures import UploadFile

from ...auth.validators import IsAuthenticatedValidator
from ...avatars.upload import store_uploaded_avatar
from ...conf import settings
from ...uploads.validators import (
    UploadContentTypeValidator,
    UploadImageValidator,
    UploadSizeValidator,
)
from ...users.models import User
from ...validation import ErrorsList, Validator, validate_data
from ..mutation import ErrorType, MutationType
from ..scalars import UploadScalar

AVATAR_CONTENT_TYPES = settings.avatar_content_types
AVATAR_MIN_SIZE = max(settings.avatar_sizes)


class AvatarUploadResultType(ObjectType):
    __schema__ = gql(
        """
        type AvatarUploadResult {
            updated: Boolean!
            user: User
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, DeferredType("User")]


class AvatarUploadMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            avatarUpload(upload: Upload!): AvatarUploadResult!
        }
        """
    )
    __requires__ = [UploadScalar, AvatarUploadResultType]

    @classmethod
    async def mutate(  # type: ignore
        cls,
        info: GraphQLResolveInfo,
        *,
        upload: UploadFile,
    ):
        cleaned_data, errors = await cls.clean_data(info, upload)
        user: User = info.context["user"]
        if errors:
            return {"errors": errors, "user": user, "updated": False}

        user = await store_uploaded_avatar(user, cleaned_data["upload"])

        return {"user": user, "updated": True}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, upload: UploadFile):
        data = {"upload": upload}
        validators: Dict[str, List[Validator]] = {
            "upload": [
                UploadSizeValidator(info.context["settings"]["avatar_upload_max_size"]),
                UploadContentTypeValidator(AVATAR_CONTENT_TYPES),
                UploadImageValidator(min_size=(AVATAR_MIN_SIZE, AVATAR_MIN_SIZE)),
            ],
            ErrorsList.ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
        }
        cleaned_data, errors = await validate_data(data, validators, ErrorsList())
        return cleaned_data, errors
