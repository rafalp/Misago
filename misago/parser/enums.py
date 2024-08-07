from enum import StrEnum


class ContentType(StrEnum):
    GROUP_DESCRIPTION = "group-description"
    POST = "post"
    SIGNATURE = "signature"


class PlainTextFormat(StrEnum):
    META_DESCRIPTION = "meta_description"
    SEARCH_DOCUMENT = "search_document"
