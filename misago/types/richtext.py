from typing import List, TypedDict


class RichTextParagraph(TypedDict):
    id: str
    type: str
    text: str


RichText = List[RichTextParagraph]
