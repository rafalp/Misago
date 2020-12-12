from typing import List, TypedDict


class RichTextParagraph(TypedDict):
    id: str
    type: str
    text: str


RichTextBlock = RichTextParagraph
RichText = List[RichTextBlock]
