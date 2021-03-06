from typing import Sequence, TypedDict, Union


class ErrorDict(TypedDict):
    loc: Sequence[Union[int, str]]
    msg: str
    type: str
