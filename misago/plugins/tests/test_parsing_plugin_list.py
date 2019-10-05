from ..pluginlist import parse_plugins_list


def test_empty_plugins_str_is_parsed_to_empty_list():
    assert parse_plugins_list("") == []


def test_comment_str_is_parsed_to_empty_list():
    assert parse_plugins_list("# comment") == []


def test_line_containing_plugin_name_is_parsed():
    assert parse_plugins_list("plugin") == ["plugin"]


def test_line_containing_local_plugin_name_is_parsed():
    assert parse_plugins_list("plugin@/local/") == ["plugin@/local/"]


def test_whitespace_is_stripped_from_local_plugin_name():
    assert parse_plugins_list("plugin @/local/") == ["plugin@/local/"]


def test_whitespace_is_stripped_from_local_plugin_path():
    assert parse_plugins_list("plugin@ /local/") == ["plugin@/local/"]


def test_comment_is_removed_from_line_containing_plugin_name():
    assert parse_plugins_list("plugin # comment") == ["plugin"]


def test_multiple_lines_containing_plugin_names_are_parsed():
    assert parse_plugins_list("plugin1\nplugin2") == ["plugin1", "plugin2"]


def test_empty_lines_are_skipped_by_parser():
    assert parse_plugins_list("plugin1\n\nplugin2") == ["plugin1", "plugin2"]


def test_comments_are_filtered_from_plugin_list():
    assert parse_plugins_list("plugin1\n# comment\nplugin2") == ["plugin1", "plugin2"]


def test_whitespace_is_stripped_from_line_start_and_end_by_parser():
    assert parse_plugins_list("plugin1\n  plugin2") == ["plugin1", "plugin2"]
