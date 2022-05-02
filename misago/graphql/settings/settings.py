from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...conf import settings
from ...users.validators import PASSWORD_MAX_LENGTH


class SettingsType(ObjectType):
    __schema__ = gql(
        """
        type Settings {
            avatarUploadContentTypes: [String!]!
            avatarUploadImageMinSize: Int!
            avatarUploadMaxSize: Int!
            bulkActionLimit: Int!
            enableSiteWizard: Boolean!
            forumIndexHeader: String!
            forumIndexThreads: Boolean!
            forumIndexTitle: String!
            forumName: String!
            passwordMinLength: Int!
            passwordMaxLength: Int!
            postMinLength: Int!
            threadTitleMinLength: Int!
            threadTitleMaxLength: Int!
            usernameMinLength: Int!
            usernameMaxLength: Int!
        }
        """
    )
    __aliases__ = {
        "avatarUploadContentTypes": "avatar_upload_content_types",
        "avatarUploadImageMinSize": "avatar_upload_image_min_size",
        "avatarUploadMaxSize": "avatar_upload_max_size",
        "bulkActionLimit": "bulk_action_limit",
        "enableSiteWizard": "enable_site_wizard",
        "forumIndexHeader": "forum_index_header",
        "forumIndexThreads": "forum_index_threads",
        "forumIndexTitle": "forum_index_title",
        "forumName": "forum_name",
        "passwordMinLength": "password_min_length",
        "passwordMaxLength": "password_max_length",
        "postMinLength": "post_min_length",
        "threadTitleMinLength": "thread_title_min_length",
        "threadTitleMaxLength": "thread_title_max_length",
        "usernameMinLength": "username_min_length",
        "usernameMaxLength": "username_max_length",
    }

    @staticmethod
    def resolve_avatar_upload_content_types(*_):
        return settings.avatar_content_types

    @staticmethod
    def resolve_avatar_upload_image_min_size(*_):
        return max(settings.avatar_sizes)

    @staticmethod
    def resolve_avatar_upload_max_size(_, info: GraphQLResolveInfo):
        return info.context["settings"]["avatar_upload_max_size"]

    @staticmethod
    def resolve_password_max_length(*_):
        return PASSWORD_MAX_LENGTH


class AdminSettingsType(ObjectType):
    __schema__ = gql(
        """
        extend type Settings {
            jwtExp: Int!
            postsPerPage: Int!
            postsPerPageOrphans: Int!
            threadsPerPage: Int!
        }
        """
    )
    __aliases__ = {
        "jwtExp": "jwt_exp",
        "postsPerPage": "posts_per_page",
        "postsPerPageOrphans": "posts_per_page_orphans",
        "threadsPerPage": "threads_per_page",
    }
    __requires__ = [SettingsType]
