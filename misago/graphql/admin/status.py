from enum import IntEnum

from ariadne import EnumType


class Status(IntEnum):
    ERROR = 0
    WARNING = 1
    SUCCESS = 2


status = EnumType("Status", Status)
