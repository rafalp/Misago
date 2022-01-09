from typing import Dict, List

from pydantic import PydanticValueError

from ariadne import MutationType
from asgiref.sync import sync_to_async
from graphql import GraphQLResolveInfo
from starlette.datastructures import UploadFile

from ....avatars.upload import store_uploaded_avatar
from ....errors import ErrorsList
from ....uploads.validators import UploadSizeValidator
from ....users.models import User
from ....validation import (
    UserIsAuthorizedRootValidator,
    Validator,
    validate_data,
)
from ...errorhandler import error_handler

avatar_upload_mutation = MutationType()


@avatar_upload_mutation.field("avatarUpload")
@error_handler
async def resolve_avatar_uploadd(_, info: GraphQLResolveInfo, *, upload: UploadFile):
    data = {"upload": upload}
    validators: Dict[str, List[Validator]] = {
        "upload": [
            UploadSizeValidator(info.context["settings"]["avatar_max_size"]),
            validate_avatar_file,
        ],
        ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
    }
    cleaned_data, errors = await validate_data(data, validators, ErrorsList())

    if errors:
        return {"errors": errors}

    user: User = info.context["user"]
    user = await store_uploaded_avatar(user, cleaned_data["upload"])

    return {
        "user": user,
        "errors": None,
    }


IMAGE_FILE_MEDIA = (
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
)


class ImageError(PydanticValueError):
    code = "image.type"
    msg_template = "image type unrecognized"


@sync_to_async
def validate_avatar_file(value: UploadFile, errors: ErrorsList, field_name: str):
    if value.content_type not in IMAGE_FILE_MEDIA:
        raise ImageError()

    return value
