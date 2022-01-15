from typing import Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, conint, constr, create_model

from ....conf.cache import clear_settings_cache
from ....conf.dynamicsettings import get_settings_from_db
from ....conf.update import update_settings
from ....validation import PASSWORD_MAX_LENGTH, validate_model
from ...errorhandler import error_handler
from ..decorators import admin_resolver

settings_update_mutation = MutationType()


@settings_update_mutation.field("settingsUpdate")
@admin_resolver
@error_handler
@convert_kwargs_to_snake_case
async def resolve_settings_update(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    validated_data, errors = validate_model(SettingsChangeInputModel, input)
    clean_settings = {
        setting: value for setting, value in validated_data.items() if value is not None
    }

    if clean_settings:
        # Run second stage validation for cases where min is greater than max
        SecondStageModel = create_second_stage_model(
            clean_settings, info.context["settings"]
        )

        if SecondStageModel:
            _, second_stage_errors = validate_model(SecondStageModel, clean_settings)
            errors += second_stage_errors

    if errors:
        return {
            "errors": errors,
            "updated": False,
            "settings": info.context["settings"],
        }

    if clean_settings:
        await update_settings(clean_settings)
        await clear_settings_cache()

    return {"updated": bool(clean_settings), "settings": await get_settings_from_db()}


SettingsChangeInputModel: Type[BaseModel] = create_model(
    "SettingsChangeInputModel",
    avatar_upload_max_size=(conint(ge=1), None),
    bulk_action_limit=(conint(ge=5), None),
    forum_index_header=(
        constr(min_length=0, max_length=255, strip_whitespace=True),
        None,
    ),
    forum_index_threads=(bool, None),
    forum_index_title=(
        constr(min_length=0, max_length=255, strip_whitespace=True),
        None,
    ),
    forum_name=(constr(min_length=1, max_length=255, strip_whitespace=True), None),
    jwt_exp=(conint(ge=300), None),
    password_min_length=(conint(ge=4, le=PASSWORD_MAX_LENGTH - 1), None),
    post_min_length=(conint(ge=1), None),
    posts_per_page=(conint(ge=5, le=100), None),
    posts_per_page_orphans=(conint(ge=0), None),
    thread_title_min_length=(conint(ge=1), None),
    thread_title_max_length=(conint(ge=4, le=255), None),
    threads_per_page=(conint(ge=5, le=150), None),
    username_min_length=(conint(ge=1), None),
    username_max_length=(conint(le=50), None),
)


def create_second_stage_model(clean_settings, settings):
    rules = {}

    second_stage_rules = [
        (set_second_stage_int_min_rule, "posts_per_page", "posts_per_page_orphans"),
        (set_second_stage_int_max_rule, "posts_per_page_orphans", "posts_per_page"),
        (
            set_second_stage_int_max_rule,
            "thread_title_min_length",
            "thread_title_max_length",
        ),
        (
            set_second_stage_int_min_rule,
            "thread_title_max_length",
            "thread_title_min_length",
        ),
        (set_second_stage_int_max_rule, "username_min_length", "username_max_length"),
        (set_second_stage_int_min_rule, "username_max_length", "username_min_length"),
    ]

    for set_rule, setting_name, limit_name in second_stage_rules:
        if setting_name in clean_settings:
            set_rule(rules, setting_name, limit_name, clean_settings, settings)

    if not rules:
        return None

    return create_model("SecondStageModel", **rules)


def set_second_stage_int_min_rule(
    rules: dict,
    setting_name: str,
    limit_name: str,
    clean_settings: dict,
    settings: dict,
):
    setting_min_value = clean_settings.get(limit_name) or settings[limit_name]
    rules[setting_name] = (conint(gt=setting_min_value), ...)


def set_second_stage_int_max_rule(
    rules: dict,
    setting_name: str,
    limit_name: str,
    clean_settings: dict,
    settings: dict,
):
    setting_max_value = clean_settings.get(limit_name) or settings[limit_name]
    rules[setting_name] = (conint(lt=setting_max_value), ...)
