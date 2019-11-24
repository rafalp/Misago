from typing import List

from ..types import ErrorsList


def get_errors_locations(errors: ErrorsList) -> List[str]:
    return [".".join(e["loc"]) for e in errors]


def get_errors_types(errors: ErrorsList) -> List[str]:
    return [e["type"] for e in errors]
