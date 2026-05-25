from dataclasses import dataclass


@dataclass
class TextMetaData:
    type = "text"

    id: str
    text: str
    icon: str | None = None
    title: str | None = None
