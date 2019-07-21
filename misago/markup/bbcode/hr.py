import re

from markdown.blockprocessors import HRProcessor


class BBCodeHRProcessor(HRProcessor):
    RE = r"^\[hr\]*"

    # Detect hr on any line of a block.
    SEARCH_RE = re.compile(RE, re.MULTILINE | re.IGNORECASE)
