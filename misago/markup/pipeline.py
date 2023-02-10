from importlib import import_module

from .. import hooks
from ..conf import settings
from .htmlparser import parse_html_string, print_html_string


class MarkupPipeline:
    """small framework for extending parser"""

    def extend_markdown(self, md):
        for extension in settings.MISAGO_MARKUP_EXTENSIONS:
            module = import_module(extension)
            if hasattr(module, "extend_markdown"):
                hook = getattr(module, "extend_markdown")
                hook.extend_markdown(md)

        for extension in hooks.markdown_extensions:
            extension(md)

        return md

    def process_result(self, result):
        if (
            not settings.MISAGO_MARKUP_EXTENSIONS
            and not hooks.parsing_result_processors
        ):
            return result

        html_tree = parse_html_string(result["parsed_text"])
        for extension in settings.MISAGO_MARKUP_EXTENSIONS:
            module = import_module(extension)
            if hasattr(module, "clean_parsed"):
                hook = getattr(module, "clean_parsed")
                hook.process_result(result, html_tree)

        for extension in hooks.parsing_result_processors:
            extension(result, html_tree)

        result["parsed_text"] = print_html_string(html_tree)
        return result


pipeline = MarkupPipeline()
