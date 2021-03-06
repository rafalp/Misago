from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import constr, create_model

from ....conf.cache import clear_settings_cache
from ....conf.dynamicsettings import get_settings_from_db
from ....conf.update import update_settings
from ....validation import validate_model
from ...errorhandler import error_handler
from ..decorators import admin_mutation

change_settings_mutation = MutationType()


@change_settings_mutation.field("changeSettings")
@error_handler
@admin_mutation
@convert_kwargs_to_snake_case
async def resolve_change_settings(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    validated_data, errors = validate_model(InputModel, input)
    if errors:
        return {"errors": errors, "settings": info.context["settings"]}

    await update_settings(validated_data)
    await clear_settings_cache()

    return {"settings": await get_settings_from_db()}


InputModel = create_model(
    "InputModel",
    forum_index_header=(constr(min_length=0, max_length=255), ...),
    forum_index_threads=(bool, ...),
    forum_index_title=(constr(min_length=0, max_length=255), ...),
    forum_name=(constr(min_length=1, max_length=255), ...),
)
