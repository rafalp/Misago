from ..query import resolve_settings


def test_settings_resolver_returns_settings_from_context(
    graphql_info, dynamic_settings
):
    value = resolve_settings(None, graphql_info)
    assert value is dynamic_settings
