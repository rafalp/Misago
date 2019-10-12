from importlib import import_module

from bs4 import BeautifulSoup

from .. import hooks
from ..conf import settings


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
        soup = BeautifulSoup(result["parsed_text"], "html5lib")
        for extension in settings.MISAGO_MARKUP_EXTENSIONS:
            module = import_module(extension)
            if hasattr(module, "clean_parsed"):
                hook = getattr(module, "clean_parsed")
                hook.process_result(result, soup)

        for extension in hooks.parsing_result_processors:
            extension(result, soup)

        souped_text = str(soup.body).strip()[6:-7]
        result["parsed_text"] = souped_text.strip()
        return result


pipeline = MarkupPipeline()
