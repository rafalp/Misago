from textwrap import dedent

import pytest

from ...permissions.proxy import UserPermissionsProxy
from ..context import create_parser_context
from ..factory import create_parser


@pytest.fixture
def parser(parser_context):
    return create_parser(parser_context)


@pytest.fixture
def parser_context(dynamic_settings, cache_versions, user):
    dynamic_settings.forum_address = "http://example.org"

    return create_parser_context(
        user_permissions=UserPermissionsProxy(user, cache_versions),
        settings=dynamic_settings,
        cache_versions=cache_versions,
    )


@pytest.fixture
def parse_markup(parser):
    def parse_markup_func(markup: str) -> list[dict]:
        return parser(dedent(markup).strip())

    return parse_markup_func
