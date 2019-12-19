from typing import TypedDict, Sequence, Union


class ErrorDict(TypedDict):
    loc: Sequence[Union[int, str]]
    msg: str
    type: str
