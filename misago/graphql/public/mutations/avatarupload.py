from typing import Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo
from starlette.datastructures import UploadFile

from ....avatars.upload import store_uploaded_avatar
from ....conf import settings
from ....errors import ErrorsList
from ....uploads.validators import (
    UploadContentTypeValidator,
    UploadImageValidator,
    UploadSizeValidator,
)
from ....users.models import User
from ....validation import (
    UserIsAuthorizedRootValidator,
    Validator,
    validate_data,
)
from ...errorhandler import error_handler

AVATAR_CONTENT_TYPES = settings.avatar_content_types
AVATAR_MIN_SIZE = max(settings.avatar_sizes)

avatar_upload_mutation = MutationType()


@avatar_upload_mutation.field("avatarUpload")
@error_handler
async def resolve_avatar_upload(_, info: GraphQLResolveInfo, *, upload: UploadFile):
    data = {"upload": upload}
    validators: Dict[str, List[Validator]] = {
        "upload": [
            UploadSizeValidator(info.context["settings"]["avatar_upload_max_size"]),
            UploadContentTypeValidator(AVATAR_CONTENT_TYPES),
            UploadImageValidator(min_size=(AVATAR_MIN_SIZE, AVATAR_MIN_SIZE)),
        ],
        ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
    }
    cleaned_data, errors = await validate_data(data, validators, ErrorsList())

    user: User = info.context["user"]
    if errors:
        return {"errors": errors, "user": user}

    user = await store_uploaded_avatar(user, cleaned_data["upload"])

    return {"user": user}
