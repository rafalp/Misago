from typing import Optional
from urllib.parse import urlparse

from ariadne_graphql_modules import ObjectType, gql

from ...plugins import PluginData

REPO_ICONS = {
    "bitbucket.org": "fab fa-bitbucket",
    "github.com": "fab fa-github",
    "gitlab.com": "fab fa-gitlab",
}


class PluginHomepageType(ObjectType):
    __schema__ = gql(
        """
        type PluginHomepage {
            domain: String!
            url: String!
        }
        """
    )


class PluginRepoType(ObjectType):
    __schema__ = gql(
        """
        type PluginRepo {
            domain: String!
            icon: String
            url: String!
        }
        """
    )


class PluginType(ObjectType):
    __schema__ = gql(
        """
        type Plugin {
            name: String!
            description: String
            license: String
            icon: String
            color: String
            version: String
            author: String
            homepage: PluginHomepage
            repo: PluginRepo
            directory: String!
            admin: Boolean!
            client: Boolean!
        }
        """
    )
    __requires__ = [PluginHomepageType, PluginRepoType]

    @staticmethod
    def resolve_homepage(obj: PluginData, *_) -> Optional[dict]:
        if not obj.homepage:
            return None

        try:
            parsed_uri = urlparse(obj.homepage)
            if parsed_uri.hostname:
                return {
                    "domain": parsed_uri.hostname.lower(),
                    "url": obj.homepage,
                }
        except (ValueError, TypeError):
            return None

        return None

    @staticmethod
    def resolve_repo(obj: PluginData, *_) -> Optional[dict]:
        if not obj.repo:
            return None

        try:
            parsed_uri = urlparse(obj.repo)
            if parsed_uri.hostname:
                clean_hostname = parsed_uri.hostname.lower()
                return {
                    "domain": clean_hostname,
                    "icon": REPO_ICONS.get(clean_hostname.lower().strip()) or None,
                    "url": obj.repo,
                }
        except (ValueError, TypeError):
            return None

        return None
