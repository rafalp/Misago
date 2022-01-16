from typing import TypedDict


class ErrorDict(TypedDict):
    loc: str
    msg: str
    type: str
