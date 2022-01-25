from typing import List, Sequence, Union

from .errordict import ErrorDict
from .format import ROOT_LOCATION as DEFAULT_ROOT_LOCATION
from .format import get_error_dict


class ErrorsList(List[ErrorDict]):
    ROOT_LOCATION = DEFAULT_ROOT_LOCATION

    def __add__(self, other_list: Sequence[ErrorDict]) -> "ErrorsList":
        errors_list = list(self)
        for error in other_list:
            if error not in errors_list:
                errors_list.append(error)
        return ErrorsList(errors_list)

    def copy(self):
        return ErrorsList(self[:])

    def add_root_error(self, error: Exception):
        self.add_error(self.ROOT_LOCATION, error)

    def add_error(self, location: Union[str, Sequence[str]], error: Exception):
        error_dict = get_error_dict(error, location)
        if error_dict not in self:  # pylint: disable=unsupported-membership-test
            super().append(error_dict)

    def get_errors_locations(self) -> List[str]:
        return [
            ".".join(map(str, e["loc"]))
            for e in self  # pylint: disable=not-an-iterable
        ]

    def get_errors_types(self) -> List[str]:
        return [e["type"] for e in self]  # pylint: disable=not-an-iterable

    def has_errors_at_location(self, location: str) -> bool:
        for e in self:  # pylint: disable=not-an-iterable
            if e["loc"] and e["loc"][0] == location:
                return True
        return False

    @property
    def has_root_errors(self) -> bool:
        locations = [e["loc"] for e in self]  # pylint: disable=not-an-iterable
        return ErrorsList.ROOT_LOCATION in locations
