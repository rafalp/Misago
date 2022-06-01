from typing import Type

from ariadne_graphql_modules import InputType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, conint, constr, create_model

from ...conf.cache import clear_settings_cache
from ...conf.dynamicsettings import get_settings_from_db
from ...conf.update import update_settings
from ...users.validators import PASSWORD_MAX_LENGTH
from ...validation import validate_model
from ..mutation import AdminMutationType, ErrorType
from .settings import AdminSettingsType


class AdminSettingsUpdateInputType(InputType):
    __schema__ = gql(
        """
        input SettingsUpdateInput {
            avatarUploadMaxSize: Int
            bulkActionLimit: Int
            forumIndexHeader: String
            forumIndexThreads: Boolean
            forumIndexTitle: String
            forumName: String
            jwtExp: Int
            passwordMinLength: Int
            postMinLength: Int
            postsPerPage: Int
            postsPerPageOrphans: Int
            threadTitleMinLength: Int
            threadTitleMaxLength: Int
            threadsPerPage: Int
            usernameMinLength: Int
            usernameMaxLength: Int
        }
        """
    )
    __args__ = {
        "avatarUploadMaxSize": "avatar_upload_max_size",
        "bulkActionLimit": "bulk_action_limit",
        "forumIndexHeader": "forum_index_header",
        "forumIndexThreads": "forum_index_threads",
        "forumIndexTitle": "forum_index_title",
        "forumName": "forum_name",
        "jwtExp": "jwt_exp",
        "passwordMinLength": "password_min_length",
        "postMinLength": "post_min_length",
        "postsPerPage": "posts_per_page",
        "postsPerPageOrphans": "posts_per_page_orphans",
        "threadTitleMinLength": "thread_title_min_length",
        "threadTitleMaxLength": "thread_title_max_length",
        "threadsPerPage": "threads_per_page",
        "usernameMinLength": "username_min_length",
        "usernameMaxLength": "username_max_length",
    }


class AdminSettingsUpdateResultType(ObjectType):
    __schema__ = gql(
        """
        type SettingsUpdateResult {
            updated: Boolean!
            settings: Settings
            errors: [Error!]
        }
        """
    )
    __requires__ = [AdminSettingsType, ErrorType]


class AdminSettingsUpdateMutation(AdminMutationType):
    __schema__ = gql(
        """
        type Mutation {
            settingsUpdate(input: SettingsUpdateInput!): SettingsUpdateResult!
        }
        """
    )
    __requires__ = [AdminSettingsUpdateInputType, AdminSettingsUpdateResultType]

    @classmethod
    async def mutate(  # type: ignore
        cls,
        info: GraphQLResolveInfo,
        *,
        input: dict,  # pylint: disable=redefined-builtin
    ):
        clean_settings, errors = cls.clean_data(info, input)

        if errors:
            return {
                "errors": errors,
                "updated": False,
                "settings": info.context["settings"],
            }

        if clean_settings:
            await update_settings(clean_settings)
            await clear_settings_cache()

        return {
            "updated": bool(clean_settings),
            "settings": await get_settings_from_db(),
        }

    @classmethod
    def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        validated_data, errors = validate_model(SettingsChangeInputModel, data)
        clean_settings = {
            setting: value
            for setting, value in validated_data.items()
            if value is not None
        }

        if clean_settings:
            # Run second stage validation for cases where min is greater than max
            SecondStageModel = create_second_stage_model(
                clean_settings, info.context["settings"]
            )

            if SecondStageModel:
                _, second_stage_errors = validate_model(
                    SecondStageModel, clean_settings
                )
                errors += second_stage_errors

        return clean_settings, errors


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
    password_min_length=(conint(ge=4, le=PASSWORD_MAX_LENGTH), None),
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
