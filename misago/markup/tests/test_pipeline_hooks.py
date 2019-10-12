from unittest.mock import ANY

from ..pipeline import pipeline


def test_markdown_extensions_hook_is_called_by_pipeline(mocker):
    plugin = mocker.Mock()
    mocker.patch("misago.markup.pipeline.hooks.markdown_extensions", [plugin])
    pipeline.extend_markdown(mocker.Mock())
    plugin.asssert_called_once_with(ANY)


def test_parsing_result_processors_hook_is_called_by_pipeline(mocker):
    plugin = mocker.Mock()
    mocker.patch("misago.markup.pipeline.hooks.parsing_result_processors", [plugin])
    pipeline.extend_markdown(mocker.Mock())
    plugin.asssert_called_once_with(ANY, ANY)
