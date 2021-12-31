from unittest.mock import patch

from ..runtime import read_runtime, is_line_with_source_mapping


RUNTIME_PATH = "misago/js/runtime-main.ef606b99.js"


def test_runtime_is_read_from_given_path(static_path):
    with patch("misago.conf.settings._static_root", static_path):
        assert read_runtime(RUNTIME_PATH)


def test_runtime_map_url_is_rewritten(static_path):
    with patch("misago.conf.settings._static_root", static_path):
        runtime = read_runtime(RUNTIME_PATH)
        assert runtime.splitlines()[-1] == (
            "//# sourceMappingURL=/static/misago/js/runtime-main.ef606b99.js.map"
        )


def test_runtime_line_check_handles_empty_str():
    assert not is_line_with_source_mapping("", RUNTIME_PATH)


def test_runtime_line_check_handles_invalid_str():
    assert not is_line_with_source_mapping("loremIpsum", RUNTIME_PATH)


def test_runtime_line_check_detects_valid_line():
    assert is_line_with_source_mapping(
        "//# sourceMappingURL=runtime-main.ef606b99.js.map", RUNTIME_PATH
    )
